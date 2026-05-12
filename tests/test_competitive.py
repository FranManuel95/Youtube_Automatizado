"""Tests del módulo competitive (cliente YouTube + scanner + outliers)."""

from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from yt_auto.competitive import (
    Channel,
    ChannelStatistics,
    NicheScanReport,
    OutlierVideo,
    Video,
    VideoStatistics,
    YouTubeAPIError,
    YouTubeDataClient,
    detect_outliers,
    scan_niche,
)
from yt_auto.publishing.niche_profile import load_profile

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------


def _make_client(handler) -> YouTubeDataClient:
    return YouTubeDataClient("fake-key", transport=httpx.MockTransport(handler))


def _search_channels_response(channel_ids: list[str]) -> dict:
    return {
        "items": [
            {"id": {"kind": "youtube#channel", "channelId": cid}}
            for cid in channel_ids
        ]
    }


def _channels_response(channels: list[dict]) -> dict:
    return {"items": channels}


def _channel_payload(
    *,
    channel_id: str,
    title: str,
    subs: int,
    videos: int,
    views: int,
    uploads_id: str,
    country: str = "US",
    published_at: str = "2020-01-01T00:00:00Z",
) -> dict:
    return {
        "id": channel_id,
        "snippet": {
            "title": title,
            "description": "test",
            "country": country,
            "publishedAt": published_at,
            "customUrl": f"@{title.lower().replace(' ', '')}",
        },
        "statistics": {
            "subscriberCount": str(subs),
            "viewCount": str(views),
            "videoCount": str(videos),
            "hiddenSubscriberCount": False,
        },
        "contentDetails": {"relatedPlaylists": {"uploads": uploads_id}},
    }


def _video_payload(
    *,
    video_id: str,
    channel_id: str,
    title: str,
    views: int,
    duration: str = "PT12M30S",
    published_at: str = "2025-01-01T00:00:00Z",
) -> dict:
    return {
        "id": video_id,
        "snippet": {
            "channelId": channel_id,
            "title": title,
            "description": "",
            "publishedAt": published_at,
            "tags": [],
        },
        "statistics": {
            "viewCount": str(views),
            "likeCount": str(views // 50),
            "commentCount": str(views // 200),
        },
        "contentDetails": {"duration": duration},
    }


# --------------------------------------------------------------------------
# Cliente
# --------------------------------------------------------------------------


def test_client_rejects_empty_api_key():
    with pytest.raises(ValueError, match="YOUTUBE_API_KEY"):
        YouTubeDataClient("")


def test_search_channels_returns_ids_and_tracks_quota():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/youtube/v3/search"
        assert "key=fake-key" in str(request.url)
        assert "q=ITIN+credito" in str(request.url) or "q=ITIN%20credito" in str(request.url)
        return httpx.Response(200, json=_search_channels_response(["UC_A", "UC_B"]))

    with _make_client(handler) as client:
        ids = client.search_channels("ITIN credito", max_results=2)

    assert ids == ["UC_A", "UC_B"]
    assert client.quota.units_spent == 100


def test_channels_batches_up_to_50():
    captured_calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured_calls.append(request.url)
        # Devuelve un canal por cada ID solicitado
        ids = request.url.params.get("id", "").split(",")
        items = [
            _channel_payload(
                channel_id=cid,
                title=f"Canal {cid}",
                subs=10_000,
                videos=100,
                views=1_000_000,
                uploads_id=f"UU_{cid}",
            )
            for cid in ids
        ]
        return httpx.Response(200, json=_channels_response(items))

    # 60 IDs → debería partirse en 2 batches (50 + 10)
    ids = [f"UC_{i:03d}" for i in range(60)]
    with _make_client(handler) as client:
        channels = client.channels(ids)

    assert len(channels) == 60
    assert len(captured_calls) == 2
    assert client.quota.units_spent == 2  # 1 por batch


def test_channels_parses_statistics():
    def handler(request):
        return httpx.Response(
            200,
            json=_channels_response([
                _channel_payload(
                    channel_id="UC_1",
                    title="Super Dinero",
                    subs=125_000,
                    videos=350,
                    views=50_000_000,
                    uploads_id="UU_1",
                )
            ]),
        )

    with _make_client(handler) as client:
        channels = client.channels(["UC_1"])

    assert len(channels) == 1
    ch = channels[0]
    assert ch.statistics.subscriber_count == 125_000
    assert ch.avg_views_per_video > 0
    assert ch.uploads_playlist_id == "UU_1"


def test_videos_parses_duration_iso8601():
    def handler(request):
        return httpx.Response(
            200,
            json={
                "items": [
                    _video_payload(
                        video_id="v1",
                        channel_id="UC_1",
                        title="Test",
                        views=10_000,
                        duration="PT1H23M45S",
                    )
                ]
            },
        )

    with _make_client(handler) as client:
        videos = client.videos(["v1"])

    assert videos[0].duration_seconds == 3600 + 23 * 60 + 45


def test_client_raises_on_4xx_with_quota_unchanged_logic():
    def handler(request):
        return httpx.Response(
            403,
            json={
                "error": {
                    "message": (
                        "The request cannot be completed because you have "
                        "exceeded your quota."
                    ),
                    "code": 403,
                }
            },
        )

    with _make_client(handler) as client, pytest.raises(YouTubeAPIError) as exc_info:
        client.search_channels("test")
    assert exc_info.value.status_code == 403
    assert "quota" in str(exc_info.value).lower()


# --------------------------------------------------------------------------
# Scanner
# --------------------------------------------------------------------------


def test_scan_niche_uses_profile_keywords_when_no_query_override(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(
        "yt_auto.competitive.scanner.DEFAULT_CACHE_DIR", tmp_path / "cache"
    )

    profile = load_profile("real_estate_latino")
    captured_queries: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/youtube/v3/search":
            captured_queries.append(request.url.params.get("q", ""))
            return httpx.Response(200, json=_search_channels_response(["UC_RE_1"]))
        if request.url.path == "/youtube/v3/channels":
            return httpx.Response(
                200,
                json=_channels_response([
                    _channel_payload(
                        channel_id="UC_RE_1",
                        title="Felipe Padilla Realtor",
                        subs=45_000,
                        videos=200,
                        views=8_000_000,
                        uploads_id="UU_RE_1",
                    )
                ]),
            )
        return httpx.Response(404)

    with _make_client(handler) as client:
        report = scan_niche(profile, client=client, max_channels=1)

    assert isinstance(report, NicheScanReport)
    assert report.niche_profile_id == "real_estate_latino"
    assert len(report.channels) == 1
    assert "homeownership" in captured_queries[0] or "comprar casa" in captured_queries[0]


def test_scan_niche_caches_results(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(
        "yt_auto.competitive.scanner.DEFAULT_CACHE_DIR", tmp_path / "cache"
    )

    profile = load_profile("real_estate_latino")
    call_count = {"search": 0, "channels": 0}

    def handler(request):
        if request.url.path == "/youtube/v3/search":
            call_count["search"] += 1
            return httpx.Response(200, json=_search_channels_response(["UC_X"]))
        if request.url.path == "/youtube/v3/channels":
            call_count["channels"] += 1
            return httpx.Response(
                200,
                json=_channels_response([
                    _channel_payload(
                        channel_id="UC_X",
                        title="X",
                        subs=1000,
                        videos=10,
                        views=10000,
                        uploads_id="UU_X",
                    )
                ]),
            )
        return httpx.Response(404)

    # 1ª llamada: hit a la API
    with _make_client(handler) as client:
        r1 = scan_niche(profile, client=client, max_channels=1)
    # 2ª llamada: debería leer caché
    with _make_client(handler) as client:
        r2 = scan_niche(profile, client=client, max_channels=1)

    assert call_count["search"] == 1
    assert call_count["channels"] == 1
    assert len(r1.channels) == len(r2.channels) == 1


def test_scan_niche_no_cache_forces_call(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(
        "yt_auto.competitive.scanner.DEFAULT_CACHE_DIR", tmp_path / "cache"
    )

    profile = load_profile("itin_credito")
    counts = {"calls": 0}

    def handler(request):
        if request.url.path == "/youtube/v3/search":
            counts["calls"] += 1
            return httpx.Response(200, json=_search_channels_response(["UC_Y"]))
        return httpx.Response(
            200,
            json=_channels_response([
                _channel_payload(
                    channel_id="UC_Y",
                    title="Y",
                    subs=1,
                    videos=1,
                    views=1,
                    uploads_id="UU_Y",
                )
            ]),
        )

    with _make_client(handler) as client:
        scan_niche(profile, client=client, max_channels=1, use_cache=False)
    with _make_client(handler) as client:
        scan_niche(profile, client=client, max_channels=1, use_cache=False)

    assert counts["calls"] == 2


def test_fragmentation_score_labels():
    channels = [
        Channel(
            channel_id="UC1",
            title="A",
            statistics=ChannelStatistics(subscriber_count=50_000, view_count=1, video_count=1),
        ),
        Channel(
            channel_id="UC2",
            title="B",
            statistics=ChannelStatistics(subscriber_count=80_000, view_count=1, video_count=1),
        ),
    ]
    report = NicheScanReport(
        niche_profile_id="x", query_used="q", channels=channels
    )
    assert report.big_fish_count == 0
    assert report.fragmentation_score == "fragmentado-bajo"

    channels.append(
        Channel(
            channel_id="UC3",
            title="C",
            statistics=ChannelStatistics(subscriber_count=500_000, view_count=1, video_count=1),
        )
    )
    report = NicheScanReport(niche_profile_id="x", query_used="q", channels=channels)
    assert report.big_fish_count == 1
    assert report.fragmentation_score == "fragmentado-medio"


# --------------------------------------------------------------------------
# Outlier detector
# --------------------------------------------------------------------------


def _channel_with_uploads(uploads_id: str = "UU_TEST") -> Channel:
    return Channel(
        channel_id="UC_TEST",
        title="Test Canal",
        statistics=ChannelStatistics(
            subscriber_count=50_000, view_count=5_000_000, video_count=100
        ),
        uploads_playlist_id=uploads_id,
    )


def test_detect_outliers_identifies_3x_median(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(
        "yt_auto.competitive.scanner.DEFAULT_CACHE_DIR", tmp_path / "cache"
    )

    channel = _channel_with_uploads()
    # 9 videos con 1000 views + 1 outlier con 10_000 views
    video_payloads = [
        _video_payload(
            video_id=f"v{i}",
            channel_id=channel.channel_id,
            title=f"Video {i}",
            views=1000,
        )
        for i in range(9)
    ]
    video_payloads.append(
        _video_payload(
            video_id="v_out",
            channel_id=channel.channel_id,
            title="OUTLIER super viral",
            views=10_000,
        )
    )

    def handler(request):
        if request.url.path == "/youtube/v3/playlistItems":
            return httpx.Response(
                200,
                json={
                    "items": [
                        {"contentDetails": {"videoId": p["id"]}} for p in video_payloads
                    ]
                },
            )
        if request.url.path == "/youtube/v3/videos":
            return httpx.Response(200, json={"items": video_payloads})
        return httpx.Response(404)

    with _make_client(handler) as client:
        outliers = detect_outliers(channel, client=client, sample_size=10)

    assert len(outliers) == 1
    assert outliers[0].video.video_id == "v_out"
    assert outliers[0].multiplier_vs_median >= 3.0
    assert outliers[0].channel_median_views == 1000


def test_detect_outliers_returns_empty_when_no_uploads(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(
        "yt_auto.competitive.scanner.DEFAULT_CACHE_DIR", tmp_path / "cache"
    )
    channel = Channel(channel_id="UC_X", title="x")  # sin uploads_playlist_id

    def handler(request):
        return httpx.Response(200, json={"items": []})

    with _make_client(handler) as client:
        outliers = detect_outliers(channel, client=client)
    assert outliers == []


def test_outlier_video_strong_threshold():
    v = Video(
        video_id="x",
        channel_id="UC",
        title="t",
        published_at="2025-01-01T00:00:00Z",
        statistics=VideoStatistics(view_count=5000),
    )
    weak = OutlierVideo(video=v, channel_median_views=2500, multiplier_vs_median=2.0)
    strong = OutlierVideo(video=v, channel_median_views=1000, multiplier_vs_median=5.0)
    assert weak.is_strong_outlier is False
    assert strong.is_strong_outlier is True
