"""Persistencia y exportación de planes de audio.

Genera tres tipos de salida por cada `AudioReport`:
1. `<base>.json` con el reporte completo (fuente de verdad).
2. `<base>.md` con un dashboard legible.
3. `<base>/blocks/NN_<role>.txt` para arrastrar al panel de ElevenLabs uno a uno.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from yt_auto.audio.models import AudioReport, NarrationBlock
from yt_auto.audio.voices import by_key
from yt_auto.config import ROOT_DIR

OUTPUT_DIR = ROOT_DIR / "output" / "audio"
ARCHIVE_DIR = ROOT_DIR / "docs" / "audio-archive"


def _slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:70] or "audio"


def _base_name(report: AudioReport) -> str:
    ts = report.generated_at.strftime("%Y-%m-%d_%H%M")
    return f"{ts}_{_slug(report.script_title)}"


def save_report(report: AudioReport, *, archive: bool = False) -> tuple[Path, Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    base = _base_name(report)
    json_path = OUTPUT_DIR / f"{base}.json"
    md_path = OUTPUT_DIR / f"{base}.md"
    blocks_dir = OUTPUT_DIR / base / "blocks"
    blocks_dir.mkdir(parents=True, exist_ok=True)

    json_path.write_text(
        report.model_dump_json(indent=2, exclude_none=False),
        encoding="utf-8",
    )
    md_path.write_text(render_markdown(report), encoding="utf-8")

    for block in report.plan.blocks:
        fname = f"{block.block_id:02d}_{block.role.value}.txt"
        (blocks_dir / fname).write_text(block.text, encoding="utf-8")

    if archive:
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        (ARCHIVE_DIR / json_path.name).write_text(json_path.read_text("utf-8"), "utf-8")
        (ARCHIVE_DIR / md_path.name).write_text(md_path.read_text("utf-8"), "utf-8")

    return json_path, md_path, blocks_dir


def load_report(path: Path) -> AudioReport:
    data = json.loads(Path(path).read_text("utf-8"))
    return AudioReport.model_validate(data)


def render_markdown(report: AudioReport) -> str:
    p = report.plan
    preset = by_key(p.voice_preset_key)
    lines: list[str] = []

    lines.append(f"# Plan de audio · {report.script_title}")
    lines.append("")
    lines.append(f"- **Guion origen**: `{report.script_ref}`")
    lines.append(f"- **Voz recomendada**: {preset.display_name} ({preset.accent})")
    lines.append(f"- **Modelo**: `{p.model_id}`")
    lines.append(f"- **Bloques**: {len(p.blocks)}")
    lines.append(f"- **Total palabras**: {p.total_words}")
    lines.append(f"- **Total caracteres**: {p.total_chars}")
    lines.append(f"- **Duración estimada**: {p.estimated_duration_sec}s")
    fits_label = "✓ cabe" if report.eleven_free_tier_fits else "✗ NO cabe"
    lines.append(f"- **Plan Free ElevenLabs (10.000 chars/mes)**: {fits_label}")
    lines.append("")

    lines.append("## Cómo usar este plan (modo interactivo ElevenLabs Free)")
    lines.append("")
    lines.append(
        "1. Entra a https://elevenlabs.io/app/speech-synthesis. "
        "Si no tienes voz seleccionada, busca en la VoiceLab una que coincida con: "
        f"**{preset.display_name}** · {preset.note_es or preset.accent}."
    )
    lines.append("2. Copia el `Voice ID` que veas en el panel y pégalo en `.env` "
                 f"como `{p.voice_id_env_var}=...`")
    lines.append("3. Configura los sliders en el panel a los valores **suggested_settings** "
                 "de cada bloque (stability ≈ 0.5, similarity ≈ 0.75, style ≈ 0.3).")
    lines.append("4. Por cada bloque, abre el archivo `.txt` correspondiente "
                 "en `output/audio/<base>/blocks/`, pega el contenido en el TextArea "
                 "de ElevenLabs y dale 'Generate'. Descarga el `.mp3` resultante con el "
                 "mismo nombre del bloque.")
    lines.append("5. Guarda todos los `.mp3` en `output/audio/<base>/mp3/` con el "
                 "mismo prefijo numérico para mantener orden.")
    lines.append("")

    lines.append("## Bloques de locución")
    lines.append("")
    for b in p.blocks:
        lines.append(_render_block(b))
        lines.append("")

    if report.notes:
        lines.append("## Notas")
        lines.append("")
        lines.append(report.notes)
        lines.append("")

    return "\n".join(lines) + "\n"


def _render_block(b: NarrationBlock) -> str:
    s = b.suggested_settings
    return (
        f"### Bloque {b.block_id:02d} · {b.role.value.upper()} · {b.heading}\n\n"
        f"_Duración objetivo: **{b.target_duration_sec}s** · "
        f"Palabras: {b.word_count} · Caracteres: {b.character_count}_\n\n"
        f"_Settings_: stability={s.stability:.2f}, similarity_boost={s.similarity_boost:.2f}, "
        f"style={s.style:.2f}, speaker_boost={'on' if s.use_speaker_boost else 'off'}\n\n"
        f"```\n{b.text}\n```"
    )


def latest_report_path() -> Path | None:
    if not OUTPUT_DIR.exists():
        return None
    jsons = sorted(OUTPUT_DIR.glob("*.json"))
    return jsons[-1] if jsons else None
