"""Prompts maestros para que Claude diseñe el plan visual a partir del guion.

Codifica las reglas del informe `docs/04_generacion_visual.md`:
- Reference Sheet con 4 vistas obligatorias.
- Realismo fotográfico (no plástico).
- Pattern interrupts cada 30-45s.
- Miniatura 4K con regla de 3 elementos.
"""

from __future__ import annotations

import json

from yt_auto.scripts.models import ScriptReport
from yt_auto.visuals.presets import (
    NANO_BANANA_REALISM_BASE,
    SEEDANCE_CLIP_BASE,
    SUBJECT_CONSISTENCY_BASE,
    THUMBNAIL_4K_BASE,
)

VISUALS_SYSTEM = """\
Eres el director de arte de un canal automatizado de YouTube que compite
en el Living Room contra Netflix. Trabajas con Nano Banana (imagen) y
Seedance 2.0 (animación) bajo el estándar 2026:

REGLAS NO NEGOCIABLES:

1. **Realismo fotográfico**. Nunca produces piel "perfecta y plástica".
   Imperfecciones naturales: poros, micro-arrugas, subsurface scattering.
   Lente cinematográfico (35-85mm, f/1.8), iluminación tipo Rembrandt o
   soft cinematic.

2. **Consistencia de personaje** vía Reference Sheet. Mínimo 4 vistas:
   frontal, perfil, 3/4 y trasera. Rasgos físicos FIJOS, replicados
   palabra por palabra en cada prompt.

3. **Storyboard mapeado al guion**. Cada sección del guion recibe 2-4
   shots. Mezcla planos cerrados (autoridad) con planos contextuales
   (gravitas cinematográfica). Cada plano dura entre 3 y 15 segundos.

4. **Pattern Interrupts** declarados: al menos 1 por sección. Pueden ser
   cambios bruscos de plano, B-roll inesperado, cifras gigantes en
   pantalla, glitches, cambios cromáticos.

5. **Seedance 2.0**: clips de máximo 15 segundos, 720p, 16:9, fps 24.
   Si una sección requiere más de 15s, divide en sub-shots.

6. **Miniatura 4K (3840x2160)**: regla de 3 elementos (cara + objeto +
   máximo 3 palabras), pattern interrupt cromático (saco rojo o
   minimalismo si el nicho está saturado de diseños barrocos), texto
   nunca repite el título.

7. **Anti AI-Slop visual**: prohibido el "look plástico". Cada prompt
   JSON debe incluir explícitamente el bloque `skin_details` con poros
   y micro-imperfecciones.

Tu salida SIEMPRE es JSON válido contra el modelo `VisualReport` del
proyecto. Sin prosa fuera del JSON.
"""


def _bases_block() -> str:
    return (
        "Bases obligatorias (debes incluirlas y EXTENDERLAS, no eliminarlas):\n\n"
        "NANO_BANANA_REALISM_BASE:\n```json\n"
        + json.dumps(NANO_BANANA_REALISM_BASE, indent=2, ensure_ascii=False)
        + "\n```\n\nSUBJECT_CONSISTENCY_BASE:\n```json\n"
        + json.dumps(SUBJECT_CONSISTENCY_BASE, indent=2, ensure_ascii=False)
        + "\n```\n\nSEEDANCE_CLIP_BASE:\n```json\n"
        + json.dumps(SEEDANCE_CLIP_BASE, indent=2, ensure_ascii=False)
        + "\n```\n\nTHUMBNAIL_4K_BASE:\n```json\n"
        + json.dumps(THUMBNAIL_4K_BASE, indent=2, ensure_ascii=False)
        + "\n```"
    )


def build_visuals_prompt(report: ScriptReport, *, script_ref: str) -> str:
    """Construye el prompt usuario para Claude a partir de un guion."""
    d = report.draft
    sections_summary = "\n".join(
        f"  - {i + 1}. {sec.heading} ({sec.duration_sec}s)" for i, sec in enumerate(d.sections)
    )

    return f"""\
Diseña el plan visual completo (Reference Sheet del personaje + shots +
miniatura) para el siguiente guion.

GUION ORIGEN:
- Path: {script_ref}
- Título: {d.title}
- Nicho: {d.niche}
- Mercado: {d.target_market} / Idioma: {d.target_language}
- Duración total: {d.target_duration_min} min ({d.total_duration_sec}s reales)

VIEWER IDEAL:
- {d.viewer_ideal.nombre}, {d.viewer_ideal.edad}, {d.viewer_ideal.ubicacion}
- Situación: {d.viewer_ideal.situacion}
- Dolor: {d.viewer_ideal.dolor}

ESTRUCTURA NARRATIVA:
- Hook: {d.hook.duration_sec}s · visual_cue: {d.hook.visual_cue}
- Secciones:
{sections_summary}
- CTA: {len(d.cta)} caracteres

INSTRUCCIONES:

1. Define `character` con un narrador consistente para todo el video.
   - physical_features: rasgos FIJOS replicables (cara, ojos, pelo,
     complexión, marcas distintivas).
   - outfit_base: vestimenta concreta (color, prenda, estilo).
   - accent_notes: si el personaje es hispano US, especifica matiz
     cultural (mexicano, caribeño, sudamericano) para coherencia visual.
   - views: mínimo {{frontal, profile_left, three_quarter}}, deseable
     incluir back también. Cada vista es un PROMPT JSON COMPLETO que
     extiende NANO_BANANA_REALISM_BASE + SUBJECT_CONSISTENCY_BASE.

2. Diseña `shots`: 2-4 por sección + 1-2 para el hook + 1 para el CTA.
   Total esperado: 15-25 shots para un video de {d.target_duration_min} min.

   Por cada shot:
   - shot_id correlativo.
   - related_block: "hook", "section_1", "section_2", ..., "cta".
   - timecode_start_sec: dónde arranca en la línea de tiempo total.
   - duration_sec: entre 3 y 15.
   - shot_type: del enum (closeup, medium, wide, broll, insert, etc.).
   - description, motion, lighting, ambient.
   - nano_banana_prompt_json: extiende NANO_BANANA_REALISM_BASE +
     SUBJECT_CONSISTENCY_BASE con la composición específica.
   - seedance_prompt_json: extiende SEEDANCE_CLIP_BASE con motion vector.
   - pattern_interrupt: true si ese shot es un quiebro declarado.

   Mínimo 1 pattern_interrupt por sección. Para el guion de finanzas,
   ideas: cifras gigantes animadas, formularios oficiales en B-roll,
   comparativas split-screen rojo/verde, planos cerrados de manos
   firmando, gráficos de FICO score animados.

3. Diseña `thumbnail`:
   - title_overlay: MÁXIMO 3 PALABRAS, no repite el título principal.
   - face_element: expresión emocional clara (sorpresa, intriga, autoridad).
   - object_element: 1 objeto disruptivo que simbolice el tema (tarjeta
     de crédito partida, formulario W-7, llave, etc.).
   - pattern_interrupt_strategy: cómo rompe el estilo del nicho.
   - color_strategy: paleta + 'saco rojo' (dónde está el contraste).
   - nano_banana_prompt_json: extiende THUMBNAIL_4K_BASE con la
     composición específica.

4. notes: cualquier salvedad o decisión que merezca discusión humana.

{_bases_block()}

FORMATO DE SALIDA: JSON válido. Sin texto fuera. Estructura raíz:

{{
  "script_ref": "{script_ref}",
  "script_title": "{d.title}",
  "model_used": "claude-opus-4-7",
  "mode": "interactive",
  "notes": "...",
  "character": {{...}},
  "shots": [{{...}}, ...],
  "thumbnail": {{...}}
}}
"""
