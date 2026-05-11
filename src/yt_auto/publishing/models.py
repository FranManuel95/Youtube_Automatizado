"""Modelos de dominio para publicación en YouTube.

Sigue las reglas del informe `docs/06_publicacion_y_escalado.md`:
- Metadata SEO con título <70 chars, descripción con CTA + capítulos +
  disclaimers + timestamps.
- Multi-Language Audio (MLA) para captar mercado US-Hispanic (RPM x4).
- Likeness Detection: declaración de uso de IA obligatoria.
- Categorías YPP / YMYL con disclaimers cuando corresponde.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class Privacy(str, Enum):
    public = "public"
    unlisted = "unlisted"
    private = "private"


class Category(str, Enum):
    """Subset relevante de categorías YouTube."""

    howto = "Howto & Style"
    education = "Education"
    people_blogs = "People & Blogs"
    news_politics = "News & Politics"
    nonprofits = "Nonprofits & Activism"


class Chapter(BaseModel):
    timecode_sec: int = Field(..., ge=0)
    title: str = Field(..., max_length=100)

    def youtube_timestamp(self) -> str:
        """Formato HH:MM:SS o MM:SS aceptado por YouTube."""
        s = int(self.timecode_sec)
        h, rem = divmod(s, 3600)
        m, sec = divmod(rem, 60)
        if h:
            return f"{h}:{m:02d}:{sec:02d}"
        return f"{m:02d}:{sec:02d}"


class MLATrack(BaseModel):
    """Pista de audio Multi-Language para una localización extra."""

    language_code: str = Field(..., description="BCP-47: en-US, es-MX, pt-BR, …")
    audio_file_ref: str = Field(..., description="Ruta al .mp3 del doblaje")
    is_default: bool = False
    notes: str | None = None


class YouTubeMetadata(BaseModel):
    title: str = Field(..., max_length=100, description="YouTube hard limit")
    description: str = Field(..., max_length=5000)
    tags: list[str] = Field(default_factory=list, description="Máximo 15 tags efectivos")
    category: Category = Category.education
    privacy: Privacy = Privacy.public
    publish_at: datetime | None = None
    made_for_kids: bool = False
    monetization_enabled: bool = True
    language: str = "es"


class PrePublishChecklist(BaseModel):
    """Checklist binario que bloquea la publicación si falla algún crítico."""

    # Críticos (bloquean)
    anti_ai_slop_passed: bool
    thumbnail_4k_ready: bool
    title_under_70_chars: bool
    description_has_disclaimer: bool
    likeness_declaration: bool

    # Recomendados (warnings)
    chapters_defined: bool
    tags_count_ok: bool
    dai_anchors_marked: bool
    mla_track_prepared: bool
    end_screen_planned: bool

    @property
    def critical_pass(self) -> bool:
        return all(
            [
                self.anti_ai_slop_passed,
                self.thumbnail_4k_ready,
                self.title_under_70_chars,
                self.description_has_disclaimer,
                self.likeness_declaration,
            ]
        )

    @property
    def all_pass(self) -> bool:
        return self.critical_pass and all(
            [
                self.chapters_defined,
                self.tags_count_ok,
                self.dai_anchors_marked,
                self.mla_track_prepared,
                self.end_screen_planned,
            ]
        )


class PublishingPlan(BaseModel):
    metadata: YouTubeMetadata
    chapters: list[Chapter]
    mla_tracks: list[MLATrack] = Field(default_factory=list)
    thumbnail_ref: str | None = None
    checklist: PrePublishChecklist


class PublishingReport(BaseModel):
    schema_version: str = "1.0"
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    script_ref: str
    editing_ref: str | None = None
    niche_audit_ref: str | None = None
    script_title: str

    plan: PublishingPlan
    mode: Literal["interactive", "api"] = "interactive"
    notes: str = ""
