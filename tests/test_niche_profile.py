"""Tests del loader de perfiles de nicho."""

from __future__ import annotations

import pytest

from yt_auto.publishing.niche_profile import (
    NicheProfile,
    list_profiles,
    load_profile,
    resolve_profile,
)


def test_list_profiles_returns_all_five():
    profiles = list_profiles()
    ids = {p.id for p in profiles}
    assert "real_estate_latino" in ids
    assert "tax_legal_inmigrantes" in ids
    assert "llc_emprendedor" in ids
    assert "itin_credito" in ids
    assert "finanzas_inmigrantes_paraguas" in ids


def test_load_profile_real_estate():
    p = load_profile("real_estate_latino")
    assert isinstance(p, NicheProfile)
    assert p.id == "real_estate_latino"
    assert any("FHA" in kw for kw in p.keyword_triggers)
    assert p.official_sources, "Real Estate debe declarar fuentes oficiales"
    assert any("HUD" in s.name for s in p.official_sources)


def test_load_profile_unknown_raises():
    with pytest.raises(FileNotFoundError):
        load_profile("nicho_inexistente")


def test_resolve_real_estate_from_niche_text():
    p = resolve_profile("Real estate para inmigrantes - cómo comprar primera casa con ITIN")
    assert p.id == "real_estate_latino"


def test_resolve_tax_legal_from_niche_text():
    p = resolve_profile("Tax preparation para inmigrantes con ITIN - declarar taxes")
    # Ambos perfiles disparan keywords; el tax-legal tiene más matches
    assert p.id in {"tax_legal_inmigrantes", "itin_credito"}


def test_resolve_falls_back_to_default():
    p = resolve_profile("Tema sin relación con finanzas inmigrantes")
    assert p.id == "finanzas_inmigrantes_paraguas"


def test_resolve_picks_more_specific_match():
    # "LLC" debería ganarle a "ITIN" si el texto es claramente de emprendedor
    p = resolve_profile("Abrir LLC sin SSN para freelancer 1099 inmigrante")
    assert p.id == "llc_emprendedor"


def test_yellow_icon_keywords_present_in_finance_profiles():
    for profile_id in ["real_estate_latino", "tax_legal_inmigrantes", "itin_credito"]:
        p = load_profile(profile_id)
        assert p.yellow_icon_keywords, f"{profile_id} debe declarar palabras yellow-icon"


def test_each_profile_has_disclaimer():
    for p in list_profiles():
        assert p.disclaimer.strip(), f"{p.id} sin disclaimer YMYL"
