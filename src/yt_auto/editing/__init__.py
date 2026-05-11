"""Etapa 5 - Edición dinámica y packaging de alto impacto.

Ver: docs/05_edicion_y_packaging.md

API pública:
    - build_report: ensambla ScriptReport + AudioReport + VisualReport
      en un EditingReport con timeline, subtítulos, DAI anchors y
      auditoría de la regla de 3 segundos.
    - segment_block / detect_keywords: subtítulos dinámicos.
    - save_report / load_report / render_markdown / render_subtitles_csv.

Resolución obligatoria: 4K para competir en el Living Room.
"""

from __future__ import annotations

from yt_auto.editing.assembly import build_report
from yt_auto.editing.models import (
    DAIAnchor,
    EditingPlan,
    EditingReport,
    EventType,
    Importance,
    SubtitleSegment,
    ThreeSecondRuleViolation,
    TimelineEvent,
    TransitionStyle,
)
from yt_auto.editing.storage import (
    ARCHIVE_DIR,
    OUTPUT_DIR,
    latest_report_path,
    load_report,
    render_markdown,
    render_subtitles_csv,
    save_report,
)
from yt_auto.editing.subtitles import detect_keywords, segment_block

__all__ = [
    "ARCHIVE_DIR",
    "DAIAnchor",
    "EditingPlan",
    "EditingReport",
    "EventType",
    "Importance",
    "OUTPUT_DIR",
    "SubtitleSegment",
    "ThreeSecondRuleViolation",
    "TimelineEvent",
    "TransitionStyle",
    "build_report",
    "detect_keywords",
    "latest_report_path",
    "load_report",
    "render_markdown",
    "render_subtitles_csv",
    "save_report",
    "segment_block",
]
