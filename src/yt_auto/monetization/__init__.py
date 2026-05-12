"""Etapa transversal - Monetización diversificada (afiliados + lead-gen).

El informe estratégico (sec. 8) y los benchmarks reales del nicho
US-Hispanic finanzas confirman que AdSense puro NO cubre el stack hasta
los 5-8k subs. El dinero está fuera de YouTube: afiliados CPA y lead-gen
B2B a profesionales (CPA hispanos, realtors NMLS).

Componentes:

- **Catálogo de programas** (`catalog`): 13 afiliados curados con CPA real
  2026 (Self, Kikoff, Nova Credit, Alterna, Stessa, DoorLoop, Gusto, etc.).
- **Tracking** (`tracking`): generador de UTMs estables por video para
  atribuir conversiones a piezas concretas.
- **Renderer** (`renderer`): bloque "Recursos" listo para descripción
  YouTube, ya con UTMs aplicadas.

La etapa `publishing/builder.py` debe llamar a `render_resources_block`
con el perfil de nicho resuelto para inyectar afiliados relevantes.
"""

from __future__ import annotations

from yt_auto.monetization.catalog import (
    AFFILIATE_CATALOG,
    AffiliateProgram,
    get_program,
    programs_for_profile,
)
from yt_auto.monetization.renderer import render_resources_block
from yt_auto.monetization.tracking import (
    AffiliateLink,
    UTMCampaign,
    build_affiliate_link,
    build_utm_campaign,
)

__all__ = [
    "AFFILIATE_CATALOG",
    "AffiliateLink",
    "AffiliateProgram",
    "UTMCampaign",
    "build_affiliate_link",
    "build_utm_campaign",
    "get_program",
    "programs_for_profile",
    "render_resources_block",
]
