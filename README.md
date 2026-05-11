# Youtube Automatizado · Pipeline IA 2026

Sistema de **automatización avanzada de canales de YouTube** basado en la
estrategia 2026 documentada en `/docs`. El objetivo no es generar videos
sueltos, sino construir **propiedades digitales** rentables, diversificadas y
resilientes frente a los filtros anti "AI Slop" de la plataforma.

## Objetivos estratégicos (resumen de los 7 informes)

1. **Selección de nicho** con framework de las 4 S (Streaming, Searching,
   Shopping, Scrolling) y detección de *outliers* y *gaps*.
2. **Ingeniería de guiones** con hooks "3 Points / Open Loop", bucles de
   curiosidad y paradoja emocional. Retención objetivo > 80% a los 30s.
3. **Audio cinematográfico** con ElevenLabs *Multilingual v2* y *Expressive
   Speech*; doblaje multi-idioma orientado al mercado US-Hispanic (RPM x4).
4. **Visuales consistentes** con Nano Banana + Seedance 2.0, *Reference
   Sheets*, *Storyboard 3x3* y prompts JSON para forzar fotorrealismo.
5. **Edición de alto CTR** con regla de 3 segundos, miniaturas 4K y *pattern
   interrupts*. Competimos en el Living Room contra Netflix.
6. **Escalado y seguridad**: red de 5-10 canales (5×$500 > 1×$2500), MLA,
   Back Catalog con Dynamic Ad Insertion, protocolo de apelación 24h.
7. **Auditoría continua** con Ask Studio e Inspiration Tab.

## Stack técnico

| Capa | Herramienta |
|------|-------------|
| Ideación / Auditoría | Claude Sonnet 4.6 + Claude Opus 4.7 (Vision) |
| Investigación profunda | Google Gemini Deep Research, NotebookLM |
| Locución | ElevenLabs `eleven_multilingual_v2` |
| Imagen | Nano Banana (prompt JSON) |
| Video | Seedance 2.0 (multi-reference, 720p / 15s clips) |
| Edición | CapCut / Filmora (manual sobre clips IA) |
| Publicación | YouTube Data API v3 + Multi-language Audio |

## Estructura del repositorio

```
.
├── src/yt_auto/        # paquete Python con módulos por etapa
│   ├── niche/          # 1. selección de nicho
│   ├── scripts/        # 2. guiones
│   ├── audio/          # 3. locución
│   ├── visuals/        # 4. imagen + video
│   ├── editing/        # 5. montaje + packaging
│   ├── publishing/     # 6. subida + MLA
│   ├── analytics/      # 7. auditoría
│   ├── config.py       # carga de .env via pydantic-settings
│   └── cli.py          # CLI `yt-auto`
├── assets/             # reference sheets, storyboards, outfits (git-ignored)
├── output/             # audio, visuales y videos generados (git-ignored)
├── docs/               # informes estratégicos en texto plano
├── tests/              # tests con pytest
├── notebooks/          # exploración
├── pyproject.toml
├── .env.example
└── CLAUDE.md           # guía operativa para Claude Code
```

## Puesta en marcha

```bash
# 1. Clonar y entrar al repo
git checkout claude/setup-dev-environment-Qa16G

# 2. Crear entorno virtual e instalar
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# 3. Configurar credenciales
cp .env.example .env
# editar .env con tus claves de Anthropic / Gemini / ElevenLabs / YouTube

# 4. Verificar el entorno
yt-auto info
```

## Comandos del CLI

```bash
yt-auto info                              # estado del entorno
yt-auto niche "neurodivergencia adultos"  # investigar nicho (stub)
yt-auto script "tema" --duration-min 12   # generar guion (stub)
yt-auto audio path/guion.md               # sintetizar locución (stub)
yt-auto visuals path/storyboard.json      # renderizar visuales (stub)
yt-auto publish path/video.mp4            # subir a YouTube (stub)
```

> Estado actual: **scaffold**. Los comandos imprimen `TODO`. La lógica se
> implementará iterativamente respetando la documentación de `/docs`.

## Reglas operativas críticas

- **Anti AI-Slop**: ningún guion se publica sin edición humana. Cada release
  debe pasar el *Marco de Tres Pilares para la Humanización* (dialectos,
  autoridad real, refinamiento manual).
- **Likeness Detection**: declarar el uso de IA y evitar deepfakes de marcas
  o personas reales sin autorización.
- **Apelaciones**: protocolo de 24h, nunca apelar en caliente.
- **Diversificación**: el portafolio debe poder perder un canal sin colapsar.

## Licencia

Proyecto propietario. Uso interno del equipo.
