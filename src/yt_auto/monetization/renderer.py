"""Renderer del bloque 'Recursos' para la descripción de YouTube.

Lee el `affiliate_focus` del perfil de nicho, resuelve los programas
contra el `AFFILIATE_CATALOG` y construye links con UTMs trackeables.
El bloque resultante se inyecta en `publishing/builder.py` antes de los
capítulos.

Importante (disclosure FTC): el bloque incluye AVISO de afiliación
obligatorio. Sin él, riesgo de strike y baja en CPC efectivo.
"""

from __future__ import annotations

from yt_auto.monetization.catalog import programs_for_profile
from yt_auto.monetization.tracking import build_affiliate_link
from yt_auto.publishing.niche_profile import NicheProfile

_AFFILIATE_DISCLAIMER_ES = (
    "💼 AVISO DE AFILIACIÓN: algunos de los enlaces de abajo son de afiliados; "
    "si abres una cuenta o contratas un producto, podemos recibir una pequeña "
    "comisión sin coste adicional para ti. Esto NO altera la información "
    "educativa del video."
)


def render_resources_block(
    profile: NicheProfile,
    *,
    video_title_or_id: str,
    max_links: int = 5,
    medium: str = "video_long",
) -> str:
    """Bloque 'Recursos' listo para pegar en descripción YouTube.

    Devuelve string vacío si el perfil no tiene afiliados configurados
    (perfil `_default` o nichos en exploración).
    """
    programs = programs_for_profile(profile)
    if not programs:
        return ""

    lines: list[str] = []
    lines.append("🔗 RECURSOS Y HERRAMIENTAS RECOMENDADAS")
    lines.append(_AFFILIATE_DISCLAIMER_ES)
    lines.append("")

    focus_map = {f.id: f.rationale for f in profile.affiliate_focus}

    for program in programs[:max_links]:
        link = build_affiliate_link(
            program,
            video_title_or_id=video_title_or_id,
            niche_profile_id=profile.id,
            medium=medium,  # type: ignore[arg-type]
            rationale=focus_map.get(program.id, ""),
        )
        lines.append(f"• {link.display_name}")
        lines.append(f"  → {link.url}")
        if link.rationale:
            lines.append(f"  ({link.rationale})")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
