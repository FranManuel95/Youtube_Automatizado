"""Etapa 2 - Ingeniería de guiones para máxima retención.

Ver: docs/02_ingenieria_de_guiones.md

API pública:
    - build_script_prompt: construye el prompt maestro para un video.
    - SCRIPT_SYSTEM: instrucciones de sistema con reglas no negociables.
    - ScriptReport / ScriptDraft / Hook / Section / HumanizationCheck:
      modelos Pydantic.
    - save_report / load_report / render_markdown / ingest_response.

Objetivo: retención > 80% en los primeros 30s. CTR estimado > 5.5%.
"""

from __future__ import annotations

from yt_auto.scripts.models import (
    Hook,
    HumanizationCheck,
    Section,
    ScriptDraft,
    ScriptReport,
    TitleStyle,
    ViewerIdeal,
)
from yt_auto.scripts.prompts import SCRIPT_SYSTEM, build_script_prompt
from yt_auto.scripts.storage import (
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
    "Hook",
    "HumanizationCheck",
    "OUTPUT_DIR",
    "SCRIPT_SYSTEM",
    "Section",
    "ScriptDraft",
    "ScriptReport",
    "TitleStyle",
    "ViewerIdeal",
    "build_script_prompt",
    "ingest_response",
    "latest_report_path",
    "load_report",
    "render_markdown",
    "save_report",
]
