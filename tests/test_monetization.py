"""Tests del módulo monetization (catálogo + UTMs + renderer)."""

from __future__ import annotations

import pytest

from yt_auto.monetization import (
    AFFILIATE_CATALOG,
    build_affiliate_link,
    build_utm_campaign,
    get_program,
    programs_for_profile,
    render_resources_block,
)
from yt_auto.publishing.niche_profile import load_profile

# --------------------------------------------------------------------------
# Catálogo
# --------------------------------------------------------------------------


def test_catalog_has_critical_programs():
    ids = {p.id for p in AFFILIATE_CATALOG}
    # Programas indispensables del nicho según el análisis
    for required in [
        "self_financial",
        "kikoff",
        "nova_credit",
        "alterna_card",
        "stessa",
        "doorloop",
        "gusto",
        "mercury",
        "quickbooks",
    ]:
        assert required in ids, f"Falta programa crítico: {required}"


def test_get_program_returns_correct_one():
    p = get_program("self_financial")
    assert p.id == "self_financial"
    assert p.category == "credit_builder"
    assert p.spanish_landing_available is True


def test_get_program_unknown_raises():
    with pytest.raises(KeyError):
        get_program("inexistente")


def test_programs_for_profile_resolves_focus():
    profile = load_profile("real_estate_latino")
    programs = programs_for_profile(profile)
    ids = [p.id for p in programs]
    assert "stessa" in ids
    assert "doorloop" in ids
    assert "rocket_mortgage" in ids


def test_programs_for_profile_ignores_unknown_ids(tmp_path):
    profile = load_profile("real_estate_latino")
    # Inyectamos un focus inexistente en una copia
    profile.affiliate_focus.append(
        type(profile.affiliate_focus[0])(id="programa_que_no_existe", rationale="x")
    )
    programs = programs_for_profile(profile)
    # No crashea y devuelve los que sí existen
    assert all(p.id != "programa_que_no_existe" for p in programs)


# --------------------------------------------------------------------------
# UTMs
# --------------------------------------------------------------------------


def test_build_utm_campaign_slugifies_title():
    utm = build_utm_campaign(
        video_title_or_id="¿Cómo construir crédito con ITIN en 2026?",
        niche_profile_id="itin_credito",
        affiliate_program_id="self_financial",
    )
    assert utm.campaign.startswith("c-mo-construir-cr-dito") or "como" in utm.campaign
    assert utm.content == "self_financial"
    assert utm.term == "itin_credito"


def test_utm_query_includes_all_params():
    utm = build_utm_campaign(
        video_title_or_id="test-video",
        niche_profile_id="real_estate_latino",
        affiliate_program_id="stessa",
    )
    qs = utm.as_query()
    assert "utm_source=youtube" in qs
    assert "utm_medium=video_long" in qs
    assert "utm_campaign=test-video" in qs
    assert "utm_content=stessa" in qs
    assert "utm_term=real_estate_latino" in qs


def test_build_affiliate_link_substitutes_template():
    program = get_program("self_financial")
    link = build_affiliate_link(
        program,
        video_title_or_id="primer-video",
        niche_profile_id="itin_credito",
    )
    assert "self.inc" in link.url
    assert "utm_campaign=primer-video" in link.url
    assert "utm_content=self_financial" in link.url
    assert link.cpa_usd_min == 10


# --------------------------------------------------------------------------
# Renderer
# --------------------------------------------------------------------------


def test_render_resources_block_includes_disclaimer_and_links():
    profile = load_profile("real_estate_latino")
    block = render_resources_block(profile, video_title_or_id="primera-casa-fha")

    assert "AVISO DE AFILIACIÓN" in block
    assert "Stessa" in block
    assert "DoorLoop" in block
    assert "utm_campaign=primera-casa-fha" in block


def test_render_resources_block_empty_for_default_profile():
    profile = load_profile("_default")
    block = render_resources_block(profile, video_title_or_id="x")
    # _default no tiene affiliate_focus
    assert block == ""


def test_render_respects_max_links():
    profile = load_profile("itin_credito")
    block = render_resources_block(
        profile, video_title_or_id="test", max_links=2
    )
    # Solo 2 entradas con prefijo "•"
    bullet_lines = [line for line in block.splitlines() if line.startswith("• ")]
    assert len(bullet_lines) == 2
