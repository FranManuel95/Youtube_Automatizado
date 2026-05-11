---
name: thumbnail-checklist
description: Audita o diseña miniaturas (thumbnails) de YouTube según el estándar 2026 - 4K, regla de 3 elementos, pattern interrupt y test contra estilo dominante del nicho. Úsalo cuando el usuario diga "revisa esta miniatura", "diseña una miniatura", esté generando un thumbnail con Nano Banana, o vaya a publicar un video.
---

# Thumbnail Checklist - Living Room 4K

La miniatura es el primer contacto con la propiedad digital. En 2026 compite en pantallas 4K contra Netflix. Esta skill aplica los criterios del informe `05_edicion_y_packaging.md`.

## Cuándo dispararse

- El usuario pide revisar, diseñar o comparar miniaturas.
- Antes de invocar `yt-auto publish`.
- Cuando se genera una imagen en `output/visuals/` etiquetada como `thumbnail_*`.
- Cuando el usuario menciona "miniatura", "thumbnail", "portada" o "imagen del video".

## Checklist crítico (todos obligatorios)

### Técnico
- [ ] **Resolución 4K** (3840x2160 o superior). 1080p no vale para Living Room.
- [ ] **Peso < 2 MB** (límite YouTube). Comprimir sin perder nitidez.
- [ ] **Formato** JPG/PNG/WEBP.
- [ ] **Legible a 200x150 px** (móvil) y a pantalla completa de TV.

### Regla de los 3 elementos
- [ ] **Cara**: expresión emocional clara (sorpresa, intriga, autoridad) o avatar consistente de la marca.
- [ ] **Objeto**: un único elemento central disruptivo que simbolice el tema.
- [ ] **Texto**: máximo 3 palabras, generan curiosidad, NO repiten el título.

### Pattern Interrupt
- [ ] ¿Rompe el estilo dominante del nicho? Si la competencia usa miniaturas saturadas/barrocas, tú usas minimalismo. Si usan minimalismo, tú usas contraste agresivo.
- [ ] **Saco rojo / color disruptivo**: ¿hay al menos un punto de contraste cromático fuerte (ej. rojo sobre fondo neutro)?
- [ ] ¿Pasaría el test del "scroll infinito": detendría a alguien aburrido?

### Consistencia de marca (canal automatizado)
- [ ] Si usas avatar IA, ¿es el MISMO personaje que en videos anteriores? (Reference Sheet aplicada).
- [ ] ¿La paleta cromática del canal es reconocible en el feed?

### Anti AI-Slop visual
- [ ] **Sin piel plástica**: imperfecciones visibles (poros, micro-arrugas).
- [ ] **Sin manos con 6 dedos** ni artefactos morfológicos.
- [ ] **Sin texto generado por IA** (suele tener errores). El texto se añade en CapCut/Filmora.

## Si vas a diseñar desde cero (con Nano Banana / Seedance)

Usa este esquema JSON base como prompt maestro:

```json
{
  "camera": "Sony A7R IV, 85mm lens",
  "lighting": "Cinematic soft lighting, 4k resolution",
  "skin_details": "visible pores, natural skin texture, slight imperfections, no plastic look",
  "post_processing": "color graded, high dynamic range",
  "composition": "rule of thirds, subject on left third, negative space on right for text",
  "background": "minimal, single tone, complementary to subject"
}
```

## A/B Testing (Back Catalog)

Para videos publicados:
- [ ] ¿Tiene >30 días y la retención ha caído? Probar variante con miniatura diferente.
- [ ] YouTube Studio permite hasta 3 variantes en A/B test nativo.
- [ ] Cambio de packaging puede resucitar un video y subir impresiones hasta +300%.

## Salida esperada

1. **Veredicto**: `APROBADA` / `REVISAR` / `RECHAZADA`.
2. **Checklist** con SÍ/NO por punto.
3. **Comparativa** contra el estilo dominante del nicho (si tienes referencias).
4. **Sugerencias** específicas para mejorar (qué cambiar, no qué hacer).
5. Si vas a generar la imagen, **prompt JSON** listo para Nano Banana.

## Referencias

- `docs/05_edicion_y_packaging.md` § 3 "Estrategia de Packaging" + § 4 "Pattern Interrupt"
- `docs/04_generacion_visual.md` § 1 "Prompt Maestro JSON"
- `docs/01_seleccion_de_nichos.md` § 7 "Pattern Interrupt y miniatura 4K"
