"""VideoProject: entidad de primera clase que liga todos los artefactos de un video.

Resuelve el gap detectado en la auditoría arquitectónica: hasta ahora cada
etapa guardaba su reporte con timestamp+slug independiente, sin un ID estable.
Si regenerabas el guion, el slug cambiaba y los artefactos downstream
apuntaban a ficheros huérfanos.

Cada proyecto vive en `output/projects/<project_id>/` y rastrea el estado de
las etapas en un `manifest.json`.
"""

from __future__ import annotations

import json
import secrets
import time
from datetime import datetime
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field

from yt_auto.config import ROOT_DIR

PROJECTS_DIR = ROOT_DIR / "output" / "projects"

# Crockford base32 (sin I, L, O, U) para IDs legibles y ordenables por tiempo.
_B32 = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def new_project_id() -> str:
    """ID ordenable por tiempo (ULID-like simplificado, sin dependencias)."""
    ms = int(time.time() * 1000)
    ts_part = ""
    for _ in range(10):
        ms, rem = divmod(ms, 32)
        ts_part = _B32[rem] + ts_part
    rand_part = "".join(secrets.choice(_B32) for _ in range(6))
    return ts_part + rand_part


class StageStatus(str, Enum):
    pending = "pending"
    automated = "automated"  # hecho por el pipeline sin intervención
    manual_required = "manual_required"  # requiere acción humana
    done = "done"


class Stage(str, Enum):
    niche = "niche"
    script = "script"
    audio = "audio"
    visuals = "visuals"
    screencast = "screencast"
    editing = "editing"
    thumbnail = "thumbnail"
    publishing = "publishing"


class StageState(BaseModel):
    status: StageStatus = StageStatus.pending
    artifact_path: str | None = None
    note: str = ""
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class VideoProject(BaseModel):
    project_id: str = Field(default_factory=new_project_id)
    topic: str
    niche_profile_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    stages: dict[str, StageState] = Field(default_factory=dict)

    @property
    def dir(self) -> Path:
        return PROJECTS_DIR / self.project_id

    @property
    def manifest_path(self) -> Path:
        return self.dir / "manifest.json"

    def set_stage(
        self,
        stage: Stage,
        status: StageStatus,
        *,
        artifact_path: str | None = None,
        note: str = "",
    ) -> None:
        self.stages[stage.value] = StageState(
            status=status, artifact_path=artifact_path, note=note
        )

    def save(self) -> Path:
        self.dir.mkdir(parents=True, exist_ok=True)
        self.manifest_path.write_text(
            self.model_dump_json(indent=2), encoding="utf-8"
        )
        return self.manifest_path

    @classmethod
    def load(cls, project_id: str) -> VideoProject:
        path = PROJECTS_DIR / project_id / "manifest.json"
        if not path.exists():
            raise FileNotFoundError(f"Proyecto '{project_id}' no encontrado en {path}")
        return cls.model_validate(json.loads(path.read_text(encoding="utf-8")))

    @staticmethod
    def list_all() -> list[str]:
        if not PROJECTS_DIR.exists():
            return []
        return sorted(p.name for p in PROJECTS_DIR.iterdir() if p.is_dir())
