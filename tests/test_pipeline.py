"""Tests del orquestador pipeline (producción asistida)."""

from __future__ import annotations

from pathlib import Path

import pytest

from yt_auto.pipeline import (
    Stage,
    StageStatus,
    VideoProject,
    new_project_id,
    plan_pipeline,
    start_project,
)
from yt_auto.pipeline import project as project_mod


@pytest.fixture(autouse=True)
def _tmp_projects_dir(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(project_mod, "PROJECTS_DIR", tmp_path / "projects")


def test_new_project_id_is_sortable_by_time():
    a = new_project_id()
    b = new_project_id()
    assert len(a) == 16
    assert len(b) == 16
    # Mismo o posterior en tiempo: el prefijo temporal no decrece
    assert b >= a or b[:10] >= a[:10]


def test_start_project_creates_manifest():
    project = start_project(topic="Automatización IA inmobiliaria leads", niche_profile_id="x")
    assert project.manifest_path.exists()
    assert project.topic.startswith("Automat")
    # Todas las etapas arrancan en pending
    assert all(s.status == StageStatus.pending for s in project.stages.values())


def test_start_project_resolves_niche_from_topic():
    # "CRM inmobiliario" es un keyword_trigger del perfil definitivo
    project = start_project(topic="Monta un CRM inmobiliario con IA paso a paso")
    assert project.niche_profile_id == "automatizacion_ia_inmobiliaria"


def test_plan_without_script_marks_script_manual():
    project = start_project(topic="test", niche_profile_id="x")
    plan = plan_pipeline(project, has_script=False)
    assert "script" in plan.manual_stages
    assert "script" not in plan.automated_stages


def test_plan_with_script_automates_audio_and_packaging():
    project = start_project(topic="test", niche_profile_id="x")
    plan = plan_pipeline(project, has_script=True)
    assert "audio" in plan.automated_stages
    assert "packaging" in plan.automated_stages
    assert "script" in plan.automated_stages


def test_manual_stages_always_present():
    """Screencast, editing y thumbnail SIEMPRE son manuales (foso anti-purga)."""
    project = start_project(topic="test", niche_profile_id="x")
    plan = plan_pipeline(project, has_script=True)
    assert "screencast" in plan.manual_stages
    assert "editing" in plan.manual_stages
    assert "thumbnail" in plan.manual_stages


def test_project_roundtrip_load():
    project = start_project(topic="persistencia", niche_profile_id="x")
    pid = project.project_id
    loaded = VideoProject.load(pid)
    assert loaded.project_id == pid
    assert loaded.topic == "persistencia"


def test_list_all_projects():
    p1 = start_project(topic="uno", niche_profile_id="x")
    p2 = start_project(topic="dos", niche_profile_id="x")
    ids = VideoProject.list_all()
    assert p1.project_id in ids
    assert p2.project_id in ids


def test_set_stage_updates_status():
    project = start_project(topic="test", niche_profile_id="x")
    project.set_stage(Stage.audio, StageStatus.automated, note="ok")
    assert project.stages["audio"].status == StageStatus.automated
    assert project.stages["audio"].note == "ok"


def test_load_unknown_project_raises():
    with pytest.raises(FileNotFoundError):
        VideoProject.load("NOEXISTE000000000")
