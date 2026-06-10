---
name: interpretar-scan
description: Interpreta los resultados de `yt-auto competitive scan` y `competitive outliers` con reglas de decisión objetivas (saturación, hueco real, calidad de la query). Úsalo cuando el usuario pegue la tabla de un scan, pregunte "¿hay hueco en este nicho?", o antes de comprometer producción a un tema/vertical nuevo.
---

# Interpretar Competitive Scan

Los scans de YouTube Data API dan datos crudos; esta skill aplica las reglas
de decisión validadas en la selección de nicho de este proyecto.

## Antes de interpretar: ¿la query es buena?

Una query mala produce conclusiones falsas. Señales de query mala:

- Resultados de países/idiomas irrelevantes mezclados → query demasiado
  genérica (pasó con "bienes raíces homeownership").
- 0 resultados → query demasiado restrictiva; **no concluyas "desierto"
  con una sola query**: prueba 2-3 variantes más amplias (pasó con "n8n
  para abogados": 0 resultados, pero "abrir LLC español USA" reveló un
  big-fish de 133k).
- Usa las `search_queries` curadas del perfil YAML si existen.

**Regla: mínimo 2-3 queries por hipótesis antes de concluir.**

## Reglas de decisión sobre la tabla

| Señal | Lectura |
|---|---|
| 0 canales >100k subs en 2-3 queries | **Hueco real** (entrable sin autoridad) |
| 1 big-fish con cadencia ALTA (>4 vid/mes) | Muralla en lo genérico → solo entrar por sub-vertical |
| 1 big-fish con cadencia BAJA (~1 vid/mes) | Ventana por cadencia (caso Kate Siavel) |
| Mediana de subs < 1.000 pero hay 1-2 canales con views/video altos | Demanda demostrada + oferta débil = mejor señal posible |
| Mediana < 100 subs y views/video bajos en todos | Posible demanda nula — validar con Google Trends antes de entrar |
| Big-fish presente pero en OTRO idioma | Hueco en tu idioma (caso Javier Vidana: domina en inglés, español vacío) |

## Sobre `competitive outliers`

- Mira la **edad** de los outliers, no solo el multiplicador: outliers todos
  >10 meses pueden indicar ola pasada, no demanda actual (pasó con los
  outliers hipotecarios de Javier Vidana).
- Outliers recientes (<6 meses) con ≥3x mediana = tema vigente a replicar.
- Extrae el PATRÓN de los títulos outlier (cifras concretas, curiosity gap,
  formato lista), no solo el tema.

## Trampas conocidas

- **Subs ≠ verdad absoluta**: el conteo de la API es real, pero la
  relevancia del canal para tu query la decide el ranking de YouTube, que
  mezcla. Filtra a ojo los resultados off-topic antes de calcular medianas.
- **Caché de 24h**: si necesitas datos frescos tras un evento, usa
  `--no-cache`.
- **Cuota**: cada scan ≈ 101 unidades (≈99 scans/día). `outliers` ≈ 2-3.

## Salida esperada

1. Veredicto: `HUECO REAL` / `MURALLA` / `VENTANA POR CADENCIA` /
   `DEMANDA DUDOSA` / `QUERY MALA - REPETIR`.
2. Evidencia: qué filas de la tabla sostienen el veredicto.
3. Acción siguiente concreta (otra query, outliers de un channel_id,
   o decisión de entrar/descartar).

## Referencias

- `src/yt_auto/competitive/` (scanner, modelos, fragmentation_score)
- `assets/niche_profiles/*.yaml` (search_queries curadas)
- Skill `niche-validator` (validación cualitativa complementaria)
