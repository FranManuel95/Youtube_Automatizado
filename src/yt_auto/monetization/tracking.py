"""Generador de UTMs estables por video para atribución de conversiones.

Política de UTMs:
- `utm_source=youtube` (siempre que el tráfico venga de YT, otros canales
  pasarán parámetro distinto)
- `utm_medium=video_long` | `video_short` | `community_post`
- `utm_campaign=<slug-corto-del-video>` (estable, no cambia entre ediciones)
- `utm_content=<program_id>` (qué afiliado generó el click)
- `utm_term=<niche_profile_id>` (atribución del subnicho que disparó la conversión)
"""

from __future__ import annotations

import re
from typing import Literal
from urllib.parse import urlencode

from pydantic import BaseModel, Field

from yt_auto.monetization.catalog import AffiliateProgram

MediumType = Literal["video_long", "video_short", "community_post", "description_only"]


class UTMCampaign(BaseModel):
    source: str = "youtube"
    medium: MediumType = "video_long"
    campaign: str = Field(..., description="Slug corto del video (estable)")
    content: str | None = None
    term: str | None = None

    def as_query(self) -> str:
        params = {
            "utm_source": self.source,
            "utm_medium": self.medium,
            "utm_campaign": self.campaign,
        }
        if self.content:
            params["utm_content"] = self.content
        if self.term:
            params["utm_term"] = self.term
        return urlencode(params)


class AffiliateLink(BaseModel):
    program_id: str
    display_name: str
    url: str
    cpa_usd_min: float
    cpa_usd_max: float
    rationale: str = ""


def _slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:50] or "video"


def build_utm_campaign(
    *,
    video_title_or_id: str,
    medium: MediumType = "video_long",
    niche_profile_id: str | None = None,
    affiliate_program_id: str | None = None,
) -> UTMCampaign:
    return UTMCampaign(
        medium=medium,
        campaign=_slugify(video_title_or_id),
        content=affiliate_program_id,
        term=niche_profile_id,
    )


def build_affiliate_link(
    program: AffiliateProgram,
    *,
    video_title_or_id: str,
    niche_profile_id: str | None = None,
    medium: MediumType = "video_long",
    rationale: str = "",
) -> AffiliateLink:
    """Aplica la plantilla `affiliate_url_template` con UTMs trackeables."""
    utm = build_utm_campaign(
        video_title_or_id=video_title_or_id,
        medium=medium,
        niche_profile_id=niche_profile_id,
        affiliate_program_id=program.id,
    )
    url = program.affiliate_url_template.replace("{utm}", utm.as_query())
    return AffiliateLink(
        program_id=program.id,
        display_name=program.display_name,
        url=url,
        cpa_usd_min=program.cpa_usd_min,
        cpa_usd_max=program.cpa_usd_max,
        rationale=rationale,
    )
