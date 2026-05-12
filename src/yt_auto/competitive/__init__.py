"""Etapa transversal - Análisis competitivo YouTube (Data API v3).

Resuelve la limitación del análisis de nicho que dependía de
triangulación: ahora podemos pedirle a YouTube los datos reales de
canales benchmark, mediana de views, y videos outliers para alimentar
la inspiración de la siguiente ronda editorial.

Datos PÚBLICOS solo (API key, no OAuth). El upload y la lectura de
Analytics privadas se manejarán en `publishing/api.py` con OAuth aparte.
"""

from __future__ import annotations

from yt_auto.competitive.client import (
    QuotaCounter,
    YouTubeAPIError,
    YouTubeDataClient,
)
from yt_auto.competitive.models import (
    Channel,
    ChannelStatistics,
    NicheScanReport,
    OutlierVideo,
    Video,
    VideoStatistics,
)
from yt_auto.competitive.scanner import detect_outliers, scan_niche

__all__ = [
    "Channel",
    "ChannelStatistics",
    "NicheScanReport",
    "OutlierVideo",
    "QuotaCounter",
    "Video",
    "VideoStatistics",
    "YouTubeAPIError",
    "YouTubeDataClient",
    "detect_outliers",
    "scan_niche",
]
