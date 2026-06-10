# Youtube Automatizado · Pipeline de producción asistida

Pipeline en Python para producir un canal de YouTube **faceless** (voz IA +
screencast) con el máximo de automatización **sin cruzar la línea que YouTube
penaliza** (contenido 100% IA sin intervención humana). Automatiza guion →
audio → packaging → tracking; deja como manual el screencast, el montaje y la
revisión humana.

> **Nicho activo**: *Automatización IA para inmobiliarias*
> (`assets/niche_profiles/automatizacion_ia_inmobiliaria.yaml`), elegido tras
> barrido de mercado de 33 categorías + validación con YouTube Data API.
> Ver `CLAUDE.md` § "Estado estratégico actual".

## Qué hace hoy (funcional, 139+ tests)

| Comando | Función |
|---------|---------|
| `yt-auto info` | Estado del entorno y APIs configuradas |
| `yt-auto pipeline run "<tema>"` | Crea un VideoProject y separa etapas automáticas vs manuales |
| `yt-auto pipeline status [id]` | Estado de un proyecto |
| `yt-auto competitive scan --query "..."` | Top canales reales de un nicho (YouTube Data API v3) |
| `yt-auto competitive outliers <channel_id>` | Videos outlier de un canal (≥3x mediana) |
| `yt-auto script prompt/ingest` | Prompt maestro de guion + parseo de respuesta |
| `yt-auto audio plan <script.json>` | Plan de locución por bloques |
| `yt-auto audio synth <plan.json>` | Síntesis real con ElevenLabs (retry, cuota, idempotente) |
| `yt-auto audio voices --remote` | Voces de tu cuenta ElevenLabs |
| `yt-auto editing plan` / `publish prep` | Timeline + metadata YouTube con afiliados/UTMs |
| `yt-auto analytics retention` | Detección de retention leaks desde CSV |

## Módulos

```
src/yt_auto/
├── niche/         # 1. auditorías de nicho (prompts + ingest)
├── scripts/       # 2. guiones (ScriptReport, hooks, loops)
├── audio/         # 3. locución ElevenLabs (cliente httpx real + plan)
├── visuals/       # 4. plan visual
├── editing/       # 5. timeline, subtítulos, DAI anchors
├── publishing/    # 6. metadata + perfiles de nicho YAML + checklist
├── analytics/     # 7. retention parser + Ask Studio
├── compliance/    # disclosure IA, citas obligatorias, log edición humana
├── monetization/  # catálogo afiliados, UTMs, bloque Recursos
├── competitive/   # YouTube Data API v3 (scan, outliers, cuota)
└── pipeline/      # orquestador: VideoProject + automático vs manual
```

## Puesta en marcha

```bash
git checkout claude/setup-dev-environment-Qa16G
pip install -e ".[dev]"
cp .env.example .env   # rellenar ELEVENLABS_API_KEY, YOUTUBE_API_KEY, etc.
yt-auto info
python -m pytest -q    # 139+ tests, sin red real
```

## Artefactos del primer video (piloto 01)

- Guion (datos verificados NAR/HBR/MIT): `docs/scripts-archive/piloto-01-*`
- Packaging (descripción + thumbnail brief): `docs/publishing-archive/piloto-01-packaging.md`
- Lead magnet (workflow n8n importable): `assets/lead_magnets/inmobiliaria_lead_agent_n8n.json`
- Plan editorial y runbook: `docs/plan_editorial_mes_01.md`, `docs/runbook_produccion_video01.md`

## Reglas operativas críticas

- **Anti AI-Slop**: nada se publica sin edición humana documentada
  (`compliance.HumanReviewLog`) y sin pasar la skill `anti-ai-slop`.
- **Fact-check**: todo dato/estadística de un guion se verifica contra fuente
  primaria antes de producir (skill `fact-check-datos`).
- **Disclosure IA**: declarar contenido sintético en YouTube Studio siempre.
- **Estimaciones ≠ hechos**: los CPAs del catálogo de afiliados y las tablas
  RPM son investigación de agentes, no contratos verificados (ver CLAUDE.md).

## Licencia

Proyecto propietario. Uso interno.
