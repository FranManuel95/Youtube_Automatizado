"""Tests del módulo niche."""

from __future__ import annotations

import json

import pytest

from yt_auto.niche import (
    NicheAuditReport,
    build_exploration_prompt,
    ingest_response,
    render_markdown,
)


def _sample_payload() -> dict:
    return {
        "market_focus": "US-Hispanic",
        "content_format": "long_form",
        "target_count": 2,
        "methodology_notes": "test",
        "candidates": [
            {
                "name": "A",
                "headline": "h",
                "description": "d",
                "target_market": "US-Hispanic",
                "four_s": ["Streaming", "Searching"],
                "rpm": {
                    "market": "US-Hispanic",
                    "tier": "Tier 1.5 (US-Hispanic)",
                    "rpm_min_usd": 10.0,
                    "rpm_max_usd": 20.0,
                },
                "demand_evidence": ["e1"],
                "gap_hypothesis": "g",
                "competition_level": "medio",
                "niche_bending_angle": None,
                "sample_titles": ["t1"],
                "risks": ["r1"],
                "score": 9,
                "rationale": "porque sí",
            },
            {
                "name": "B",
                "headline": "h",
                "description": "d",
                "target_market": "US-Hispanic",
                "four_s": ["Searching"],
                "rpm": {
                    "market": "US-Hispanic",
                    "tier": "Tier 1.5 (US-Hispanic)",
                    "rpm_min_usd": 5.0,
                    "rpm_max_usd": 10.0,
                },
                "demand_evidence": [],
                "gap_hypothesis": "g",
                "competition_level": "alto",
                "sample_titles": [],
                "risks": [],
                "score": 6,
                "rationale": "r",
            },
        ],
    }


def test_build_prompt_includes_market_and_format():
    prompt = build_exploration_prompt(
        market="US-Hispanic",
        language="es",
        content_format="long_form",
        target_duration_min=12,
        target_count=5,
    )
    assert "US-Hispanic" in prompt
    assert "long_form" in prompt
    assert "5" in prompt


def test_ingest_response_parses_payload():
    raw = json.dumps(_sample_payload())
    report = ingest_response(raw)
    assert isinstance(report, NicheAuditReport)
    assert len(report.candidates) == 2
    assert report.top(1)[0].name == "A"


def test_ingest_response_tolerates_markdown_fence():
    raw = "```json\n" + json.dumps(_sample_payload()) + "\n```"
    report = ingest_response(raw)
    assert len(report.candidates) == 2


def test_score_range_validation():
    payload = _sample_payload()
    payload["candidates"][0]["score"] = 11
    with pytest.raises(Exception):
        NicheAuditReport.model_validate(payload)


def test_render_markdown_includes_top_table():
    report = ingest_response(json.dumps(_sample_payload()))
    md = render_markdown(report)
    assert "# Auditoría de nichos" in md
    assert "Top 3" in md
    assert "**A**" in md
