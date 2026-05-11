"""Tests del módulo audio."""

from __future__ import annotations

import json

import pytest

from yt_auto.audio import (
    AudioReport,
    BlockRole,
    build_plan,
    build_report,
    by_key,
    clean_for_tts,
    recommend_for_niche,
)
from yt_auto.scripts import ingest_response


@pytest.fixture
def sample_script_report():
    payload = {
        "candidate_name": "x",
        "draft": {
            "title": "T",
            "title_alternatives": [],
            "title_style": "3-Points / Open Loop",
            "niche": "Finanzas para inmigrantes en EE.UU.",
            "target_market": "US-Hispanic",
            "target_language": "es",
            "target_duration_min": 12,
            "viewer_ideal": {
                "nombre": "L", "edad": "30", "ubicacion": "TX",
                "situacion": "s", "dolor": "d", "deseo": "z", "objeciones": [],
            },
            "hook": {
                "text": "Hola mundo. [verificar dato] Es importante destacar que esto va al panel.",
                "duration_sec": 20,
                "visual_cue": "v",
                "promise": "p",
                "open_loop": "l",
            },
            "sections": [
                {
                    "heading": "S1",
                    "content": "Contenido (CFPB 2024). En conclusión, esto se elimina.",
                    "duration_sec": 60,
                    "sources": [],
                },
                {
                    "heading": "S2",
                    "content": "Otro bloque corto pero  con  espacios  raros.",
                    "duration_sec": 60,
                    "sources": [],
                },
            ],
            "cta": "Descarga el PDF.",
            "word_count": 100,
            "estimated_retention_30s": 0.85,
            "estimated_ctr": 0.07,
            "humanization": {
                "pilar_localizacion": True,
                "pilar_autoridad": True,
                "pilar_refinamiento": True,
                "paradoja_emocional": True,
                "pattern_interrupts_count": 4,
                "sources_count": 4,
            },
        },
    }
    return ingest_response(json.dumps(payload))


def test_clean_for_tts_strips_brackets_and_fillers():
    out = clean_for_tts("Hola [verificar fuente]. Es importante destacar que sí.")
    assert "[" not in out
    assert "Es importante destacar" not in out
    assert "Hola" in out


def test_clean_for_tts_normalizes_spaces():
    assert clean_for_tts("a    b   c") == "a b c"


def test_clean_for_tts_strips_inline_refs():
    out = clean_for_tts("Datos importantes (CFPB 2024) confirman algo.")
    assert "(CFPB" not in out
    assert "confirman algo" in out


def test_recommend_voice_for_finance_returns_authority(sample_script_report):
    preset = recommend_for_niche("Finanzas para inmigrantes", "long_form")
    assert preset.id_key == "es_us_male_authority"


def test_recommend_voice_for_shorts_returns_dynamic():
    preset = recommend_for_niche("cualquier nicho", "shorts")
    assert preset.id_key == "es_us_female_dynamic"


def test_by_key_unknown_raises():
    with pytest.raises(KeyError):
        by_key("inexistente")


def test_build_plan_creates_hook_sections_and_cta(sample_script_report):
    plan = build_plan(sample_script_report)
    assert len(plan.blocks) == 1 + 2 + 1  # hook + 2 sections + cta
    roles = [b.role for b in plan.blocks]
    assert roles[0] == BlockRole.hook
    assert roles[-1] == BlockRole.cta
    assert roles[1:-1] == [BlockRole.section, BlockRole.section]


def test_build_plan_cleans_content(sample_script_report):
    plan = build_plan(sample_script_report)
    section_text = plan.blocks[1].text
    assert "(CFPB" not in section_text
    assert "En conclusión" not in section_text


def test_build_report_detects_free_tier_fit(sample_script_report):
    report = build_report(sample_script_report, script_ref="x.json")
    assert isinstance(report, AudioReport)
    assert report.eleven_free_tier_fits is True
    assert report.script_title == "T"


def test_settings_within_recommended_range(sample_script_report):
    plan = build_plan(sample_script_report)
    s = plan.blocks[0].suggested_settings
    assert 0.40 <= s.stability <= 0.60
    assert 0.50 <= s.similarity_boost <= 0.90
