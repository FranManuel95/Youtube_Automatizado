"""Plantillas de prompts para Ask Studio (Gemini in-channel) e Inspiration Tab.

Estas plantillas se diseñan para pegar tal cual dentro de YouTube Studio
en el panel de Ask Studio o como queries en Inspiration Tab. NO son
prompts de modelo externo: son consultas estructuradas dirigidas a la
analítica nativa del propio canal.
"""

from __future__ import annotations

from yt_auto.analytics.models import AskStudioPrompt


def outlier_analysis_prompt(video_title: str, views: int, subscriber_count: int) -> AskStudioPrompt:
    ratio = views / max(subscriber_count, 1)
    return AskStudioPrompt(
        purpose="outlier_analysis",
        title=f"Análisis outlier · {video_title}",
        prompt_text=(
            f"Analiza el video '{video_title}' que tiene {views:,} vistas "
            f"({ratio:.1f}x sobre mis {subscriber_count:,} suscriptores).\n\n"
            "Específicamente quiero saber:\n"
            "1. ¿Qué porcentaje de las vistas viene de Home Page y Sugeridos "
            "(no de notificaciones ni suscripciones)?\n"
            "2. ¿Cuál es el CTR de la miniatura comparado con mi promedio del canal?\n"
            "3. ¿Cuál es la curva de retención en los primeros 30 segundos vs el resto?\n"
            "4. ¿Qué edades, géneros y geografías están sobre-representadas vs mi audiencia "
            "habitual?\n"
            "5. ¿Qué tres patrones replicables podría aplicar a mi próximo video para "
            "intentar reproducir este outlier?"
        ),
        expected_output=(
            "Recomendaciones accionables. Identificar si fue Home Page-driven, qué "
            "audiencia 'cold' captó, y 3 elementos replicables (formato, miniatura, "
            "hook o tema)."
        ),
    )


def drop_detection_prompt(video_title: str, biggest_drop_sec: int) -> AskStudioPrompt:
    return AskStudioPrompt(
        purpose="drop_detection",
        title=f"Detector de drops · {video_title}",
        prompt_text=(
            f"En el video '{video_title}', muéstrame el segundo exacto donde se produce "
            f"la mayor caída de retención (sospecho que está cerca del segundo "
            f"{biggest_drop_sec}).\n\n"
            "Devuélveme:\n"
            "1. Los 3 segundos exactos con mayor pérdida de audiencia.\n"
            "2. Para cada uno, el porcentaje de espectadores que abandonó.\n"
            "3. La causa probable (transición, ritmo, contenido).\n"
            "4. Una recomendación concreta de qué cambiar en el guion de un video "
            "similar futuro."
        ),
        expected_output="Lista priorizada de puntos de fuga con recomendaciones.",
    )


def gap_detection_prompt(niche: str, market: str) -> AskStudioPrompt:
    return AskStudioPrompt(
        purpose="gap_detection",
        title=f"Detección de gaps · {niche}",
        prompt_text=(
            f"Soy un canal de '{niche}' dirigido a '{market}'. Analiza mi catálogo "
            f"y dime:\n\n"
            "1. ¿Qué temas tienen alta demanda en mi audiencia (visible en comentarios y "
            "búsquedas dentro de YouTube) que NO he cubierto todavía?\n"
            "2. ¿Qué subtemas mis competidores directos están cubriendo y yo no?\n"
            "3. ¿Existen preguntas recurrentes en los comentarios de mis 10 videos top que "
            "merezcan un video dedicado?\n"
            "4. Para cada gap detectado, sugiere un título de video en estilo "
            "'3-Points / Open Loop' y una miniatura disruptiva."
        ),
        expected_output="3-5 ideas de video con título sugerido y razonamiento.",
    )


def competitor_pattern_prompt(competitor_channel: str) -> AskStudioPrompt:
    return AskStudioPrompt(
        purpose="competitor_pattern",
        title=f"Patrones del competidor · {competitor_channel}",
        prompt_text=(
            f"Analiza el canal competidor '{competitor_channel}'. Quiero detectar:\n\n"
            "1. Los 5 videos con mejor performance del último año (por vistas y por "
            "engagement relativo a su base de suscriptores).\n"
            "2. La fórmula recurrente en sus títulos (estructura sintáctica común).\n"
            "3. El estilo visual de sus miniaturas (paleta, composición, presencia de cara).\n"
            "4. La duración media de los 5 videos top y cómo se compara con su promedio.\n"
            "5. Qué de su fórmula podría aplicarse a mi canal sin perder mi diferenciación."
        ),
        expected_output="Patrón replicable con 3-5 puntos accionables.",
    )


def ab_test_thumbnails_prompt(video_title: str) -> AskStudioPrompt:
    return AskStudioPrompt(
        purpose="ab_test_thumbnails",
        title=f"A/B de miniaturas · {video_title}",
        prompt_text=(
            f"Para el video '{video_title}', estoy haciendo A/B test nativo de tres "
            f"miniaturas distintas.\n\n"
            "Cuando termine el test (mínimo 7 días o 1.000 impresiones por variante), "
            "dame:\n"
            "1. La variante ganadora y por qué (CTR + retención implícita).\n"
            "2. Si la diferencia es estadísticamente significativa.\n"
            "3. Qué elemento visual específico crees que marcó la diferencia.\n"
            "4. Si recomiendas extender ese patrón al resto del catálogo."
        ),
        expected_output="Conclusión accionable con confianza estadística.",
    )


ALL_BUILDERS = (
    outlier_analysis_prompt,
    drop_detection_prompt,
    gap_detection_prompt,
    competitor_pattern_prompt,
    ab_test_thumbnails_prompt,
)
