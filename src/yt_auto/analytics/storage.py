"""Persistencia y render de reports de analítica."""

from __future__ import annotations

import json
import re
from pathlib import Path

from yt_auto.analytics.models import AnalyticsReport
from yt_auto.config import ROOT_DIR

OUTPUT_DIR = ROOT_DIR / "output" / "analytics"
ARCHIVE_DIR = ROOT_DIR / "docs" / "analytics-archive"


def _slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:70] or "analytics"


def save_report(report: AnalyticsReport, *, label: str, archive: bool = False) -> tuple[Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = report.generated_at.strftime("%Y-%m-%d_%H%M")
    base = f"{ts}_{_slug(label)}"
    json_path = OUTPUT_DIR / f"{base}.json"
    md_path = OUTPUT_DIR / f"{base}.md"

    json_path.write_text(
        report.model_dump_json(indent=2, exclude_none=False), encoding="utf-8"
    )
    md_path.write_text(render_markdown(report), encoding="utf-8")

    if archive:
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        (ARCHIVE_DIR / json_path.name).write_text(json_path.read_text("utf-8"), "utf-8")
        (ARCHIVE_DIR / md_path.name).write_text(md_path.read_text("utf-8"), "utf-8")

    return json_path, md_path


def load_report(path: Path) -> AnalyticsReport:
    return AnalyticsReport.model_validate(json.loads(Path(path).read_text("utf-8")))


def render_markdown(report: AnalyticsReport) -> str:
    lines: list[str] = []
    lines.append("# Reporte de analítica")
    lines.append("")
    lines.append(f"- **Fecha**: {report.generated_at.strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"- **Videos analizados**: {len(report.videos)}")
    lines.append(f"- **Leaks detectados (total)**: {report.total_leaks}")
    lines.append(f"- **Prompts Ask Studio**: {len(report.ask_studio_prompts)}")
    lines.append(f"- **Portafolio incluido**: {'sí' if report.portfolio else 'no'}")
    lines.append("")

    if report.portfolio:
        p = report.portfolio
        lines.append("## Salud del portafolio")
        lines.append("")
        lines.append(f"- **Canales**: {len(p.channels)}")
        lines.append(f"- **Revenue mensual total**: ${p.total_monthly_revenue_usd:,.2f}")
        lines.append(f"- **Concentración (canal top)**: {p.top_channel_revenue_share_pct:.1f}%")
        lines.append(f"- **Riesgo de concentración**: `{p.concentration_risk}`")
        lines.append(f"- **Score de diversificación**: {p.diversification_score}/10")
        lines.append(f"- **Idiomas cubiertos**: {', '.join(p.languages_covered) or '—'}")
        lines.append(f"- **Exposición US-Hispanic**: {'✓' if p.has_us_hispanic_exposure else '✗'}")
        lines.append("")
        lines.append("### Canales")
        lines.append("")
        lines.append("| Canal | Mercado | Subs | Videos 30d | Revenue | RPM |")
        lines.append("|-------|---------|------|-----------|---------|-----|")
        for c in p.channels:
            rpm = f"${c.monthly_rpm_usd:.1f}" if c.monthly_rpm_usd else "—"
            lines.append(
                f"| {c.name} | {c.market_focus} | {c.subscriber_count:,} | "
                f"{c.videos_last_30d} | ${c.monthly_revenue_usd:,.0f} | {rpm} |"
            )
        lines.append("")
        lines.append("### Recomendaciones")
        lines.append("")
        for r in p.recommendations:
            lines.append(f"- {r}")
        lines.append("")

    if report.videos:
        lines.append("## Videos analizados")
        lines.append("")
        for v in report.videos:
            outlier = " · ⚡ OUTLIER" if v.is_outlier else ""
            lines.append(f"### {v.title}{outlier}")
            lines.append("")
            lines.append(f"- **ID**: `{v.video_id}` · **Duración**: {v.duration_sec}s")
            lines.append(f"- **Vistas**: {v.views:,}")
            if v.ctr is not None:
                lines.append(f"- **CTR**: {v.ctr:.1%}")
            if v.avg_retention_pct is not None:
                lines.append(f"- **Retención media**: {v.avg_retention_pct:.1f}%")
            if v.rpm_usd is not None:
                lines.append(f"- **RPM**: ${v.rpm_usd:.2f}")
            if v.retention_30s_pct is not None:
                target = "✓" if v.retention_30s_pct >= 80 else "✗"
                lines.append(f"- **Retención 30s**: {v.retention_30s_pct:.0f}% {target} (target ≥80%)")
            lines.append(f"- **Leaks detectados**: {len(v.leaks)}")
            if v.leaks:
                lines.append("")
                lines.append("| Tramo | Drop | Sección | Sugerencia |")
                lines.append("|-------|------|---------|------------|")
                for l in v.leaks:
                    sec = l.related_section or "—"
                    fix = l.suggested_fix[:80] + ("..." if len(l.suggested_fix) > 80 else "")
                    lines.append(
                        f"| {l.start_sec}-{l.end_sec}s | {l.drop_pct:.1f}% | {sec} | {fix} |"
                    )
            lines.append("")

    if report.ask_studio_prompts:
        lines.append("## Prompts para Ask Studio")
        lines.append("")
        lines.append(
            "Pega cada uno en el panel de Ask Studio (YouTube Studio > Analítica > "
            "Ask Studio) para auditar tu canal con Gemini integrado."
        )
        lines.append("")
        for p in report.ask_studio_prompts:
            lines.append(f"### {p.title}")
            lines.append("")
            lines.append(f"_Propósito: {p.purpose}_")
            lines.append("")
            lines.append("```")
            lines.append(p.prompt_text)
            lines.append("```")
            lines.append("")
            lines.append(f"**Output esperado**: {p.expected_output}")
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
