"""Modelos de dominio para la etapa de edición y packaging.

Sigue las reglas del informe `docs/05_edicion_y_packaging.md`:
- Regla de los 3 segundos (cambio visual cada 3s).
- Subtítulos dinámicos coloridos con keywords destacados.
- Dynamic Ad Insertion (DAI) anchors en puntos naturales.
- Exportación 4K para competir en Living Room.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class EventType(str, Enum):
    video_clip = "video_clip"
    audio_block = "audio_block"
    subtitle = "subtitle"
    text_overlay = "text_overlay"
    transition = "transition"
    broll_insert = "broll_insert"
    dai_anchor = "dai_anchor"


class Importance(str, Enum):
    critical = "critical"
    recommended = "recommended"
    optional = "optional"


class TransitionStyle(str, Enum):
    cut = "Cut"
    cross_dissolve = "Cross Dissolve"
    whip_pan = "Whip Pan"
    glitch = "Glitch"
    zoom_blur = "Zoom Blur"
    flash = "Flash"


class TimelineEvent(BaseModel):
    """Un evento puntual en la línea de tiempo del editor."""

    event_id: int
    timecode_sec: int = Field(..., ge=0)
    duration_sec: int = Field(..., ge=0, le=600)
    event_type: EventType
    description: str
    source_ref: str | None = Field(
        default=None,
        description="Identificador del shot/bloque/sección que alimenta este evento",
    )
    importance: Importance = Importance.recommended


class SubtitleSegment(BaseModel):
    """Un chunk de subtítulo dinámico (2-4 segundos típicamente)."""

    seg_id: int
    timecode_start_sec: float = Field(..., ge=0)
    duration_sec: float = Field(..., gt=0, le=8)
    text: str
    highlight_keywords: list[str] = Field(default_factory=list)
    motion_style: Literal["pop", "shake", "fade", "none"] = "pop"


class DAIAnchor(BaseModel):
    """Punto natural de inserción dinámica de anuncio."""

    timecode_sec: int = Field(..., ge=0)
    minimum_break_sec: int = Field(default=5, ge=3, le=30)
    rationale: str = Field(..., description="Por qué este punto NO rompe la retención")
    section_after: str = Field(..., description="Bloque del guion que sigue al anuncio")


class ThreeSecondRuleViolation(BaseModel):
    """Tramo donde no hay un cambio visual en >3 segundos."""

    start_sec: int
    end_sec: int
    duration_sec: int
    suggested_fix: str


class EditingPlan(BaseModel):
    """Plan completo de montaje de un video."""

    target_resolution: Literal["4K", "1080p"] = "4K"
    aspect_ratio: Literal["16:9", "9:16"] = "16:9"
    target_fps: int = 24

    timeline: list[TimelineEvent]
    subtitles: list[SubtitleSegment]
    dai_anchors: list[DAIAnchor]
    transitions: list[TimelineEvent] = Field(default_factory=list)

    longest_static_gap_sec: int = Field(
        ..., description="Tramo más largo sin cambio visual (objetivo ≤ 3s)"
    )
    three_second_violations: list[ThreeSecondRuleViolation] = Field(default_factory=list)

    @property
    def three_second_rule_pass(self) -> bool:
        return self.longest_static_gap_sec <= 3 and not self.three_second_violations


class EditingReport(BaseModel):
    schema_version: str = "1.0"
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    script_ref: str
    audio_ref: str | None = None
    visuals_ref: str | None = None
    script_title: str

    plan: EditingPlan
    notes: str = ""

    @property
    def event_count(self) -> int:
        return len(self.plan.timeline)
