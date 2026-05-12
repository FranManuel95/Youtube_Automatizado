"""Modelos de dominio para análisis competitivo YouTube.

Capa de tipos sobre las respuestas crudas de YouTube Data API v3.
Solo se modelan los campos que el pipeline consume.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ChannelStatistics(BaseModel):
    subscriber_count: int = Field(0, ge=0)
    view_count: int = Field(0, ge=0)
    video_count: int = Field(0, ge=0)
    hidden_subscriber_count: bool = False


class Channel(BaseModel):
    """Canal de YouTube con metadata pública."""

    channel_id: str
    title: str
    description: str = ""
    country: str | None = None
    published_at: datetime | None = None
    statistics: ChannelStatistics = Field(default_factory=ChannelStatistics)
    uploads_playlist_id: str | None = None
    custom_url: str | None = None

    @property
    def url(self) -> str:
        return f"https://www.youtube.com/channel/{self.channel_id}"

    @property
    def age_days(self) -> int | None:
        if self.published_at is None:
            return None
        return (datetime.utcnow() - self.published_at.replace(tzinfo=None)).days

    @property
    def avg_views_per_video(self) -> float:
        if self.statistics.video_count == 0:
            return 0.0
        return self.statistics.view_count / self.statistics.video_count


class VideoStatistics(BaseModel):
    view_count: int = Field(0, ge=0)
    like_count: int = Field(0, ge=0)
    comment_count: int = Field(0, ge=0)


class Video(BaseModel):
    """Video de YouTube con metadata pública."""

    video_id: str
    channel_id: str
    title: str
    description: str = ""
    published_at: datetime
    duration_seconds: int = Field(0, ge=0)
    statistics: VideoStatistics = Field(default_factory=VideoStatistics)
    tags: list[str] = Field(default_factory=list)

    @property
    def url(self) -> str:
        return f"https://www.youtube.com/watch?v={self.video_id}"

    @property
    def age_days(self) -> int:
        return (datetime.utcnow() - self.published_at.replace(tzinfo=None)).days

    @property
    def views_per_day(self) -> float:
        days = max(1, self.age_days)
        return self.statistics.view_count / days


class OutlierVideo(BaseModel):
    """Video que supera significativamente la media de su canal."""

    video: Video
    channel_median_views: int = Field(..., ge=0)
    multiplier_vs_median: float = Field(..., ge=0)
    rationale: str = ""

    @property
    def is_strong_outlier(self) -> bool:
        return self.multiplier_vs_median >= 3.0


class NicheScanReport(BaseModel):
    """Snapshot del estado competitivo de un nicho."""

    schema_version: str = "1.0"
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    niche_profile_id: str
    query_used: str
    channels: list[Channel] = Field(default_factory=list)
    quota_units_spent: int = 0

    @property
    def total_subscribers(self) -> int:
        return sum(c.statistics.subscriber_count for c in self.channels)

    @property
    def median_subscribers(self) -> int:
        if not self.channels:
            return 0
        sorted_subs = sorted(c.statistics.subscriber_count for c in self.channels)
        return sorted_subs[len(sorted_subs) // 2]

    @property
    def big_fish_count(self) -> int:
        """Cantidad de canales >100k subs (saturación alta)."""
        return sum(1 for c in self.channels if c.statistics.subscriber_count >= 100_000)

    @property
    def fragmentation_score(self) -> str:
        """Etiqueta cualitativa de saturación."""
        if self.big_fish_count == 0:
            return "fragmentado-bajo"
        if self.big_fish_count <= 2:
            return "fragmentado-medio"
        return "saturado"
