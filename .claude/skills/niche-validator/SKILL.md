---
name: niche-validator
description: Valida si un nicho o subnicho de YouTube es rentable antes de invertir tiempo de producción. Aplica el framework de las 4S, el checklist de validación y la tabla de RPM por mercado. Úsalo cuando el usuario proponga un nicho, diga "merece la pena este tema", "es buen nicho X" o vaya a iniciar la etapa 1 del pipeline.
---

# Niche Validator

Un nicho mal elegido invalida toda la producción posterior. Esta skill aplica el rigor del informe `01_seleccion_de_nichos.md` antes de gastar una sola llamada a ElevenLabs o Seedance.

## Cuándo dispararse

- El usuario propone un nicho/subnicho concreto.
- Se invoca `yt-auto niche <topic>`.
- Antes de crear un nuevo canal o pivotar uno existente.

## Inputs requeridos del usuario

Si no los tienes, PÍDELOS antes de validar:

1. **Tema / subnicho** propuesto.
2. **Mercado objetivo** (US-Hispanic, ES, LATAM, EN-US).
3. **2-3 canales competidores** (URL o nombre) que dominen ese espacio, si los conoce. Si no, márcalo como riesgo.

## Framework de las 4S - ¿en qué cuadrante encaja?

- [ ] **Streaming** (largo, sala de estar) - contenido extra-largo de autoridad.
- [ ] **Searching** (intención de búsqueda) - resolución de problemas.
- [ ] **Shopping** (preventa) - afiliación y conversión.
- [ ] **Scrolling** (Shorts) - descubrimiento rápido.

Un nicho rentable encaja en al menos 2 cuadrantes. Si solo encaja en Scrolling, advierte: RPM bajo, alto volumen requerido.

## Checklist de validación (todos deben ser SÍ)

- [ ] **Demanda confirmada**: ¿hay ≥ 3 videos del tema con >100k vistas en el último año?
- [ ] **Inactividad explotable**: ¿hay canales grandes que han bajado calidad o frecuencia?
- [ ] **Gap identificado**: ¿hay subtemas pedidos en comentarios que la competencia ignora?
- [ ] **Diferenciación técnica**: ¿puedo aplicar pattern interrupt o miniatura 4K que destaque del estilo dominante?
- [ ] **RPM viable**: ver tabla abajo.

Si falla 1: avisar. Si fallan 2 o más: BLOQUEAR y proponer pivote.

## Tabla de RPM estimado (finanzas/tech/bienestar premium)

| Mercado | RPM | Driver |
|---|---|---|
| Tier 1 (US, CH, NO, AU, CA) | $15-40 | Crédito y competencia publicitaria alta |
| **Tier 1.5 (US-Hispanic)** | **$10-25** | Acceso a crédito hispano en EE.UU. (x4 LATAM) |
| Tier 2 (ES) | $3-10 | Mercado nativo maduro |
| Tier 3 (LATAM) | $0.50-2 | Volumen alto, conversión baja |

Para mercados con RPM < $5, recomendar siempre estrategia bilingüe (MLA EN-US) o pivote a otro mercado.

## Pilares del nicho de alto rendimiento

- [ ] Demanda **constante** (no moda pasajera).
- [ ] **Utilidad** clara para el espectador.
- [ ] Alto **valor publicitario** (categoría apetecible: finanzas, salud, tech, B2B).

## Outliers - detección de potencial exponencial

Si el usuario tiene datos de canales competidores, busca **outliers**:
- Videos con vistas 3x-10x superiores a la base de suscriptores.
- Fuente de tráfico: Home Page / Sugeridos (no notificaciones).
- CTR desproporcionado.

Un outlier reciente es señal fuerte de gap explotable.

## Salida esperada

1. **Veredicto**: `VIABLE` / `VIABLE CON AJUSTES` / `BLOQUEADO`.
2. **Cuadrantes 4S** donde encaja.
3. **Checklist** con SÍ/NO/?
4. **RPM esperado** para el mercado objetivo.
5. **Riesgos** identificados (saturación, falta de gap, RPM bajo).
6. **3 ángulos de Niche Bending** sugeridos si el nicho directo está saturado (fusión con otro vertical).
7. **Próximo paso concreto**: qué auditar manualmente (canales) o qué herramienta usar (Inspiration Tab, Ask Studio).

## Referencias

- `docs/01_seleccion_de_nichos.md` (íntegro)
- `docs/07_guia_tecnica_general.md` § 1 "Framework 4S"
- `docs/06_publicacion_y_escalado.md` § 1 "Arbitraje de Mercados"
