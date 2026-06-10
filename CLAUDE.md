# Guía operativa para Claude Code

Este repo implementa un pipeline de **producción asistida** de YouTube
(faceless, voz IA + screencast). Lee los documentos de `/docs` para la
metodología (retención, packaging, anti-AI-Slop), pero ten en cuenta el
**estado estratégico actual** descrito abajo: las conclusiones de nicho del
informe original fueron superadas por validación empírica.

## Estado estratégico actual (2026-05)

- **Nicho activo**: *Automatización IA para inmobiliarias* —
  `assets/niche_profiles/automatizacion_ia_inmobiliaria.yaml`.
  Elegido tras barrido de mercado (33 categorías), 4 deep-dives y validación
  con YouTube Data API (0 big-fish, demanda demostrada).
- **Nicho original descartado**: US-Hispanic finanzas/ITIN (los docs 01-07 se
  escribieron para esa tesis). La **metodología** de los docs sigue vigente;
  sus conclusiones de nicho concretas NO.
- **Filosofía anti-purga**: YouTube penaliza contenido 100% IA sin
  intervención humana. Este pipeline automatiza lo repetitivo (guion → audio
  → packaging) y deja como manual obligatorio el screencast real, el montaje
  y la revisión humana. NO convertir esto en generación de video 100%
  automática.
- **Formato del canal**: faceless total (sin cara ni voz del usuario).
  Screencast de n8n/Make + voz ElevenLabs.

## Contexto técnico

- **Lenguaje**: Python 3.11+ · pip + `pyproject.toml` (setuptools)
- **Layout**: `src/yt_auto/` + `tests/` + `docs/` + `assets/niche_profiles/`
- **Configuración**: `pydantic-settings` cargando `.env`
- **CLI**: `typer` con entry point `yt-auto` (o `python -m yt_auto.cli`)
- **Calidad**: `ruff` (lint), `mypy`, `pytest` (139+ tests, sin red real)

## Convenciones de código

- Funciones puras siempre que sea posible; side effects en adaptadores
  (`*/client.py`, testeables con `httpx.MockTransport`).
- Type hints obligatorios en toda función pública.
- Tests con `pytest`, sin red real (mockear clientes externos).
- Llamadas HTTP externas con retry `tenacity` (429/5xx, backoff exponencial).

## Mapeo módulo → propósito

| Módulo | Propósito | Doc de referencia |
|--------|-----------|-------------------|
| `niche/` | prompts/ingest de auditorías de nicho | doc 01 (metodología) |
| `scripts/` | guiones (ScriptReport, hooks, loops) | doc 02 |
| `audio/` | plan de locución + síntesis ElevenLabs (API real) | doc 03 |
| `visuals/` | plan visual, prompts | doc 04 |
| `editing/` | timeline, subtítulos, DAI anchors | doc 05 |
| `publishing/` | metadata, capítulos, checklist + perfiles de nicho YAML | doc 06 |
| `analytics/` | retention parser, prompts Ask Studio | doc 07 |
| `compliance/` | disclosure IA, citas obligatorias, log de edición humana | anti-purga 2026 |
| `monetization/` | catálogo afiliados, UTMs, bloque Recursos | — |
| `competitive/` | YouTube Data API v3: scan de nichos, outliers | — |
| `pipeline/` | orquestador (VideoProject + qué es automático vs manual) | — |

## Modelos por defecto

- **Claude Sonnet 4.6** (`claude-sonnet-4-6`): ideación, primeras versiones.
- **Claude Opus 4.7** (`claude-opus-4-7`): auditoría profunda, supervisión.
- **Gemini 2.5 Pro**: investigación profunda, Ask Studio.
- **ElevenLabs `eleven_v3`**: default actual (`config.py`). ⚠ La afirmación
  "v3 GA feb-2026, +68% precisión" procede de investigación de agentes y NO
  está verificada contra fuente primaria — verificar en elevenlabs.io antes
  de citarla en contenido público. Nunca usar Turbo para narración >10 min.

## Reglas que Claude NUNCA debe romper

1. No publicar contenido sin un paso de edición humana documentado
   (`compliance.HumanReviewLog`).
2. No commitear `.env`, `client_secret.json`, `token.json` ni binarios
   pesados. No pegar API keys en chat.
3. No subir audio/video a servicios públicos sin autorización explícita.
4. No tocar la rama `main`. Trabajar sobre
   `claude/setup-dev-environment-Qa16G` u otra rama de feature.
5. No apelar desmonetizaciones de forma automatizada.
6. **No incluir datos/estadísticas en guiones sin verificar contra fuente
   primaria** (skill `fact-check-datos`). Caso real: el dato "78% contrata
   al primero que responde" resultó ser un matiz incorrecto del NAR y hubo
   que corregirlo antes de producir.
7. No automatizar el screencast ni eliminar la revisión humana: ese 30%
   manual es el foso contra la purga anti-AI-Slop.

## Datos del repo que son ESTIMACIONES (no verdades verificadas)

- CPAs y URL-templates de `monetization/catalog.py`: investigación de
  agentes; las plantillas de URL son **placeholders inventados** — los links
  reales los da el dashboard de cada programa al registrarse.
- Tablas RPM en docs y skills: rangos de blogs del sector (OutlierKit,
  FluxNote…), no de YouTube oficial.
- Proyecciones de ingresos (€1.5-3K/mes a mes 6): estimaciones de escenario,
  no promesas.

## Flujos típicos

- **Nuevo video**: `yt-auto pipeline run "<tema>"` → crea proyecto y dice
  qué es automático y qué manual.
- **Validar un nicho/tema**: `yt-auto competitive scan --query "..."`
  (requiere `YOUTUBE_API_KEY`; ~101 unidades de cuota por scan).
- **Audio**: `yt-auto audio plan <script.json>` → `yt-auto audio synth
  <plan.json>` (requiere `ELEVENLABS_API_KEY`).
- **Probar el entorno**: `yt-auto info` · **Instalar**: `pip install -e ".[dev]"`.
- **Tests**: `python -m pytest -q` · **Lint**: `ruff check src/ tests/`.
