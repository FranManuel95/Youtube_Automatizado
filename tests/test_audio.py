"""Tests del módulo audio."""

from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest

from yt_auto.audio import (
    AudioReport,
    BlockRole,
    ElevenLabsClient,
    ElevenLabsError,
    QuotaExceededError,
    build_plan,
    build_report,
    by_key,
    clean_for_tts,
    recommend_for_niche,
    synthesize_report,
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


# --------------------------------------------------------------------------
# Cliente ElevenLabs (sin red real, vía httpx.MockTransport)
# --------------------------------------------------------------------------


def _make_client(handler) -> ElevenLabsClient:
    return ElevenLabsClient("fake-key", transport=httpx.MockTransport(handler))


def test_client_rejects_empty_api_key():
    with pytest.raises(ValueError, match="ELEVENLABS_API_KEY"):
        ElevenLabsClient("")


def test_list_voices_parses_response():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/voices"
        assert request.headers["xi-api-key"] == "fake-key"
        return httpx.Response(
            200,
            json={
                "voices": [
                    {
                        "voice_id": "v1",
                        "name": "Mateo",
                        "category": "premade",
                        "labels": {"language": "Spanish", "gender": "male"},
                    },
                    {"voice_id": "v2", "name": "Sin labels"},
                ]
            },
        )

    with _make_client(handler) as client:
        voices = client.list_voices()
    assert [v.voice_id for v in voices] == ["v1", "v2"]
    assert voices[0].language == "Spanish"
    assert voices[0].gender == "male"
    assert voices[1].labels == {}


def test_get_subscription_computes_remaining():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/user/subscription"
        return httpx.Response(
            200,
            json={"tier": "free", "character_count": 8000, "character_limit": 10_000},
        )

    with _make_client(handler) as client:
        sub = client.get_subscription()
    assert sub.characters_remaining == 2000
    assert sub.tier == "free"


def test_text_to_speech_returns_mp3_bytes():
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["body"] = json.loads(request.content.decode())
        return httpx.Response(200, content=b"ID3-fake-mp3-bytes")

    with _make_client(handler) as client:
        from yt_auto.audio.voices import AUTHORITY_NARRATION_SETTINGS

        data = client.text_to_speech(
            voice_id="vX",
            text="hola",
            model_id="eleven_multilingual_v2",
            settings=AUTHORITY_NARRATION_SETTINGS,
        )
    assert data == b"ID3-fake-mp3-bytes"
    assert captured["path"] == "/v1/text-to-speech/vX"
    body = captured["body"]
    assert body["text"] == "hola"
    assert body["model_id"] == "eleven_multilingual_v2"
    assert 0.0 <= body["voice_settings"]["stability"] <= 1.0


def test_text_to_speech_requires_voice_id():
    from yt_auto.audio.voices import AUTHORITY_NARRATION_SETTINGS

    with (
        _make_client(lambda r: httpx.Response(200)) as client,
        pytest.raises(ValueError, match="voice_id"),
    ):
        client.text_to_speech(
            voice_id="",
            text="hola",
            model_id="eleven_multilingual_v2",
            settings=AUTHORITY_NARRATION_SETTINGS,
        )


def test_client_raises_eleven_error_on_4xx():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            401, json={"detail": {"status": "invalid_api_key", "message": "Bad key"}}
        )

    with _make_client(handler) as client, pytest.raises(ElevenLabsError) as exc_info:
        client.list_voices()
    assert exc_info.value.status_code == 401
    assert "Bad key" in str(exc_info.value)


# --------------------------------------------------------------------------
# Orquestador synth
# --------------------------------------------------------------------------


def test_synthesize_report_writes_one_mp3_per_block(sample_script_report, tmp_path: Path):
    report = build_report(sample_script_report, script_ref="x.json")

    calls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/user/subscription":
            return httpx.Response(
                200,
                json={
                    "tier": "free",
                    "character_count": 0,
                    "character_limit": 10_000,
                },
            )
        calls.append(request.url.path)
        return httpx.Response(200, content=b"mp3-bytes-" + request.url.path.encode())

    with _make_client(handler) as client:
        result = synthesize_report(
            report,
            client=client,
            voice_id="vTEST",
            output_base=tmp_path / "base",
        )

    assert result.generated_count == len(report.plan.blocks)
    assert result.skipped_count == 0
    for r in result.blocks:
        assert r.path.exists()
        assert r.path.read_bytes().startswith(b"mp3-bytes-")
    assert all(p.startswith("/v1/text-to-speech/vTEST") for p in calls)


def test_synthesize_report_skips_existing_mp3(sample_script_report, tmp_path: Path):
    report = build_report(sample_script_report, script_ref="x.json")
    base = tmp_path / "base"
    mp3_dir = base / "mp3"
    mp3_dir.mkdir(parents=True)
    first = report.plan.blocks[0]
    pre_path = mp3_dir / f"{first.block_id:02d}_{first.role.value}.mp3"
    pre_path.write_bytes(b"already-here")

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/user/subscription":
            return httpx.Response(
                200,
                json={"tier": "free", "character_count": 0, "character_limit": 10_000},
            )
        return httpx.Response(200, content=b"new")

    with _make_client(handler) as client:
        result = synthesize_report(
            report, client=client, voice_id="v", output_base=base
        )

    assert pre_path.read_bytes() == b"already-here"
    assert result.skipped_count == 1


def test_synthesize_report_overwrite_regenerates(sample_script_report, tmp_path: Path):
    report = build_report(sample_script_report, script_ref="x.json")
    base = tmp_path / "base"
    mp3_dir = base / "mp3"
    mp3_dir.mkdir(parents=True)
    first = report.plan.blocks[0]
    pre_path = mp3_dir / f"{first.block_id:02d}_{first.role.value}.mp3"
    pre_path.write_bytes(b"old")

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/user/subscription":
            return httpx.Response(
                200,
                json={"tier": "free", "character_count": 0, "character_limit": 10_000},
            )
        return httpx.Response(200, content=b"new")

    with _make_client(handler) as client:
        result = synthesize_report(
            report, client=client, voice_id="v", output_base=base, overwrite=True
        )

    assert pre_path.read_bytes() == b"new"
    assert result.skipped_count == 0


def test_synthesize_report_filter_by_block_id(sample_script_report, tmp_path: Path):
    report = build_report(sample_script_report, script_ref="x.json")

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/user/subscription":
            return httpx.Response(
                200,
                json={"tier": "free", "character_count": 0, "character_limit": 10_000},
            )
        return httpx.Response(200, content=b"x")

    with _make_client(handler) as client:
        result = synthesize_report(
            report,
            client=client,
            voice_id="v",
            output_base=tmp_path / "b",
            block_ids=[1],
        )
    assert len(result.blocks) == 1
    assert result.blocks[0].block_id == 1


def test_synthesize_report_unknown_block_raises(sample_script_report, tmp_path: Path):
    report = build_report(sample_script_report, script_ref="x.json")
    with (
        _make_client(lambda r: httpx.Response(200)) as client,
        pytest.raises(ValueError, match="inexistentes"),
    ):
        synthesize_report(
            report,
            client=client,
            voice_id="v",
            output_base=tmp_path / "b",
            block_ids=[999],
        )


def test_synthesize_report_quota_exceeded(sample_script_report, tmp_path: Path):
    report = build_report(sample_script_report, script_ref="x.json")

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/user/subscription":
            return httpx.Response(
                200,
                json={"tier": "free", "character_count": 9990, "character_limit": 10_000},
            )
        return httpx.Response(200, content=b"x")

    with (
        _make_client(handler) as client,
        pytest.raises(QuotaExceededError, match="quedan"),
    ):
        synthesize_report(
            report, client=client, voice_id="v", output_base=tmp_path / "b"
        )


def test_synthesize_report_skip_quota_check(sample_script_report, tmp_path: Path):
    report = build_report(sample_script_report, script_ref="x.json")
    visited: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        visited.append(request.url.path)
        return httpx.Response(200, content=b"x")

    with _make_client(handler) as client:
        synthesize_report(
            report,
            client=client,
            voice_id="v",
            output_base=tmp_path / "b",
            skip_quota_check=True,
        )

    assert "/v1/user/subscription" not in visited
