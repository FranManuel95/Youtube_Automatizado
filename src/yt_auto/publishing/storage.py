"""Persistencia y render de planes de publicación."""

from __future__ import annotations

import json
import re
from pathlib import Path

from yt_auto.config import ROOT_DIR
from yt_auto.publishing.models import PublishingReport

OUTPUT_DIR = ROOT_DIR / "output" / "publishing"
ARCHIVE_DIR = ROOT_DIR / "docs" / "publishing-archive"


def _slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:70] or "publish"


def _base_name(report: PublishingReport) -> str:
    ts = report.generated_at.strftime("%Y-%m-%d_%H%M")
    return f"{ts}_{_slug(report.script_title)}"


def save_report(report: PublishingReport, *, archive: bool = False) -> tuple[Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    base = _base_name(report)
    json_path = OUTPUT_DIR / f"{base}.json"
    md_path = OUTPUT_DIR / f"{base}.md"

    json_path.write_text(
        report.model_dump_json(indent=2, exclude_none=False),
        encoding="utf-8",
    )
    md_path.write_text(render_markdown(report), encoding="utf-8")

    if archive:
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        (ARCHIVE_DIR / json_path.name).write_text(json_path.read_text("utf-8"), "utf-8")
        (ARCHIVE_DIR / md_path.name).write_text(md_path.read_text("utf-8"), "utf-8")

    return json_path, md_path


def load_report(path: Path) -> PublishingReport:
    return PublishingReport.model_validate(json.loads(Path(path).read_text("utf-8")))


def render_markdown(report: PublishingReport) -> str:
    p = report.plan
    m = p.metadata
    c = p.checklist
    lines: list[str] = []

    lines.append(f"# Publicación · {report.script_title}")
    lines.append("")
    veredict = "✅ LISTO PARA PUBLICAR" if c.critical_pass else "❌ NO PUBLICAR - corrige críticos"
    lines.append(f"## {veredict}")
    lines.append("")

    lines.append("### Críticos (bloqueantes)")
    lines.append("")
    lines.append(f"- Anti-AI-Slop pasado: {'✓' if c.anti_ai_slop_passed else '✗'}")
    lines.append(f"- Miniatura 4K lista: {'✓' if c.thumbnail_4k_ready else '✗'}")
    lines.append(f"- Título <70 chars: {'✓' if c.title_under_70_chars else '✗'}")
    lines.append(f"- Descripción con disclaimer: {'✓' if c.description_has_disclaimer else '✗'}")
    lines.append(f"- Declaración Likeness/IA: {'✓' if c.likeness_declaration else '✗'}")
    lines.append("")

    lines.append("### Recomendados")
    lines.append("")
    lines.append(f"- Capítulos definidos: {'✓' if c.chapters_defined else '✗'}")
    lines.append(f"- Tags en rango 5-15: {'✓' if c.tags_count_ok else '✗'}")
    lines.append(f"- DAI anchors marcados: {'✓' if c.dai_anchors_marked else '✗'}")
    lines.append(f"- MLA preparado: {'✓' if c.mla_track_prepared else '✗'}")
    lines.append(f"- End screen planificada: {'✓' if c.end_screen_planned else '✗'}")
    lines.append("")

    lines.append("## Metadata YouTube (copiar/pegar en YouTube Studio)")
    lines.append("")
    lines.append(f"**Título** ({len(m.title)}/100 chars)")
    lines.append("")
    lines.append(f"```\n{m.title}\n```")
    lines.append("")
    lines.append(f"**Descripción** ({len(m.description)}/5000 chars)")
    lines.append("")
    lines.append(f"```\n{m.description}\n```")
    lines.append("")
    lines.append(f"**Tags** ({len(m.tags)})")
    lines.append("")
    lines.append(f"`{', '.join(m.tags)}`")
    lines.append("")
    lines.append(f"**Categoría**: {m.category.value}")
    lines.append(f"**Privacidad inicial**: {m.privacy.value} (cambiar a public al publicar)")
    lines.append(f"**Idioma**: {m.language}")
    lines.append(f"**Made for kids**: {'sí' if m.made_for_kids else 'no'}")
    lines.append(f"**Monetización**: {'on' if m.monetization_enabled else 'off'}")
    lines.append("")

    lines.append("## Capítulos")
    lines.append("")
    for ch in p.chapters:
        lines.append(f"- `{ch.youtube_timestamp()}` {ch.title}")
    lines.append("")

    if p.mla_tracks:
        lines.append("## Pistas Multi-Language Audio (MLA)")
        lines.append("")
        for t in p.mla_tracks:
            mark = " *(default)*" if t.is_default else ""
            lines.append(f"- `{t.language_code}` → `{t.audio_file_ref}`{mark}")
        lines.append("")

    if report.notes:
        lines.append("## Notas")
        lines.append("")
        lines.append(report.notes)
        lines.append("")

    return "\n".join(lines) + "\n"


def latest_report_path() -> Path | None:
    if not OUTPUT_DIR.exists():
        return None
    jsons = sorted(OUTPUT_DIR.glob("*.json"))
    return jsons[-1] if jsons else None
