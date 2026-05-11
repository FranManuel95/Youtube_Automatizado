"""Persistencia de planes visuales."""

from __future__ import annotations

import json
import re
from pathlib import Path

from yt_auto.config import ROOT_DIR
from yt_auto.visuals.models import VisualReport

OUTPUT_DIR = ROOT_DIR / "output" / "visuals"
ARCHIVE_DIR = ROOT_DIR / "docs" / "visuals-archive"


def _slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:70] or "visuals"


def _base_name(report: VisualReport) -> str:
    ts = report.generated_at.strftime("%Y-%m-%d_%H%M")
    return f"{ts}_{_slug(report.script_title)}"


def save_report(report: VisualReport, *, archive: bool = False) -> tuple[Path, Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    base = _base_name(report)
    json_path = OUTPUT_DIR / f"{base}.json"
    md_path = OUTPUT_DIR / f"{base}.md"
    prompts_dir = OUTPUT_DIR / base / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)

    json_path.write_text(
        report.model_dump_json(indent=2, exclude_none=False),
        encoding="utf-8",
    )
    md_path.write_text(render_markdown(report), encoding="utf-8")

    # Exportar cada prompt JSON como archivo independiente para arrastrar a
    # Nano Banana / Seedance directamente.
    for view, prompt in report.character.views.items():
        view_key = view.value if hasattr(view, "value") else str(view)
        (prompts_dir / f"character_{view_key}.json").write_text(
            json.dumps(prompt, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    for shot in report.shots:
        (prompts_dir / f"shot_{shot.shot_id:02d}_nanobanana.json").write_text(
            json.dumps(shot.nano_banana_prompt_json, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        (prompts_dir / f"shot_{shot.shot_id:02d}_seedance.json").write_text(
            json.dumps(shot.seedance_prompt_json, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    (prompts_dir / "thumbnail_nanobanana.json").write_text(
        json.dumps(report.thumbnail.nano_banana_prompt_json, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    if archive:
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        (ARCHIVE_DIR / json_path.name).write_text(json_path.read_text("utf-8"), "utf-8")
        (ARCHIVE_DIR / md_path.name).write_text(md_path.read_text("utf-8"), "utf-8")

    return json_path, md_path, prompts_dir


def load_report(path: Path) -> VisualReport:
    data = json.loads(Path(path).read_text("utf-8"))
    return VisualReport.model_validate(data)


def ingest_response(raw: str, *, mode: str = "interactive") -> VisualReport:
    text = raw.strip()
    fence = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    data = json.loads(text)
    data.setdefault("mode", mode)
    return VisualReport.model_validate(data)


def render_markdown(report: VisualReport) -> str:
    lines: list[str] = []
    c = report.character

    lines.append(f"# Plan visual · {report.script_title}")
    lines.append("")
    lines.append(f"- **Guion origen**: `{report.script_ref}`")
    lines.append(f"- **Shots**: {len(report.shots)}")
    lines.append(f"- **Duración total clips**: {report.total_clip_duration_sec}s")
    lines.append(f"- **Pattern interrupts**: {report.pattern_interrupt_count}")
    lines.append(f"- **Modelo**: `{report.model_used}` ({report.mode})")
    lines.append("")

    lines.append("## Cómo usar este plan")
    lines.append("")
    lines.append(
        "1. **Reference Sheet del personaje**: ve a Nano Banana, pega los prompts JSON de "
        "`prompts/character_*.json` uno por vista. Guarda las 4 imágenes en "
        "`assets/characters/<personaje>/`."
    )
    lines.append(
        "2. **Shots**: por cada shot N, pega `prompts/shot_NN_nanobanana.json` en Nano Banana "
        "para obtener el frame base. Luego carga ese frame en Seedance 2.0 con "
        "`prompts/shot_NN_seedance.json` para animarlo (15s máx)."
    )
    lines.append(
        "3. **Multi-reference en Seedance**: además del frame, sube la Reference Sheet del "
        "personaje y la imagen del outfit. Eso asegura consistencia entre clips."
    )
    lines.append(
        "4. **Miniatura**: pega `prompts/thumbnail_nanobanana.json` en Nano Banana. Exporta a "
        "4K (3840x2160). El texto NO se genera con IA, se añade en CapCut/Filmora."
    )
    lines.append(
        "5. **Auditoría**: antes de pasar a edición, ejecuta la skill `/thumbnail-checklist` "
        "y `/anti-ai-slop` sobre los assets generados."
    )
    lines.append("")

    lines.append("## Personaje")
    lines.append("")
    lines.append(f"**{c.name}** · {c.role} · {c.age}")
    lines.append("")
    lines.append(f"- **Outfit base**: {c.outfit_base}")
    if c.accent_notes:
        lines.append(f"- **Notas de acento/etnia**: {c.accent_notes}")
    lines.append("- **Rasgos físicos**:")
    for k, v in c.physical_features.items():
        lines.append(f"  - {k}: {v}")
    lines.append(f"- **Vistas disponibles**: {', '.join(v.value for v in c.views.keys())}")
    if not c.has_mandatory_views():
        lines.append(
            "  > ⚠ Faltan vistas obligatorias. Mínimo: frontal, profile_left, three_quarter."
        )
    lines.append("")

    lines.append("## Shot list")
    lines.append("")
    lines.append("| # | Bloque | TC inicio | Dur | Plano | Pattern Int. | Descripción |")
    lines.append("|---|--------|-----------|-----|-------|--------------|-------------|")
    for s in report.shots:
        pi = "✓" if s.pattern_interrupt else ""
        desc = s.description if len(s.description) <= 60 else s.description[:57] + "..."
        lines.append(
            f"| {s.shot_id:02d} | {s.related_block} | {s.timecode_start_sec}s | "
            f"{s.duration_sec}s | {s.shot_type.value} | {pi} | {desc} |"
        )
    lines.append("")

    lines.append("## Detalles de shots")
    lines.append("")
    for s in report.shots:
        lines.append(
            f"### Shot {s.shot_id:02d} · {s.shot_type.value} · {s.duration_sec}s · "
            f"@{s.timecode_start_sec}s ({s.related_block})"
        )
        lines.append("")
        if s.pattern_interrupt:
            lines.append("_⚡ Pattern interrupt declarado_")
            lines.append("")
        lines.append(f"**Descripción**: {s.description}")
        lines.append("")
        lines.append(f"- **Motion**: {s.motion}")
        lines.append(f"- **Lighting**: {s.lighting}")
        lines.append(f"- **Ambient**: {s.ambient}")
        lines.append(f"- **Personaje en escena**: {'sí' if s.requires_character else 'no'}")
        lines.append("")

    lines.append("## Miniatura (4K)")
    lines.append("")
    t = report.thumbnail
    lines.append(f"- **Texto en pantalla**: \"{t.title_overlay}\" (max 3 palabras)")
    lines.append(f"- **Cara**: {t.face_element}")
    lines.append(f"- **Objeto**: {t.object_element}")
    lines.append(f"- **Pattern interrupt**: {t.pattern_interrupt_strategy}")
    lines.append(f"- **Color**: {t.color_strategy}")
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
