# PLAN OPERATIVO — Canal "Automatización IA para negocios"

> **Documento canónico de operación.** Sustituye la cadencia del
> `plan_editorial_mes_01.md` (2 vídeos/sem) por la cadencia defendible
> según el deep-research (`docs/research/2026-05_viabilidad_faceless_ai.md`):
> **1 vídeo/semana de calidad**, screencast real, revisión humana.
>
> Compromiso del operador: **5-15 h/semana consistentes**.
> Presupuesto: ~32 €/mes. Horizonte de evaluación: 6 meses con puertas
> de decisión en semanas 6, 12 y 24.

---

## 0. Los fundamentos (por qué este plan es así)

1. **La política de YouTube no prohíbe IA** — prohíbe mass-produced sin
   insight. Portavoz oficial: *"channels that use AI remain eligible to
   monetize"*. El patrón que mata: >3 vídeos/semana templated.
2. **Screencast técnico = cuadrante sano** (*"strongest CPM-plus-affiliate
   combination"*), rango realista $200-2.000/mes.
3. **No existe el atajo <2h/semana** — verificado. Los que facturan meten
   10-15h. Este plan pide ~8-10h/semana efectivas.
4. **El dinero del primer año NO viene de AdSense** — viene de plantillas
   propias + afiliados recurrentes (Make 35%/12m, n8n 30%/12m). AdSense
   llega tras YPP (mes 4-8 realista).

## 1. Reglas inquebrantables (el foso anti-purga)

1. **1 vídeo/semana máximo** los primeros 3 meses. Nunca producción en masa.
2. **Screencast real en cada vídeo** (n8n/Make funcionando en pantalla).
3. **Todo dato pasa `fact-check-datos`** antes de sintetizar audio.
4. **Disclosure de contenido sintético** en YouTube Studio en cada subida.
5. **Revisión humana documentada** (ver el vídeo entero antes de publicar,
   registrar en `compliance.HumanReviewLog`).
6. **Nunca prometer** "hazte rico / 100% pasivo / sin trabajar" (yellow icon).

## 2. Herramientas y costes

| Herramienta | Para qué | Coste |
|---|---|---|
| ElevenLabs Creator | Voz IA (Eleven v3, uso comercial) | 22 €/mes |
| OBS Studio | Grabar screencast | 0 € |
| DaVinci Resolve | Montaje + subtítulos | 0 € |
| n8n (self-hosted local) | El software que enseñas | 0 € |
| Ideogram | Thumbnails (texto legible) | ~8-10 €/mes |
| Gumroad | Lead magnet + venta plantillas | 0 € fijo (10% por venta) |
| MailerLite | Email list (<1k subs) | 0 € |
| Pipeline `yt-auto` | Guion→audio→packaging | 0 € |
| **Total** | | **~32 €/mes** |

## 3. El ciclo semanal (≈8-10h, repetible)

| Día | Sesión | Tiempo | Qué haces |
|---|---|---|---|
| **Lunes** | Planificación | 0,5-1h | Pides a Claude el paquete semanal (guion verificado + plantilla n8n + packaging). Lo revisas y ajustas a tu gusto |
| **Martes** | Workflow + grabación | 2-3h | Importas la plantilla n8n, la pruebas, grabas el screencast con OBS siguiendo el guion |
| **Jueves** | Audio + montaje | 2-3h | Sintetizas la voz (1 comando del pipeline), montas en DaVinci (voz + screencast + subtítulos automáticos) |
| **Viernes** | Publicación | 1-1,5h | Thumbnail (Ideogram), subes en PRIVADO, revisión humana completa, marcas disclosure IA, programas para sábado/domingo |
| **Fin de semana** | Comunidad + datos | 0,5-1h | Respondes TODOS los comentarios, anotas métricas (CTR, retención, subs, emails), se las pasas a Claude |

**División del trabajo:**

- **Claude (cada lunes)**: guion nuevo verificado con fuentes + plantilla
  n8n del vídeo (lead magnet) + títulos A/B + descripción con afiliados/UTMs
  + prompt de thumbnail + análisis de las métricas de la semana anterior.
- **Tú**: grabar, montar, publicar, responder, reportar. Lo que ninguna IA
  puede hacer sin caer en la purga.

## 4. Fases y puertas de decisión

### Semana 0 — Setup (una sola vez, ~3-4h)
- [ ] **Revocar la API key de ElevenLabs expuesta** y crear una nueva al
      suscribir Creator (22 €).
- [ ] Elegir voz (Spanish + Male + narration) → `ELEVENLABS_VOICE_ID` en `.env`.
- [ ] Instalar OBS + DaVinci Resolve + n8n local (`npx n8n`).
- [ ] Crear canal YouTube (nombre, banner sin cara — Ideogram).
- [ ] Cuenta Gumroad + MailerLite.
- [ ] Registrarse en afiliados: n8n, Make, Hostinger, GoHighLevel,
      ElevenLabs → guardar los enlaces REALES (los del catálogo son
      placeholders).
- [ ] Subir el lead magnet 1 (`assets/lead_magnets/inmobiliaria_lead_agent_n8n.json`)
      a Gumroad como producto gratis (pide email).

### Semanas 1-6 — Posicionamiento (vídeos 1-6, foco inmobiliaria)
Vídeos del plan editorial (captar → atender → calificar → seguir →
comparativa → recopilatorio), 1 por semana. Cada uno con su lead magnet.
Objetivo: que el algoritmo clasifique el canal + primeros 100-300 emails.
**Ingresos esperados: ~0 €. Es siembra.**

**🚦 PUERTA SEMANA 6** — con 5-6 vídeos publicados:
- CTR medio ≥3% y retención 30s ≥40% en al menos 2 vídeos → **continuar**.
- Por debajo en todos → **sesión de calibración con Claude** (hooks,
  thumbnails, formato) antes de producir el 7º. No abandonar: ajustar.

### Semanas 7-12 — Primera monetización
- Lanzar **"Kit Inmobiliaria IA"** (bundle plantillas, 49 €) a la email list.
- Afiliados ya sembrados en todas las descripciones.
- Empezar a rotar verticales si los datos lo piden (dentista, gimnasio,
  despacho — mismo sistema, otro sector).

**🚦 PUERTA SEMANA 12** — con ~12 vídeos:
- ≥500 subs o ≥50 €/mes (ventas+afiliados) → **continuar, doblar en lo que funciona**.
- <300 subs y 0 ventas → **pivote de ángulo dentro del nicho** con Claude
  (los datos dirán hacia dónde).

### Meses 4-6 — Consolidación
- YPP tier de entrada (500 subs) → memberships posibles.
- Curso/producto mayor (97-197 €) si las plantillas venden.
- Evaluar 2º vídeo semanal SOLO si el primero sale en <8h y hay tracción.

**🚦 PUERTA MES 6** — la decisión seria:
- ≥1.000 subs o ≥300 €/mes → el canal es un negocio en construcción.
  Continuar hacia 2.000-5.000 €/mes en mes 12 (rango del research).
- Por debajo de ambos → sentarse con los datos y decidir: pivote de nicho
  (el pipeline es agnóstico) o cierre ordenado. Sin drama: 6 meses de
  datos reales valen más que cualquier análisis previo.

## 5. Expectativas honestas de ingresos (estimaciones, no promesas)

| Hito | Rango realista | Fuente de ingreso |
|---|---|---|
| Mes 1-2 | 0 € | — (siembra + lista) |
| Mes 3-4 | 30-300 €/mes | Plantillas 27-49 € + primeros afiliados |
| Mes 6 | 300-1.000 €/mes | Kit + afiliados recurrentes acumulándose |
| Mes 12 | 1.000-3.000 €/mes | + curso + AdSense + recurrentes de 12 meses |

El rango del research para canales screencast establecidos: $200-2.000/mes.
Adavia Davis ($40-60k/mes) requirió red de 5 canales + 14h/sem + software
propio — NO es el benchmark de un canal individual.

## 6. Qué pedir a Claude cada semana (literal)

Lunes, en Claude Code, en este repo:

> "Semana N: aquí están las métricas del vídeo anterior [pegar CTR,
> retención, subs, emails]. Prepara el paquete del vídeo N+1: [tema del
> plan editorial o el que los datos sugieran]."

Claude devuelve: guion ScriptReport verificado + plantilla n8n + packaging
completo + ajustes basados en tus métricas. Tú produces.

## 7. Registro de progreso

Mantener en `docs/metricas_semanales.md` (se crea en semana 1): fecha,
vídeo, CTR, retención 30s, AVD, subs totales, emails, ingresos. Es la
fuente de verdad de las puertas de decisión — no las sensaciones.
