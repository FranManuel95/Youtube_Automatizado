"""Etapa 1 - Inteligencia de mercado y validación de nicho.

Ver: docs/01_seleccion_de_nichos.md

Componentes previstos:
    - research(topic)           -> ideación masiva con Claude Sonnet 4.6 (10-15 subnichos)
    - audit_competitors(urls)   -> Claude Opus 4.7 (Vision) sobre capturas de miniaturas
    - gaps(niche)               -> detección de "huecos" via Gemini Deep Research
    - validate(niche)           -> checklist de demanda / inactividad / diferenciación
    - rpm_estimate(niche, market) -> tabla de RPM por Tier 1 / 1.5 / 2 / 3

Framework de las 4 S: Streaming, Searching, Shopping, Scrolling.
"""
