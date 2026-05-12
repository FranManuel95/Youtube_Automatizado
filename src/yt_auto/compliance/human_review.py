"""Log persistente de horas de edición humana por video.

Trazabilidad mínima para apelaciones futuras a YouTube si el canal entra
en revisión por la oleada anti-AI-Slop. Cada entrada registra:

- `video_project_id` (o slug temporal si todavía no hay ProjectId)
- minutos invertidos en cada etapa por un humano (no IA)
- notas de qué se revisó/cambió manualmente

Se persiste en `output/_compliance/human_review.jsonl` como append-only
para que sea auditable. Nunca se trunca ni reescribe.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from yt_auto.config import ROOT_DIR

ReviewStage = Literal["niche", "script", "audio", "visuals", "editing", "publishing"]

DEFAULT_LOG_PATH = ROOT_DIR / "output" / "_compliance" / "human_review.jsonl"


class HumanReviewEntry(BaseModel):
    """Una sesión de revisión humana sobre un proyecto."""

    timestamp: datetime = Field(default_factory=datetime.utcnow)
    video_project_id: str = Field(..., description="ULID o slug temporal del video")
    stage: ReviewStage
    minutes_spent: int = Field(..., ge=1, description="Mínimo 1 minuto registrable")
    editor: str = Field(default="self", description="Nombre o handle del editor humano")
    notes: str = ""

    def to_jsonl(self) -> str:
        return self.model_dump_json() + "\n"


class HumanReviewLog(BaseModel):
    """Vista agregada del log de revisiones de un proyecto."""

    video_project_id: str
    entries: list[HumanReviewEntry] = Field(default_factory=list)

    @property
    def total_minutes(self) -> int:
        return sum(e.minutes_spent for e in self.entries)

    @property
    def stages_with_review(self) -> set[str]:
        return {e.stage for e in self.entries}


def append_review_entry(entry: HumanReviewEntry, *, log_path: Path | None = None) -> Path:
    path = log_path or DEFAULT_LOG_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(entry.to_jsonl())
    return path


def load_review_log(video_project_id: str, *, log_path: Path | None = None) -> HumanReviewLog:
    path = log_path or DEFAULT_LOG_PATH
    entries: list[HumanReviewEntry] = []
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            if data.get("video_project_id") == video_project_id:
                entries.append(HumanReviewEntry.model_validate(data))
    return HumanReviewLog(video_project_id=video_project_id, entries=entries)
