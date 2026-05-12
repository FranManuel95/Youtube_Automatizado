"""Cliente HTTP de YouTube Data API v3.

Wrapper fino sobre `httpx.Client`. Solo cubre los endpoints que el módulo
`competitive` necesita: search, channels, playlistItems, videos.

Datos públicos exclusivamente (API key, no OAuth). Para subir videos o
leer Analytics privadas se necesitará un cliente OAuth aparte.

Cuota YouTube Data API v3:
- search.list: 100 unidades
- channels.list / videos.list / playlistItems.list: 1 unidad cada uno
- Cuota gratuita: 10.000 unidades/día por proyecto Google Cloud
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Self

import httpx
from pydantic import BaseModel
from tenacity import (
    Retrying,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from yt_auto.competitive.models import (
    Channel,
    ChannelStatistics,
    Video,
    VideoStatistics,
)

_DEFAULT_BASE_URL = "https://www.googleapis.com/youtube/v3"
_DEFAULT_TIMEOUT = 60.0
_RETRYABLE_STATUS = {429, 500, 502, 503, 504}


class YouTubeAPIError(RuntimeError):
    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(f"YouTube API {status_code}: {message}")
        self.status_code = status_code
        self.message = message


class QuotaCounter(BaseModel):
    """Contador local de unidades de cuota consumidas en la sesión."""

    units_spent: int = 0

    def add(self, n: int) -> None:
        self.units_spent += n


class YouTubeDataClient:
    """Cliente sincrónico de YouTube Data API v3 (datos públicos).

    Inyectable en tests con `httpx.MockTransport`. Reintenta 429/5xx con
    backoff exponencial. Trackea cuota consumida en `QuotaCounter`.
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = _DEFAULT_TIMEOUT,
        transport: httpx.BaseTransport | None = None,
        max_attempts: int = 4,
    ) -> None:
        if not api_key:
            raise ValueError("YOUTUBE_API_KEY vacía. Configúrala en .env.")
        self._api_key = api_key
        self._client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            transport=transport,
            headers={"accept": "application/json"},
        )
        self._max_attempts = max_attempts
        self.quota = QuotaCounter()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def close(self) -> None:
        self._client.close()

    # ------------------------------------------------------------------
    # Endpoints públicos
    # ------------------------------------------------------------------

    def search_channels(
        self,
        query: str,
        *,
        max_results: int = 10,
        region_code: str | None = None,
        relevance_language: str | None = "es",
    ) -> list[str]:
        """Busca canales por keyword. Devuelve channel_ids (no detalles).

        Coste: 100 unidades por llamada.
        """
        params: dict[str, Any] = {
            "part": "snippet",
            "q": query,
            "type": "channel",
            "maxResults": min(max(1, max_results), 50),
            "order": "relevance",
        }
        if region_code:
            params["regionCode"] = region_code
        if relevance_language:
            params["relevanceLanguage"] = relevance_language

        data = self._get("/search", params)
        self.quota.add(100)
        ids: list[str] = []
        for item in data.get("items", []):
            cid = item.get("id", {}).get("channelId")
            if cid:
                ids.append(cid)
        return ids

    def channels(self, channel_ids: list[str]) -> list[Channel]:
        """Detalle de canales (snippet + statistics + contentDetails).

        Coste: 1 unidad por llamada (batch hasta 50 IDs).
        """
        if not channel_ids:
            return []
        out: list[Channel] = []
        # Batches de 50 por llamada (límite de la API)
        for batch in _chunks(channel_ids, 50):
            params = {
                "part": "snippet,statistics,contentDetails",
                "id": ",".join(batch),
                "maxResults": 50,
            }
            data = self._get("/channels", params)
            self.quota.add(1)
            for item in data.get("items", []):
                out.append(_parse_channel(item))
        return out

    def playlist_items(self, playlist_id: str, *, max_results: int = 50) -> list[str]:
        """Devuelve video_ids de un playlist (uploads).

        Coste: 1 unidad por llamada.
        """
        params = {
            "part": "contentDetails",
            "playlistId": playlist_id,
            "maxResults": min(max(1, max_results), 50),
        }
        data = self._get("/playlistItems", params)
        self.quota.add(1)
        ids: list[str] = []
        for item in data.get("items", []):
            vid = item.get("contentDetails", {}).get("videoId")
            if vid:
                ids.append(vid)
        return ids

    def videos(self, video_ids: list[str]) -> list[Video]:
        """Detalle de videos (batch hasta 50)."""
        if not video_ids:
            return []
        out: list[Video] = []
        for batch in _chunks(video_ids, 50):
            params = {
                "part": "snippet,statistics,contentDetails",
                "id": ",".join(batch),
                "maxResults": 50,
            }
            data = self._get("/videos", params)
            self.quota.add(1)
            for item in data.get("items", []):
                out.append(_parse_video(item))
        return out

    # ------------------------------------------------------------------
    # Internos
    # ------------------------------------------------------------------

    def _get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        params_with_key = {**params, "key": self._api_key}
        response: httpx.Response | None = None
        for attempt in self._retrying():
            with attempt:
                response = self._client.get(path, params=params_with_key)
                self._raise_for_status(response)
        assert response is not None
        return response.json()

    def _retrying(self) -> Retrying:
        return Retrying(
            stop=stop_after_attempt(self._max_attempts),
            wait=wait_exponential(multiplier=1, min=2, max=30),
            retry=retry_if_exception(
                lambda e: isinstance(e, YouTubeAPIError)
                and e.status_code in _RETRYABLE_STATUS
            ),
            reraise=True,
        )

    @staticmethod
    def _raise_for_status(response: httpx.Response) -> None:
        if response.is_success:
            return
        message = response.text
        try:
            data = response.json()
            err = data.get("error", {}) if isinstance(data, dict) else {}
            message = err.get("message") or message
        except ValueError:
            pass
        raise YouTubeAPIError(response.status_code, message)


def _chunks(items: list[str], size: int):
    for i in range(0, len(items), size):
        yield items[i : i + size]


def _parse_channel(item: dict[str, Any]) -> Channel:
    snippet = item.get("snippet", {})
    stats = item.get("statistics", {})
    content = item.get("contentDetails", {}).get("relatedPlaylists", {})
    return Channel(
        channel_id=item["id"],
        title=snippet.get("title", ""),
        description=snippet.get("description", ""),
        country=snippet.get("country"),
        published_at=_parse_dt(snippet.get("publishedAt")),
        statistics=ChannelStatistics(
            subscriber_count=int(stats.get("subscriberCount", 0)),
            view_count=int(stats.get("viewCount", 0)),
            video_count=int(stats.get("videoCount", 0)),
            hidden_subscriber_count=bool(stats.get("hiddenSubscriberCount", False)),
        ),
        uploads_playlist_id=content.get("uploads"),
        custom_url=snippet.get("customUrl"),
    )


def _parse_video(item: dict[str, Any]) -> Video:
    snippet = item.get("snippet", {})
    stats = item.get("statistics", {})
    content = item.get("contentDetails", {})
    return Video(
        video_id=item["id"],
        channel_id=snippet.get("channelId", ""),
        title=snippet.get("title", ""),
        description=snippet.get("description", ""),
        published_at=_parse_dt(snippet.get("publishedAt")) or datetime.utcnow(),
        duration_seconds=_iso8601_duration_to_seconds(content.get("duration", "PT0S")),
        statistics=VideoStatistics(
            view_count=int(stats.get("viewCount", 0)),
            like_count=int(stats.get("likeCount", 0)),
            comment_count=int(stats.get("commentCount", 0)),
        ),
        tags=snippet.get("tags", []),
    )


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    # YouTube uses RFC3339 with 'Z' suffix
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _iso8601_duration_to_seconds(duration: str) -> int:
    """Parsea PT#H#M#S → segundos. Solo cubre el subset que YouTube emite."""
    import re

    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration or "PT0S")
    if not m:
        return 0
    h, mm, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mm * 60 + s
