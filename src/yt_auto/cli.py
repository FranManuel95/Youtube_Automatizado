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
publish_app = typer.Typer(help="Etapa 6 - publicación YouTube.")
analytics_app = typer.Typer(help="Etapa 7 - analítica, retention leaks y Ask Studio.")
competitive_app = typer.Typer(help="Análisis competitivo - YouTube Data API v3.")
app.add_typer(niche_app, name="niche")
app.add_typer(script_app, name="script")
app.add_typer(audio_app, name="audio")
app.add_typer(visuals_app, name="visuals")
app.add_typer(editing_app, name="editing")
app.add_typer(publish_app, name="publish")
app.add_typer(analytics_app, name="analytics")
app.add_typer(competitive_app, name="competitive")

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


@audio_app.command("voices")
def audio_voices(
    remote: bool = typer.Option(
        False, "--remote", help="Consulta las voces reales de tu cuenta ElevenLabs"
    ),
    lang: str | None = typer.Option(
        None, "--lang", help="Filtra por idioma/acento (substring case-insensitive)"
    ),
) -> None:
    """Lista presets curados o las voces de tu cuenta ElevenLabs."""
    from yt_auto.audio import CATALOG

    if not remote:
        table = Table(title="Catálogo local (presets curados)")
        table.add_column("Key")
        table.add_column("Nombre")
        table.add_column("Género")
        table.add_column("Acento")
        for v in CATALOG:
            table.add_row(v.id_key, v.display_name, v.gender, v.accent)
        console.print(table)
        console.print(
            "\n[dim]Usa `--remote` para listar las voces reales de tu cuenta "
            "y copiar un voice_id a .env como ELEVENLABS_VOICE_ID.[/dim]"
        )
        return

    from yt_auto.audio.client import ElevenLabsClient, ElevenLabsError

    s = get_settings()
    if not s.elevenlabs_api_key:
        console.print("[red]Falta ELEVENLABS_API_KEY en .env[/red]")
        raise typer.Exit(code=1)

    try:
        with ElevenLabsClient(s.elevenlabs_api_key) as client:
            voices = client.list_voices()
            sub = client.get_subscription()
    except ElevenLabsError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc

    if lang:
        needle = lang.lower()
        voices = [
            v
            for v in voices
            if any(needle in (val or "").lower() for val in v.labels.values())
            or needle in v.name.lower()
        ]

    table = Table(title=f"Voces remotas ({sub.tier}) · {len(voices)} resultado(s)")
    table.add_column("voice_id")
    table.add_column("Nombre")
    table.add_column("Género")
    table.add_column("Acento/Idioma")
    table.add_column("Categoría")
    for v in voices:
        table.add_row(
            v.voice_id,
            v.name,
            v.gender or "-",
            v.language or "-",
            v.category or "-",
        )
    console.print(table)
    console.print(
        f"\n[dim]Cuota: {sub.character_count}/{sub.character_limit} chars usados "
        f"({sub.characters_remaining} disponibles este ciclo).[/dim]"
    )
    console.print(
        "[dim]Copia el voice_id deseado a .env como `ELEVENLABS_VOICE_ID=...`[/dim]"
    )


@audio_app.command("synth")
def audio_synth(
    plan_file: Path = typer.Argument(..., help="JSON de un AudioReport"),
    blocks: list[int] = typer.Option(
        None, "--block", "-b", help="Solo estos bloques (repetible). Si se omite, todos."
    ),
    voice_id: str | None = typer.Option(
        None, "--voice-id", help="Override de ELEVENLABS_VOICE_ID"
    ),
    overwrite: bool = typer.Option(
        False, "--overwrite", help="Regenera los MP3 aunque ya existan"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Solo muestra el coste estimado, no llama a la API"
    ),
) -> None:
    """Sintetiza un AudioReport a MP3 vía API de ElevenLabs."""
    from yt_auto.audio import NarrationBlock, load_report
    from yt_auto.audio.api import (
        QuotaExceededError,
        mp3_dir_for,
        synthesize_report,
    )
    from yt_auto.audio.client import ElevenLabsClient, ElevenLabsError

    report = load_report(plan_file)
    plan_file = plan_file.resolve()
    output_base = plan_file.parent / plan_file.stem

    s = get_settings()
    resolved_voice = voice_id or s.elevenlabs_voice_id

    selected = (
        [b for b in report.plan.blocks if b.block_id in set(blocks)]
        if blocks
        else list(report.plan.blocks)
    )
    if not selected:
        console.print(f"[red]Ningún bloque coincide con --block {blocks}[/red]")
        raise typer.Exit(code=1)

    mp3_dir = mp3_dir_for(output_base)

    def _mp3_path(b: NarrationBlock) -> Path:
        return mp3_dir / f"{b.block_id:02d}_{b.role.value}.mp3"

    pending = [b for b in selected if overwrite or not _mp3_path(b).exists()]
    pending_chars = sum(b.character_count for b in pending)

    console.print(f"  Guion:        {report.script_title}")
    console.print(f"  Bloques sel.: {len(selected)} (de {len(report.plan.blocks)})")
    console.print(f"  Ya en disco:  {len(selected) - len(pending)}")
    console.print(f"  A sintetizar: {len(pending)} ({pending_chars} chars)")
    console.print(f"  Modelo:       {report.plan.model_id}")
    console.print(f"  Voice ID:     {resolved_voice or '[red]NO DEFINIDA[/red]'}")
    console.print(f"  Destino:      {mp3_dir.relative_to(ROOT_DIR)}/")

    if dry_run:
        console.print("\n[yellow]--dry-run: no se llama a la API.[/yellow]")
        return
    if not pending:
        console.print("\n[green]Nada que sintetizar.[/green]")
        return
    if not s.elevenlabs_api_key:
        console.print("[red]Falta ELEVENLABS_API_KEY en .env[/red]")
        raise typer.Exit(code=1)
    if not resolved_voice:
        console.print(
            "[red]Falta voice_id. Usa `yt-auto audio voices --remote` y "
            "fija ELEVENLABS_VOICE_ID en .env, o pasa --voice-id.[/red]"
        )
        raise typer.Exit(code=1)

    try:
        with ElevenLabsClient(s.elevenlabs_api_key) as client:
            result = synthesize_report(
                report,
                client=client,
                voice_id=resolved_voice,
                output_base=output_base,
                block_ids=blocks or None,
                overwrite=overwrite,
            )
    except QuotaExceededError as exc:
        console.print(f"\n[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    except ElevenLabsError as exc:
        console.print(f"\n[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc

    console.print(
        f"\n[green]MP3 generados: {result.generated_count}[/green] "
        f"(saltados: {result.skipped_count})"
    )
    for r in result.blocks:
        marker = "·" if r.skipped else "[green]✓[/green]"
        console.print(
            f"  {marker} {r.block_id:02d}_{r.role}  {r.path.relative_to(ROOT_DIR)}"
        )
    if result.subscription_before is not None:
        sub = result.subscription_before
        console.print(
            f"\n[dim]Cuota pre-synth: {sub.character_count}/{sub.character_limit} "
            f"({sub.tier}). Gastados ahora: {result.total_characters_used} chars.[/dim]"
        )


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


# -------------------- publish --------------------


@publish_app.command("prep")
def publish_prep(
    script_file: Path = typer.Argument(..., help="ScriptReport JSON"),
    editing_file: Path = typer.Argument(..., help="EditingReport JSON"),
    pdf_url: str = typer.Option(
        "https://<pendiente-de-configurar>/recurso",
        "--pdf-url",
        help="URL del PDF/recurso del CTA",
    ),
    extra_tags: str | None = typer.Option(None, "--tags", help="Tags extra separados por coma"),
    archive: bool = typer.Option(False, "--archive"),
) -> None:
    """Genera metadata YouTube + capítulos + checklist pre-publish."""
    from yt_auto.editing import load_report as load_editing
    from yt_auto.publishing import build_report, save_report
    from yt_auto.scripts import load_report as load_script

    script_report = load_script(script_file)
    editing_report = load_editing(editing_file)
    extra = [t.strip() for t in extra_tags.split(",")] if extra_tags else None

    report = build_report(
        script=script_report,
        editing=editing_report,
        script_ref=str(script_file),
        editing_ref=str(editing_file),
        pdf_url=pdf_url,
        extra_tags=extra,
    )
    json_path, md_path = save_report(report, archive=archive)

    console.print(f"[green]Plan de publicación guardado[/green]:")
    console.print(f"  JSON  -> {json_path}")
    console.print(f"  MD    -> {md_path}")
    if archive:
        console.print("  [bold]Archivado en docs/publishing-archive/[/bold]")

    c = report.plan.checklist
    veredict_color = "green" if c.critical_pass else "red"
    veredict_label = "LISTO PARA PUBLICAR" if c.critical_pass else "NO PUBLICAR"
    console.print()
    console.print(f"  [{veredict_color}]{veredict_label}[/{veredict_color}]")
    console.print(f"  Críticos pasados: {sum([c.anti_ai_slop_passed, c.thumbnail_4k_ready, c.title_under_70_chars, c.description_has_disclaimer, c.likeness_declaration])}/5")
    console.print(f"  Capítulos: {len(report.plan.chapters)}")
    console.print(f"  Tags: {len(report.plan.metadata.tags)}")
    if report.notes:
        console.print(f"\n[yellow]Notas:[/yellow]\n{report.notes}")


@publish_app.command("list")
def publish_list() -> None:
    """Lista planes de publicación guardados."""
    from yt_auto.publishing import OUTPUT_DIR

    if not OUTPUT_DIR.exists():
        console.print("[yellow]No hay planes de publicación todavía.[/yellow]")
        return
    files = sorted(OUTPUT_DIR.glob("*.json"))
    if not files:
        console.print("[yellow]No hay planes de publicación todavía.[/yellow]")
        return
    for f in files:
        console.print(f"  {f.relative_to(ROOT_DIR)}")


# -------------------- analytics --------------------


@analytics_app.command("ask")
def analytics_ask(
    purpose: str = typer.Argument(
        ...,
        help="outlier | drops | gaps | competitor | thumbnails",
    ),
    video_title: str = typer.Option("", "--video", help="Título del video"),
    views: int = typer.Option(0, "--views"),
    subscribers: int = typer.Option(0, "--subs"),
    niche: str = typer.Option("", "--niche"),
    market: str = typer.Option("", "--market"),
    competitor: str = typer.Option("", "--competitor"),
    biggest_drop_sec: int = typer.Option(60, "--drop-sec"),
) -> None:
    """Genera un prompt para Ask Studio (Gemini in-channel)."""
    from yt_auto.analytics import (
        ab_test_thumbnails_prompt,
        competitor_pattern_prompt,
        drop_detection_prompt,
        gap_detection_prompt,
        outlier_analysis_prompt,
    )

    s = get_settings()
    market = market or (s.target_markets_list[0] if s.target_markets_list else "US-Hispanic")

    if purpose == "outlier":
        p = outlier_analysis_prompt(video_title or "<título>", views, subscribers)
    elif purpose == "drops":
        p = drop_detection_prompt(video_title or "<título>", biggest_drop_sec)
    elif purpose == "gaps":
        p = gap_detection_prompt(niche or s.default_niche or "<nicho>", market)
    elif purpose == "competitor":
        p = competitor_pattern_prompt(competitor or "<canal-competidor>")
    elif purpose == "thumbnails":
        p = ab_test_thumbnails_prompt(video_title or "<título>")
    else:
        console.print(f"[red]Propósito desconocido: {purpose}[/red]")
        raise typer.Exit(code=1)

    console.rule(f"[bold cyan]{p.title}")
    console.print(p.prompt_text)
    console.rule("[bold cyan]Output esperado")
    console.print(p.expected_output)


@analytics_app.command("retention")
def analytics_retention(
    csv_file: Path = typer.Argument(..., help="CSV exportado de YouTube Studio"),
    duration_sec: int = typer.Option(..., "--duration", "-d", help="Duración del video en segundos"),
    drop_threshold: float = typer.Option(5.0, "--threshold", help="Caída mínima para marcar leak (%)"),
    archive: bool = typer.Option(False, "--archive"),
) -> None:
    """Parsea retention CSV y detecta retention leaks."""
    from yt_auto.analytics import (
        AnalyticsReport,
        VideoPerformance,
        detect_leaks,
        parse_retention_csv,
        save_report,
    )

    content = csv_file.read_text("utf-8")
    points = parse_retention_csv(content, total_duration_sec=duration_sec)
    leaks = detect_leaks(points, drop_threshold_pct=drop_threshold)

    video = VideoPerformance(
        video_id=csv_file.stem,
        title=csv_file.stem,
        duration_sec=duration_sec,
        retention_curve=points,
        leaks=leaks,
    )
    report = AnalyticsReport(videos=[video])
    json_path, md_path = save_report(report, label=f"retention_{csv_file.stem}", archive=archive)

    console.print(f"[green]Análisis de retention guardado[/green]:")
    console.print(f"  JSON  -> {json_path}")
    console.print(f"  MD    -> {md_path}")
    console.print()
    console.print(f"  Puntos parseados: {len(points)}")
    console.print(f"  Leaks detectados: {len(leaks)}")
    for l in leaks[:5]:
        console.print(f"    [yellow]{l.start_sec}-{l.end_sec}s[/yellow] drop {l.drop_pct:.1f}%")


@analytics_app.command("list")
def analytics_list() -> None:
    """Lista reportes de analítica guardados."""
    from yt_auto.analytics import OUTPUT_DIR

    if not OUTPUT_DIR.exists():
        console.print("[yellow]No hay reportes todavía.[/yellow]")
        return
    files = sorted(OUTPUT_DIR.glob("*.json"))
    if not files:
        console.print("[yellow]No hay reportes todavía.[/yellow]")
        return
    for f in files:
        console.print(f"  {f.relative_to(ROOT_DIR)}")


# -------------------- competitive (YouTube Data API v3) --------------------


@competitive_app.command("scan")
def competitive_scan(
    niche: str | None = typer.Option(
        None,
        "--niche",
        "-n",
        help="ID del perfil de nicho. Opcional si pasas --query (modo exploratorio).",
    ),
    query: str | None = typer.Option(
        None, "--query", "-q", help="Query de búsqueda. Si lo pasas, --niche es opcional."
    ),
    max_channels: int = typer.Option(10, "--max", help="Cuántos canales top devolver (1-50)"),
    no_cache: bool = typer.Option(False, "--no-cache", help="Fuerza llamada real, salta caché 24h"),
) -> None:
    """Escanea los canales referentes de un nicho con datos reales de la API.

    Dos modos:
    - Con perfil: `competitive scan --niche real_estate_latino`
    - Exploratorio: `competitive scan --query "tu búsqueda"` (sin perfil)
    """
    from yt_auto.competitive import YouTubeAPIError, YouTubeDataClient, scan_niche
    from yt_auto.publishing.niche_profile import load_profile

    s = get_settings()
    if not s.youtube_api_key:
        console.print(
            "[red]Falta YOUTUBE_API_KEY en .env. "
            "Crea una en https://console.cloud.google.com/apis/credentials[/red]"
        )
        raise typer.Exit(code=1)

    if niche is None and not query:
        console.print(
            "[red]Debes pasar --niche <perfil> o --query \"búsqueda\" (o ambos).[/red]"
        )
        raise typer.Exit(code=1)

    if niche is not None:
        try:
            profile = load_profile(niche)
        except FileNotFoundError:
            console.print(f"[red]Perfil de nicho '{niche}' no existe.[/red]")
            console.print("[dim]Disponibles:[/dim]")
            from yt_auto.publishing.niche_profile import list_profiles

            for p in list_profiles():
                console.print(f"  {p.id} - {p.display_name}")
            raise typer.Exit(code=1) from None
    else:
        # Modo exploratorio: perfil sintético ad-hoc a partir de la query
        from yt_auto.publishing.niche_profile import NicheProfile

        profile = NicheProfile(
            id="_exploratorio",
            display_name=f"Exploratorio: {query}",
            search_queries=[query] if query else [],
        )

    try:
        with YouTubeDataClient(s.youtube_api_key) as client:
            report = scan_niche(
                profile,
                client=client,
                query_override=query,
                max_channels=max_channels,
                use_cache=not no_cache,
            )
    except YouTubeAPIError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc

    console.rule(f"[bold cyan]Análisis competitivo · {profile.display_name}")
    console.print(f"  Query usada:   '{report.query_used}'")
    console.print(f"  Canales:       {len(report.channels)}")
    console.print(f"  Subs mediana:  {report.median_subscribers:,}")
    console.print(f"  Subs total:    {report.total_subscribers:,}")
    color = {"fragmentado-bajo": "green", "fragmentado-medio": "yellow"}.get(
        report.fragmentation_score, "red"
    )
    console.print(
        f"  Saturación:    [{color}]{report.fragmentation_score}[/{color}] "
        f"({report.big_fish_count} canales >100k subs)"
    )
    console.print(f"  Cuota gastada: {report.quota_units_spent} unidades")
    console.print()

    table = Table(title="Top canales (orden por relevancia)")
    table.add_column("channel_id", overflow="fold")
    table.add_column("Canal")
    table.add_column("Subs", justify="right")
    table.add_column("Videos", justify="right")
    table.add_column("Views totales", justify="right")
    table.add_column("Views/video", justify="right")
    table.add_column("Edad (d)", justify="right")
    table.add_column("País")
    for ch in report.channels:
        table.add_row(
            ch.channel_id,
            ch.title[:35],
            f"{ch.statistics.subscriber_count:,}",
            f"{ch.statistics.video_count:,}",
            f"{ch.statistics.view_count:,}",
            f"{int(ch.avg_views_per_video):,}",
            str(ch.age_days or "-"),
            ch.country or "-",
        )
    console.print(table)
    console.print(
        "\n[dim]Para análisis profundo de un canal:[/dim]\n"
        "[dim]  yt-auto competitive outliers <channel_id>[/dim]\n"
        "[dim]  yt-auto competitive channel <channel_id>[/dim]"
    )


@competitive_app.command("outliers")
def competitive_outliers(
    channel_id: str = typer.Argument(..., help="channel_id del canal (UCxxxxxxxx)"),
    sample: int = typer.Option(30, "--sample", help="Cuántos videos analizar"),
    min_multiplier: float = typer.Option(3.0, "--multiplier", help="Umbral X veces mediana"),
    no_cache: bool = typer.Option(False, "--no-cache"),
) -> None:
    """Detecta videos outliers de un canal (views >= X veces la mediana)."""
    from yt_auto.competitive import YouTubeAPIError, YouTubeDataClient, detect_outliers

    s = get_settings()
    if not s.youtube_api_key:
        console.print("[red]Falta YOUTUBE_API_KEY en .env[/red]")
        raise typer.Exit(code=1)

    try:
        with YouTubeDataClient(s.youtube_api_key) as client:
            chs = client.channels([channel_id])
            if not chs:
                console.print(f"[red]Canal {channel_id} no encontrado.[/red]")
                raise typer.Exit(code=1)
            channel = chs[0]
            outliers = detect_outliers(
                channel,
                client=client,
                sample_size=sample,
                min_multiplier=min_multiplier,
                use_cache=not no_cache,
            )
    except YouTubeAPIError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc

    console.rule(f"[bold cyan]Outliers · {channel.title}")
    console.print(
        f"  Mediana del canal: "
        f"{outliers[0].channel_median_views if outliers else '-'} views"
    )
    console.print(f"  Outliers (>= {min_multiplier}x): {len(outliers)}")
    console.print(f"  Cuota gastada:     {client.quota.units_spent} unidades")
    console.print()

    if not outliers:
        console.print(
            "[dim]Sin outliers. El canal tiene rendimiento homogéneo o tu --multiplier es muy alto.[/dim]"
        )
        return

    table = Table(title="Videos outlier")
    table.add_column("Multiplicador", justify="right")
    table.add_column("Views", justify="right")
    table.add_column("Edad")
    table.add_column("Título")
    for o in outliers[:15]:
        table.add_row(
            f"{o.multiplier_vs_median:.1f}x",
            f"{o.video.statistics.view_count:,}",
            f"{o.video.age_days}d",
            o.video.title[:60],
        )
    console.print(table)


@competitive_app.command("channel")
def competitive_channel(
    channel_id: str = typer.Argument(..., help="channel_id (UCxxx) o handle (@nombre)"),
) -> None:
    """Detalle de un canal: stats + últimos videos."""
    from yt_auto.competitive import YouTubeAPIError, YouTubeDataClient

    s = get_settings()
    if not s.youtube_api_key:
        console.print("[red]Falta YOUTUBE_API_KEY en .env[/red]")
        raise typer.Exit(code=1)

    try:
        with YouTubeDataClient(s.youtube_api_key) as client:
            chs = client.channels([channel_id])
            if not chs:
                console.print(f"[red]Canal {channel_id} no encontrado.[/red]")
                raise typer.Exit(code=1)
            ch = chs[0]
            recent_ids = (
                client.playlist_items(ch.uploads_playlist_id, max_results=10)
                if ch.uploads_playlist_id
                else []
            )
            recent = client.videos(recent_ids) if recent_ids else []
    except YouTubeAPIError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc

    console.rule(f"[bold cyan]{ch.title}")
    console.print(f"  URL:        {ch.url}")
    console.print(f"  País:       {ch.country or '-'}")
    console.print(f"  Antigüedad: {ch.age_days or '-'} días")
    console.print(f"  Subs:       {ch.statistics.subscriber_count:,}")
    console.print(f"  Videos:     {ch.statistics.video_count:,}")
    console.print(f"  Views:      {ch.statistics.view_count:,}")
    console.print(f"  Views/vid:  {int(ch.avg_views_per_video):,}")
    console.print()

    if recent:
        table = Table(title="Últimos 10 videos")
        table.add_column("Edad", justify="right")
        table.add_column("Views", justify="right")
        table.add_column("Likes", justify="right")
        table.add_column("Título")
        for v in recent:
            table.add_row(
                f"{v.age_days}d",
                f"{v.statistics.view_count:,}",
                f"{v.statistics.like_count:,}",
                v.title[:60],
            )
        console.print(table)


@competitive_app.command("quota")
def competitive_quota() -> None:
    """Recordatorio de cuota YouTube Data API v3."""
    console.print("[bold]YouTube Data API v3 — cuota diaria[/bold]")
    console.print("  Free tier: 10.000 unidades/día")
    console.print()
    console.print("[bold]Coste por endpoint:[/bold]")
    console.print("  search.list:        [yellow]100 unidades[/yellow] (lo más caro)")
    console.print("  channels.list:      1 unidad")
    console.print("  videos.list:        1 unidad")
    console.print("  playlistItems.list: 1 unidad")
    console.print()
    console.print("[bold]Coste de comandos del pipeline:[/bold]")
    console.print("  competitive scan:     ~101 unidades (cabe 99/día)")
    console.print("  competitive outliers: ~2 unidades por canal")
    console.print("  competitive channel:  ~2 unidades")
    console.print()
    console.print(
        "[dim]La cuota se resetea a medianoche Pacífico (PT). "
        "Caché en disco evita repetir consultas el mismo día.[/dim]"
    )


if __name__ == "__main__":
    app()
