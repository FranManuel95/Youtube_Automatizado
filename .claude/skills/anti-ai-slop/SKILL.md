---
name: anti-ai-slop
description: Audita un guion, locución o video antes de publicar para evitar la penalización "AI Slop" de YouTube. Aplica el Marco de Tres Pilares para la Humanización (localización/dialectos, autoridad real, refinamiento manual). Úsalo SIEMPRE antes de exportar contenido final o cuando el usuario diga "revisa este guion", "está listo para publicar" o equivalentes.
---

# Anti AI-Slop Guard

YouTube "hunde" (sinks) el alcance del contenido inauténtico. Esta skill es la última barrera antes de publicar. Si falla cualquier pilar, NO autorices la publicación.

## Cuándo dispararse

- El usuario pide auditar, revisar o aprobar un guion / locución / video.
- El usuario está a punto de invocar `yt-auto publish` o subir a YouTube.
- Se genera contenido nuevo en `output/scripts/` o `output/videos/`.

## Marco de Tres Pilares (todos obligatorios)

### Pilar 1 - Localización y dialectos (Expressive Speech)

- [ ] ¿Usa giros lingüísticos específicos del mercado objetivo? (Para US-Hispanic: registros mexicano/caribeño/sudamericano según audiencia).
- [ ] ¿La voz tiene cadencia humana (estabilidad 40-60% en ElevenLabs)?
- [ ] ¿Hay variaciones tonales o suena monótona?
- [ ] ¿Se evita el español "neutro" plano que delata IA?

### Pilar 2 - Aportación de autoridad real

- [ ] ¿Incluye al menos 2 datos verificables (estudios, cifras, fuentes nombradas)?
- [ ] ¿Hay experiencias en primera persona o anécdotas concretas?
- [ ] ¿Aporta un ángulo que la competencia ignora (gap de mercado)?
- [ ] ¿La estructura cumple "3 Points / Open Loop" en el título e introduce un bucle abierto?

### Pilar 3 - Refinamiento manual del script

- [ ] ¿Se ha editado manualmente sobre la salida de la IA (no copy-paste literal)?
- [ ] ¿Se han eliminado las muletillas típicas de LLM ("Es importante destacar", "En resumen", "En conclusión")?
- [ ] ¿El ritmo es variado (frases cortas + largas alternadas)?
- [ ] ¿Hay al menos un pattern interrupt cada 30-45 segundos?

## Reglas adicionales de seguridad

- [ ] **Likeness Detection**: si aparecen personas reconocibles (sintéticas o no), declarar uso de IA en YouTube Studio.
- [ ] **Sin deepfakes** no autorizados de personajes públicos o marcas registradas.
- [ ] **Subtítulos** dinámicos generados (no auto-traducción cruda).

## Salida esperada

Devuelve al usuario:

1. **Veredicto**: `APROBADO` / `BLOQUEADO`.
2. **Pilares fallidos** (si alguno) con la cita exacta del problema.
3. **Sugerencia de remedio** concreta para cada fallo.
4. **Riesgo estimado de AI Slop**: bajo / medio / alto.

Si el veredicto es `BLOQUEADO`, NO continúes con la publicación. Devuelve el control al usuario para que corrija.

## Referencias

- `docs/02_ingenieria_de_guiones.md` § 4 "Combatiendo el AI Slop"
- `docs/06_publicacion_y_escalado.md` § 2 "Marco Normativo de YouTube"
- `docs/03_audio_y_locucion.md` § 7 "Conclusiones y Gestión de Riesgos"
