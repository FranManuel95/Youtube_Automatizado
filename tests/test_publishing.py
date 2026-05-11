"""Tests del módulo publishing."""

from __future__ import annotations

import json

import pytest

from yt_auto.audio import build_report as build_audio
from yt_auto.editing import build_report as build_editing
from yt_auto.publishing import (
    Category,
    Chapter,
    PublishingReport,
    build_report,
    render_markdown,
)
from yt_auto.scripts import ingest_response as ingest_script
from yt_auto.visuals import ingest_response as ingest_visuals

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from test_editing import _script_payload, _visuals_payload  # noqa: E402


@pytest.fixture
def reports():
    s = ingest_script(json.dumps(_script_payload()))
    a = build_audio(s, script_ref="s.json")
    v = ingest_visuals(json.dumps(_visuals_payload()))
    e = build_editing(script=s, audio=a, visuals=v, script_ref="s.json")
    return s, e


def test_chapter_timestamp_formats():
    assert Chapter(timecode_sec=0, title="x").youtube_timestamp() == "00:00"
    assert Chapter(timecode_sec=65, title="x").youtube_timestamp() == "01:05"
    assert Chapter(timecode_sec=3661, title="x").youtube_timestamp() == "1:01:01"


def test_build_report_produces_youtube_metadata(reports):
    s, e = reports
    r = build_report(script=s, editing=e, script_ref="s.json", editing_ref="e.json")
    assert isinstance(r, PublishingReport)
    assert r.plan.metadata.title == s.draft.title[:100]
    assert r.plan.metadata.category == Category.education
    assert r.plan.metadata.language == s.draft.target_language


def test_description_includes_disclaimer_for_finance(reports):
    s, e = reports
    r = build_report(script=s, editing=e, script_ref="s.json", editing_ref="e.json")
    assert "AVISO IMPORTANTE" in r.plan.metadata.description
    assert "TRANSPARENCIA" in r.plan.metadata.description


def test_chapters_include_intro_and_cta(reports):
    s, e = reports
    r = build_report(script=s, editing=e, script_ref="s.json", editing_ref="e.json")
    assert r.plan.chapters[0].timecode_sec == 0
    assert "Introducción" in r.plan.chapters[0].title
    assert "Plan de acción" in r.plan.chapters[-1].title


def test_checklist_critical_pass_when_all_ok(reports):
    s, e = reports
    r = build_report(script=s, editing=e, script_ref="s.json", editing_ref="e.json")
    c = r.plan.checklist
    # title "T" (1 char) pasa, anti-AI-Slop pasa por fixture, descripción tiene disclaimer
    assert c.critical_pass is True


def test_checklist_fails_when_title_too_long(reports):
    s, e = reports
    s.draft.title = "x" * 80  # supera 70
    r = build_report(script=s, editing=e, script_ref="s.json", editing_ref="e.json")
    assert r.plan.checklist.title_under_70_chars is False
    assert r.plan.checklist.critical_pass is False


def test_tags_in_valid_range(reports):
    s, e = reports
    r = build_report(script=s, editing=e, script_ref="s.json", editing_ref="e.json")
    assert 5 <= len(r.plan.metadata.tags) <= 15


def test_render_markdown_includes_verdict_section(reports):
    s, e = reports
    r = build_report(script=s, editing=e, script_ref="s.json", editing_ref="e.json")
    md = render_markdown(r)
    assert "LISTO PARA PUBLICAR" in md or "NO PUBLICAR" in md
    assert "Metadata YouTube" in md
    assert "Capítulos" in md


def test_description_length_under_youtube_limit(reports):
    s, e = reports
    r = build_report(script=s, editing=e, script_ref="s.json", editing_ref="e.json")
    assert len(r.plan.metadata.description) <= 5000
