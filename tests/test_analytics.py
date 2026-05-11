"""Tests del módulo analytics."""

from __future__ import annotations

import pytest

from yt_auto.analytics import (
    AnalyticsReport,
    ChannelHealth,
    RetentionPoint,
    assess_portfolio,
    competitor_pattern_prompt,
    detect_leaks,
    drop_detection_prompt,
    gap_detection_prompt,
    outlier_analysis_prompt,
    parse_retention_csv,
    render_markdown,
)


# ----- retention parser -----

def test_parse_retention_csv_english_headers():
    csv = "Video position (%),Relative retention\n0,100\n50,80\n100,60\n"
    points = parse_retention_csv(csv, total_duration_sec=600)
    assert len(points) == 3
    assert points[0].timecode_sec == 0
    assert points[1].timecode_sec == 300
    assert points[2].timecode_sec == 600
    # 80 (>1.5) se interpreta como porcentaje y se normaliza a 0.80
    assert points[1].relative_retention == 0.80


def test_parse_retention_csv_spanish_headers():
    csv = "Posición del video (%),Retención relativa\n0,1.0\n100,0.5\n"
    points = parse_retention_csv(csv, total_duration_sec=200)
    assert len(points) == 2
    assert points[0].relative_retention == 1.0
    assert points[1].relative_retention == 0.5


def test_parse_retention_csv_rejects_unknown_headers():
    with pytest.raises(ValueError):
        parse_retention_csv("col_a,col_b\n1,2\n", total_duration_sec=100)


# ----- leak detector -----

def test_detect_leaks_finds_sharp_drops():
    points = [
        RetentionPoint(timecode_sec=0, relative_retention=1.0),
        RetentionPoint(timecode_sec=5, relative_retention=0.90),  # drop 10%
        RetentionPoint(timecode_sec=10, relative_retention=0.88),
    ]
    leaks = detect_leaks(points, drop_threshold_pct=5.0, window_sec=5)
    assert len(leaks) == 1
    assert leaks[0].drop_pct >= 10


def test_detect_leaks_uses_section_map():
    points = [
        RetentionPoint(timecode_sec=0, relative_retention=1.0),
        RetentionPoint(timecode_sec=10, relative_retention=0.80),
    ]
    section_map = {0: "Hook", 5: "Sección 1"}
    leaks = detect_leaks(points, drop_threshold_pct=5.0, window_sec=15, section_map=section_map)
    assert leaks
    assert leaks[0].related_section in {"Hook", "Sección 1"}


def test_detect_leaks_empty_when_no_drops():
    points = [
        RetentionPoint(timecode_sec=0, relative_retention=1.0),
        RetentionPoint(timecode_sec=10, relative_retention=0.99),
    ]
    assert detect_leaks(points, drop_threshold_pct=5.0) == []


# ----- portfolio -----

def test_portfolio_empty_returns_critical():
    p = assess_portfolio([])
    assert p.concentration_risk == "crítico"
    assert p.diversification_score == 1


def test_portfolio_single_channel_critical_concentration():
    p = assess_portfolio(
        [ChannelHealth(channel_id="x", name="Único", market_focus="ES", monthly_revenue_usd=1000)]
    )
    assert p.top_channel_revenue_share_pct == 100.0
    assert p.concentration_risk == "crítico"


def test_portfolio_5_channels_us_hispanic_bilingual_scores_high():
    chans = [
        ChannelHealth(channel_id=f"c{i}", name=f"C{i}", market_focus="US-Hispanic" if i == 0 else "ES",
                      subscriber_count=10000, videos_last_30d=4, monthly_revenue_usd=500,
                      monthly_rpm_usd=12.0, languages=["es", "en"] if i == 0 else ["es"])
        for i in range(5)
    ]
    p = assess_portfolio(chans)
    assert p.diversification_score >= 8
    assert p.concentration_risk in {"bajo", "medio"}
    assert p.has_us_hispanic_exposure is True


def test_portfolio_recommends_us_hispanic_when_missing():
    chans = [
        ChannelHealth(channel_id="c", name="C", market_focus="ES", monthly_revenue_usd=500)
    ]
    p = assess_portfolio(chans)
    assert any("US-Hispanic" in r for r in p.recommendations)


# ----- Ask Studio prompts -----

def test_outlier_prompt_includes_ratio():
    p = outlier_analysis_prompt("Video X", 100000, 10000)
    assert "10.0x" in p.prompt_text
    assert "100,000" in p.prompt_text or "100000" in p.prompt_text


def test_drop_prompt_includes_timecode():
    p = drop_detection_prompt("Video X", 95)
    assert "95" in p.prompt_text


def test_gap_prompt_includes_niche_and_market():
    p = gap_detection_prompt("Finanzas", "US-Hispanic")
    assert "Finanzas" in p.prompt_text
    assert "US-Hispanic" in p.prompt_text


def test_competitor_prompt_includes_channel():
    p = competitor_pattern_prompt("@TheCreditCoach")
    assert "TheCreditCoach" in p.prompt_text


# ----- render -----

def test_render_markdown_runs_on_minimal_report():
    r = AnalyticsReport()
    md = render_markdown(r)
    assert "Reporte de analítica" in md
    assert "Videos analizados" in md
