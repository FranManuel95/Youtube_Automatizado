"""Modelos de dominio para la etapa de audio.

Sigue el flujo del informe `docs/03_audio_y_locucion.md`:
- Generación por bloques (Hook + Secciones + CTA).
- Modelo `eleven_multilingual_v2` como estándar.
- Settings de Expressive Speech con stability 40-60%.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class BlockRole(str, Enum):
    hook = "hook"
    section = "section"
    cta = "cta"


class VoicePreset(BaseModel):
    """Voz recomendada para un mercado y estilo concreto."""

    id_key: str = Field(..., description="Clave operativa interna (no es el voice_id real)")
    display_name: str
    gender: Literal["male", "female", "neutral"]
    age_bracket: str = Field(..., description="Ej. 35-50")
    accent: str = Field(..., description="Acento sugerido del producto comercial")
    use_case: str = Field(..., description="Cuándo usarla")
    note_es: str | None = None


class VoiceSettings(BaseModel):
    """Sliders de ElevenLabs (Expressive Speech)."""

    stability: float = Field(..., ge=0.0, le=1.0, description="40-60% recomendado para narración")
    similarity_boost: float = Field(..., ge=0.0, le=1.0)
    style: float = Field(0.0, ge=0.0, le=1.0, description="Exageración estilística")
    use_speaker_boost: bool = True


class NarrationBlock(BaseModel):
    """Un bloque de locución listo para pegar en el panel de ElevenLabs."""

    block_id: int
    role: BlockRole
    heading: str = Field(..., description="Etiqueta humana - ej. 'Hook' o 'Sección 3: Secured cards'")
    text: str = Field(..., description="Texto limpio (sin visuales, sin [verificar], puntuado para TTS)")
    target_duration_sec: int
    word_count: int
    character_count: int
    suggested_settings: VoiceSettings


class AudioPlan(BaseModel):
    """Plan completo de locución para un guion."""

    voice_preset_key: str
    voice_id_env_var: str = Field(
        default="ELEVENLABS_VOICE_ID",
        description="Variable de entorno donde el usuario fija el voice_id real",
    )
    model_id: str = "eleven_multilingual_v2"
    blocks: list[NarrationBlock]

    @property
    def total_chars(self) -> int:
        return sum(b.character_count for b in self.blocks)

    @property
    def total_words(self) -> int:
        return sum(b.word_count for b in self.blocks)

    @property
    def estimated_duration_sec(self) -> int:
        return sum(b.target_duration_sec for b in self.blocks)


class AudioReport(BaseModel):
    schema_version: str = "1.0"
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    script_ref: str = Field(..., description="Path al ScriptReport origen")
    script_title: str

    plan: AudioPlan

    eleven_free_tier_fits: bool = Field(
        ..., description="¿Cabe en los 10.000 chars/mes del plan Free?"
    )
    notes: str = ""
