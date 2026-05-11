# Planes de publicación archivados

Hitos commiteados al repo. El acto de publicar real es manual en
YouTube Studio (modo interactivo, sin OAuth de momento).

## Convención

- Nombre: `YYYY-MM-DD_HHMM_<slug>.{json,md}`.
- JSON validado contra `PublishingReport`.
- MD = guía de copy/paste a YouTube Studio + checklist pre-publish.

## Cómo usar

1. Abre el `.md`.
2. Verifica el **veredicto** al principio. Si "NO PUBLICAR", corrige
   los críticos primero.
3. Si "LISTO":
   - Copia el título (campo Title).
   - Copia la descripción completa (campo Description).
   - Copia los tags separados por coma.
   - Configura categoría, idioma, made-for-kids, privacidad.
   - Sube la miniatura 4K generada en etapa 4.
   - YouTube detectará los capítulos automáticamente desde la descripción.
4. Antes de hacer click en **Publish**, repasa visualmente el
   checklist completo del `.md`.

## Histórico

| Fecha | Plan | Críticos | Tags | Capítulos | Veredicto |
|---|---|---|---|---|---|
| 2026-05-11 | El crédito americano sin Social Security | 4/5 | 15 | 8 | ⚠ título 79 chars - usar alternativa más corta |
