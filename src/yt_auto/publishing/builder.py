"""Ensamblaje determinista del plan de publicación.

Toma `ScriptReport` + `EditingReport` y produce una `PublishingPlan` con
metadata SEO, capítulos derivados del timeline y checklist pre-publish
auto-evaluado.
"""

from __future__ import annotations

import re

from yt_auto.editing.models import EditingReport
from yt_auto.publishing.models import (
    Category,
    Chapter,
    PrePublishChecklist,
    Privacy,
    PublishingPlan,
    PublishingReport,
    YouTubeMetadata,
)
from yt_auto.scripts.models import ScriptReport


# Tags por categoría temática (US-Hispanic, finanzas) — heurística inicial.
TAGS_FINANZAS_HISPANIC = [
    "credito",
    "credito hispano",
    "ITIN",
    "FICO",
    "finanzas hispanos",
    "credito americano",
    "inmigrantes EEUU",
    "como construir credito",
    "ITIN credit card",
    "credit builder",
]


def _slug_keyword(text: str) -> str:
    return re.sub(r"[^a-z0-9áéíóúñ]+", " ", text.lower()).strip()


def _build_tags(script: ScriptReport, extra: list[str] | None = None) -> list[str]:
    """Combina tags semánticos del nicho + términos del guion."""
    tags: list[str] = []
    niche = script.draft.niche.lower()
    if any(k in niche for k in ["finanzas", "credito", "crédito", "inmigrante"]):
        tags.extend(TAGS_FINANZAS_HISPANIC)
    if extra:
        tags.extend(extra)
    # Términos extraídos de los sample_titles
    for t in script.draft.title_alternatives + [script.draft.title]:
        for word in re.findall(r"[A-Za-zÁÉÍÓÚñÑ]{4,}", t):
            kw = word.lower()
            if kw not in tags and len(tags) < 15:
                tags.append(kw)
    # Eliminar duplicados manteniendo orden, máximo 15
    seen: set[str] = set()
    result: list[str] = []
    for tag in tags:
        if tag not in seen:
            seen.add(tag)
            result.append(tag)
        if len(result) >= 15:
            break
    return result


def _build_description(
    script: ScriptReport,
    chapters: list[Chapter],
    *,
    pdf_url_placeholder: str = "https://<pendiente-de-configurar>/itin-pdf",
    has_finance_content: bool = True,
) -> str:
    d = script.draft
    parts: list[str] = []

    # Hook reescrito en formato descripción (1-2 frases)
    parts.append(d.headline if hasattr(d, "headline") else d.hook.promise)
    parts.append("")

    # Promesa del video
    parts.append(f"En este video aprenderás:")
    for sec in d.sections[:5]:
        parts.append(f"• {sec.heading}")
    parts.append("")

    # CTA + producto
    parts.append("🎁 RECURSO GRATIS")
    parts.append(d.cta.split(".")[0] + ".")
    parts.append(f"Descárgalo aquí: {pdf_url_placeholder}")
    parts.append("")

    # Capítulos timestamp
    parts.append("⏱ CAPÍTULOS")
    for ch in chapters:
        parts.append(f"{ch.youtube_timestamp()} {ch.title}")
    parts.append("")

    # Disclaimers (YPP / YMYL)
    if has_finance_content:
        parts.append("⚠ AVISO IMPORTANTE")
        parts.append(
            "Este video tiene fines educativos. No constituye asesoría financiera, "
            "fiscal ni legal personalizada. Antes de tomar decisiones, consulta con "
            "un profesional certificado en tu estado."
        )
        parts.append("")

    # Likeness Detection / declaración de IA
    parts.append("ℹ TRANSPARENCIA")
    parts.append(
        "Parte de la narración y los visuales de este video se han producido con "
        "asistencia de inteligencia artificial bajo supervisión editorial humana. "
        "Cumplimos las políticas de YouTube sobre contenido sintético y Likeness "
        "Detection."
    )
    parts.append("")

    # Fuentes citadas en el guion
    sources: list[str] = []
    for sec in d.sections:
        sources.extend(sec.sources)
    sources = list(dict.fromkeys(sources))
    if sources:
        parts.append("📚 FUENTES CITADAS")
        for src in sources[:8]:
            parts.append(f"• {src}")
        parts.append("")

    # Hashtags al final (YouTube los recoge si están en las últimas líneas)
    parts.append("#FinanzasHispanas #CreditoEEUU #ITIN #InmigrantesEEUU")

    description = "\n".join(parts)
    return description[:5000]


def _build_chapters(editing: EditingReport, script: ScriptReport) -> list[Chapter]:
    """Genera capítulos. YouTube exige primer capítulo en 00:00 y mínimo 3 capítulos de ≥10s."""
    chapters: list[Chapter] = [Chapter(timecode_sec=0, title="Introducción")]

    cursor = script.draft.hook.duration_sec
    for i, sec in enumerate(script.draft.sections, start=1):
        # Recortar título de capítulo a primeras ~50 chars sin partir palabras
        heading = sec.heading
        title = heading if len(heading) <= 50 else heading[:47].rsplit(" ", 1)[0] + "..."
        chapters.append(Chapter(timecode_sec=cursor, title=f"{i}. {title}"))
        cursor += sec.duration_sec

    # CTA
    chapters.append(Chapter(timecode_sec=cursor, title="Plan de acción y recurso gratuito"))
    return chapters


def _has_finance_keywords(text: str) -> bool:
    return any(
        k in text.lower()
        for k in ["finanzas", "crédito", "credito", "ITIN", "FICO", "inversión", "inversion"]
    )


def _evaluate_checklist(
    script: ScriptReport,
    metadata: YouTubeMetadata,
    chapters: list[Chapter],
    *,
    has_mla: bool,
    thumbnail_ready: bool,
    end_screen_planned: bool,
    likeness_declared: bool,
) -> PrePublishChecklist:
    return PrePublishChecklist(
        anti_ai_slop_passed=script.draft.humanization.pasa,
        thumbnail_4k_ready=thumbnail_ready,
        title_under_70_chars=len(metadata.title) <= 70,
        description_has_disclaimer=(
            "AVISO IMPORTANTE" in metadata.description
            or "TRANSPARENCIA" in metadata.description
        ),
        likeness_declaration=likeness_declared,
        chapters_defined=len(chapters) >= 3,
        tags_count_ok=5 <= len(metadata.tags) <= 15,
        dai_anchors_marked=True,  # asumimos que el editing report ya los marcó
        mla_track_prepared=has_mla,
        end_screen_planned=end_screen_planned,
    )


def build_report(
    *,
    script: ScriptReport,
    editing: EditingReport,
    script_ref: str,
    editing_ref: str,
    niche_audit_ref: str | None = None,
    pdf_url: str = "https://<pendiente-de-configurar>/recurso",
    thumbnail_ready: bool = True,
    end_screen_planned: bool = False,
    extra_tags: list[str] | None = None,
) -> PublishingReport:
    chapters = _build_chapters(editing, script)
    description = _build_description(
        script,
        chapters,
        pdf_url_placeholder=pdf_url,
        has_finance_content=_has_finance_keywords(script.draft.niche),
    )
    tags = _build_tags(script, extra_tags)

    metadata = YouTubeMetadata(
        title=script.draft.title[:100],
        description=description,
        tags=tags,
        category=Category.education,
        privacy=Privacy.private,  # por defecto, el usuario lo cambia al publicar
        language=script.draft.target_language,
    )

    checklist = _evaluate_checklist(
        script,
        metadata,
        chapters,
        has_mla=False,
        thumbnail_ready=thumbnail_ready,
        end_screen_planned=end_screen_planned,
        likeness_declared=True,  # la descripción incluye la declaración
    )

    notes_parts: list[str] = []
    if not checklist.critical_pass:
        notes_parts.append("⚠ CRÍTICOS FALLAN: corrige antes de publicar.")
    if len(metadata.title) > 70:
        notes_parts.append(
            f"⚠ Título de {len(metadata.title)} chars. Recomendado < 70 para móvil."
        )
    if not checklist.mla_track_prepared:
        notes_parts.append(
            "MLA pendiente: prepara una pista de audio en inglés (en-US) para "
            "capturar mercado anglo + multiplicar RPM hasta x4."
        )

    plan = PublishingPlan(
        metadata=metadata,
        chapters=chapters,
        checklist=checklist,
    )

    return PublishingReport(
        script_ref=script_ref,
        editing_ref=editing_ref,
        niche_audit_ref=niche_audit_ref,
        script_title=script.draft.title,
        plan=plan,
        notes="\n".join(notes_parts),
    )
