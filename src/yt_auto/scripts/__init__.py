"""Etapa 2 - Ingeniería de guiones para máxima retención.

Ver: docs/02_ingenieria_de_guiones.md

Componentes previstos:
    - reverse_engineer(competitor_urls) -> patrones de títulos/hooks
    - generate(topic, duration, viewer_ideal) -> guion con Claude Opus
    - title_3points_open_loop(topic)    -> fórmula "La Psicología de + Sujeto + ..."
    - audit_retention(script)           -> detección de puntos de fuga
    - humanize(script)                  -> anti-AI-Slop (paradoja emocional, autoridad real)

Objetivo: retención > 80% en los primeros 30 segundos. CTR estimado > 5.5/10.
"""
