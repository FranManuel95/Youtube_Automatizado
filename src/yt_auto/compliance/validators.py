"""Validadores anti-AI-Slop: citas obligatorias y palabras de riesgo.

El sello "agregador-educador" exige que cada video referencie al menos
una `OfficialSource` declarada en el perfil de nicho. Sin esa cita,
el contenido se trata como opinión sin respaldo y dispara yellow icon.
"""

from __future__ import annotations

from pydantic import BaseModel

from yt_auto.publishing.niche_profile import NicheProfile


class CitationValidationResult(BaseModel):
    """Resultado del check de citas oficiales."""

    passed: bool
    matched_sources: list[str]
    missing_critical: bool
    yellow_icon_hits: list[str]
    reasons: list[str]


def _normalize(text: str) -> str:
    return text.lower()


def validate_citations(
    *,
    description: str,
    title: str,
    profile: NicheProfile,
    additional_sources_in_script: list[str] | None = None,
) -> CitationValidationResult:
    """Comprueba que la descripción cite al menos 1 fuente oficial del perfil
    y que el título no contenga `yellow_icon_keywords`.

    No es un validador legal — es una guardia contra olvidos del agregador-
    educador. Si el perfil no declara fuentes oficiales (perfil `_default`),
    se considera que el check no aplica (`missing_critical=False`).
    """
    desc_norm = _normalize(description)
    title_norm = _normalize(title)

    matched: list[str] = []
    for source in profile.official_sources:
        if source.url.lower() in desc_norm or source.name.lower() in desc_norm:
            matched.append(source.name)

    additional = additional_sources_in_script or []
    has_additional = any(s for s in additional if s.strip())

    needs_official = bool(profile.official_sources)
    passed_citations = (not needs_official) or bool(matched) or has_additional
    missing_critical = needs_official and not matched and not has_additional

    yellow_hits = [kw for kw in profile.yellow_icon_keywords if kw.lower() in title_norm]

    reasons: list[str] = []
    if missing_critical:
        reasons.append(
            f"El perfil '{profile.id}' exige al menos una cita oficial; "
            f"ninguna URL/nombre de {len(profile.official_sources)} fuentes "
            "declaradas aparece en la descripción."
        )
    if yellow_hits:
        reasons.append(
            f"El título contiene palabras de yellow-icon ({', '.join(yellow_hits)}). "
            "Reescribe para evitar 'limited ads'."
        )

    return CitationValidationResult(
        passed=passed_citations and not yellow_hits,
        matched_sources=matched,
        missing_critical=missing_critical,
        yellow_icon_hits=yellow_hits,
        reasons=reasons,
    )
