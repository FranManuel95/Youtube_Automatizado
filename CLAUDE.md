# Guía operativa para Claude Code

Este repo implementa el pipeline de automatización de YouTube descrito en los
informes estratégicos de `/docs`. Lee siempre los documentos de `/docs` antes
de tomar decisiones de producto: contienen las decisiones de negocio y los
límites operativos (anti-AI-Slop, MLA, RPM por mercado, etc.).

## Contexto del proyecto

- **Lenguaje**: Python 3.11+
- **Gestor de paquetes**: pip + `pyproject.toml` (setuptools)
- **Layout**: `src/yt_auto/` (paquete) + `tests/` + `docs/`
- **Configuración**: `pydantic-settings` cargando `.env`
- **CLI**: `typer` con entry point `yt-auto`
- **Calidad**: `ruff` (lint + format), `mypy`, `pytest`

## Convenciones de código

- Funciones puras siempre que sea posible; side effects aislados en
  adaptadores (`*/client.py`).
- Type hints obligatorios en toda función pública.
- Imports ordenados por `ruff`/`isort`.
- Sin comentarios redundantes; los `__init__.py` de cada etapa documentan el
  contrato pendiente.
- Tests con `pytest`, sin red real (mockear clientes externos).

## Mapeo etapa → documento estratégico

| Módulo | Documento de referencia |
|--------|--------------------------|
| `niche/` | *Estrategia Avanzada de Selección de Nichos Rentables* |
| `scripts/` | *Ingeniería de Guiones para Máxima Retención y Viralidad* |
| `audio/` | *Producción de Audio y Locución con IA* |
| `visuals/` | *Generación Visual Dinámica y Consistencia de Personajes* |
| `editing/` | *Edición Dinámica y Packaging de Alto Impacto* |
| `publishing/` | *Gestión, Seguridad y Escalado del Negocio* |
| `analytics/` | *Guía Técnica: Automatización Avanzada* (sección Ask Studio) |

## Modelos por defecto

- **Claude Sonnet 4.6** (`claude-sonnet-4-6`): ideación, mapeo de subnichos,
  hooks, primeras versiones de guion.
- **Claude Opus 4.7** (`claude-opus-4-7`): auditoría profunda con visión,
  análisis de miniaturas competidoras, supervisión de coherencia.
- **Gemini 2.5 Pro**: investigación profunda, Ask Studio, Inspiration Tab.
- **ElevenLabs `eleven_multilingual_v2`**: locución de autoridad de largo
  formato. Nunca usar Turbo para narraciones >10 min.

## Reglas que Claude NUNCA debe romper

1. No publicar contenido sin un paso de edición humana documentado (sello
   anti-AI-Slop).
2. No commitear `.env`, `client_secret.json`, `token.json` ni assets binarios
   pesados.
3. No subir audio/video a servicios públicos sin autorización explícita del
   usuario (Likeness Detection, derechos de imagen).
4. No tocar la rama `main`. Trabajar siempre sobre
   `claude/setup-dev-environment-Qa16G` u otra rama de feature.
5. No apelar desmonetizaciones de forma automatizada.

## Flujos típicos

- **Añadir una función a una etapa**: tocar el módulo correspondiente en
  `src/yt_auto/<etapa>/`, añadir test en `tests/`, ejecutar `ruff check` y
  `pytest`.
- **Probar el entorno**: `yt-auto info`.
- **Instalar deps en dev**: `pip install -e ".[dev]"`.
