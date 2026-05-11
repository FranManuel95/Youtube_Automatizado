# Auditorías de nicho archivadas

Carpeta de auditorías commiteadas al repo como hitos del proyecto. Las
auditorías de trabajo diario viven en `output/niche/` (git-ignored).

## Convención

- Nombre: `YYYY-MM-DD_HHMM_<mercado>_<vertical>.{json,md}`.
- El JSON es la fuente de verdad (validado contra `NicheAuditReport`).
- El MD es el render legible generado por `yt_auto.niche.render_markdown`.

## Cómo archivar una auditoría nueva

```bash
yt-auto niche ingest output/niche/last_response.json --archive
```

## Histórico

| Fecha | Mercado | Top 1 | Score |
|---|---|---|---|
| 2026-05-11 | US-Hispanic | Finanzas para inmigrantes / Real estate hispano | 9/10 |
