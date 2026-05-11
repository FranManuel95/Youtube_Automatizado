"""Etapa 3 - Producción de audio y locución.

Ver: docs/03_audio_y_locucion.md

API pública:
    - build_plan / build_report: transforman un ScriptReport en un AudioReport.
    - clean_for_tts: limpieza determinista del texto para síntesis.
    - CATALOG / recommend_for_niche: catálogo curado de presets de voz.
    - save_report / load_report / render_markdown.

Modelo estándar: ElevenLabs `eleven_multilingual_v2` (máxima estabilidad
narrativa para 10-25 minutos). Modo actual: interactivo, compatible con
el plan Free de ElevenLabs (10.000 chars/mes).
"""

from __future__ import annotations

from yt_auto.audio.models import (
    AudioPlan,
    AudioReport,
    BlockRole,
    NarrationBlock,
    VoicePreset,
    VoiceSettings,
)
from yt_auto.audio.narration import build_plan, build_report, clean_for_tts
from yt_auto.audio.storage import (
    ARCHIVE_DIR,
    OUTPUT_DIR,
    latest_report_path,
    load_report,
    render_markdown,
    save_report,
)
from yt_auto.audio.voices import (
    AUTHORITY_NARRATION_SETTINGS,
    CATALOG,
    DYNAMIC_SHORTS_SETTINGS,
    by_key,
    recommend_for_niche,
)

__all__ = [
    "ARCHIVE_DIR",
    "AUTHORITY_NARRATION_SETTINGS",
    "AudioPlan",
    "AudioReport",
    "BlockRole",
    "CATALOG",
    "DYNAMIC_SHORTS_SETTINGS",
    "NarrationBlock",
    "OUTPUT_DIR",
    "VoicePreset",
    "VoiceSettings",
    "build_plan",
    "build_report",
    "by_key",
    "clean_for_tts",
    "latest_report_path",
    "load_report",
    "recommend_for_niche",
    "render_markdown",
    "save_report",
]
