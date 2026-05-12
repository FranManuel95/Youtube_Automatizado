"""Orquestación del análisis competitivo de un nicho.

`scan_niche` busca el top N de canales para una query, obtiene sus
estadísticas y devuelve un `NicheScanReport` listo para persistir.

`detect_outliers` toma un canal y devuelve los videos cuyos views
superan en >=3x la mediana del canal — la señal de "outlier" que el
informe estratégico marca como input para la próxima ronda editorial.

Todas las operaciones usan caché en disco con TTL 24h para no agotar la
cuota gratuita (10k unidades/día) al reusar análisis del mismo día.
"""

from __future__ import annotations

import hashlib
import json
import statistics
from datetime import datetime, timedelta
from pathlib import Path

from yt_auto.competitive.client import YouTubeDataClient
from yt_auto.competitive.models import (
    Channel,
    NicheScanReport,
    OutlierVideo,
    Video,
)
from yt_auto.config import ROOT_DIR
from yt_auto.publishing.niche_profile import NicheProfile

DEFAULT_CACHE_DIR = ROOT_DIR / "output" / "_competitive_cache"
CACHE_TTL = timedelta(hours=24)


def _cache_key(prefix: str, payload: str) -> Path:
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return DEFAULT_CACHE_DIR / f"{prefix}_{digest}.json"


def _read_cache(path: Path) -> dict | None:
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    fetched_at = datetime.fromisoformat(data["_fetched_at"])
    if datetime.utcnow() - fetched_at > CACHE_TTL:
        return None
    return data["payload"]


def _write_cache(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {"_fetched_at": datetime.utcnow().isoformat(), "payload": payload},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def scan_niche(
    profile: NicheProfile,
    *,
    client: YouTubeDataClient,
    query_override: str | None = None,
    max_channels: int = 10,
    use_cache: bool = True,
) -> NicheScanReport:
    """Escanea el top de canales para un perfil de nicho.

    Estrategia: construye la query desde `keyword_triggers` del perfil
    (top 3 keywords concatenadas), busca canales en español, y obtiene
    detalle de los top N.

    Coste estimado: 100 (search) + 1 (channels batch) = ~101 unidades.
    Cabe ~99 scans en la cuota gratuita diaria.
    """
    query = query_override or _build_query(profile)
    cache_key = _cache_key(f"scan_{profile.id}", query + str(max_channels))

    if use_cache:
        cached = _read_cache(cache_key)
        if cached is not None:
            return NicheScanReport.model_validate(cached)

    channel_ids = client.search_channels(query, max_results=max_channels)
    channels = client.channels(channel_ids)

    report = NicheScanReport(
        niche_profile_id=profile.id,
        query_used=query,
        channels=channels,
        quota_units_spent=client.quota.units_spent,
    )

    if use_cache:
        _write_cache(cache_key, report.model_dump(mode="json"))

    return report


def detect_outliers(
    channel: Channel,
    *,
    client: YouTubeDataClient,
    sample_size: int = 30,
    min_multiplier: float = 3.0,
    use_cache: bool = True,
) -> list[OutlierVideo]:
    """Detecta videos outlier (views >= min_multiplier × mediana del canal).

    Coste: 1 (playlistItems) + 1 (videos batch) = 2 unidades por canal.
    """
    if not channel.uploads_playlist_id:
        return []

    cache_key = _cache_key(
        f"outliers_{channel.channel_id}", f"{sample_size}_{min_multiplier}"
    )
    if use_cache:
        cached = _read_cache(cache_key)
        if cached is not None:
            return [OutlierVideo.model_validate(x) for x in cached]

    video_ids = client.playlist_items(
        channel.uploads_playlist_id, max_results=sample_size
    )
    videos = client.videos(video_ids)
    if not videos:
        return []

    view_counts = [v.statistics.view_count for v in videos if v.statistics.view_count > 0]
    if not view_counts:
        return []
    median_views = int(statistics.median(view_counts))
    if median_views == 0:
        return []

    outliers: list[OutlierVideo] = []
    for v in videos:
        multiplier = v.statistics.view_count / median_views
        if multiplier >= min_multiplier:
            outliers.append(
                OutlierVideo(
                    video=v,
                    channel_median_views=median_views,
                    multiplier_vs_median=round(multiplier, 2),
                    rationale=_outlier_rationale(v, median_views, multiplier),
                )
            )

    outliers.sort(key=lambda o: -o.multiplier_vs_median)

    if use_cache:
        _write_cache(
            cache_key, [o.model_dump(mode="json") for o in outliers]
        )

    return outliers


def _build_query(profile: NicheProfile) -> str:
    """Construye una query relevante para YouTube Search.

    Prefiere `search_queries[0]` (curado y validado). Si no hay, cae a
    los top 3 `keyword_triggers` más largos (heurística más débil).
    """
    if profile.search_queries:
        return profile.search_queries[0]
    if not profile.keyword_triggers:
        return profile.display_name
    top_keywords = sorted(profile.keyword_triggers, key=len, reverse=True)[:3]
    return " ".join(top_keywords)


def _outlier_rationale(video: Video, median: int, multiplier: float) -> str:
    return (
        f"{video.statistics.view_count:,} views vs mediana del canal {median:,} "
        f"({multiplier:.1f}x). Publicado hace {video.age_days} días."
    )
