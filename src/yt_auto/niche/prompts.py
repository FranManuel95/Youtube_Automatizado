"""Plantillas de prompts para la etapa de selección de nicho.

Los prompts están diseñados para Claude Opus 4.7 (auditoría profunda) y
Claude Sonnet 4.6 (ideación masiva). Reflejan literalmente las reglas
operativas del informe `docs/01_seleccion_de_nichos.md`.
"""

from __future__ import annotations

EXPLORATION_SYSTEM = """\
Eres un estratega senior de YouTube especializado en construir "Propiedades
Digitales" rentables y resilientes en el ecosistema 2026. Trabajas con el
marco operativo definido en los informes internos de la empresa:

REGLAS OPERATIVAS NO NEGOCIABLES:
1. Framework 4 S: cada nicho debe encajar en al menos 2 de Streaming,
   Searching, Shopping, Scrolling. Si solo encaja en Scrolling, es de
   bajo valor.
2. Tres pilares del nicho rentable: demanda constante, utilidad real para
   el espectador, alto valor publicitario (categoría apetecible).
3. RPM por mercado (USD/1k impresiones):
   - Tier 1 (US, CH, NO, AU, CA): $15-40
   - Tier 1.5 (US-Hispanic): $10-25
   - Tier 2 (ES): $3-10
   - Tier 3 (LATAM): $0.50-2
4. El mercado US-Hispanic da hasta 4x el RPM de LATAM nativo. Prioriza
   subnichos donde el público hispano residente en EE.UU. tiene poder
   adquisitivo y acceso a crédito.
5. Detecta gaps reales: nichos con demanda confirmada pero oferta de baja
   calidad o canales grandes inactivos. NO propongas mercados saturados
   con dominantes activos a menos que tengas un ángulo de "Niche Bending"
   claro.
6. Niche Bending: fusión de un patrón viral de un vertical con otro
   subnicho emergente (ej. Documentales Esotéricos + Psicología Moderna
   -> Numerología y Sistemas Simbólicos).
7. Anti AI-Slop: descarta nichos donde la producción 100% automatizada
   sin valor humano es la norma; YouTube hunde ese alcance.

Tu salida será JSON estricto, validable con los modelos Pydantic del
proyecto.
"""


def build_exploration_prompt(
    *,
    market: str,
    language: str,
    content_format: str,
    target_duration_min: int,
    target_count: int = 10,
    vertical_filter: str | None = None,
) -> str:
    vertical_section = (
        f"\nVERTICAL OBLIGATORIO: {vertical_filter}. "
        f"Todos los subnichos deben estar dentro de este paraguas temático.\n"
        if vertical_filter
        else "\nVERTICAL: abierto. Explora libremente entre verticales rentables.\n"
    )
    return f"""\
Tarea: identificar {target_count} subnichos candidatos para crear un canal
automatizado nuevo bajo los siguientes parámetros.

PARÁMETROS DEL CANAL:
- Mercado primario: {market}
- Idioma de producción: {language}
- Formato: {content_format} ({target_duration_min} minutos objetivo)
{vertical_section}
INSTRUCCIONES:

1. Genera {target_count} subnichos diferenciados. NO repitas verticales.
2. Para cada subnicho aplica el framework 4S y descártalo internamente si
   solo encaja en Scrolling.
3. Para cada uno entrega:
   - name: nombre operativo corto.
   - headline: pitch de una línea para el canal.
   - description: 2-4 frases con el ángulo concreto.
   - target_market: "{market}".
   - target_language: "{language}".
   - four_s: lista de las S aplicables (mínimo 2).
   - rpm: {{market, tier, rpm_min_usd, rpm_max_usd}} con tier de la tabla.
   - demand_evidence: 2-4 evidencias (canales reales o tendencias
     reconocibles - si no estás seguro, márcalo como hipótesis a validar).
   - gap_hypothesis: el hueco concreto que justifica el nicho hoy.
   - competition_level: "bajo" | "medio" | "alto" | "saturado".
   - niche_bending_angle: si propones una fusión, descríbela; si no, null.
   - sample_titles: 3 títulos en formato "3 Points/Open Loop"
     (Ej: "La psicología del silencio: por qué los genios callan 3 razones críticas").
   - risks: 2-4 riesgos honestos (saturación, sensibilidad de YouTube,
     RPM volátil, dependencia de personajes, etc.).
   - score: 1-10 sobre rentabilidad esperada considerando todos los
     factores anteriores.
   - rationale: 1-2 frases justificando el score.

4. Tras la lista, añade un objeto "methodology_notes" con:
   - Tu nivel de confianza global.
   - Qué subnichos requieren validación urgente con datos externos
     (Inspiration Tab, Ask Studio, búsqueda manual).
   - 2-3 verticales que descartaste y por qué.

FORMATO DE SALIDA: JSON válido siguiendo este esquema raíz:

{{
  "market_focus": "{market}",
  "content_format": "{content_format}",
  "target_count": {target_count},
  "vertical_filter": {f'"{vertical_filter}"' if vertical_filter else "null"},
  "methodology_notes": "...",
  "candidates": [ {{...}}, ... ]
}}

No incluyas comentarios, prosa fuera del JSON ni código markdown. Solo el
JSON. Si tienes que hacer una aclaración, mételo dentro de
"methodology_notes".
"""
