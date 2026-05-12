"""Disclosures de IA y contenido sintético.

YouTube 2026 exige `altered_content=true` en la API de upload cuando se
usa voz/imagen/video generados por IA con potencial de confundir. Además
la política "Likeness Detection" se aplica a voces clonadas y avatares.

Este módulo proporciona el texto estándar (ES) que el pipeline inyecta
en la descripción y la bandera que `publishing/api.py` debe enviar al
endpoint `youtube.videos.insert`.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

DEFAULT_AI_DISCLOSURE_ES = (
    "Parte de la narración y los visuales de este video se han producido con "
    "asistencia de inteligencia artificial bajo supervisión editorial humana. "
    "Cumplimos las políticas de YouTube sobre contenido sintético y Likeness "
    "Detection. Los datos numéricos, normativas y casos citados provienen de "
    "fuentes oficiales enlazadas en la descripción; este contenido es educativo "
    "y no constituye asesoría personalizada."
)


class AIDisclosure(BaseModel):
    """Declaración de uso de IA conforme a política YouTube 2026."""

    altered_or_synthetic_content: bool = True
    voice_is_ai_generated: bool = True
    visuals_are_ai_generated: bool = True
    avatar_uses_likeness_of_real_person: bool = False
    disclosure_text_es: str = Field(default=DEFAULT_AI_DISCLOSURE_ES)


def render_disclosure_block(disclosure: AIDisclosure | None = None) -> str:
    """Devuelve el bloque markdown listo para inyectar en la descripción."""
    d = disclosure or AIDisclosure()
    return f"ℹ TRANSPARENCIA\n{d.disclosure_text_es}\n"
