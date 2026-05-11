"""Persistencia y render de planes de edición."""

from __future__ import annotations

import csv
import json
import re
from io import StringIO
from pathlib import Path

from yt_auto.config import ROOT_DIR
from yt_auto.editing.models import EditingReport

OUTPUT_DIR = ROOT_DIR / "output" / "editing"
ARCHIVE_DIR = ROOT_DIR / "docs" / "editing-archive"


def _slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:70] or "editing"


def _base_name(report: EditingReport) -> str:
    ts = report.generated_at.strftime("%Y-%m-%d_%H%M")
    return f"{ts}_{_slug(report.script_title)}"


def save_report(report: EditingReport, *, archive: bool = False) -> tuple[Path, Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    base = _base_name(report)
    json_path = OUTPUT_DIR / f"{base}.json"
    md_path = OUTPUT_DIR / f"{base}.md"
    csv_path = OUTPUT_DIR / f"{base}_subtitles.csv"

    json_path.write_text(
        report.model_dump_json(indent=2, exclude_none=False),
        encoding="utf-8",
    )
    md_path.write_text(render_markdown(report), encoding="utf-8")
    csv_path.write_text(render_subtitles_csv(report), encoding="utf-8")

    if archive:
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        (ARCHIVE_DIR / json_path.name).write_text(json_path.read_text("utf-8"), "utf-8")
        (ARCHIVE_DIR / md_path.name).write_text(md_path.read_text("utf-8"), "utf-8")
        (ARCHIVE_DIR / csv_path.name).write_text(csv_path.read_text("utf-8"), "utf-8")

    return json_path, md_path, csv_path


def load_report(path: Path) -> EditingReport:
    return EditingReport.model_validate(json.loads(Path(path).read_text("utf-8")))


def render_subtitles_csv(report: EditingReport) -> str:
    """CSV importable directamente en CapCut o Premiere (start/end/text)."""
    buf = StringIO()
    w = csv.writer(buf)
    w.writerow(["start_sec", "end_sec", "text", "highlight_keywords", "motion_style"])
    for seg in report.plan.subtitles:
        w.writerow(
            [
                f"{seg.timecode_start_sec:.2f}",
                f"{seg.timecode_start_sec + seg.duration_sec:.2f}",
                seg.text,
                "|".join(seg.highlight_keywords),
                seg.motion_style,
            ]
        )
    return buf.getvalue()


def render_markdown(report: EditingReport) -> str:
    p = report.plan
    lines: list[str] = []

    lines.append(f"# Plan de edición · {report.script_title}")
    lines.append("")
    lines.append(f"- **Guion**: `{report.script_ref}`")
    if report.audio_ref:
        lines.append(f"- **Audio**: `{report.audio_ref}`")
    if report.visuals_ref:
        lines.append(f"- **Visuales**: `{report.visuals_ref}`")
    lines.append("")
    lines.append(f"- **Resolución**: {p.target_resolution} · **Aspect**: {p.aspect_ratio} · **FPS**: {p.target_fps}")
    lines.append(f"- **Eventos timeline**: {len(p.timeline)}")
    lines.append(f"- **Subtítulos**: {len(p.subtitles)} segmentos")
    lines.append(f"- **Transiciones**: {len(p.transitions)}")
    lines.append(f"- **DAI anchors**: {len(p.dai_anchors)}")
    rule_label = "✓ pasa" if p.three_second_rule_pass else f"✗ falla (gap {p.longest_static_gap_sec}s)"
    lines.append(f"- **Regla de 3s**: {rule_label}")
    lines.append("")

    lines.append("## Cómo usar este plan en CapCut/Filmora")
    lines.append("")
    lines.append("1. Importa los 8 archivos de audio (.mp3) generados en la etapa 3.")
    lines.append("2. Importa las imágenes/clips generados con Nano Banana y Seedance.")
    lines.append("3. Ordena la pista de video según la tabla **Timeline (video clips)** de abajo.")
    lines.append("4. Importa los subtítulos desde `<base>_subtitles.csv` (CapCut: Subtitles -> Import).")
    lines.append("5. Aplica el color de destacado a las **keywords** (rojo o amarillo según paleta del canal).")
    lines.append("6. Inserta marcadores de DAI en los puntos indicados (YouTube Studio los recogerá automáticamente al subir).")
    lines.append("7. Aplica las transiciones recomendadas entre shots.")
    lines.append("8. Exporta en 4K, 24fps, MP4 H.264 (o el preset 'YouTube 4K' de CapCut).")
    lines.append("")

    if p.three_second_violations:
        lines.append("## ⚠ Violaciones de la regla de 3 segundos")
        lines.append("")
        for v in p.three_second_violations:
            lines.append(f"- **{v.start_sec}-{v.end_sec}s** ({v.duration_sec}s): {v.suggested_fix}")
        lines.append("")

    # Timeline de video
    video_events = [e for e in p.timeline if e.event_type.value == "video_clip"]
    if video_events:
        lines.append("## Timeline (video clips)")
        lines.append("")
        lines.append("| TC inicio | Dur | Importancia | Origen | Descripción |")
        lines.append("|-----------|-----|-------------|--------|-------------|")
        for e in video_events:
            desc = e.description if len(e.description) <= 60 else e.description[:57] + "..."
            lines.append(
                f"| {e.timecode_sec}s | {e.duration_sec}s | "
                f"{e.importance.value} | `{e.source_ref}` | {desc} |"
            )
        lines.append("")

    # DAI anchors
    if p.dai_anchors:
        lines.append("## DAI Anchors (Dynamic Ad Insertion)")
        lines.append("")
        for a in p.dai_anchors:
            lines.append(f"- **{a.timecode_sec}s** (pausa mín. {a.minimum_break_sec}s): {a.rationale}")
        lines.append("")

    # Sample de subtítulos
    if p.subtitles:
        lines.append("## Subtítulos (primeros 15 segmentos · CSV completo aparte)")
        lines.append("")
        lines.append("| # | TC | Dur | Texto | Keywords | Motion |")
        lines.append("|---|----|----|-------|----------|--------|")
        for s in p.subtitles[:15]:
            kws = ", ".join(s.highlight_keywords) if s.highlight_keywords else "—"
            txt = s.text if len(s.text) <= 50 else s.text[:47] + "..."
            lines.append(
                f"| {s.seg_id} | {s.timecode_start_sec:.1f}s | "
                f"{s.duration_sec:.1f}s | {txt} | {kws} | {s.motion_style} |"
            )
        if len(p.subtitles) > 15:
            lines.append(f"\n_… {len(p.subtitles) - 15} segmentos más en el CSV_")
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
