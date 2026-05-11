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

import typer
from rich.console import Console

from yt_auto.config import get_settings

app = typer.Typer(help="Pipeline de automatización de YouTube con IA - estrategia 2026.")
console = Console()


@app.command()
def info() -> None:
    """Muestra la configuración cargada y la salud del entorno."""
    s = get_settings()
    console.rule("[bold cyan]yt-auto - estado del entorno")
    console.print(f"Proyecto:        {s.project_name}")
    console.print(f"Idioma por defecto: {s.default_language}")
    console.print(f"Mercados objetivo:  {', '.join(s.target_markets_list)}")
    console.print(f"Nicho por defecto:  {s.default_niche or '[no definido]'}")

    console.rule("[bold cyan]APIs configuradas")
    checks = {
        "Anthropic (Claude)": bool(s.anthropic_api_key),
        "Google Gemini": bool(s.gemini_api_key),
        "ElevenLabs": bool(s.elevenlabs_api_key),
        "Nano Banana": bool(s.nanobanana_api_key),
        "Seedance / TopMedia": bool(s.seedance_api_key or s.topmedia_api_key),
        "YouTube OAuth": (s.assets_dir.parent / s.youtube_client_secrets_file).exists(),
    }
    for name, ok in checks.items():
        marker = "[green]OK[/green]" if ok else "[yellow]falta[/yellow]"
        console.print(f"  {marker}  {name}")


@app.command()
def niche(topic: str = typer.Argument(..., help="Tema o subnicho a auditar")) -> None:
    """Investigación de nicho (stub) - usar Claude Sonnet 4.6 / Opus 4.7 Vision."""
    console.print(f"[yellow]TODO[/yellow] niche.research(topic={topic!r})")


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
