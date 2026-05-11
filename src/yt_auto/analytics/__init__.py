"""Etapa 7 - Auditoría y mejora continua (Ask Studio / Inspiration Tab).

Ver: docs/07_guia_tecnica_general.md (sección Ask Studio) y
docs/05_edicion_y_packaging.md § 6 (Auditoría).

API pública:
    - parse_retention_csv / detect_leaks: parser de YouTube Studio.
    - assess_portfolio: scorer de salud multi-canal.
    - Builders de prompts Ask Studio: outlier, drops, gaps, competidores, A/B.
    - save_report / load_report / render_markdown.

El algoritmo no es código, es la audiencia: estos prompts y métricas
sirven para priorizar la satisfacción humana real (informe doc/02 § 6).
"""

from __future__ import annotations

from yt_auto.analytics.ask_studio import (
    ALL_BUILDERS,
    ab_test_thumbnails_prompt,
    competitor_pattern_prompt,
    drop_detection_prompt,
    gap_detection_prompt,
    outlier_analysis_prompt,
)
from yt_auto.analytics.models import (
    AnalyticsReport,
    AskStudioPrompt,
    ChannelHealth,
    PortfolioHealth,
    RetentionLeak,
    RetentionPoint,
    VideoPerformance,
)
from yt_auto.analytics.portfolio import assess_portfolio
from yt_auto.analytics.retention import (
    DEFAULT_DROP_THRESHOLD_PCT,
    DEFAULT_WINDOW_SEC,
    detect_leaks,
    load_csv,
    parse_retention_csv,
)
from yt_auto.analytics.storage import (
    ARCHIVE_DIR,
    OUTPUT_DIR,
    latest_report_path,
    load_report,
    render_markdown,
    save_report,
)

__all__ = [
    "ALL_BUILDERS",
    "ARCHIVE_DIR",
    "AnalyticsReport",
    "AskStudioPrompt",
    "ChannelHealth",
    "DEFAULT_DROP_THRESHOLD_PCT",
    "DEFAULT_WINDOW_SEC",
    "OUTPUT_DIR",
    "PortfolioHealth",
    "RetentionLeak",
    "RetentionPoint",
    "VideoPerformance",
    "ab_test_thumbnails_prompt",
    "assess_portfolio",
    "competitor_pattern_prompt",
    "detect_leaks",
    "drop_detection_prompt",
    "gap_detection_prompt",
    "latest_report_path",
    "load_csv",
    "load_report",
    "outlier_analysis_prompt",
    "parse_retention_csv",
    "render_markdown",
    "save_report",
]
