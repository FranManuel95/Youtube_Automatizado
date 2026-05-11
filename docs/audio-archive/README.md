# Planes de audio archivados

Hitos commiteados al repo. Trabajo diario en `output/audio/`
(git-ignored), pero los archivos de audio (`.mp3`, `.wav`) nunca se
suben ni siquiera al output — solo el plan y los textos.

## Convención

- Nombre: `YYYY-MM-DD_HHMM_<slug>.{json,md}`.
- JSON validado contra `AudioReport`.
- MD = dashboard de bloques con settings y textos listos para pegar.

## Cómo usar un plan archivado (ElevenLabs Free, modo interactivo)

1. Abre el `.md` correspondiente: contiene la guía paso a paso.
2. Cada bloque (`01_hook.txt`, `02_section.txt`, …) está en
   `output/audio/<base>/blocks/`.
3. Pegas cada bloque en https://elevenlabs.io/app/speech-synthesis con
   los settings indicados y descargas el `.mp3`.
4. Los `.mp3` van a `output/audio/<base>/mp3/` (no se commitean).

## Histórico

| Fecha | Guion | Bloques | Chars | Free fit |
|---|---|---|---|---|
| 2026-05-11 | El crédito americano sin Social Security | 8 | 9.801 | sí |
