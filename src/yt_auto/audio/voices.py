"""Catálogo curado de voces ElevenLabs por mercado y rol.

Los `voice_id` reales no se hardcodean (varían por cuenta y cambian con
el catálogo). Cada preset es una recomendación de perfil; el usuario
escoge la voz concreta en el panel web de ElevenLabs y la fija en
`.env` con `ELEVENLABS_VOICE_ID`.
"""

from __future__ import annotations

from yt_auto.audio.models import VoicePreset, VoiceSettings

# Settings base para narración de autoridad (10-25 min, US-Hispanic).
AUTHORITY_NARRATION_SETTINGS = VoiceSettings(
    stability=0.50,
    similarity_boost=0.75,
    style=0.30,
    use_speaker_boost=True,
)

DYNAMIC_SHORTS_SETTINGS = VoiceSettings(
    stability=0.40,
    similarity_boost=0.80,
    style=0.55,
    use_speaker_boost=True,
)

CATALOG: list[VoicePreset] = [
    VoicePreset(
        id_key="es_us_male_authority",
        display_name="Narrador masculino autoridad (latino US)",
        gender="male",
        age_bracket="35-55",
        accent="Latino neutro con ligero matiz mexicano",
        use_case=(
            "Narrador principal para finanzas, salud, real estate. "
            "Voz pausada, tono ejecutivo. Equivalente a 'Leonidas' en biblioteca."
        ),
        note_es="Buscar en biblioteca de ElevenLabs filtros: Spanish + Male + Mature + Authoritative.",
    ),
    VoicePreset(
        id_key="es_us_female_warm",
        display_name="Narradora femenina cálida (latina US)",
        gender="female",
        age_bracket="30-45",
        accent="Latino neutro con calidez caribeña/colombiana",
        use_case=(
            "Salud mental, crianza, longevidad. Tono empático, "
            "calidez sin perder rigor."
        ),
        note_es="Filtros: Spanish + Female + Young/Middle Aged + Warm/Calm.",
    ),
    VoicePreset(
        id_key="es_us_male_documentary",
        display_name="Narrador documental (historia/cultura)",
        gender="male",
        age_bracket="45-60",
        accent="Castellano cinematográfico o latino formal",
        use_case=(
            "Historia oculta, documentales esotéricos, narrativa cinematográfica. "
            "Tono grave, ritmo lento, gravitas estilo Nat Geo."
        ),
        note_es="Filtros: Spanish + Male + Old + Deep/Narrative.",
    ),
    VoicePreset(
        id_key="es_us_female_dynamic",
        display_name="Voz femenina dinámica (shorts/jóvenes)",
        gender="female",
        age_bracket="22-32",
        accent="Latino US con energía",
        use_case=(
            "Shorts, ganchos rápidos, contenido juvenil. Ataques vocales fuertes "
            "en los primeros 3 segundos."
        ),
        note_es="Filtros: Spanish + Female + Young + Energetic.",
    ),
]


def by_key(key: str) -> VoicePreset:
    for v in CATALOG:
        if v.id_key == key:
            return v
    raise KeyError(f"Voice preset '{key}' no existe en el catálogo")


def recommend_for_niche(niche: str, format_: str) -> VoicePreset:
    """Recomendación pragmática según el nicho y formato.

    No es exhaustivo: es un punto de partida razonable que el usuario puede
    cambiar a mano.
    """
    n = niche.lower()
    if format_ == "shorts":
        return by_key("es_us_female_dynamic")
    if any(k in n for k in ["finanzas", "real estate", "inmigrante", "emprend", "tech", "ia "]):
        return by_key("es_us_male_authority")
    if any(k in n for k in ["salud", "crianza", "menopaus", "longevidad", "mental"]):
        return by_key("es_us_female_warm")
    if any(k in n for k in ["historia", "documental", "esotéri", "numerolog"]):
        return by_key("es_us_male_documentary")
    return by_key("es_us_male_authority")
