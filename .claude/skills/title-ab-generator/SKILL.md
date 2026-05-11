---
name: title-ab-generator
description: Genera 6-10 títulos alternativos para A/B testing a partir de un guion o tema, cubriendo los 4 estilos del informe (3-Points / Open Loop, Psicología de + Sujeto, Paradoja Emocional, Revelación Disruptiva). Úsalo cuando el usuario diga "dame títulos alternativos", "necesito A/B de títulos", "el título no me convence", o vaya a publicar un video.
---

# Title A/B Generator

YouTube Studio permite A/B testing nativo de hasta 3 variantes de título. Un cambio de packaging puede subir impresiones hasta +300%. Esta skill produce variantes coherentes con los 4 estilos validados del informe.

## Cuándo dispararse

- El usuario tiene un guion (ScriptReport) y duda del título.
- Va a invocar `yt-auto publish` y quiere probar variantes.
- Un video del Back Catalog está perdiendo tracción y necesita repackaging.
- El usuario explícitamente pide alternativas: "más títulos", "variaciones", "A/B".

## Inputs necesarios

1. **Tema o título actual** del video.
2. **Nicho** y **mercado** (US-Hispanic, ES, etc.).
3. **Promesa central** del video (qué se lleva el espectador).
4. **Open loop** o pregunta abierta que el video resuelve (si existe).
5. *(Opcional)* Datos numéricos concretos del video que pueden ir en el título.

## Los 4 estilos del informe (genera 2 por estilo)

### 1. 3-Points / Open Loop
**Fórmula**: `<concepto> + <número> + <razón/error/jugada> + <adjetivo cualificador>`

Ejemplos para el nicho de crédito ITIN:
- "El crédito americano sin Social Security: 3 jugadas legales que tu banco oculta"
- "Construir crédito con ITIN: las 4 puertas que el sistema no te enseña"

Reglas:
- El número debe ser real (cuenta los puntos del video).
- Termina con palabra cualitativa que abra loop: "oculta", "irreversibles", "críticas", "letales", "olvidadas".

### 2. La Psicología de + Sujeto
**Fórmula**: `La psicología de <sujeto/objeto/situación>: <razón emocional> + <número> + <consecuencia>`

Ejemplos:
- "La psicología del crédito americano: por qué los hispanos lo construimos mal 3 errores irreversibles"
- "La psicología del efectivo: la creencia heredada que mantiene invisibles a 26 millones de hispanos"

Reglas:
- Apela a una emoción o creencia inconsciente.
- Funciona muy bien en autoridad (finanzas, salud, desarrollo personal).

### 3. Paradoja Emocional
**Fórmula**: `<acción aparentemente buena> + te está + <consecuencia inesperada>`

Ejemplos:
- "Pagar todo en efectivo te está empobreciendo en EE.UU. y nadie te lo explicó"
- "Vivir sin deudas es lo que mantiene atascado tu crédito americano"

Reglas:
- Disonancia "sientes X pero la realidad es Y".
- Genera mayor CTR pero requiere que el video lo justifique sólidamente.

### 4. Revelación Disruptiva
**Fórmula**: `<idea contra intuitiva> + <evidencia/dato>` o bien `Todo lo que sabes sobre <tema> es falso por esta razón`

Ejemplos:
- "Tu banco te oculta este formulario del IRS porque no le conviene que lo conozcas"
- "26 millones de hispanos son invisibles para el sistema financiero: tú probablemente eres uno"

Reglas:
- Empieza con verdad incómoda verificable.
- NO clickbait sin sustento; el video debe entregar la revelación.

## Reglas globales

- **Idioma**: respeta el mercado. Para US-Hispanic, registro neutro mexicano con palabras que no chocan en LATAM.
- **Longitud**: 50-65 caracteres ideal (entran en móvil y en sugeridos sin truncar). Máximo 100.
- **Sin clickbait vacío**: si el video no entrega, la retención cae y el algoritmo hunde el canal (AI Slop).
- **Sin emojis** en el título principal salvo nichos juveniles/Shorts.
- **Mayúscula inicial** sí. CAPS COMPLETAS no.

## Salida esperada

Devuelve al usuario:

1. **Tabla de 8-10 variantes** con: estilo, título, longitud (chars), CTR estimado (rango bajo/medio/alto), riesgo de clickbait.
2. **Ranking sugerido**: las 3 mejores para A/B test inicial en YouTube Studio.
3. **Razonamiento** breve por variante (1 línea).
4. **Advertencias**: si alguna variante roza el filtro YPP o requiere disclaimer en descripción.

Si el usuario lo pide, también puedes generar **miniaturas-texto coherentes** (max 3 palabras) que combinen bien con cada título — pero recuerda invocar `/thumbnail-checklist` para la auditoría final.

## Referencias

- `docs/02_ingenieria_de_guiones.md` § 1 "Ingeniería de Títulos de Alto Rendimiento"
- `docs/05_edicion_y_packaging.md` § 4 "Pattern Interrupt"
- `docs/06_publicacion_y_escalado.md` § 4 "Re-monetización del Back Catalog"
