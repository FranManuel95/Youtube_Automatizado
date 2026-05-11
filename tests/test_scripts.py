"""Tests del módulo scripts."""

from __future__ import annotations

import json

import pytest

from yt_auto.scripts import (
    HumanizationCheck,
    ScriptReport,
    build_script_prompt,
    ingest_response,
    render_markdown,
)


def _payload() -> dict:
    return {
        "candidate_name": "Finanzas para inmigrantes en EE.UU.",
        "model_used": "claude-opus-4-7",
        "mode": "interactive",
        "notes": "",
        "draft": {
            "title": "Test Title",
            "title_alternatives": [],
            "title_style": "3-Points / Open Loop",
            "niche": "Finanzas",
            "target_market": "US-Hispanic",
            "target_language": "es",
            "target_duration_min": 12,
            "viewer_ideal": {
                "nombre": "Luis",
                "edad": "28-42",
                "ubicacion": "TX",
                "situacion": "x",
                "dolor": "y",
                "deseo": "z",
                "objeciones": [],
            },
            "hook": {
                "text": "...",
                "duration_sec": 25,
                "visual_cue": "split screen",
                "promise": "p",
                "open_loop": "l",
            },
            "sections": [
                {
                    "heading": "S1",
                    "content": "c",
                    "duration_sec": 60,
                    "sources": ["fuente1"],
                }
            ],
            "cta": "cta",
            "word_count": 1800,
            "estimated_retention_30s": 0.85,
            "estimated_ctr": 0.07,
            "humanization": {
                "pilar_localizacion": True,
                "pilar_autoridad": True,
                "pilar_refinamiento": True,
                "paradoja_emocional": True,
                "pattern_interrupts_count": 5,
                "sources_count": 4,
            },
        },
    }


def test_build_prompt_includes_required_fields():
    p = build_script_prompt(
        niche="Finanzas",
        candidate_name="Cred ITIN",
        target_market="US-Hispanic",
        target_language="es",
        target_duration_min=12,
        topic="Cómo construir crédito con ITIN",
    )
    assert "Finanzas" in p
    assert "US-Hispanic" in p
    assert "12" in p
    assert "ITIN" in p


def test_ingest_response_parses_full_payload():
    raw = json.dumps(_payload())
    r = ingest_response(raw)
    assert isinstance(r, ScriptReport)
    assert r.draft.title == "Test Title"
    assert r.draft.humanization.pasa is True


def test_humanization_fails_when_paradox_missing():
    payload = _payload()
    payload["draft"]["humanization"]["paradoja_emocional"] = False
    r = ingest_response(json.dumps(payload))
    assert r.draft.humanization.pasa is False


def test_humanization_fails_with_few_pattern_interrupts():
    payload = _payload()
    payload["draft"]["humanization"]["pattern_interrupts_count"] = 1
    r = ingest_response(json.dumps(payload))
    assert r.draft.humanization.pasa is False


def test_retention_out_of_range_rejected():
    payload = _payload()
    payload["draft"]["estimated_retention_30s"] = 1.5
    with pytest.raises(Exception):
        ScriptReport.model_validate(payload)


def test_total_duration_sums_hook_and_sections():
    r = ingest_response(json.dumps(_payload()))
    assert r.draft.total_duration_sec == 25 + 60


def test_render_markdown_includes_hook_and_cta():
    r = ingest_response(json.dumps(_payload()))
    md = render_markdown(r)
    assert "Hook" in md
    assert "## CTA" in md
    assert "anti-AI-Slop" in md
