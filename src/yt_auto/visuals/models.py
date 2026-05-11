"""Modelos de dominio para la etapa de visuales.

Sigue el flujo del informe `docs/04_generacion_visual.md`:
- Reference Sheet del personaje (4 vistas obligatorias).
- Shots cinematográficos mapeados a las secciones del guion.
- Plan de miniatura con regla de 3 elementos y pattern interrupt.
- Prompts JSON estructurados (Nano Banana / Seedance 2.0).
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


class ShotType(str, Enum):
    extreme_closeup = "Extreme Close-Up"
    closeup = "Close-Up"
    medium = "Medium Shot"
    full = "Full Shot"
    wide = "Wide / Establishing"
    over_shoulder = "Over the Shoulder"
    pov = "POV"
    insert = "Insert / Detail"
    broll = "B-Roll"


class CharacterView(str, Enum):
    frontal = "frontal"
    profile_left = "profile_left"
    profile_right = "profile_right"
    three_quarter = "three_quarter"
    back = "back"


class CharacterReferenceSheet(BaseModel):
    """Hoja de referencia técnica del personaje (avatar consistente).

    Cada vista incluye un prompt JSON listo para Nano Banana que fuerza
    los rasgos físicos y de iluminación.
    """

    name: str
    role: str = Field(..., description="Ej. 'narrador principal del canal'")
    age: str
    physical_features: dict[str, str] = Field(
        ..., description="Rasgos fijos clave: cara, pelo, ojos, complexión, marcas"
    )
    outfit_base: str = Field(..., description="Vestimenta base del personaje en este video")
    accent_notes: str | None = Field(
        default=None, description="Aspectos étnicos/culturales relevantes para coherencia"
    )
    views: dict[CharacterView, dict[str, Any]] = Field(
        ..., description="Vista -> prompt JSON completo para Nano Banana"
    )

    def has_mandatory_views(self) -> bool:
        mandatory = {
            CharacterView.frontal,
            CharacterView.profile_left,
            CharacterView.three_quarter,
        }
        return mandatory.issubset(set(self.views.keys()))


class VisualShot(BaseModel):
    """Un plano cinematográfico mapeado a una porción del guion."""

    shot_id: int
    related_block: str = Field(
        ..., description="Bloque/sección del guion que ilustra - ej. 'hook' o 'section_3'"
    )
    timecode_start_sec: int = Field(..., ge=0)
    duration_sec: int = Field(
        ...,
        ge=2,
        le=180,
        description=(
            "Duración del shot en la línea de tiempo. Puede superar 15s; en ese caso "
            "se compone de múltiples clips Seedance concatenados (Seedance limita 15s/clip)."
        ),
    )
    shot_type: ShotType

    description: str = Field(..., description="Descripción humana del plano")
    motion: str = Field(..., description="Vector de movimiento - ej. 'dolly in lento', 'pan derecha'")
    lighting: str
    ambient: str

    nano_banana_prompt_json: dict[str, Any] = Field(
        ..., description="Prompt JSON listo para generar el frame base con Nano Banana"
    )
    seedance_prompt_json: dict[str, Any] = Field(
        ..., description="Prompt JSON listo para animar con Seedance 2.0 (16:9, 720p, ≤15s)"
    )

    requires_character: bool = True
    pattern_interrupt: bool = Field(
        default=False, description="Si este shot es un pattern interrupt declarado"
    )


class ThumbnailPlan(BaseModel):
    """Plan de miniatura 4K con regla de 3 elementos."""

    title_overlay: str = Field(..., max_length=40, description="Máximo 3 palabras")
    face_element: str = Field(..., description="Descripción de la cara/expresión")
    object_element: str = Field(..., description="Objeto central disruptivo")
    pattern_interrupt_strategy: str = Field(..., description="Cómo rompe el estilo del nicho")
    color_strategy: str = Field(..., description="Paleta y dónde está el 'saco rojo'")

    resolution: Literal["4K"] = "4K"
    aspect_ratio: Literal["16:9"] = "16:9"

    nano_banana_prompt_json: dict[str, Any]


class VisualReport(BaseModel):
    schema_version: str = "1.0"
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    script_ref: str
    script_title: str

    character: CharacterReferenceSheet
    shots: list[VisualShot]
    thumbnail: ThumbnailPlan

    model_used: str = "claude-opus-4-7"
    mode: Literal["interactive", "api"] = "interactive"
    notes: str = ""

    @property
    def total_clip_duration_sec(self) -> int:
        return sum(s.duration_sec for s in self.shots)

    @property
    def pattern_interrupt_count(self) -> int:
        return sum(1 for s in self.shots if s.pattern_interrupt)
