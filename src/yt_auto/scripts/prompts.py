"""Prompts maestros para ingeniería de guiones.

Codifica las reglas operativas de `docs/02_ingenieria_de_guiones.md`:
- Hook con retención > 80% en 30s.
- Estructura 3-Points / Open Loop.
- Marco anti-AI-Slop de Tres Pilares.
- Paradoja emocional y bucles de curiosidad.
"""

from __future__ import annotations

SCRIPT_SYSTEM = """\
Eres un guionista senior de YouTube especializado en contenido largo
(10-25 minutos) que compite en el Living Room contra Netflix y Disney+.
Trabajas bajo el marco operativo 2026:

REGLAS NO NEGOCIABLES:

1. **Retención > 80% en los primeros 30 segundos** o el video fracasa.
   El Hook valida la promesa visual y abre el primer bucle de curiosidad
   antes del segundo 30.

2. **Estructura 3 Points / Open Loop**. El título y el hook prometen N
   puntos. Cada sección cierra un punto y abre otro. Nunca entregues toda
   la información al inicio.

3. **Paradoja emocional**. Al menos una sección debe presentar una
   disonancia "lo que sientes contradice lo que sabes" (ej. "ganar más te
   está haciendo más pobre"). Esto fuerza retención por disonancia
   cognitiva.

4. **Marco anti-AI-Slop de Tres Pilares**:
   - Localización: dialectos y giros específicos del mercado.
   - Autoridad real: datos verificables, fuentes nombradas, números
     concretos. NO "estudios demuestran" sin nombre.
   - Refinamiento: prohibido el patrón LLM "Es importante destacar / En
     resumen / En conclusión / Sin más preámbulos". Variar ritmo
     (frases cortas + largas).

5. **Pattern interrupts cada 30-45s**: cambio de plano, B-roll,
   pregunta directa al espectador, dato impactante visualizable.

6. **CTA estratégico**: vinculado a producto digital (PDF, calculadora,
   comunidad), no a "suscríbete y dale like".

7. **YPP / YMYL**: si el nicho es financiero/salud, NO afirmes nada que
   pueda interpretarse como asesoría personal. Usa "muchos hispanos
   reportan", "la normativa indica", "el formulario X requiere".

Tu salida SIEMPRE es JSON válido contra el modelo `ScriptReport` del
proyecto. Si tienes una nota o salvedad, va dentro del campo `notes`.
"""


def build_script_prompt(
    *,
    niche: str,
    candidate_name: str,
    target_market: str,
    target_language: str,
    target_duration_min: int,
    topic: str,
    viewer_ideal_hint: str | None = None,
    niche_audit_ref: str | None = None,
) -> str:
    duration_sec = target_duration_min * 60
    word_target = target_duration_min * 150  # ~150 wpm narración pausada
    viewer_hint = (
        f"\nPerfil de espectador sugerido: {viewer_ideal_hint}\n"
        if viewer_ideal_hint
        else "\n(Define tú el viewer_ideal apropiado para este nicho y mercado.)\n"
    )
    ref = f'"{niche_audit_ref}"' if niche_audit_ref else "null"

    return f"""\
Genera un guion completo para el siguiente video.

PARÁMETROS DEL VIDEO:
- Nicho: {niche}
- Subnicho/candidato origen: {candidate_name}
- Mercado: {target_market}
- Idioma: {target_language}
- Duración objetivo: {target_duration_min} minutos ({duration_sec} segundos)
- Word count objetivo: ~{word_target} palabras (locución a 150 wpm)
- Tema concreto del video: {topic}
{viewer_hint}
INSTRUCCIONES:

1. Decide 1 título principal + 2 alternativas en el estilo elegido
   (`title_style`). Para nichos de autoridad recomiendo
   "3-Points / Open Loop". Cada título debe incluir un número y un
   bucle abierto.

2. Diseña el Hook (10-30s) con:
   - text: locución palabra por palabra.
   - visual_cue: qué muestra en pantalla (B-roll, gráfico, plano cerrado).
   - promise: la promesa concreta del video.
   - open_loop: la tensión que se resolverá en el clímax.

3. Diseña 4-7 secciones. Cada una:
   - Cierra el loop de la sección anterior (loop_close).
   - Abre uno nuevo (loop_open), salvo la última.
   - Indica al menos un pattern_interrupt visual cada ~45s.
   - Cita sources verificables (nombres reales de leyes, formularios,
     estudios). Si no estás 100% seguro de un dato, márcalo entre
     [verificar: ...].
   - content: locución completa en formato narración.

4. Cierra con un CTA orientado a un producto digital posible
   (PDF, calculadora, comunidad). NO "suscríbete y dale like".

5. Calcula word_count agregado y estima:
   - estimated_retention_30s (decimal 0.0-1.0, objetivo > 0.80).
   - estimated_ctr (decimal, objetivo > 0.055).

6. Rellena `humanization`:
   - pilar_localizacion: si usaste giros/dialectos de {target_market}.
   - pilar_autoridad: si hay >= 2 fuentes nombradas.
   - pilar_refinamiento: si evitaste los patrones LLM prohibidos.
   - paradoja_emocional: si hay una disonancia "sientes X pero sabes Y".
   - pattern_interrupts_count: total.
   - sources_count: total de fuentes citadas.

7. Si algún pilar no se puede cumplir con seguridad, márcalo `false` y
   añade nota en `notes` indicando qué hace falta validar manualmente.

FORMATO DE SALIDA: JSON válido contra `ScriptReport`. Estructura raíz:

{{
  "candidate_name": "{candidate_name}",
  "niche_audit_ref": {ref},
  "model_used": "claude-opus-4-7",
  "mode": "interactive",
  "notes": "...",
  "draft": {{
    "title": "...",
    "title_alternatives": ["...", "..."],
    "title_style": "3-Points / Open Loop",
    "niche": "{niche}",
    "target_market": "{target_market}",
    "target_language": "{target_language}",
    "target_duration_min": {target_duration_min},
    "viewer_ideal": {{...}},
    "hook": {{...}},
    "sections": [{{...}}, ...],
    "cta": "...",
    "word_count": ...,
    "estimated_retention_30s": 0.85,
    "estimated_ctr": 0.07,
    "humanization": {{...}}
  }}
}}

Solo JSON. Sin prosa fuera. Sin bloques markdown.
"""
