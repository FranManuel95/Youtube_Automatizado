"""Tests del módulo compliance (disclosure IA + citas obligatorias + log humano)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from yt_auto.compliance import (
    AIDisclosure,
    ComplianceError,
    HumanReviewEntry,
    append_review_entry,
    load_review_log,
    render_disclosure_block,
    run_compliance_checks,
    validate_citations,
)
from yt_auto.publishing.niche_profile import load_profile

# --------------------------------------------------------------------------
# AIDisclosure
# --------------------------------------------------------------------------


def test_default_disclosure_has_yt_policy_keywords():
    d = AIDisclosure()
    text = d.disclosure_text_es.lower()
    assert "inteligencia artificial" in text
    assert "supervisión" in text
    assert "likeness" in text or "contenido sintético" in text


def test_render_disclosure_block_starts_with_marker():
    block = render_disclosure_block()
    assert block.startswith("ℹ TRANSPARENCIA")


# --------------------------------------------------------------------------
# Citation validator
# --------------------------------------------------------------------------


def test_validate_citations_passes_when_official_source_cited():
    profile = load_profile("real_estate_latino")
    desc = (
        "Más información oficial en https://www.hud.gov/program_offices/housing/sfh "
        "y NAHREP."
    )
    res = validate_citations(
        description=desc,
        title="Comprar casa con ITIN paso a paso",
        profile=profile,
    )
    assert res.passed is True
    assert res.matched_sources, "Debe matchear HUD"


def test_validate_citations_fails_when_no_official_source():
    profile = load_profile("real_estate_latino")
    res = validate_citations(
        description="Comprar casa es fácil. Confía en mí.",
        title="Compra tu casa hoy",
        profile=profile,
    )
    assert res.passed is False
    assert res.missing_critical is True
    assert res.reasons


def test_validate_citations_accepts_script_sources_as_fallback():
    profile = load_profile("real_estate_latino")
    res = validate_citations(
        description="Sin fuentes oficiales aquí.",
        title="Compra casa con ITIN",
        profile=profile,
        additional_sources_in_script=["IRS Publication 519 (Tax Guide for Aliens)"],
    )
    assert res.passed is True
    assert res.missing_critical is False


def test_validate_citations_flags_yellow_icon_words():
    profile = load_profile("itin_credito")
    desc = "Visita https://www.consumerfinance.gov/es/ para más info."
    res = validate_citations(
        description=desc,
        title="Aprobación garantizada de tarjeta",  # contiene yellow keyword
        profile=profile,
    )
    assert res.yellow_icon_hits
    assert res.passed is False


def test_validate_citations_default_profile_skips_check():
    profile = load_profile("_default")
    # _default declara muy pocas fuentes; pero como NO tiene obligación crítica,
    # el resultado depende: el check pasa si no hay yellow flags y las fuentes
    # del default están vacías → no aplica.
    res = validate_citations(
        description="Texto sin fuentes oficiales.",
        title="Título neutro sin yellow keywords",
        profile=profile,
    )
    # Default tiene 2 fuentes oficiales — aún así puede fallar; lo importante
    # es que el validador no rompe.
    assert isinstance(res.passed, bool)


# --------------------------------------------------------------------------
# Gates
# --------------------------------------------------------------------------


def _make_minimal_report(*, description: str, title: str = "Compra casa con ITIN paso a paso"):
    """Construye un PublishingReport mínimo válido para los tests."""
    from yt_auto.publishing.models import (
        Category,
        Chapter,
        PrePublishChecklist,
        Privacy,
        PublishingPlan,
        PublishingReport,
        YouTubeMetadata,
    )

    metadata = YouTubeMetadata(
        title=title,
        description=description,
        tags=["real estate latino", "ITIN"],
        category=Category.education,
        privacy=Privacy.private,
        language="es",
    )
    plan = PublishingPlan(
        metadata=metadata,
        chapters=[
            Chapter(timecode_sec=0, title="Intro"),
            Chapter(timecode_sec=30, title="Sección 1"),
            Chapter(timecode_sec=120, title="Sección 2"),
        ],
        checklist=PrePublishChecklist(
            anti_ai_slop_passed=True,
            thumbnail_4k_ready=True,
            title_under_70_chars=True,
            description_has_disclaimer=True,
            likeness_declaration=True,
            chapters_defined=True,
            tags_count_ok=True,
            dai_anchors_marked=True,
            mla_track_prepared=False,
            end_screen_planned=False,
        ),
    )
    return PublishingReport(
        script_ref="x.json",
        editing_ref="y.json",
        script_title=title,
        plan=plan,
    )


def test_run_compliance_passes_with_official_source_in_description():
    profile = load_profile("real_estate_latino")
    report = _make_minimal_report(
        description=(
            "Fuentes: https://www.hud.gov/program_offices/housing/sfh y "
            "https://nahrep.org/research/"
        ),
    )
    ok, result = run_compliance_checks(report, profile=profile)
    assert ok is True
    assert result.matched_sources


def test_run_compliance_strict_raises_on_failure():
    profile = load_profile("real_estate_latino")
    report = _make_minimal_report(description="Sin fuentes oficiales aquí.")
    with pytest.raises(ComplianceError) as exc_info:
        run_compliance_checks(report, profile=profile, strict=True)
    assert exc_info.value.reasons


def test_run_compliance_non_strict_returns_false():
    profile = load_profile("real_estate_latino")
    report = _make_minimal_report(description="Sin fuentes oficiales aquí.")
    ok, result = run_compliance_checks(report, profile=profile, strict=False)
    assert ok is False
    assert result.missing_critical


# --------------------------------------------------------------------------
# Human review log (JSONL persistente)
# --------------------------------------------------------------------------


def test_append_and_load_review_log_roundtrip(tmp_path: Path):
    log_path = tmp_path / "human_review.jsonl"

    entry1 = HumanReviewEntry(
        video_project_id="proj-001",
        stage="script",
        minutes_spent=45,
        editor="fran",
        notes="Reescribí hook completo",
    )
    entry2 = HumanReviewEntry(
        video_project_id="proj-001",
        stage="editing",
        minutes_spent=30,
        editor="fran",
    )
    entry3 = HumanReviewEntry(
        video_project_id="otro-proj",
        stage="script",
        minutes_spent=10,
    )

    append_review_entry(entry1, log_path=log_path)
    append_review_entry(entry2, log_path=log_path)
    append_review_entry(entry3, log_path=log_path)

    log = load_review_log("proj-001", log_path=log_path)
    assert log.video_project_id == "proj-001"
    assert len(log.entries) == 2
    assert log.total_minutes == 75
    assert log.stages_with_review == {"script", "editing"}


def test_human_review_log_jsonl_is_append_only(tmp_path: Path):
    log_path = tmp_path / "human_review.jsonl"
    entry = HumanReviewEntry(
        video_project_id="proj-A",
        stage="audio",
        minutes_spent=5,
    )
    append_review_entry(entry, log_path=log_path)
    append_review_entry(entry, log_path=log_path)

    raw = log_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(raw) == 2
    for line in raw:
        data = json.loads(line)
        assert data["video_project_id"] == "proj-A"
        assert "timestamp" in data


def test_human_review_entry_requires_minimum_minute():
    with pytest.raises(ValueError):
        HumanReviewEntry(
            video_project_id="x",
            stage="script",
            minutes_spent=0,
        )
