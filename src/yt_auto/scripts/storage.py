"""Persistencia de guiones en JSON + Markdown.

Trabajo diario: `output/scripts/`. Hitos archivables: `docs/scripts-archive/`.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from yt_auto.config import ROOT_DIR
from yt_auto.scripts.models import ScriptReport

OUTPUT_DIR = ROOT_DIR / "output" / "scripts"
ARCHIVE_DIR = ROOT_DIR / "docs" / "scripts-archive"


def _slug(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:70] or "script"


def _base_name(report: ScriptReport) -> str:
    ts = report.generated_at.strftime("%Y-%m-%d_%H%M")
    return f"{ts}_{_slug(report.draft.title)}"


def save_report(report: ScriptReport, *, archive: bool = False) -> tuple[Path, Path]:
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


def load_report(path: Path) -> ScriptReport:
    data = json.loads(Path(path).read_text("utf-8"))
    return ScriptReport.model_validate(data)


def ingest_response(raw: str, *, mode: str = "interactive") -> ScriptReport:
    text = raw.strip()
    fence = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    data = json.loads(text)
    data.setdefault("mode", mode)
    return ScriptReport.model_validate(data)


def render_markdown(report: ScriptReport) -> str:
    d = report.draft
    h = d.humanization
    lines: list[str] = []

    lines.append(f"# {d.title}")
    lines.append("")
    lines.append(f"_Estilo: {d.title_style.value}_")
    lines.append("")
    if d.title_alternatives:
        lines.append("**Alternativas de título**:")
        for t in d.title_alternatives:
            lines.append(f"- {t}")
        lines.append("")

    lines.append("## Ficha de producción")
    lines.append("")
    lines.append(f"- **Nicho**: {d.niche}")
    lines.append(f"- **Mercado**: {d.target_market} ({d.target_language})")
    lines.append(f"- **Duración objetivo**: {d.target_duration_min} min")
    lines.append(f"- **Word count**: {d.word_count}")
    lines.append(f"- **Duración real estimada**: {d.total_duration_sec}s")
    lines.append(f"- **Retención 30s estimada**: {d.estimated_retention_30s:.0%}")
    lines.append(f"- **CTR estimado**: {d.estimated_ctr:.1%}")
    lines.append(f"- **Modelo**: `{report.model_used}` ({report.mode})")
    if report.niche_audit_ref:
        lines.append(f"- **Auditoría origen**: `{report.niche_audit_ref}`")
    lines.append("")

    lines.append("## Viewer Ideal")
    lines.append("")
    vi = d.viewer_ideal
    lines.append(f"- **{vi.nombre}** · {vi.edad} · {vi.ubicacion}")
    lines.append(f"- **Situación**: {vi.situacion}")
    lines.append(f"- **Dolor**: {vi.dolor}")
    lines.append(f"- **Deseo**: {vi.deseo}")
    if vi.objeciones:
        lines.append(f"- **Objeciones**: {'; '.join(vi.objeciones)}")
    lines.append("")

    lines.append("## Hook (primeros segundos)")
    lines.append("")
    lines.append(f"**Duración**: {d.hook.duration_sec}s · **Visual**: {d.hook.visual_cue}")
    lines.append("")
    lines.append(f"> {d.hook.text}")
    lines.append("")
    lines.append(f"- **Promesa**: {d.hook.promise}")
    lines.append(f"- **Loop abierto**: {d.hook.open_loop}")
    lines.append("")

    lines.append("## Cuerpo del guion")
    lines.append("")
    for i, sec in enumerate(d.sections, 1):
        lines.append(f"### {i}. {sec.heading} ({sec.duration_sec}s)")
        lines.append("")
        if sec.loop_close:
            lines.append(f"_Cierra loop_: {sec.loop_close}")
        if sec.loop_open:
            lines.append(f"_Abre loop_: {sec.loop_open}")
        if sec.pattern_interrupt:
            lines.append(f"_Pattern interrupt_: {sec.pattern_interrupt}")
        if sec.sources:
            lines.append(f"_Fuentes_: {'; '.join(sec.sources)}")
        lines.append("")
        lines.append(sec.content)
        lines.append("")

    lines.append("## CTA")
    lines.append("")
    lines.append(d.cta)
    lines.append("")

    lines.append("## Auditoría anti-AI-Slop")
    lines.append("")
    veredict = "APROBADO" if h.pasa else "REQUIERE EDICIÓN HUMANA"
    lines.append(f"**Veredicto**: `{veredict}`")
    lines.append("")
    lines.append(f"- Pilar localización: {'✓' if h.pilar_localizacion else '✗'}")
    lines.append(f"- Pilar autoridad: {'✓' if h.pilar_autoridad else '✗'}")
    lines.append(f"- Pilar refinamiento: {'✓' if h.pilar_refinamiento else '✗'}")
    lines.append(f"- Paradoja emocional: {'✓' if h.paradoja_emocional else '✗'}")
    lines.append(f"- Pattern interrupts: {h.pattern_interrupts_count} (mínimo 2)")
    lines.append(f"- Fuentes citadas: {h.sources_count} (mínimo 2)")
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
