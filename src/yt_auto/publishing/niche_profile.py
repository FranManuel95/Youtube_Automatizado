"""Carga y resolución de perfiles de nicho declarativos.

Sustituye el hardcoding de `TAGS_FINANZAS_HISPANIC` por perfiles YAML en
`assets/niche_profiles/`. Cada perfil declara:

- tags / hashtags / disclaimer / official_sources / mla_target_markets
- yellow_icon_keywords que disparan limited ads
- affiliate_focus y leadgen_channels consumidos por el módulo `monetization/`

La resolución es por keyword matching contra `script.draft.niche` con
fallback a `_default.yaml` si nada coincide.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from yt_auto.config import ROOT_DIR

PROFILES_DIR = ROOT_DIR / "assets" / "niche_profiles"
_DEFAULT_PROFILE_ID = "_default"


class OfficialSource(BaseModel):
    name: str
    url: str


class MLATargets(BaseModel):
    primary: str
    secondary: list[str] = Field(default_factory=list)


class AffiliateFocus(BaseModel):
    id: str
    rationale: str


class NicheProfile(BaseModel):
    """Perfil de nicho declarativo cargado desde YAML."""

    id: str
    display_name: str
    parent_niche: str = ""
    keyword_triggers: list[str] = Field(
        default_factory=list,
        description="Keywords para resolver el perfil desde script.draft.niche",
    )
    search_queries: list[str] = Field(
        default_factory=list,
        description=(
            "Queries optimizadas para YouTube Search. Si está vacío, se "
            "genera una desde keyword_triggers (subóptimo)."
        ),
    )
    tags: list[str] = Field(default_factory=list)
    hashtags: list[str] = Field(default_factory=list)
    disclaimer: str = ""
    official_sources: list[OfficialSource] = Field(default_factory=list)
    mla_target_markets: MLATargets | None = None
    youtube_category: str = "education"
    yellow_icon_keywords: list[str] = Field(default_factory=list)
    affiliate_focus: list[AffiliateFocus] = Field(default_factory=list)
    leadgen_channels: list[str] = Field(default_factory=list)


def load_profile(profile_id: str, *, profiles_dir: Path | None = None) -> NicheProfile:
    base = profiles_dir or PROFILES_DIR
    path = base / f"{profile_id}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Perfil de nicho '{profile_id}' no encontrado en {base}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return NicheProfile.model_validate(data)


def list_profiles(*, profiles_dir: Path | None = None) -> list[NicheProfile]:
    base = profiles_dir or PROFILES_DIR
    if not base.exists():
        return []
    out: list[NicheProfile] = []
    for path in sorted(base.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        out.append(NicheProfile.model_validate(data))
    return out


def resolve_profile(niche_text: str, *, profiles_dir: Path | None = None) -> NicheProfile:
    """Resuelve el perfil más específico que matchea `niche_text`.

    Estrategia: scoreamos por número de `keyword_triggers` que aparecen como
    substring case-insensitive en `niche_text`. Empate → primer match alfabético.
    Sin match → `_default`.
    """
    niche_lower = niche_text.lower()
    profiles = list_profiles(profiles_dir=profiles_dir)
    if not profiles:
        raise FileNotFoundError("No hay perfiles de nicho disponibles.")

    scored: list[tuple[int, NicheProfile]] = []
    for prof in profiles:
        if prof.id == _DEFAULT_PROFILE_ID:
            continue
        score = sum(1 for kw in prof.keyword_triggers if kw.lower() in niche_lower)
        if score > 0:
            scored.append((score, prof))

    if scored:
        scored.sort(key=lambda x: (-x[0], x[1].id))
        return scored[0][1]

    return load_profile(_DEFAULT_PROFILE_ID, profiles_dir=profiles_dir)
