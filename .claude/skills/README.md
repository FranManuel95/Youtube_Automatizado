# Skills del proyecto

Skills de Claude Code específicas para este pipeline. Se cargan automáticamente al abrir el repo con Claude Code y se invocan solas cuando su `description` matchea el contexto. También se pueden lanzar manualmente con `/skill <nombre>`.

## Capa 1 - Skills guardia (operativas)

| Skill | Función |
|---|---|
| `anti-ai-slop` | Audita guiones/videos antes de publicar. Aplica los 3 pilares de humanización. |
| `fact-check-datos` | Verifica datos/cifras de un guion contra fuente PRIMARIA antes de producir. BLOQUEANTE. |
| `niche-validator` | Valida un nicho con framework 4S + scan empírico con YouTube Data API. |
| `interpretar-scan` | Reglas de decisión para leer las tablas de `competitive scan` / `outliers`. |
| `thumbnail-checklist` | Audita o diseña miniaturas 4K con regla de 3 elementos y pattern interrupt. |
| `monetization-appeal` | Redacta apelaciones siguiendo el protocolo 24h + 4 puntos. |

## Capa 2 - Skills operativas (nacen con cada etapa)

| Skill | Función | Estado |
|---|---|---|
| `title-ab-generator` | Genera 6-10 variantes de título cubriendo los 4 estilos del informe. | ✅ activa |
| `audio-elevenlabs` | Wrapper de buenas prácticas ElevenLabs (settings, voces, divisor de chars). | pendiente |
| `nano-banana-workflow` | Auditoría automática de prompts JSON tras ingest de etapa 4. | pendiente |
| `retention-leak-detector` | Detecta retention leaks a partir de CSV exportado de Ask Studio. | pendiente |
| `publishing-youtube` | Wrapper de YouTube Data API + MLA + Shorts simulcast. | pendiente |

## Cómo añadir una skill nueva

```
.claude/skills/<nombre-skill>/SKILL.md
```

Frontmatter obligatorio:

```yaml
---
name: <nombre-skill>
description: Una frase clara de cuándo debe usarse. Claude la lee para decidir el auto-trigger.
---
```

Cuerpo: instrucciones, checklists, plantillas, referencias a `docs/`. Mantenerlas cortas y enfocadas (una skill = una responsabilidad).

## Convención

- Cada skill debe referenciar el documento de `docs/` del que extrae sus reglas.
- Si una skill bloquea una acción (anti-ai-slop, monetization-appeal), debe decir explícitamente "BLOQUEADO" y devolver el control al usuario.
- Los checklists deben ser binarios (SÍ/NO), no escalas subjetivas.
