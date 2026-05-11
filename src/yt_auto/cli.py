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
script_app = typer.Typer(help="Etapa 2 - ingeniería de guiones.")
audio_app = typer.Typer(help="Etapa 3 - locución con ElevenLabs.")
visuals_app = typer.Typer(help="Etapa 4 - generación visual (Nano Banana + Seedance).")
editing_app = typer.Typer(help="Etapa 5 - edición y packaging.")
app.add_typer(niche_app, name="niche")
app.add_typer(script_app, name="script")
app.add_typer(audio_app, name="audio")
app.add_typer(visuals_app, name="visuals")
app.add_typer(editing_app, name="editing")

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


# -------------------- script --------------------


@script_app.command("prompt")
def script_prompt(
    topic: str = typer.Argument(..., help="Tema concreto del video"),
    niche: str = typer.Option(..., "--niche", "-n", help="Subnicho del canal"),
    candidate_name: str = typer.Option(
        ..., "--candidate", "-c", help="Nombre del candidato en la auditoría origen"
    ),
    duration_min: int = typer.Option(0, "--duration", "-d", help="Override de duración"),
    viewer_hint: str | None = typer.Option(None, "--viewer", help="Hint del viewer_ideal"),
    audit_ref: str | None = typer.Option(None, "--audit-ref", help="Path de la auditoría origen"),
    save: bool = typer.Option(True, "--save/--no-save"),
) -> None:
    """Genera el prompt maestro de un guion para sesión interactiva con Claude."""
    from yt_auto.scripts import OUTPUT_DIR, SCRIPT_SYSTEM, build_script_prompt

    s = get_settings()
    market = s.target_markets_list[0] if s.target_markets_list else "US-Hispanic"
    duration = duration_min or s.target_duration_min

    body = build_script_prompt(
        niche=niche,
        candidate_name=candidate_name,
        target_market=market,
        target_language=s.default_language,
        target_duration_min=duration,
        topic=topic,
        viewer_ideal_hint=viewer_hint,
        niche_audit_ref=audit_ref,
    )

    console.rule("[bold cyan]System prompt")
    console.print(SCRIPT_SYSTEM)
    console.rule("[bold cyan]User prompt")
    console.print(body)

    if save:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        path = OUTPUT_DIR / "last_prompt.md"
        path.write_text(f"# System\n\n{SCRIPT_SYSTEM}\n\n# User\n\n{body}\n", "utf-8")
        console.print(f"\n[green]Prompt guardado en[/green] {path}")


@script_app.command("ingest")
def script_ingest(
    response_file: Path = typer.Argument(...),
    archive: bool = typer.Option(False, "--archive"),
) -> None:
    """Parsea la respuesta JSON de Claude y guarda el guion."""
    from yt_auto.scripts import ingest_response, save_report

    raw = response_file.read_text("utf-8")
    report = ingest_response(raw)
    json_path, md_path = save_report(report, archive=archive)
    h = report.draft.humanization

    console.print(f"[green]Guion guardado[/green]:")
    console.print(f"  JSON  -> {json_path}")
    console.print(f"  MD    -> {md_path}")
    if archive:
        console.print("  [bold]Archivado en docs/scripts-archive/[/bold]")

    veredict_color = "green" if h.pasa else "yellow"
    console.print(
        f"\n[{veredict_color}]Anti-AI-Slop: {'APROBADO' if h.pasa else 'REQUIERE EDICIÓN'}[/{veredict_color}]"
    )
    console.print(f"  Retención 30s estimada: {report.draft.estimated_retention_30s:.0%}")
    console.print(f"  CTR estimado: {report.draft.estimated_ctr:.1%}")


@script_app.command("list")
def script_list() -> None:
    """Lista guiones guardados."""
    from yt_auto.scripts import OUTPUT_DIR

    if not OUTPUT_DIR.exists():
        console.print("[yellow]No hay guiones todavía.[/yellow]")
        return
    files = sorted(OUTPUT_DIR.glob("*.json"))
    if not files:
        console.print("[yellow]No hay guiones todavía.[/yellow]")
        return
    for f in files:
        console.print(f"  {f.relative_to(ROOT_DIR)}")


# -------------------- audio --------------------


@audio_app.command("plan")
def audio_plan(
    script_file: Path = typer.Argument(..., help="JSON de un ScriptReport"),
    archive: bool = typer.Option(False, "--archive"),
) -> None:
    """Genera un plan de locución por bloques a partir de un guion."""
    from yt_auto.audio import build_report, save_report
    from yt_auto.scripts import load_report as load_script_report

    script_report = load_script_report(script_file)
    audio_report = build_report(script_report, script_ref=str(script_file))
    json_path, md_path, blocks_dir = save_report(audio_report, archive=archive)

    p = audio_report.plan
    console.print(f"[green]Plan de audio creado[/green]:")
    console.print(f"  JSON     -> {json_path}")
    console.print(f"  MD       -> {md_path}")
    console.print(f"  blocks/  -> {blocks_dir}")
    if archive:
        console.print("  [bold]Archivado en docs/audio-archive/[/bold]")

    fits_color = "green" if audio_report.eleven_free_tier_fits else "yellow"
    fits_label = "cabe en Free" if audio_report.eleven_free_tier_fits else "NO cabe en Free"
    console.print()
    console.print(f"  Bloques:       {len(p.blocks)}")
    console.print(f"  Palabras:      {p.total_words}")
    console.print(f"  Caracteres:    {p.total_chars} [{fits_color}]({fits_label})[/{fits_color}]")
    console.print(f"  Duración est.: {p.estimated_duration_sec}s")
    if audio_report.notes:
        console.print(f"\n[yellow]Nota:[/yellow] {audio_report.notes}")


@audio_app.command("list")
def audio_list() -> None:
    """Lista planes de audio guardados."""
    from yt_auto.audio import OUTPUT_DIR

    if not OUTPUT_DIR.exists():
        console.print("[yellow]No hay planes de audio todavía.[/yellow]")
        return
    files = sorted(OUTPUT_DIR.glob("*.json"))
    if not files:
        console.print("[yellow]No hay planes de audio todavía.[/yellow]")
        return
    for f in files:
        console.print(f"  {f.relative_to(ROOT_DIR)}")


# -------------------- visuals --------------------


@visuals_app.command("prompt")
def visuals_prompt(
    script_file: Path = typer.Argument(..., help="JSON de un ScriptReport"),
    save: bool = typer.Option(True, "--save/--no-save"),
) -> None:
    """Genera el prompt maestro para diseñar el plan visual (interactivo)."""
    from yt_auto.scripts import load_report as load_script_report
    from yt_auto.visuals import OUTPUT_DIR, VISUALS_SYSTEM, build_visuals_prompt

    script_report = load_script_report(script_file)
    body = build_visuals_prompt(script_report, script_ref=str(script_file))

    console.rule("[bold cyan]System prompt")
    console.print(VISUALS_SYSTEM)
    console.rule("[bold cyan]User prompt")
    console.print(body[:2000] + ("\n... (truncado, ver archivo completo)" if len(body) > 2000 else ""))

    if save:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        path = OUTPUT_DIR / "last_prompt.md"
        path.write_text(f"# System\n\n{VISUALS_SYSTEM}\n\n# User\n\n{body}\n", "utf-8")
        console.print(f"\n[green]Prompt guardado en[/green] {path}")


@visuals_app.command("ingest")
def visuals_ingest(
    response_file: Path = typer.Argument(...),
    archive: bool = typer.Option(False, "--archive"),
) -> None:
    """Parsea la respuesta JSON de Claude y exporta el plan visual completo."""
    from yt_auto.visuals import ingest_response, save_report

    raw = response_file.read_text("utf-8")
    report = ingest_response(raw)
    json_path, md_path, prompts_dir = save_report(report, archive=archive)

    console.print(f"[green]Plan visual guardado[/green]:")
    console.print(f"  JSON      -> {json_path}")
    console.print(f"  MD        -> {md_path}")
    console.print(f"  prompts/  -> {prompts_dir}")
    if archive:
        console.print("  [bold]Archivado en docs/visuals-archive/[/bold]")

    console.print()
    console.print(f"  Personaje:       {report.character.name}")
    console.print(f"  Vistas:          {len(report.character.views)}")
    console.print(f"  Shots:           {len(report.shots)}")
    console.print(f"  Pattern interr.: {report.pattern_interrupt_count}")
    if not report.character.has_mandatory_views():
        console.print("  [yellow]⚠ Faltan vistas obligatorias del personaje[/yellow]")


@visuals_app.command("list")
def visuals_list() -> None:
    """Lista planes visuales guardados."""
    from yt_auto.visuals import OUTPUT_DIR

    if not OUTPUT_DIR.exists():
        console.print("[yellow]No hay planes visuales todavía.[/yellow]")
        return
    files = sorted(OUTPUT_DIR.glob("*.json"))
    if not files:
        console.print("[yellow]No hay planes visuales todavía.[/yellow]")
        return
    for f in files:
        console.print(f"  {f.relative_to(ROOT_DIR)}")


# -------------------- editing --------------------


@editing_app.command("plan")
def editing_plan(
    script_file: Path = typer.Argument(..., help="ScriptReport JSON"),
    audio_file: Path = typer.Argument(..., help="AudioReport JSON"),
    visuals_file: Path | None = typer.Option(None, "--visuals", help="VisualReport JSON"),
    archive: bool = typer.Option(False, "--archive"),
) -> None:
    """Ensambla el plan de edición a partir de las etapas 2-4."""
    from yt_auto.audio import load_report as load_audio
    from yt_auto.editing import build_report, save_report
    from yt_auto.scripts import load_report as load_script
    from yt_auto.visuals import load_report as load_visuals

    script_report = load_script(script_file)
    audio_report = load_audio(audio_file)
    visual_report = load_visuals(visuals_file) if visuals_file else None

    report = build_report(
        script=script_report,
        audio=audio_report,
        visuals=visual_report,
        script_ref=str(script_file),
        audio_ref=str(audio_file),
        visuals_ref=str(visuals_file) if visuals_file else None,
    )
    json_path, md_path, csv_path = save_report(report, archive=archive)

    console.print("[green]Plan de edición guardado[/green]:")
    console.print(f"  JSON  -> {json_path}")
    console.print(f"  MD    -> {md_path}")
    console.print(f"  CSV   -> {csv_path}")
    if archive:
        console.print("  [bold]Archivado en docs/editing-archive/[/bold]")

    p = report.plan
    console.print()
    console.print(f"  Eventos:        {len(p.timeline)}")
    console.print(f"  Subtítulos:     {len(p.subtitles)}")
    console.print(f"  DAI anchors:    {len(p.dai_anchors)}")
    rule_color = "green" if p.three_second_rule_pass else "yellow"
    rule_label = "pasa" if p.three_second_rule_pass else f"falla ({p.longest_static_gap_sec}s)"
    console.print(f"  Regla de 3s:    [{rule_color}]{rule_label}[/{rule_color}]")
    if p.three_second_violations:
        console.print(f"  [yellow]{len(p.three_second_violations)} violaciones de la regla 3s[/yellow]")


@editing_app.command("list")
def editing_list() -> None:
    """Lista planes de edición guardados."""
    from yt_auto.editing import OUTPUT_DIR

    if not OUTPUT_DIR.exists():
        console.print("[yellow]No hay planes de edición todavía.[/yellow]")
        return
    files = sorted(OUTPUT_DIR.glob("*.json"))
    if not files:
        console.print("[yellow]No hay planes de edición todavía.[/yellow]")
        return
    for f in files:
        console.print(f"  {f.relative_to(ROOT_DIR)}")


# -------------------- placeholders --------------------


@app.command()
def publish(video_path: str = typer.Argument(...)) -> None:
    """Publicar video en YouTube (stub) - con MLA y miniatura 4K."""
    console.print(f"[yellow]TODO[/yellow] publishing.upload(video={video_path!r})")


if __name__ == "__main__":
    app()
