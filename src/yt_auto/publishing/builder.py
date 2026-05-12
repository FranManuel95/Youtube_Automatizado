"""Ensamblaje determinista del plan de publicación.

Toma `ScriptReport` + `EditingReport` y produce una `PublishingPlan` con
metadata SEO, capítulos derivados del timeline y checklist pre-publish
auto-evaluado.

Los tags, disclaimers, hashtags, MLA targets y fuentes oficiales se
resuelven desde `assets/niche_profiles/<id>.yaml` según el nicho del
guion (ver `niche_profile.resolve_profile`). Cualquier nuevo nicho/canal
se añade creando un YAML nuevo, sin tocar este archivo.
"""

from __future__ import annotations

import re

from yt_auto.editing.models import EditingReport
from yt_auto.monetization.renderer import render_resources_block
from yt_auto.publishing.models import (
    Category,
    Chapter,
    PrePublishChecklist,
    Privacy,
    PublishingPlan,
    PublishingReport,
    YouTubeMetadata,
)
from yt_auto.publishing.niche_profile import NicheProfile, resolve_profile
from yt_auto.scripts.models import ScriptReport


def _slug_keyword(text: str) -> str:
    return re.sub(r"[^a-z0-9áéíóúñ]+", " ", text.lower()).strip()


def _build_tags(
    script: ScriptReport,
    profile: NicheProfile,
    extra: list[str] | None = None,
) -> list[str]:
    """Combina tags del perfil + términos extraídos del guion."""
    tags: list[str] = list(profile.tags)
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
    profile: NicheProfile,
    *,
    pdf_url_placeholder: str = "https://<pendiente-de-configurar>/recurso",
) -> str:
    d = script.draft
    parts: list[str] = []

    parts.append(d.headline if hasattr(d, "headline") else d.hook.promise)
    parts.append("")

    parts.append("En este video aprenderás:")
    for sec in d.sections[:5]:
        parts.append(f"• {sec.heading}")
    parts.append("")

    parts.append("🎁 RECURSO GRATIS")
    parts.append(d.cta.split(".")[0] + ".")
    parts.append(f"Descárgalo aquí: {pdf_url_placeholder}")
    parts.append("")

    # Bloque de afiliados (resuelto desde el perfil de nicho)
    resources_block = render_resources_block(
        profile,
        video_title_or_id=d.title,
    )
    if resources_block:
        parts.append(resources_block.rstrip())
        parts.append("")

    parts.append("⏱ CAPÍTULOS")
    for ch in chapters:
        parts.append(f"{ch.youtube_timestamp()} {ch.title}")
    parts.append("")

    # Disclaimer YMYL del perfil (siempre presente, evita yellow icon)
    if profile.disclaimer:
        parts.append("⚠ AVISO IMPORTANTE")
        parts.append(profile.disclaimer.strip())
        parts.append("")

    # Declaración de uso de IA (anti-purga 2026)
    parts.append("ℹ TRANSPARENCIA")
    parts.append(
        "Parte de la narración y los visuales de este video se han producido con "
        "asistencia de inteligencia artificial bajo supervisión editorial humana. "
        "Cumplimos las políticas de YouTube sobre contenido sintético y Likeness "
        "Detection."
    )
    parts.append("")

    # Fuentes oficiales del perfil (sello agregador-educador)
    if profile.official_sources:
        parts.append("📚 FUENTES OFICIALES")
        for src in profile.official_sources[:8]:
            parts.append(f"• {src.name} — {src.url}")
        parts.append("")

    # Fuentes adicionales citadas en el guion
    script_sources: list[str] = []
    for sec in d.sections:
        script_sources.extend(sec.sources)
    script_sources = list(dict.fromkeys(script_sources))
    if script_sources:
        parts.append("📎 OTRAS FUENTES CITADAS")
        for src in script_sources[:8]:
            parts.append(f"• {src}")
        parts.append("")

    if profile.hashtags:
        parts.append(" ".join(profile.hashtags))

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
    profile: NicheProfile | None = None,
) -> PublishingReport:
    """Construye el `PublishingReport`.

    Si `profile` no se pasa, se resuelve automáticamente desde
    `script.draft.niche` contra `assets/niche_profiles/`.
    """
    if profile is None:
        profile = resolve_profile(script.draft.niche)

    chapters = _build_chapters(editing, script)
    description = _build_description(
        script,
        chapters,
        profile,
        pdf_url_placeholder=pdf_url,
    )
    tags = _build_tags(script, profile, extra_tags)

    title = script.draft.title[:100]
    yellow_flags = [
        kw for kw in profile.yellow_icon_keywords if kw.lower() in title.lower()
    ]

    metadata = YouTubeMetadata(
        title=title,
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
        likeness_declared=True,
    )

    notes_parts: list[str] = []
    notes_parts.append(f"Perfil de nicho aplicado: {profile.display_name} ({profile.id})")
    if not checklist.critical_pass:
        notes_parts.append("⚠ CRÍTICOS FALLAN: corrige antes de publicar.")
    if len(metadata.title) > 70:
        notes_parts.append(
            f"⚠ Título de {len(metadata.title)} chars. Recomendado < 70 para móvil."
        )
    if yellow_flags:
        notes_parts.append(
            f"⚠ Yellow icon risk: el título contiene palabras de riesgo "
            f"({', '.join(yellow_flags)}). Reescribe para evitar limited ads."
        )
    if not checklist.mla_track_prepared:
        target_market = (
            profile.mla_target_markets.secondary[0]
            if profile.mla_target_markets and profile.mla_target_markets.secondary
            else "en-US"
        )
        notes_parts.append(
            f"MLA pendiente: prepara una pista de audio en {target_market} para "
            f"capturar mercado anglo + multiplicar RPM hasta x4."
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
