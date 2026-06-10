---
name: fact-check-datos
description: Verifica contra fuente primaria TODOS los datos, cifras y estadísticas de un guion antes de producirlo o publicarlo. Úsalo siempre que un guion contenga números, porcentajes, estudios citados o afirmaciones del tipo "según X", y antes de sintetizar audio o exportar contenido final. También cuando el usuario diga "verifica los datos", "¿es cierto que...?" o el guion provenga de un agente/LLM.
---

# Fact-Check de Datos

Un dato falso en un video destruye la credibilidad del canal, puede activar
penalizaciones por desinformación y rompe el sello agregador-educador.
**Esta skill es BLOQUEANTE: si un dato no se verifica, no se produce.**

## Caso real que motiva esta skill (no repetir)

El guion piloto 01 afirmaba *"el 78% de los compradores contrata a la
primera inmobiliaria que le responde"*. Al verificar contra fuente primaria:

- El dato real (NAR) es *"~7 de cada 10 compradores entrevistan a UN SOLO
  agente"* — mide selección temprana, **no** velocidad de respuesta.
- El "9x al responder en 5 min" era la cifra débil; las defendibles son
  **7x en la primera hora** (HBR, 1,25M leads) y **21x para cualificar**
  (MIT/Oldroyd).
- El "50% de leads fuera de horario" **no tiene fuente primaria** → se
  reformuló a afirmación cualitativa sin cifra.

Tres datos "plausibles", tres correcciones necesarias. Asume que todo dato
generado por un LLM o un agente de investigación está mal hasta probarse.

## Procedimiento (por cada dato del guion)

1. **Extraer**: lista cada cifra, porcentaje, estudio o "según X" del guion.
2. **Clasificar la fuente**:
   - Fuente primaria (el estudio/organismo original): ✅ citable.
   - Blog/agregador del sector (OutlierKit, FluxNote, Miraflow, MilX...):
     ⚠️ NO citable como hecho — buscar la primaria o degradar.
   - Sin fuente / "datos del sector": ❌ no usable como cifra.
3. **Verificar** con WebSearch/WebFetch la fuente primaria. Comprobar:
   - ¿La cifra exacta coincide?
   - ¿El MATIZ coincide? (el error típico no es la cifra, es qué mide).
   - ¿Sigue vigente o es de hace 10 años sin actualizar?
4. **Resolver** según resultado:
   - Verificado → mantener + anotar fuente con URL en las notas de
     producción (y citarla en pantalla/descripción).
   - Matiz incorrecto → reescribir la frase para que diga lo que la fuente
     dice de verdad.
   - No verificable → eliminar la cifra y reformular en cualitativo
     ("una parte importante de...", "los estudios del sector apuntan...").

## Reglas duras

- Nunca inventar una URL ni atribuir un dato a una institución sin haber
  visto la fuente.
- Nunca "redondear hacia lo viral" (convertir 7x en 10x porque suena mejor).
- Las proyecciones propias (ingresos, conversiones) se etiquetan SIEMPRE
  como estimaciones, jamás como datos.
- Si el guion pasa por `anti-ai-slop`, esta skill cubre el Pilar 2
  (autoridad real): sin fact-check no hay autoridad.

## Salida esperada

1. Tabla: dato → estado (`VERIFICADO` / `CORREGIDO` / `ELIMINADO`) →
   fuente primaria con URL → redacción final segura.
2. Veredicto global: `APROBADO PARA PRODUCIR` / `BLOQUEADO` (si queda
   algún dato sin resolver).
3. Lista de citas para mostrar en pantalla/descripción (E-E-A-T).

## Referencias

- `CLAUDE.md` § regla 6
- `docs/scripts-archive/piloto-01-inmobiliaria-leads.md` § "Notas de
  producción" (ejemplo de datos verificados con URLs)
- Skill `anti-ai-slop` (Pilar 2)
