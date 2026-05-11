"""Etapa 4 - Generación visual dinámica y consistencia de personajes.

Ver: docs/04_generacion_visual.md

Componentes previstos:
    - build_reference_sheet(character)  -> frontal / lateral / trasera / 3/4
    - build_storyboard_3x3(script)      -> 9 celdas (plano, luz, ambiente, acción)
    - generate_image(prompt_json)       -> Nano Banana con JSON master prompt
    - animate_clip(image, motion)       -> Seedance 2.0 multi-reference, 15s / 720p / 16:9
    - inpaint_fix(frame, artifact)      -> corrección de manos / drift
    - interpolate_frames(clip)          -> Filmora frame interpolation

Estándar fotorealista: piel porosa, micro-textura, lente cinematográfico, no plástico.
"""
