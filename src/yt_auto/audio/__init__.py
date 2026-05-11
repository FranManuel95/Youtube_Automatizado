"""Etapa 3 - Producción de audio y locución con IA.

Ver: docs/03_audio_y_locucion.md

Componentes previstos:
    - synthesize(script, voice_id, model="eleven_multilingual_v2")
    - synthesize_blocks(scenes)         -> generación por bloques (6-10 escenas)
    - apply_expressive_speech(audio)    -> sliders estabilidad 40-60%
    - dub_multilingual(audio, langs)    -> doblaje (US-Hispanic = 4x RPM)
    - export(audio, format="wav", bitrate="320k")

Modelo estándar: ElevenLabs Multilingual v2 (máxima estabilidad narrativa).
"""
