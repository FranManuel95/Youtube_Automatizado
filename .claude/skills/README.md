# Skills del proyecto

Skills de Claude Code específicas para este pipeline. Se cargan automáticamente al abrir el repo con Claude Code y se invocan solas cuando su `description` matchea el contexto. También se pueden lanzar manualmente con `/skill <nombre>`.

## Capa 1 - Skills guardia (operativas hoy)

| Skill | Función |
|---|---|
| `anti-ai-slop` | Audita guiones/videos antes de publicar. Aplica los 3 pilares de humanización. |
| `niche-validator` | Valida un nicho con framework 4S, checklist y tabla RPM. |
| `thumbnail-checklist` | Audita o diseña miniaturas 4K con regla de 3 elementos y pattern interrupt. |
| `monetization-appeal` | Redacta apelaciones siguiendo el protocolo 24h + 4 puntos. |

## Capa 2 - Skills operativas (se crearán al implementar cada etapa)

| Skill prevista | Etapa | Activación |
|---|---|---|
| `audio-elevenlabs` | `src/yt_auto/audio/` | Al integrar ElevenLabs |
| `visuals-nanobanana` | `src/yt_auto/visuals/` | Al integrar Nano Banana |
| `visuals-seedance` | `src/yt_auto/visuals/` | Al integrar Seedance 2.0 |
| `publishing-youtube` | `src/yt_auto/publishing/` | Al integrar YouTube Data API + MLA |
| `analytics-ask-studio` | `src/yt_auto/analytics/` | Al integrar Ask Studio |

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
