"""Tests del módulo editing."""

from __future__ import annotations

import json

import pytest

from yt_auto.audio import build_report as build_audio_report
from yt_auto.editing import (
    EditingReport,
    build_report,
    detect_keywords,
    render_subtitles_csv,
    segment_block,
)
from yt_auto.scripts import ingest_response as ingest_script
from yt_auto.visuals import ingest_response as ingest_visuals


def _script_payload() -> dict:
    return {
        "candidate_name": "x",
        "draft": {
            "title": "T",
            "title_alternatives": [],
            "title_style": "3-Points / Open Loop",
            "niche": "Finanzas",
            "target_market": "US-Hispanic",
            "target_language": "es",
            "target_duration_min": 12,
            "viewer_ideal": {
                "nombre": "L", "edad": "30", "ubicacion": "TX",
                "situacion": "s", "dolor": "d", "deseo": "z", "objeciones": [],
            },
            "hook": {
                "text": "Hay un hispano con FICO 782. Tres puertas legales en EE.UU.",
                "duration_sec": 20,
                "visual_cue": "v",
                "promise": "p",
                "open_loop": "l",
            },
            "sections": [
                {
                    "heading": "Sec 1",
                    "content": "El ITIN cuesta 0 dólares. Form W-7 del IRS. Reporta a CFPB.",
                    "duration_sec": 60,
                    "sources": [],
                },
                {
                    "heading": "Sec 2",
                    "content": "Capital One acepta ITIN. Discover también. Construyes FICO 700+.",
                    "duration_sec": 60,
                    "sources": [],
                },
            ],
            "cta": "Descarga el PDF gratuito.",
            "word_count": 100,
            "estimated_retention_30s": 0.85,
            "estimated_ctr": 0.07,
            "humanization": {
                "pilar_localizacion": True, "pilar_autoridad": True,
                "pilar_refinamiento": True, "paradoja_emocional": True,
                "pattern_interrupts_count": 3, "sources_count": 3,
            },
        },
    }


def _visuals_payload() -> dict:
    nb = {"composition": "x", "subject": "y"}
    sd = {"motion_description": "static"}
    return {
        "script_ref": "x.json",
        "script_title": "T",
        "character": {
            "name": "Luis", "role": "n", "age": "38",
            "physical_features": {"pelo": "negro"},
            "outfit_base": "camisa",
            "accent_notes": None,
            "views": {
                "frontal": nb, "profile_left": nb, "three_quarter": nb,
            },
        },
        "shots": [
            {
                "shot_id": 1, "related_block": "hook",
                "timecode_start_sec": 0, "duration_sec": 20,
                "shot_type": "Medium Shot",
                "description": "Luis hablando", "motion": "static",
                "lighting": "soft", "ambient": "office",
                "nano_banana_prompt_json": nb, "seedance_prompt_json": sd,
                "requires_character": True, "pattern_interrupt": False,
            },
            {
                "shot_id": 2, "related_block": "section_1",
                "timecode_start_sec": 20, "duration_sec": 60,
                "shot_type": "Insert / Detail",
                "description": "Form W-7 closeup", "motion": "dolly",
                "lighting": "warm", "ambient": "desk",
                "nano_banana_prompt_json": nb, "seedance_prompt_json": sd,
                "requires_character": False, "pattern_interrupt": False,
            },
        ],
        "thumbnail": {
            "title_overlay": "TRES PUERTAS",
            "face_element": "f", "object_element": "o",
            "pattern_interrupt_strategy": "p", "color_strategy": "c",
            "nano_banana_prompt_json": nb,
        },
    }


@pytest.fixture
def reports():
    s = ingest_script(json.dumps(_script_payload()))
    a = build_audio_report(s, script_ref="x.json")
    v = ingest_visuals(json.dumps(_visuals_payload()))
    return s, a, v


def test_detect_keywords_finds_numbers_and_dollars():
    kws = detect_keywords("$1,500 al ITIN y FICO 782 después de 90 días")
    assert "$1,500" in kws or "1,500" in " ".join(kws)
    assert "ITIN" in kws
    assert "FICO" in kws
    assert any("782" in k for k in kws)


def test_detect_keywords_finds_domain_terms():
    kws = detect_keywords("Capital One acepta ITIN y reporta a TransUnion")
    assert any("Capital One" in k for k in kws)
    assert "ITIN" in kws
    assert "TransUnion" in kws


def test_segment_block_creates_multiple_segments():
    segs = segment_block(
        text="El ITIN cuesta cero dólares. Form W-7 del IRS. Reporta a tres burós distintos para construir crédito real.",
        block_start_sec=10,
        block_duration_sec=12,
    )
    assert len(segs) >= 2
    assert segs[0].timecode_start_sec >= 10


def test_segment_block_highlights_keywords():
    segs = segment_block(
        text="Tu FICO sube a 720 con ITIN y secured card.",
        block_start_sec=0,
        block_duration_sec=4,
    )
    all_kws = [k for s in segs for k in s.highlight_keywords]
    assert any("FICO" in k for k in all_kws)


def test_build_report_combines_three_sources(reports):
    s, a, v = reports
    r = build_report(script=s, audio=a, visuals=v, script_ref="s.json")
    assert isinstance(r, EditingReport)
    assert len(r.plan.timeline) > 0
    assert len(r.plan.subtitles) > 0
    assert r.script_title == "T"


def test_dai_anchors_detected_between_sections(reports):
    s, a, v = reports
    r = build_report(script=s, audio=a, visuals=v, script_ref="s.json")
    # Con 2 secciones esperamos 1-2 DAI anchors
    assert len(r.plan.dai_anchors) >= 1
    # Todos los anchors deben estar dentro del rango temporal
    for anchor in r.plan.dai_anchors:
        assert anchor.timecode_sec > 0


def test_three_second_rule_detects_violations(reports):
    s, a, v = reports
    r = build_report(script=s, audio=a, visuals=v, script_ref="s.json")
    # El shot 2 dura 60s sin pattern_interrupt → violación esperada
    assert not r.plan.three_second_rule_pass
    assert len(r.plan.three_second_violations) >= 1


def test_three_second_rule_passes_when_no_visuals(reports):
    """Sin visuals no se puede auditar; se marca como violación informativa."""
    s, a, _ = reports
    r = build_report(script=s, audio=a, visuals=None, script_ref="s.json")
    assert not r.plan.three_second_rule_pass


def test_render_subtitles_csv_has_headers(reports):
    s, a, v = reports
    r = build_report(script=s, audio=a, visuals=v, script_ref="s.json")
    csv = render_subtitles_csv(r)
    assert csv.split("\n")[0].startswith("start_sec,end_sec,text")
    assert len(csv.split("\n")) > 1
