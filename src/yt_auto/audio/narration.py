"""Transformación de un guion en bloques de locución listos para TTS.

Limpia el texto narrativo de marcadores que rompen la síntesis (notas
entre corchetes, indicaciones de visual, fuentes citadas en línea) y
genera un plan por bloques manejable por el plan Free de ElevenLabs
(10.000 caracteres/mes).
"""

from __future__ import annotations

import re

from yt_auto.audio.models import (
    AudioPlan,
    AudioReport,
    BlockRole,
    NarrationBlock,
    VoiceSettings,
)
from yt_auto.audio.voices import (
    AUTHORITY_NARRATION_SETTINGS,
    DYNAMIC_SHORTS_SETTINGS,
    recommend_for_niche,
)
from yt_auto.scripts.models import ScriptReport

# Patrones que NO deben aparecer en la locución final.
_BRACKET_ANNOTATION = re.compile(r"\[\s*verificar[^\]]*\]", re.IGNORECASE)
_PARENTHETICAL_REF = re.compile(r"\((CFPB|IRS|myFICO|Experian|Equifax|TransUnion)[^\)]*\)")
_MULTIPLE_SPACES = re.compile(r"\s{2,}")
_PROHIBITED_LLM_FILLERS = [
    "Es importante destacar que ",
    "Es importante destacar ",
    "En resumen, ",
    "En conclusión, ",
    "Cabe mencionar que ",
    "Sin más preámbulos, ",
]


def clean_for_tts(text: str) -> str:
    """Elimina anotaciones, normaliza espacios y quita muletillas LLM."""
    out = text
    out = _BRACKET_ANNOTATION.sub("", out)
    out = _PARENTHETICAL_REF.sub("", out)
    for filler in _PROHIBITED_LLM_FILLERS:
        out = out.replace(filler, "")
    out = _MULTIPLE_SPACES.sub(" ", out)
    return out.strip()


def _settings_for_format(content_format: str) -> VoiceSettings:
    if content_format == "shorts":
        return DYNAMIC_SHORTS_SETTINGS
    return AUTHORITY_NARRATION_SETTINGS


def build_plan(report: ScriptReport) -> AudioPlan:
    """Genera un AudioPlan a partir de un ScriptReport validado."""
    draft = report.draft
    settings = _settings_for_format(_infer_format_from(draft.target_duration_min))
    preset = recommend_for_niche(draft.niche, _infer_format_from(draft.target_duration_min))

    blocks: list[NarrationBlock] = []

    # Hook
    hook_text = clean_for_tts(draft.hook.text)
    blocks.append(
        NarrationBlock(
            block_id=1,
            role=BlockRole.hook,
            heading="Hook",
            text=hook_text,
            target_duration_sec=draft.hook.duration_sec,
            word_count=len(hook_text.split()),
            character_count=len(hook_text),
            suggested_settings=settings,
        )
    )

    # Secciones
    for i, sec in enumerate(draft.sections, start=2):
        sec_text = clean_for_tts(sec.content)
        blocks.append(
            NarrationBlock(
                block_id=i,
                role=BlockRole.section,
                heading=f"Sección {i - 1}: {sec.heading}",
                text=sec_text,
                target_duration_sec=sec.duration_sec,
                word_count=len(sec_text.split()),
                character_count=len(sec_text),
                suggested_settings=settings,
            )
        )

    # CTA
    cta_text = clean_for_tts(draft.cta)
    blocks.append(
        NarrationBlock(
            block_id=len(blocks) + 1,
            role=BlockRole.cta,
            heading="CTA",
            text=cta_text,
            target_duration_sec=max(20, len(cta_text.split()) * 60 // 150),
            word_count=len(cta_text.split()),
            character_count=len(cta_text),
            suggested_settings=settings,
        )
    )

    return AudioPlan(
        voice_preset_key=preset.id_key,
        blocks=blocks,
    )


def build_report(report: ScriptReport, *, script_ref: str) -> AudioReport:
    plan = build_plan(report)
    fits = plan.total_chars <= 10_000
    notes = ""
    if not fits:
        notes = (
            f"El plan supera los 10.000 caracteres del tier Free de ElevenLabs "
            f"({plan.total_chars} chars). Opciones: 1) sintetizar por partes en "
            f"varios meses del Free, 2) subir a plan Starter ($5) que da 30.000 chars."
        )
    return AudioReport(
        script_ref=script_ref,
        script_title=report.draft.title,
        plan=plan,
        eleven_free_tier_fits=fits,
        notes=notes,
    )


def _infer_format_from(duration_min: int) -> str:
    if duration_min <= 1:
        return "shorts"
    if duration_min >= 60:
        return "masterclass"
    return "long_form"
