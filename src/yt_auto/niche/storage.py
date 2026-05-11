"""Persistencia de auditorías de nicho en JSON + Markdown.

Las auditorías se guardan por defecto en `output/niche/` (no commiteable).
Si una auditoría es un hito que merece quedar en el repo, se archiva en
`docs/niche-audits/` con `archive_report`.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from yt_auto.config import ROOT_DIR
from yt_auto.niche.models import NicheAuditReport

OUTPUT_DIR = ROOT_DIR / "output" / "niche"
ARCHIVE_DIR = ROOT_DIR / "docs" / "niche-audits"


def _slug(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:60] or "report"


def _base_name(report: NicheAuditReport) -> str:
    ts = report.generated_at.strftime("%Y-%m-%d_%H%M")
    market = _slug(report.market_focus)
    vertical = _slug(report.vertical_filter) if report.vertical_filter else "open"
    return f"{ts}_{market}_{vertical}"


def save_report(report: NicheAuditReport, *, archive: bool = False) -> tuple[Path, Path]:
    """Guarda el reporte en JSON + Markdown. Devuelve (json_path, md_path).

    Si `archive=True`, también copia ambos a `docs/niche-audits/` para que
    queden bajo control de versiones.
    """
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


def load_report(path: Path) -> NicheAuditReport:
    data = json.loads(Path(path).read_text("utf-8"))
    return NicheAuditReport.model_validate(data)


def render_markdown(report: NicheAuditReport) -> str:
    lines: list[str] = []
    lines.append(f"# Auditoría de nichos · {report.market_focus}")
    lines.append("")
    lines.append(f"- **Fecha**: {report.generated_at.strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"- **Formato**: `{report.content_format}`")
    lines.append(f"- **Vertical**: {report.vertical_filter or 'exploración abierta'}")
    lines.append(f"- **Modelo**: `{report.model_used}` ({report.mode})")
    lines.append(f"- **Candidatos**: {len(report.candidates)}")
    lines.append("")

    if report.methodology_notes:
        lines.append("## Notas de metodología")
        lines.append("")
        lines.append(report.methodology_notes)
        lines.append("")

    top = report.top(3)
    if top:
        lines.append("## Top 3 (por score)")
        lines.append("")
        lines.append("| # | Nicho | Score | RPM | Competencia |")
        lines.append("|---|-------|-------|-----|--------------|")
        for i, c in enumerate(top, 1):
            rpm = f"${c.rpm.rpm_min_usd:.1f}-{c.rpm.rpm_max_usd:.1f}"
            lines.append(f"| {i} | **{c.name}** | {c.score}/10 | {rpm} | {c.competition_level} |")
        lines.append("")

    lines.append("## Todos los candidatos")
    lines.append("")
    for c in sorted(report.candidates, key=lambda x: x.score, reverse=True):
        lines.append(f"### {c.name} · score {c.score}/10")
        lines.append("")
        lines.append(f"_{c.headline}_")
        lines.append("")
        lines.append(c.description)
        lines.append("")
        lines.append(f"- **Mercado**: {c.target_market} ({c.target_language})")
        lines.append(
            f"- **4S**: {', '.join(s.value for s in c.four_s) if c.four_s else '—'}"
        )
        lines.append(
            f"- **RPM estimado**: ${c.rpm.rpm_min_usd:.1f}-{c.rpm.rpm_max_usd:.1f} "
            f"({c.rpm.tier.value})"
        )
        lines.append(f"- **Competencia**: {c.competition_level}")
        if c.niche_bending_angle:
            lines.append(f"- **Niche bending**: {c.niche_bending_angle}")
        lines.append(f"- **Gap**: {c.gap_hypothesis}")
        if c.demand_evidence:
            lines.append("- **Evidencias de demanda**:")
            for e in c.demand_evidence:
                lines.append(f"  - {e}")
        if c.sample_titles:
            lines.append("- **Títulos de prueba**:")
            for t in c.sample_titles:
                lines.append(f"  - {t}")
        if c.risks:
            lines.append("- **Riesgos**:")
            for r in c.risks:
                lines.append(f"  - {r}")
        lines.append(f"- **Razonamiento**: {c.rationale}")
        lines.append("")

    return "\n".join(lines) + "\n"


def latest_report_path() -> Path | None:
    if not OUTPUT_DIR.exists():
        return None
    jsons = sorted(OUTPUT_DIR.glob("*.json"))
    return jsons[-1] if jsons else None
