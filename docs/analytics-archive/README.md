# Reportes de analítica archivados

Hitos commiteados al repo: snapshots de la salud del portafolio, parseos
de retention CSV con leaks detectados, y prompts Ask Studio que merecen
quedar como referencia.

## Convención

- Nombre: `YYYY-MM-DD_HHMM_<slug>.{json,md}`.
- JSON validado contra `AnalyticsReport`.
- MD = dashboard navegable con tabla de canales, leaks por video y
  prompts copy/paste para Ask Studio.

## Cómo usar

1. **Retention real**: en YouTube Studio, exporta la curva de retención
   de un video (Analytics → Audience retention → Export). Pasa el CSV a:
   ```
   yt-auto analytics retention <csv> --duration <seconds> --archive
   ```
2. **Ask Studio**: genera prompts con `yt-auto analytics ask <purpose>`
   y pégalos en YouTube Studio → Ask Studio.
3. **Portafolio**: edita un JSON con tus canales reales y ejecuta el
   scorer (de momento se hace por código, ver `analytics/portfolio.py`).

## Histórico

| Fecha | Reporte | Score | Leaks | Notas |
|---|---|---|---|---|
| 2026-05-11 | Piloto Crédito Hispano | 2/10 (riesgo crítico) | 7 sintéticos | Portafolio recién lanzado, 1 canal. Recomendaciones del informe aplicadas. |
