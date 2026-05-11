"""Etapa 4 - Generación visual dinámica y consistencia de personajes.

Ver: docs/04_generacion_visual.md

API pública:
    - build_visuals_prompt: prompt maestro para que Claude diseñe el plan.
    - VISUALS_SYSTEM: instrucciones de sistema con reglas no negociables.
    - Modelos: CharacterReferenceSheet, VisualShot, ThumbnailPlan, VisualReport.
    - Presets: NANO_BANANA_REALISM_BASE, SUBJECT_CONSISTENCY_BASE,
      SEEDANCE_CLIP_BASE, THUMBNAIL_4K_BASE + helpers de merge.
    - save_report / load_report / render_markdown / ingest_response.

Estándar fotorrealista 2026: piel porosa, micro-textura, lente
cinematográfico, prohibido el look plástico.
"""

from __future__ import annotations

from yt_auto.visuals.models import (
    CharacterReferenceSheet,
    CharacterView,
    ShotType,
    ThumbnailPlan,
    VisualReport,
    VisualShot,
)
from yt_auto.visuals.presets import (
    NANO_BANANA_REALISM_BASE,
    SEEDANCE_CLIP_BASE,
    SUBJECT_CONSISTENCY_BASE,
    THUMBNAIL_4K_BASE,
    merge_nano_banana_base,
    merge_seedance_base,
    merge_thumbnail_base,
)
from yt_auto.visuals.prompts import VISUALS_SYSTEM, build_visuals_prompt
from yt_auto.visuals.storage import (
    ARCHIVE_DIR,
    OUTPUT_DIR,
    ingest_response,
    latest_report_path,
    load_report,
    render_markdown,
    save_report,
)

__all__ = [
    "ARCHIVE_DIR",
    "CharacterReferenceSheet",
    "CharacterView",
    "NANO_BANANA_REALISM_BASE",
    "OUTPUT_DIR",
    "SEEDANCE_CLIP_BASE",
    "SUBJECT_CONSISTENCY_BASE",
    "ShotType",
    "THUMBNAIL_4K_BASE",
    "ThumbnailPlan",
    "VISUALS_SYSTEM",
    "VisualReport",
    "VisualShot",
    "build_visuals_prompt",
    "ingest_response",
    "latest_report_path",
    "load_report",
    "merge_nano_banana_base",
    "merge_seedance_base",
    "merge_thumbnail_base",
    "render_markdown",
    "save_report",
]
