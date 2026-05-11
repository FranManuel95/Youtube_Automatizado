"""Presets JSON base del informe `docs/04_generacion_visual.md`.

Estos diccionarios son los "Prompt Maestros" que fuerzan el realismo
fotográfico y la consistencia de Nano Banana / Seedance 2.0. Sirven
como BASE: el LLM rellena los huecos específicos de cada shot.
"""

from __future__ import annotations

from typing import Any

# Esquema base de realismo fotográfico (Nano Banana). Fuerza
# imperfecciones naturales y rompe el "look plástico" típico de IA.
NANO_BANANA_REALISM_BASE: dict[str, Any] = {
    "camera": "Sony A7R IV, 85mm lens",
    "f_stop": "f/1.8",
    "iso": 400,
    "lighting": "Cinematic soft lighting, 4k resolution",
    "skin_details": (
        "visible pores, natural skin texture, slight imperfections, "
        "subsurface scattering, no plastic look"
    ),
    "post_processing": "color graded, high dynamic range, subtle film grain",
    "render_engine": "nano_banana_sampling",
}

# Esquema de consistencia de personaje (a sumar al base por cada vista).
SUBJECT_CONSISTENCY_BASE: dict[str, Any] = {
    "subject_consistency": {
        "facial_features": "fixed",
        "skin_texture": "porous_natural",
        "imperfections": ["freckles", "micro-creases", "subsurface_scattering"],
    }
}

# Esquema base de animación Seedance 2.0 (clip 15s, 720p, 16:9).
SEEDANCE_CLIP_BASE: dict[str, Any] = {
    "resolution": "720p",
    "aspect_ratio": "16:9",
    "duration_sec": 15,
    "fps": 24,
    "motion_intensity": "medium",
    "frame_interpolation": True,
}

# Base de miniatura 4K Living Room.
THUMBNAIL_4K_BASE: dict[str, Any] = {
    "resolution": "3840x2160",
    "aspect_ratio": "16:9",
    "composition": "rule of thirds, subject on left third, negative space on right for text",
    "lighting": "Cinematic soft lighting, dramatic contrast",
    "skin_details": (
        "visible pores, natural skin texture, slight imperfections, "
        "subsurface scattering, no plastic look"
    ),
    "background": "minimal, single tone, complementary to subject",
    "post_processing": "color graded, high dynamic range",
}


def merge_nano_banana_base(extra: dict[str, Any]) -> dict[str, Any]:
    """Combina la base realista con la especificación concreta de un shot."""
    out: dict[str, Any] = {**NANO_BANANA_REALISM_BASE, **SUBJECT_CONSISTENCY_BASE}
    out.update(extra)
    return out


def merge_seedance_base(extra: dict[str, Any]) -> dict[str, Any]:
    return {**SEEDANCE_CLIP_BASE, **extra}


def merge_thumbnail_base(extra: dict[str, Any]) -> dict[str, Any]:
    return {**THUMBNAIL_4K_BASE, **extra}
