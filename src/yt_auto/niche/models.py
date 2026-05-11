"""Modelos de dominio para la etapa de selección de nicho.

Mapea los conceptos del informe `docs/01_seleccion_de_nichos.md` a tipos
Pydantic verificables.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class FourS(str, Enum):
    """Framework de las 4 S del consumo en YouTube 2026."""

    streaming = "Streaming"
    searching = "Searching"
    shopping = "Shopping"
    scrolling = "Scrolling"


class MarketTier(str, Enum):
    tier1 = "Tier 1"
    tier1_5 = "Tier 1.5 (US-Hispanic)"
    tier2 = "Tier 2"
    tier3 = "Tier 3"


CompetitionLevel = Literal["bajo", "medio", "alto", "saturado"]


class RPMEstimate(BaseModel):
    market: str
    tier: MarketTier
    rpm_min_usd: float
    rpm_max_usd: float


class NicheCandidate(BaseModel):
    """Un subnicho candidato evaluado bajo el framework completo."""

    name: str = Field(..., description="Nombre operativo del subnicho")
    headline: str = Field(..., description="Pitch de una línea para el canal")
    description: str = Field(..., description="2-4 frases explicando el ángulo")

    target_market: str
    target_language: str = "es"

    four_s: list[FourS] = Field(default_factory=list)
    rpm: RPMEstimate

    demand_evidence: list[str] = Field(
        default_factory=list,
        description="Pruebas de demanda: canales referencia, videos virales, tendencias",
    )
    gap_hypothesis: str = Field(
        ...,
        description="Hueco concreto que la competencia ignora y que justifica el nicho",
    )
    competition_level: CompetitionLevel
    niche_bending_angle: str | None = Field(
        default=None,
        description="Fusión propuesta si el nicho directo está saturado",
    )

    sample_titles: list[str] = Field(
        default_factory=list,
        description="3-5 títulos en formato '3 Points/Open Loop' para tantear",
    )
    risks: list[str] = Field(default_factory=list)
    score: int = Field(..., ge=1, le=10, description="Puntuación global 1-10")
    rationale: str = Field(..., description="Por qué este score y no otro")


class NicheAuditReport(BaseModel):
    """Resultado completo de una sesión de auditoría de nichos."""

    schema_version: str = "1.0"
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    market_focus: str
    content_format: Literal["long_form", "masterclass", "shorts", "mixed"]
    target_count: int

    vertical_filter: str | None = None
    methodology_notes: str = ""
    model_used: str = "claude-opus-4-7"
    mode: Literal["interactive", "api"] = "interactive"

    candidates: list[NicheCandidate] = Field(default_factory=list)

    def top(self, n: int = 3) -> list[NicheCandidate]:
        return sorted(self.candidates, key=lambda c: c.score, reverse=True)[:n]
