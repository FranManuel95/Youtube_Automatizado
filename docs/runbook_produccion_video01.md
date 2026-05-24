# Runbook de producción — Video 01

Guía paso a paso, en orden, para producir y publicar el primer video.
Sigue de arriba a abajo. Tiempo total estimado: **6-9 horas** (repartibles en 2-3 sesiones).
Todo lo que sigue es TU parte (yo no puedo ejecutarlo desde el sandbox).

---

## SESIÓN 0 — Setup de cuentas (~45 min, una sola vez)

- [ ] **ElevenLabs Creator** ($22/mes): https://elevenlabs.io/pricing → suscribir. Habilita uso comercial + Eleven v3 + voces hispanas.
- [ ] Elegir voz: en ElevenLabs → Voices → filtrar Spanish + Male + "narration/professional". Copiar el `voice_id` → ponerlo en `.env` como `ELEVENLABS_VOICE_ID=...`
- [ ] **OBS Studio** (gratis): https://obsproject.com → instalar (para grabar screencast de n8n).
- [ ] **DaVinci Resolve** (gratis): https://www.blackmagicdesign.com/products/davinciresolve → instalar (montaje).
- [ ] **n8n** (gratis): instalar local (`npx n8n`) o cloud trial. Importar la plantilla `assets/lead_magnets/inmobiliaria_lead_agent_n8n.json`.
- [ ] **Gumroad** o **Stan.store** (gratis): crear cuenta (para el lead magnet + producto).
- [ ] **Afiliados** (gratis registrarse): n8n (n8n.io/affiliates), Make (make.com/affiliate), Hostinger, GoHighLevel, ElevenLabs. Obtener tus enlaces → reemplazar `tucanal` en la descripción.
- [ ] **Canal YouTube**: crear/configurar. Nombre sugerido: algo tipo "AutomatizaIA" o "IA para tu Negocio". Banner + foto (genera con Ideogram, sin cara).

---

## SESIÓN 1 — Audio (~1.5 h)

El guion está en `docs/scripts-archive/piloto-01-inmobiliaria-leads.md`, ya troceado en bloques (Hook, Sección 1-4, CTA).

**Opción A — Manual (más control):**
- [ ] Abre ElevenLabs → Text to Speech → modelo **Eleven v3**.
- [ ] Pega cada bloque (Hook, Sec 1, Sec 2, Sec 3, Sec 4, CTA) por separado. Genera y descarga el MP3 de cada uno.
- [ ] Settings: Stability ~0.5, Similarity ~0.75.

**Opción B — Pipeline (automatizado):**
- [ ] (Requiere el guion en formato ScriptReport JSON — pídemelo si quieres esta vía; te genero el JSON y usas `audio synth`.)

- [ ] Escucha los 6 MP3. ¿Suena natural? ¿Pronuncia bien "n8n" (di "ene-ocho-ene"), "webhook", "lead"? Si masacra una palabra técnica, reescríbela fonética en el guion ("webhook" → "uebjuk" si hace falta) y re-sintetiza.

---

## SESIÓN 2 — Screencast (~1.5 h)

- [ ] Abre n8n con la plantilla importada.
- [ ] Abre OBS → grabar pantalla a 1080p o 4K, 30fps.
- [ ] Graba siguiendo la **Sección 3** del guion: construye el workflow nodo a nodo, despacio, mostrando cada conexión. No te preocupes por la voz (va aparte).
- [ ] Graba la **demo** (Sección 4): manda un mensaje de prueba y muestra la respuesta llegando + el evento en calendario.
- [ ] Graba b-roll extra: el dashboard de n8n, zooms a los nodos clave. Tendrás material para cubrir las secciones 1-2 (narración sobre b-roll).

---

## SESIÓN 3 — Montaje en DaVinci (~2-3 h)

- [ ] Importa los 6 MP3 + el screencast.
- [ ] Timeline: coloca el audio en orden (Hook → Sec1 → ... → CTA).
- [ ] Sincroniza el screencast con la narración. Donde hablas del problema (Sec 1-2), usa b-roll + gráficos simples. Donde montas (Sec 3), el screencast real.
- [ ] **Subtítulos**: DaVinci tiene transcripción automática (Edit → Create Subtitles from Audio). Imprescindible: 70% ve sin sonido al principio.
- [ ] **Texto en pantalla** para las fuentes (sello anti-AI-Slop): cuando menciones NAR/HBR/MIT, pon el nombre en pantalla.
- [ ] Ritmo: corte o cambio visual cada 8-15 segundos (no cada 3 — eso es dogma viejo). Que no haya pantalla estática >15s.
- [ ] Exporta: 4K si puedes, H.264, ~16 Mbps.

---

## SESIÓN 4 — Thumbnail + lead magnet (~1 h)

**Thumbnail:**
- [ ] Ideogram (https://ideogram.ai, ~$0.08): usa el prompt del brief en `docs/publishing-archive/piloto-01-packaging.md`.
- [ ] Texto grande "30 SEGUNDOS", fondo oscuro, sin cara. Verifica que se lee a 320px (míralo en el móvil).

**Lead magnet:**
- [ ] Sube `inmobiliaria_lead_agent_n8n.json` a Gumroad como producto gratis (pide email).
- [ ] Copia el enlace → reemplaza `[LINK A TU LEAD MAGNET]` en la descripción.

---

## SESIÓN 5 — Publicación (~30 min)

- [ ] Sube el video a YouTube en **PRIVADO**.
- [ ] Pega título (elige 1 de los 3 A/B), descripción (de `piloto-01-packaging.md` con tus enlaces de afiliado reales), tags.
- [ ] Sube el thumbnail.
- [ ] Marca "contenido alterado/sintético" en la sección de YouTube (disclosure IA — obligatorio).
- [ ] Añade capítulos (ya están en la descripción).
- [ ] **REVISIÓN HUMANA anti-AI-Slop** (regla #1 de CLAUDE.md): míralo entero una vez. ¿Suena a robot? ¿Hay algún error de dato? ¿El screencast se entiende? Registra que lo revisaste.
- [ ] Cambia a **Público** (o programa). Mejor hora para España/LatAm: 18-21h.

---

## DESPUÉS (primeros 7 días)

- [ ] Día 1-2: responde TODOS los comentarios (señal de engagement para el algoritmo).
- [ ] Día 7: anota en YouTube Studio → CTR, retención 30s, retención media, subs ganados, emails capturados.
- [ ] **Vuelve con esos datos** → escribimos el guion 2 calibrado con lo aprendido.

---

## Coste real de este primer video

| Item | Coste |
|---|---|
| ElevenLabs Creator | $22/mes |
| Ideogram (thumbnail) | ~$0.08 |
| Todo lo demás (OBS, DaVinci, n8n, Gumroad) | $0 |
| **Total para arrancar** | **~$22** |
