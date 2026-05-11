# Planes de edición archivados

Hitos commiteados al repo. La salida del editor (video final `.mp4`)
nunca se commitea: son los `.mp3`, `.png`, `.jpg`, `.mp4` del editor
local (CapCut/Filmora) los que producen el archivo final.

## Convención

- Nombre: `YYYY-MM-DD_HHMM_<slug>.{json,md,_subtitles.csv}`.
- JSON validado contra `EditingReport`.
- MD = guía paso a paso para el editor humano.
- CSV de subtítulos importable directamente en CapCut / Premiere.

## Cómo usar

1. Importa los `.mp3` de la etapa 3 a CapCut.
2. Importa los visuales de la etapa 4 (imágenes Nano Banana + clips Seedance).
3. Ordena la pista de video según la tabla **Timeline** del `.md`.
4. Import subtitles desde `<base>_subtitles.csv` (CapCut: Subtitles → Import).
5. Aplica color de destacado a las keywords (rojo o amarillo).
6. Inserta marcadores de DAI en los timecodes indicados.
7. Aplica transiciones recomendadas entre shots.
8. Exporta 4K, 24fps, MP4 H.264, preset YouTube 4K.

## Histórico

| Fecha | Plan | Eventos | Subs | DAI | Regla 3s |
|---|---|---|---|---|---|
| 2026-05-11 | El crédito americano sin Social Security | 20 | 203 | 2 | ⚠ 6 violaciones (esperado, requiere subdivisión manual en CapCut) |
