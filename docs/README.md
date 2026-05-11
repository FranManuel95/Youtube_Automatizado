# Informes estratégicos

Versión en texto plano (Markdown) de los 7 documentos `.docx` originales del
repositorio. Sirven como fuente de verdad para las decisiones de producto del
pipeline `yt_auto`.

| # | Archivo | Mapea con módulo |
|---|---------|-------------------|
| 01 | `01_seleccion_de_nichos.md` | `src/yt_auto/niche/` |
| 02 | `02_ingenieria_de_guiones.md` | `src/yt_auto/scripts/` |
| 03 | `03_audio_y_locucion.md` | `src/yt_auto/audio/` |
| 04 | `04_generacion_visual.md` | `src/yt_auto/visuals/` |
| 05 | `05_edicion_y_packaging.md` | `src/yt_auto/editing/` |
| 06 | `06_publicacion_y_escalado.md` | `src/yt_auto/publishing/` |
| 07 | `07_guia_tecnica_general.md` | (transversal - resumen ejecutivo) |

Los `.docx` originales se conservan en la raíz del repo. Si se actualiza un
documento, regenerar el `.md` correspondiente con `python-docx` para mantener
sincronía.
