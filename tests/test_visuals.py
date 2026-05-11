"""Tests del módulo visuals."""

from __future__ import annotations

import json

import pytest

from yt_auto.visuals import (
    NANO_BANANA_REALISM_BASE,
    SUBJECT_CONSISTENCY_BASE,
    THUMBNAIL_4K_BASE,
    CharacterReferenceSheet,
    CharacterView,
    VisualReport,
    ingest_response,
    merge_nano_banana_base,
    merge_thumbnail_base,
    render_markdown,
)


def _minimal_payload() -> dict:
    nb = {"composition": "x", "subject": "y"}
    sd = {"motion_description": "static"}
    return {
        "script_ref": "x.json",
        "script_title": "T",
        "model_used": "claude-opus-4-7",
        "mode": "interactive",
        "character": {
            "name": "Luis",
            "role": "narrador",
            "age": "38",
            "physical_features": {"pelo": "negro"},
            "outfit_base": "camisa azul",
            "accent_notes": None,
            "views": {
                "frontal": {**NANO_BANANA_REALISM_BASE, **SUBJECT_CONSISTENCY_BASE, **nb},
                "profile_left": {**NANO_BANANA_REALISM_BASE, **nb},
                "three_quarter": {**NANO_BANANA_REALISM_BASE, **nb},
            },
        },
        "shots": [
            {
                "shot_id": 1,
                "related_block": "hook",
                "timecode_start_sec": 0,
                "duration_sec": 10,
                "shot_type": "Medium Shot",
                "description": "d",
                "motion": "static",
                "lighting": "l",
                "ambient": "a",
                "nano_banana_prompt_json": nb,
                "seedance_prompt_json": sd,
                "requires_character": True,
                "pattern_interrupt": False,
            },
            {
                "shot_id": 2,
                "related_block": "section_1",
                "timecode_start_sec": 10,
                "duration_sec": 5,
                "shot_type": "Insert / Detail",
                "description": "d",
                "motion": "static",
                "lighting": "l",
                "ambient": "a",
                "nano_banana_prompt_json": nb,
                "seedance_prompt_json": sd,
                "requires_character": False,
                "pattern_interrupt": True,
            },
        ],
        "thumbnail": {
            "title_overlay": "TRES PUERTAS",
            "face_element": "f",
            "object_element": "o",
            "pattern_interrupt_strategy": "minimalismo",
            "color_strategy": "saco rojo",
            "nano_banana_prompt_json": {**THUMBNAIL_4K_BASE, **nb},
        },
    }


def test_merge_nano_banana_keeps_realism_base():
    out = merge_nano_banana_base({"composition": "centered"})
    assert out["skin_details"] == NANO_BANANA_REALISM_BASE["skin_details"]
    assert out["composition"] == "centered"
    assert "subject_consistency" in out


def test_merge_thumbnail_preserves_4k():
    out = merge_thumbnail_base({"subject": "x"})
    assert out["resolution"] == "3840x2160"
    assert out["aspect_ratio"] == "16:9"


def test_ingest_response_parses_minimal_payload():
    raw = json.dumps(_minimal_payload())
    r = ingest_response(raw)
    assert isinstance(r, VisualReport)
    assert r.character.name == "Luis"
    assert len(r.shots) == 2


def test_character_mandatory_views():
    raw = json.dumps(_minimal_payload())
    r = ingest_response(raw)
    assert r.character.has_mandatory_views() is True


def test_character_mandatory_views_fails_when_missing():
    payload = _minimal_payload()
    payload["character"]["views"].pop("three_quarter")
    r = ingest_response(json.dumps(payload))
    assert r.character.has_mandatory_views() is False


def test_thumbnail_title_overlay_max_length():
    payload = _minimal_payload()
    payload["thumbnail"]["title_overlay"] = "x" * 50
    with pytest.raises(Exception):
        VisualReport.model_validate(payload)


def test_shot_duration_allows_long_shots():
    payload = _minimal_payload()
    payload["shots"][0]["duration_sec"] = 120
    r = VisualReport.model_validate(payload)
    assert r.shots[0].duration_sec == 120


def test_pattern_interrupt_count():
    r = ingest_response(json.dumps(_minimal_payload()))
    assert r.pattern_interrupt_count == 1


def test_total_clip_duration_sums_shots():
    r = ingest_response(json.dumps(_minimal_payload()))
    assert r.total_clip_duration_sec == 15


def test_render_markdown_includes_character_and_thumbnail():
    r = ingest_response(json.dumps(_minimal_payload()))
    md = render_markdown(r)
    assert "Personaje" in md
    assert "Luis" in md
    assert "Miniatura" in md
    assert "TRES PUERTAS" in md
