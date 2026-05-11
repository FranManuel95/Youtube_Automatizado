# Guiones archivados

Hitos de producción commiteados al repo. Los guiones de trabajo diario
viven en `output/scripts/` (git-ignored).

## Convención

- Nombre: `YYYY-MM-DD_HHMM_<slug-del-titulo>.{json,md}`.
- JSON validado contra `ScriptReport` (`src/yt_auto/scripts/models.py`).
- MD generado por `yt_auto.scripts.render_markdown`.

## Cómo archivar uno nuevo

```bash
yt-auto script ingest output/scripts/last_response.json --archive
```

## Histórico

| Fecha | Título | Nicho | Retención 30s | CTR est. |
|---|---|---|---|---|
| 2026-05-11 | El crédito americano sin Social Security | Finanzas para inmigrantes EE.UU. | 84% | 7.8% |
