"""Etapa 1 - Inteligencia de mercado y validación de nicho.

Ver: docs/01_seleccion_de_nichos.md

API pública:
    - build_exploration_prompt: construye el prompt maestro para auditoría.
    - NicheCandidate / NicheAuditReport: modelos Pydantic de dominio.
    - save_report / load_report / render_markdown: persistencia.
    - ingest_response: parsea una respuesta JSON de Claude a un report.

Modo de trabajo:
    - "interactive": el CLI genera el prompt y el usuario lo pasa a Claude
      en sesión; la respuesta se ingesta con `yt-auto niche ingest`.
    - "api" (pendiente): llamada directa al SDK de Anthropic.

Framework de las 4 S: Streaming, Searching, Shopping, Scrolling.
"""

from __future__ import annotations

import json
import re

from yt_auto.niche.models import (
    CompetitionLevel,
    FourS,
    MarketTier,
    NicheAuditReport,
    NicheCandidate,
    RPMEstimate,
)
from yt_auto.niche.prompts import EXPLORATION_SYSTEM, build_exploration_prompt
from yt_auto.niche.storage import (
    ARCHIVE_DIR,
    OUTPUT_DIR,
    latest_report_path,
    load_report,
    render_markdown,
    save_report,
)

__all__ = [
    "ARCHIVE_DIR",
    "CompetitionLevel",
    "EXPLORATION_SYSTEM",
    "FourS",
    "MarketTier",
    "NicheAuditReport",
    "NicheCandidate",
    "OUTPUT_DIR",
    "RPMEstimate",
    "build_exploration_prompt",
    "ingest_response",
    "latest_report_path",
    "load_report",
    "render_markdown",
    "save_report",
]


def ingest_response(
    raw: str,
    *,
    model_used: str = "claude-opus-4-7",
    mode: str = "interactive",
) -> NicheAuditReport:
    """Convierte una respuesta cruda de Claude (string) en un report validado.

    Tolera que Claude envuelva el JSON en un bloque ```json ... ```.
    """
    text = raw.strip()
    fence = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    data = json.loads(text)
    data.setdefault("model_used", model_used)
    data.setdefault("mode", mode)
    return NicheAuditReport.model_validate(data)
