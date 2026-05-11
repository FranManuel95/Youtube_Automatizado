"""Etapa 6 - Publicación, MLA y gestión de la propiedad digital.

Ver: docs/06_publicacion_y_escalado.md

API pública:
    - build_report: ensambla ScriptReport + EditingReport en un
      PublishingReport con metadata SEO, capítulos y checklist.
    - Modelos: YouTubeMetadata, Chapter, MLATrack, PrePublishChecklist,
      PublishingPlan, PublishingReport.
    - save_report / load_report / render_markdown.

Modo actual: interactivo (genera el contenido para pegar en YouTube
Studio, sin OAuth). Modo `api` previsto con google-api-python-client.

Regla de oro: 5 canales x $500 > 1 canal x $2.500. La publicación se
diseña pensando en fragmentación de riesgo.
"""

from __future__ import annotations

from yt_auto.publishing.builder import build_report
from yt_auto.publishing.models import (
    Category,
    Chapter,
    MLATrack,
    PrePublishChecklist,
    Privacy,
    PublishingPlan,
    PublishingReport,
    YouTubeMetadata,
)
from yt_auto.publishing.storage import (
    ARCHIVE_DIR,
    OUTPUT_DIR,
    latest_report_path,
    load_report,
    render_markdown,
    save_report,
)

__all__ = [
    "ARCHIVE_DIR",
    "Category",
    "Chapter",
    "MLATrack",
    "OUTPUT_DIR",
    "PrePublishChecklist",
    "Privacy",
    "PublishingPlan",
    "PublishingReport",
    "YouTubeMetadata",
    "build_report",
    "latest_report_path",
    "load_report",
    "render_markdown",
    "save_report",
]
