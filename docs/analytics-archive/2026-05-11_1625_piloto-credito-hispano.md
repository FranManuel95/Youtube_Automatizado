# Reporte de analítica

- **Fecha**: 2026-05-11 16:25 UTC
- **Videos analizados**: 1
- **Leaks detectados (total)**: 7
- **Prompts Ask Studio**: 5
- **Portafolio incluido**: sí

## Salud del portafolio

- **Canales**: 1
- **Revenue mensual total**: $0.00
- **Concentración (canal top)**: 100.0%
- **Riesgo de concentración**: `crítico`
- **Score de diversificación**: 2/10
- **Idiomas cubiertos**: es
- **Exposición US-Hispanic**: ✓

### Canales

| Canal | Mercado | Subs | Videos 30d | Revenue | RPM |
|-------|---------|------|-----------|---------|-----|
| Crédito Hispano USA | US-Hispanic | 0 | 1 | $0 | — |

### Recomendaciones

- Tienes 1 canal/es. La regla del informe es 5 canales mínimo (5x$500 > 1x$2500). Plan: lanzar 4 canales más en los próximos 12 meses.
- El canal top representa el 100% del revenue. Concentración de riesgo crítica: una sola desmonetización colapsa el negocio. Acelera la producción de los canales secundarios o lanza un canal hermano del top en otro mercado.
- Solo cubres un idioma. Activa el doblaje automático (MLA) en al menos un canal para abrir un mercado anglosajón secundario.

## Videos analizados

### El crédito americano sin Social Security: 3 jugadas legales

- **ID**: `pilot_itin_001` · **Duración**: 708s
- **Vistas**: 0
- **Retención 30s**: 95% ✓ (target ≥80%)
- **Leaks detectados**: 7

| Tramo | Drop | Sección | Sugerencia |
|-------|------|---------|------------|
| 0-71s | 10.0% | — | Caída fuerte (10%) en este tramo. Probable fricción narrativa. Insertar B-roll, ... |
| 71-142s | 8.0% | — | Caída fuerte (8%) en este tramo. Probable fricción narrativa. Insertar B-roll, c... |
| 177-283s | 5.0% | — | Caída moderada (5%) en este tramo. Añadir un pattern interrupt o variación visua... |
| 425-496s | 13.0% | — | Caída fuerte (13%) en este tramo. Probable fricción narrativa. Insertar B-roll, ... |
| 496-566s | 10.0% | — | Caída fuerte (10%) en este tramo. Probable fricción narrativa. Insertar B-roll, ... |
| 566-637s | 7.0% | — | Caída moderada (7%) en este tramo. Añadir un pattern interrupt o variación visua... |
| 637-708s | 8.0% | — | Caída fuerte (8%) en este tramo. Probable fricción narrativa. Insertar B-roll, c... |

## Prompts para Ask Studio

Pega cada uno en el panel de Ask Studio (YouTube Studio > Analítica > Ask Studio) para auditar tu canal con Gemini integrado.

### Análisis outlier · El crédito americano sin Social Security

_Propósito: outlier_analysis_

```
Analiza el video 'El crédito americano sin Social Security' que tiene 250,000 vistas (50.0x sobre mis 5,000 suscriptores).

Específicamente quiero saber:
1. ¿Qué porcentaje de las vistas viene de Home Page y Sugeridos (no de notificaciones ni suscripciones)?
2. ¿Cuál es el CTR de la miniatura comparado con mi promedio del canal?
3. ¿Cuál es la curva de retención en los primeros 30 segundos vs el resto?
4. ¿Qué edades, géneros y geografías están sobre-representadas vs mi audiencia habitual?
5. ¿Qué tres patrones replicables podría aplicar a mi próximo video para intentar reproducir este outlier?
```

**Output esperado**: Recomendaciones accionables. Identificar si fue Home Page-driven, qué audiencia 'cold' captó, y 3 elementos replicables (formato, miniatura, hook o tema).

### Detector de drops · El crédito americano sin Social Security

_Propósito: drop_detection_

```
En el video 'El crédito americano sin Social Security', muéstrame el segundo exacto donde se produce la mayor caída de retención (sospecho que está cerca del segundo 95).

Devuélveme:
1. Los 3 segundos exactos con mayor pérdida de audiencia.
2. Para cada uno, el porcentaje de espectadores que abandonó.
3. La causa probable (transición, ritmo, contenido).
4. Una recomendación concreta de qué cambiar en el guion de un video similar futuro.
```

**Output esperado**: Lista priorizada de puntos de fuga con recomendaciones.

### Detección de gaps · Finanzas para inmigrantes en EE.UU.

_Propósito: gap_detection_

```
Soy un canal de 'Finanzas para inmigrantes en EE.UU.' dirigido a 'US-Hispanic'. Analiza mi catálogo y dime:

1. ¿Qué temas tienen alta demanda en mi audiencia (visible en comentarios y búsquedas dentro de YouTube) que NO he cubierto todavía?
2. ¿Qué subtemas mis competidores directos están cubriendo y yo no?
3. ¿Existen preguntas recurrentes en los comentarios de mis 10 videos top que merezcan un video dedicado?
4. Para cada gap detectado, sugiere un título de video en estilo '3-Points / Open Loop' y una miniatura disruptiva.
```

**Output esperado**: 3-5 ideas de video con título sugerido y razonamiento.

### Patrones del competidor · Canal Hipotético - The Credit Coach

_Propósito: competitor_pattern_

```
Analiza el canal competidor 'Canal Hipotético - The Credit Coach'. Quiero detectar:

1. Los 5 videos con mejor performance del último año (por vistas y por engagement relativo a su base de suscriptores).
2. La fórmula recurrente en sus títulos (estructura sintáctica común).
3. El estilo visual de sus miniaturas (paleta, composición, presencia de cara).
4. La duración media de los 5 videos top y cómo se compara con su promedio.
5. Qué de su fórmula podría aplicarse a mi canal sin perder mi diferenciación.
```

**Output esperado**: Patrón replicable con 3-5 puntos accionables.

### A/B de miniaturas · El crédito americano sin Social Security

_Propósito: ab_test_thumbnails_

```
Para el video 'El crédito americano sin Social Security', estoy haciendo A/B test nativo de tres miniaturas distintas.

Cuando termine el test (mínimo 7 días o 1.000 impresiones por variante), dame:
1. La variante ganadora y por qué (CTR + retención implícita).
2. Si la diferencia es estadísticamente significativa.
3. Qué elemento visual específico crees que marcó la diferencia.
4. Si recomiendas extender ese patrón al resto del catálogo.
```

**Output esperado**: Conclusión accionable con confianza estadística.

## Notas

Piloto sintético: simulación de curva de retención esperada para el video ITIN. Los datos reales se obtendrán al publicar.

