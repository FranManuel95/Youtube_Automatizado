"""Orquestación del pipeline end-to-end (producción asistida).

Automatiza lo repetitivo (audio plan, packaging, tracking) y marca como
manual lo que protege de la purga de YouTube 2026 (guion verificado,
screencast real, montaje). NO es generación de video 100% automática.
"""

from __future__ import annotations

from yt_auto.pipeline.project import (
    Stage,
    StageState,
    StageStatus,
    VideoProject,
    new_project_id,
)
from yt_auto.pipeline.runner import PipelinePlan, plan_pipeline, start_project

__all__ = [
    "PipelinePlan",
    "Stage",
    "StageState",
    "StageStatus",
    "VideoProject",
    "new_project_id",
    "plan_pipeline",
    "start_project",
]
