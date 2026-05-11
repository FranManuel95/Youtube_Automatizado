# Planes visuales archivados

Hitos commiteados al repo. Las imágenes/videos generados no se commitean
nunca (ni siquiera en `output/`) por tamaño y derechos. Los JSON de
prompts sí, porque son texto y son la receta para reproducir el resultado.

## Convención

- Nombre: `YYYY-MM-DD_HHMM_<slug>.{json,md}`.
- JSON validado contra `VisualReport`.
- MD = dashboard navegable con Reference Sheet, shot list, miniatura.
- Los prompts JSON individuales viven en `output/visuals/<base>/prompts/`
  (git-ignored, regenerables desde el JSON archivado).

## Cómo usar un plan archivado

1. Abre el `.md`: contiene el flujo paso a paso.
2. Reference Sheet → Nano Banana → 4 imágenes en `assets/characters/`.
3. Cada shot:
   - Nano Banana para frame base (con la Reference Sheet como reference).
   - Seedance 2.0 para animación (multi-reference: frame + character + outfit).
4. Miniatura → Nano Banana → 4K final (texto se añade en CapCut).

## Histórico

| Fecha | Plan | Shots | PI | Personaje |
|---|---|---|---|---|
| 2026-05-11 | El crédito americano sin Social Security | 12 | 6 | Luis (4 vistas) |
