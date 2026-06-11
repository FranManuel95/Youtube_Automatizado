# Shot-list OBS — Vídeo 01 (formato showcase, ~30-40 min de grabación)

> Plan de grabación pantalla a pantalla. La voz se sintetiza aparte
> (Eleven v3) y se sincroniza en DaVinci — **graba SIN audio, a tu ritmo,
> repitiendo las tomas que salgan mal**. Graba cada bloque como clip
> separado (más fácil de montar).
>
> Preparación previa (15 min, fuera de cámara):
> - n8n abierto con la plantilla importada (`inmobiliaria_lead_agent_n8n.json`)
>   y credenciales configuradas (API de IA + Calendar o mock).
> - Zoom del navegador al 110-125% (legibilidad móvil).
> - Tema oscuro de n8n (mejor contraste en vídeo).
> - Cierra pestañas/notificaciones. Modo no molestar.
> - OBS: 1080p mínimo (4K si tu equipo puede), 30 fps.

## CLIP 1 — Hook (para los primeros 20s del vídeo) · ~3 min de grabación

| Toma | Qué grabar | Duración útil |
|---|---|---|
| 1.1 | Vista general del workflow completo, cursor quieto. Luego ejecuta el workflow con un mensaje de prueba ya preparado y deja que se enciendan los nodos en cadena | 15-20s |
| 1.2 | Zoom a la respuesta generada por la IA apareciendo (el JSON de salida o el chat) | 10s |

*El hook narra el dato del NAR — el montaje pone este clip de fondo.*

## CLIP 2 — Sección 1 "El problema" (b-roll) · ~5 min de grabación

| Toma | Qué grabar | Duración útil |
|---|---|---|
| 2.1 | Un portal inmobiliario real (Idealista/Fotocasa) scrolleando anuncios | 20s |
| 2.2 | Un formulario de contacto de inmobiliaria cualquiera, cursor rellenándolo despacio | 15s |
| 2.3 | Reloj del sistema / pestaña de email vacía (metáfora de la espera) | 10s |

*La narración (HBR 7x, MIT 21x) va sobre estos planos + los gráficos
que añadirás en DaVinci (texto en pantalla con las fuentes).*

## CLIP 3 — Sección 2 "Arquitectura" (diagrama) · ~3 min

| Toma | Qué grabar | Duración útil |
|---|---|---|
| 3.1 | Vista del workflow ALEJADA, recorriendo con el cursor las 4 zonas mientras "señalas": entrada → IA → switch → acciones | 40-60s |

*Alternativa: dibuja el diagrama de 4 bloques en Excalidraw (gratis,
excalidraw.com) y graba el recorrido — queda más limpio que n8n para
esta sección.*

## CLIP 4 — Sección 3 "El sistema por dentro" (EL CORE) · ~15 min

| Toma | Qué grabar | Duración útil |
|---|---|---|
| 4.1 | Vista general del workflow, 5s quieto, luego zoom lento hacia el nodo Webhook | 15s |
| 4.2 | Doble clic en el Webhook: se ve la URL generada. Cursor la señala | 15s |
| 4.3 | Abrir el nodo de IA. **LA TOMA MÁS IMPORTANTE**: scroll lento por el system prompt completo, dejando legible cada línea ~2s. Señala con el cursor la frase "Nunca inventes propiedades que no existen" | 40s |
| 4.4 | Abrir el nodo Switch: mostrar las 2 ramas (calificado / falta info), cursor recorre cada camino | 20s |
| 4.5 | Zoom a los nodos de Calendar + notificación. Si tienes Calendar conectado, muestra el calendario en otra pestaña | 20s |
| 4.6 | Vuelta a vista general del workflow completo, quieto 5s | 10s |

## CLIP 5 — Sección 4 "Demo en vivo" · ~10 min (repite hasta que salga limpia)

| Toma | Qué grabar | Duración útil |
|---|---|---|
| 5.1 | Enviar el mensaje de prueba: "Hola, busco un piso de dos habitaciones en Valencia, presupuesto hasta 200.000 euros" (desde Postman, el form de test del webhook, o curl — lo que uses) | 15s |
| 5.2 | La ejecución encendiéndose en n8n nodo a nodo | 10s |
| 5.3 | La respuesta de la IA visible y legible (zoom) | 15s |
| 5.4 | El evento creado en Google Calendar (pestaña al lado) | 10s |
| 5.5 | La notificación llegando (Telegram/email en pantalla) | 10s |

## CLIP 6 — CTA · ~2 min

| Toma | Qué grabar | Duración útil |
|---|---|---|
| 6.1 | La página de Gumroad con la plantilla gratis (tu lead magnet ya subido) | 10s |
| 6.2 | Vista general del workflow una última vez | 10s |

---

## Checklist post-grabación

- [ ] 6 clips guardados con nombre claro (`clip1_hook.mkv`, etc.)
- [ ] La toma 4.3 (system prompt) es legible a tamaño móvil — si no, regrabar con más zoom
- [ ] Ningún dato personal visible (emails reales, API keys, nombre) — **revisar antes de montar**
- [ ] Total material: ~4-6 min útiles para un vídeo de ~9-10 min (el resto lo cubren zooms repetidos y los gráficos de DaVinci)
