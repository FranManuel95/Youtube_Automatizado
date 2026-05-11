"""CLI principal del pipeline yt-auto.

Etapas del pipeline (ver documentación en /docs):
    1. niche       - investigación y validación de nichos (Claude + Gemini)
    2. scripts     - ingeniería de guiones (hooks, bucles de curiosidad)
    3. audio       - locución con ElevenLabs Multilingual v2
    4. visuals     - generación de imagen/video (Nano Banana, Seedance 2.0)
    5. editing     - montaje dinámico (regla de 3 segundos, packaging 4K)
    6. publishing  - subida a YouTube + Multi-language Audio
    7. analytics   - auditoría con Ask Studio / Inspiration Tab
"""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from yt_auto.config import ROOT_DIR, get_settings

app = typer.Typer(help="Pipeline de automatización de YouTube con IA - estrategia 2026.")
niche_app = typer.Typer(help="Etapa 1 - selección y validación de nichos.")
app.add_typer(niche_app, name="niche")

console = Console()


@app.command()
def info() -> None:
    """Muestra la configuración cargada y la salud del entorno."""
    s = get_settings()
    console.rule("[bold cyan]yt-auto - estado del entorno")
    console.print(f"Proyecto:           {s.project_name}")
    console.print(f"Idioma:             {s.default_language}")
    console.print(f"Mercados objetivo:  {', '.join(s.target_markets_list)}")
    console.print(f"Formato:            {s.content_format} ({s.target_duration_min} min)")
    console.print(f"Nicho por defecto:  {s.default_niche or '[no definido]'}")

    console.rule("[bold cyan]APIs configuradas")
    checks = {
        "Anthropic (Claude)": bool(s.anthropic_api_key),
        "Google Gemini": bool(s.gemini_api_key),
        "ElevenLabs": bool(s.elevenlabs_api_key),
        "Nano Banana": bool(s.nanobanana_api_key),
        "Seedance / TopMedia": bool(s.seedance_api_key or s.topmedia_api_key),
        "YouTube OAuth": (ROOT_DIR / s.youtube_client_secrets_file).exists(),
    }
    for name, ok in checks.items():
        marker = "[green]OK[/green]" if ok else "[yellow]falta[/yellow]"
        console.print(f"  {marker}  {name}")

    console.print(
        "\n[dim]Modo: sin API key se trabaja en modo interactivo "
        "(usa `yt-auto niche prompt` y pásame el resultado).[/dim]"
    )


# -------------------- niche --------------------


@niche_app.command("prompt")
def niche_prompt(
    count: int = typer.Option(10, "--count", "-n", help="Número de subnichos a pedir"),
    vertical: str | None = typer.Option(None, "--vertical", "-v", help="Filtrar a un vertical"),
    save: bool = typer.Option(True, "--save/--no-save", help="Guardar el prompt en output/"),
) -> None:
    """Genera el prompt maestro para una auditoría de nichos (modo interactivo).

    Copia el prompt en tu sesión con Claude (Opus 4.7 recomendado).
    Después usa `yt-auto niche ingest <archivo>` para guardar la respuesta.
    """
    from yt_auto.niche import OUTPUT_DIR, build_exploration_prompt
    from yt_auto.niche.prompts import EXPLORATION_SYSTEM

    s = get_settings()
    market = s.target_markets_list[0] if s.target_markets_list else "US-Hispanic"
    body = build_exploration_prompt(
        market=market,
        language=s.default_language,
        content_format=s.content_format,
        target_duration_min=s.target_duration_min,
        target_count=count,
        vertical_filter=vertical,
    )

    console.rule("[bold cyan]System prompt")
    console.print(EXPLORATION_SYSTEM)
    console.rule("[bold cyan]User prompt")
    console.print(body)

    if save:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        path = OUTPUT_DIR / "last_prompt.md"
        path.write_text(
            f"# System\n\n{EXPLORATION_SYSTEM}\n\n# User\n\n{body}\n",
            encoding="utf-8",
        )
        console.print(f"\n[green]Prompt guardado en[/green] {path}")


@niche_app.command("ingest")
def niche_ingest(
    response_file: Path = typer.Argument(..., help="Archivo con la respuesta JSON de Claude"),
    archive: bool = typer.Option(False, "--archive", help="Copiar también a docs/niche-audits/"),
) -> None:
    """Parsea la respuesta JSON de Claude y la guarda como reporte."""
    from yt_auto.niche import ingest_response, save_report

    raw = response_file.read_text("utf-8")
    report = ingest_response(raw)
    json_path, md_path = save_report(report, archive=archive)

    console.print(f"[green]Reporte guardado[/green]:")
    console.print(f"  JSON  -> {json_path}")
    console.print(f"  MD    -> {md_path}")
    if archive:
        console.print("  [bold]Archivado en docs/niche-audits/[/bold]")

    table = Table(title=f"Top {min(3, len(report.candidates))} candidatos")
    table.add_column("Nicho")
    table.add_column("Score", justify="right")
    table.add_column("RPM", justify="right")
    table.add_column("Competencia")
    for c in report.top(3):
        table.add_row(
            c.name,
            f"{c.score}/10",
            f"${c.rpm.rpm_min_usd:.1f}-{c.rpm.rpm_max_usd:.1f}",
            c.competition_level,
        )
    console.print(table)


@niche_app.command("list")
def niche_list() -> None:
    """Lista todas las auditorías guardadas."""
    from yt_auto.niche import OUTPUT_DIR

    if not OUTPUT_DIR.exists():
        console.print("[yellow]No hay auditorías todavía.[/yellow]")
        return
    files = sorted(OUTPUT_DIR.glob("*.json"))
    if not files:
        console.print("[yellow]No hay auditorías todavía.[/yellow]")
        return
    for f in files:
        console.print(f"  {f.relative_to(ROOT_DIR)}")


# -------------------- placeholders --------------------


@app.command()
def script(topic: str = typer.Argument(...), duration_min: int = 12) -> None:
    """Generar guion (stub) - hooks, open loops, anti-AI-Slop."""
    console.print(f"[yellow]TODO[/yellow] scripts.generate(topic={topic!r}, duration={duration_min}min)")


@app.command()
def audio(script_path: str = typer.Argument(...)) -> None:
    """Sintetizar locución (stub) - ElevenLabs Multilingual v2."""
    console.print(f"[yellow]TODO[/yellow] audio.synthesize(script={script_path!r})")


@app.command()
def visuals(storyboard_path: str = typer.Argument(...)) -> None:
    """Generar visuales (stub) - Nano Banana + Seedance 2.0, multi-reference."""
    console.print(f"[yellow]TODO[/yellow] visuals.render(storyboard={storyboard_path!r})")


@app.command()
def publish(video_path: str = typer.Argument(...)) -> None:
    """Publicar video en YouTube (stub) - con MLA y miniatura 4K."""
    console.print(f"[yellow]TODO[/yellow] publishing.upload(video={video_path!r})")


if __name__ == "__main__":
    app()
