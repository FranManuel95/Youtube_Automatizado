"""Diagnóstico de salud del portafolio multi-canal.

Implementa la regla de oro del informe: 5 canales x $500 > 1 canal x $2.500.
Calcula concentración de riesgo, diversificación lingüística/geográfica y
emite recomendaciones operativas.
"""

from __future__ import annotations

from yt_auto.analytics.models import ChannelHealth, PortfolioHealth


def assess_portfolio(channels: list[ChannelHealth]) -> PortfolioHealth:
    if not channels:
        return PortfolioHealth(
            channels=[],
            total_monthly_revenue_usd=0.0,
            top_channel_revenue_share_pct=0.0,
            concentration_risk="crítico",
            diversification_score=1,
            recommendations=["No hay canales en el portafolio. Lanza el primer canal."],
        )

    total = sum(c.monthly_revenue_usd for c in channels)
    top = max(channels, key=lambda c: c.monthly_revenue_usd)
    top_share = (top.monthly_revenue_usd / total * 100) if total > 0 else 100.0

    if top_share >= 80:
        risk = "crítico"
    elif top_share >= 60:
        risk = "alto"
    elif top_share >= 40:
        risk = "medio"
    else:
        risk = "bajo"

    languages = sorted({lang for c in channels for lang in c.languages})
    has_us_hispanic = any(c.market_focus == "US-Hispanic" for c in channels)

    score = _score_diversification(
        n_channels=len(channels),
        top_share=top_share,
        n_languages=len(languages),
        has_us_hispanic=has_us_hispanic,
    )

    recs = _recommendations(
        channels=channels,
        top_share=top_share,
        languages=languages,
        has_us_hispanic=has_us_hispanic,
        n_channels=len(channels),
    )

    return PortfolioHealth(
        channels=channels,
        total_monthly_revenue_usd=round(total, 2),
        top_channel_revenue_share_pct=round(top_share, 1),
        concentration_risk=risk,  # type: ignore[arg-type]
        diversification_score=score,
        languages_covered=languages,
        has_us_hispanic_exposure=has_us_hispanic,
        recommendations=recs,
    )


def _score_diversification(
    *, n_channels: int, top_share: float, n_languages: int, has_us_hispanic: bool
) -> int:
    """Score 1-10 simple basado en heurísticas del informe."""
    score = 0
    # Número de canales (regla 5x500 > 1x2500)
    score += min(n_channels, 5)
    # Concentración
    if top_share < 30:
        score += 3
    elif top_share < 50:
        score += 2
    elif top_share < 70:
        score += 1
    # Idiomas
    score += min(n_languages - 1, 1)
    # US-Hispanic exposure (RPM x4)
    if has_us_hispanic:
        score += 1
    return min(max(score, 1), 10)


def _recommendations(
    *,
    channels: list[ChannelHealth],
    top_share: float,
    languages: list[str],
    has_us_hispanic: bool,
    n_channels: int,
) -> list[str]:
    recs: list[str] = []

    if n_channels < 5:
        recs.append(
            f"Tienes {n_channels} canal/es. La regla del informe es 5 canales mínimo "
            f"(5x$500 > 1x$2500). Plan: lanzar {5 - n_channels} canales más en los "
            f"próximos 12 meses."
        )

    if top_share >= 60:
        recs.append(
            f"El canal top representa el {top_share:.0f}% del revenue. Concentración "
            f"de riesgo {top_share >= 80 and 'crítica' or 'alta'}: una sola "
            f"desmonetización colapsa el negocio. Acelera la producción de los "
            f"canales secundarios o lanza un canal hermano del top en otro mercado."
        )

    if not has_us_hispanic:
        recs.append(
            "Ningún canal del portafolio sirve al mercado US-Hispanic (RPM Tier 1.5, "
            "hasta x4 vs LATAM). Considera lanzar uno o doblar un canal existente "
            "vía Multi-Language Audio."
        )

    if len(languages) < 2:
        recs.append(
            "Solo cubres un idioma. Activa el doblaje automático (MLA) en al menos "
            "un canal para abrir un mercado anglosajón secundario."
        )

    inactive = [c for c in channels if c.videos_last_30d == 0]
    if inactive:
        recs.append(
            f"{len(inactive)} canal/es sin publicaciones en 30 días "
            f"({', '.join(c.name for c in inactive[:3])}). El Back Catalog sigue "
            f"generando pero la frecuencia de publicación protege contra cambios "
            f"algorítmicos. Plan: 1 video/mes mínimo por canal activo."
        )

    low_rpm = [c for c in channels if (c.monthly_rpm_usd or 0) > 0 and c.monthly_rpm_usd < 3]
    if low_rpm:
        recs.append(
            f"{len(low_rpm)} canal/es con RPM < $3 ({', '.join(c.name for c in low_rpm[:3])}). "
            f"Pivote sugerido: doblaje al inglés o reorientación a temas con CPM premium "
            f"(finanzas, B2B, tech)."
        )

    if not recs:
        recs.append(
            "Portafolio saludable. Mantén la frecuencia de publicación y el "
            "Back Catalog activo. Considera Dynamic Ad Insertion en videos >12 meses."
        )

    return recs
