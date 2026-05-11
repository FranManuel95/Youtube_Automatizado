"""Modelos de dominio para la etapa de analítica y auditoría.

Sigue el informe `docs/07_guia_tecnica_general.md` (sección Ask Studio,
Inspiration Tab) + las menciones del resto de informes sobre métricas
clave (RPM, retención, CTR, outliers).
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class RetentionPoint(BaseModel):
    """Un punto de la curva de retención exportada por YouTube Studio."""

    timecode_sec: int = Field(..., ge=0)
    relative_retention: float = Field(..., ge=0.0, le=1.5)
    is_leak: bool = False


class RetentionLeak(BaseModel):
    """Un tramo donde la curva cae más del umbral en pocos segundos."""

    start_sec: int
    end_sec: int
    drop_pct: float = Field(..., description="Pérdida en puntos porcentuales")
    related_section: str | None = Field(
        default=None,
        description="Sección del guion que coincide con el tramo (si se conoce)",
    )
    suggested_fix: str


class VideoPerformance(BaseModel):
    """Métricas de un video publicado."""

    video_id: str
    title: str
    duration_sec: int

    views: int = 0
    impressions: int = 0
    ctr: float | None = None
    avg_view_duration_sec: int | None = None
    avg_retention_pct: float | None = None
    subscribers_gained: int = 0
    revenue_usd: float | None = None
    rpm_usd: float | None = None

    retention_curve: list[RetentionPoint] = Field(default_factory=list)
    leaks: list[RetentionLeak] = Field(default_factory=list)

    is_outlier: bool = Field(
        default=False, description="Vistas 3x-10x sobre la base de suscriptores del canal"
    )

    @property
    def retention_30s_pct(self) -> float | None:
        """Retención estimada a los 30 segundos."""
        for p in self.retention_curve:
            if p.timecode_sec >= 30:
                return p.relative_retention * 100
        return None


class ChannelHealth(BaseModel):
    """Salud de un canal individual del portafolio."""

    channel_id: str
    name: str
    market_focus: str = Field(..., description="US-Hispanic, ES, LATAM, EN-US, ...")
    subscriber_count: int = 0
    videos_last_30d: int = 0
    monthly_revenue_usd: float = 0.0
    monthly_rpm_usd: float | None = None
    avg_retention_30d_pct: float | None = None
    languages: list[str] = Field(default_factory=lambda: ["es"])


class PortfolioHealth(BaseModel):
    """Diagnóstico del portafolio multi-canal (regla de oro: 5x500 > 1x2500)."""

    channels: list[ChannelHealth]
    total_monthly_revenue_usd: float
    top_channel_revenue_share_pct: float = Field(
        ..., description="% que representa el canal top sobre el revenue total"
    )
    concentration_risk: Literal["bajo", "medio", "alto", "crítico"]
    diversification_score: int = Field(..., ge=1, le=10)
    languages_covered: list[str] = Field(default_factory=list)
    has_us_hispanic_exposure: bool = False
    recommendations: list[str] = Field(default_factory=list)


class AskStudioPrompt(BaseModel):
    """Prompt estructurado para pegar en Ask Studio (Gemini in-channel)."""

    purpose: Literal[
        "outlier_analysis",
        "drop_detection",
        "gap_detection",
        "competitor_pattern",
        "ab_test_thumbnails",
    ]
    title: str
    prompt_text: str
    expected_output: str


class AnalyticsReport(BaseModel):
    schema_version: str = "1.0"
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    videos: list[VideoPerformance] = Field(default_factory=list)
    portfolio: PortfolioHealth | None = None
    ask_studio_prompts: list[AskStudioPrompt] = Field(default_factory=list)
    notes: str = ""

    @property
    def total_leaks(self) -> int:
        return sum(len(v.leaks) for v in self.videos)
