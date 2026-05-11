"""Parser de retention CSV exportado por YouTube Studio + detector de leaks.

YouTube Studio exporta la "audience retention" como CSV con columnas
`Video position (%)` y `Relative retention`. Esta utilidad lo parsea,
escala a segundos y detecta caídas significativas (retention leaks).
"""

from __future__ import annotations

import csv
import re
from io import StringIO
from pathlib import Path

from yt_auto.analytics.models import RetentionLeak, RetentionPoint

# Caída > 5 puntos porcentuales en 5 segundos = leak por defecto.
DEFAULT_DROP_THRESHOLD_PCT = 5.0
DEFAULT_WINDOW_SEC = 5


def parse_retention_csv(content: str, *, total_duration_sec: int) -> list[RetentionPoint]:
    """Parsea un CSV de retention de YouTube Studio.

    Tolera headers en inglés y español:
      - "Video position (%)" / "Posición del video (%)"
      - "Relative retention" / "Retención relativa"
    """
    reader = csv.DictReader(StringIO(content.strip()))
    # Mapear cabeceras posibles a las dos columnas que necesitamos
    fieldnames = [f.strip() for f in (reader.fieldnames or [])]
    position_key = None
    retention_key = None
    for f in fieldnames:
        f_lower = f.lower()
        if "position" in f_lower or "posición" in f_lower or "posicion" in f_lower:
            position_key = f
        if "retention" in f_lower or "retención" in f_lower or "retencion" in f_lower:
            retention_key = f

    if not position_key or not retention_key:
        raise ValueError(
            f"CSV no reconocido. Headers: {fieldnames}. "
            "Esperaba columnas de posición y retención."
        )

    points: list[RetentionPoint] = []
    for row in reader:
        pos_str = row[position_key].strip()
        ret_str = row[retention_key].strip()
        pos_pct = _coerce_float(pos_str)
        ret_val = _coerce_float(ret_str)
        if pos_pct is None or ret_val is None:
            continue
        # YouTube exporta retención en formato 0-1 o 0-100 según versión
        if ret_val > 1.5:
            ret_val = ret_val / 100.0
        tc_sec = int(round((pos_pct / 100.0) * total_duration_sec))
        points.append(RetentionPoint(timecode_sec=tc_sec, relative_retention=ret_val))

    return points


def _coerce_float(s: str) -> float | None:
    s = s.replace("%", "").replace(",", ".").strip()
    m = re.search(r"-?\d+(?:\.\d+)?", s)
    return float(m.group(0)) if m else None


def detect_leaks(
    points: list[RetentionPoint],
    *,
    drop_threshold_pct: float = DEFAULT_DROP_THRESHOLD_PCT,
    window_sec: int = DEFAULT_WINDOW_SEC,
    section_map: dict[int, str] | None = None,
) -> list[RetentionLeak]:
    """Detecta tramos donde la retención cae más de `drop_threshold_pct` en
    una ventana de `window_sec`.

    `section_map` opcional: dict timecode_sec -> nombre de sección del guion,
    para enriquecer cada leak con su sección de origen.
    """
    if len(points) < 2:
        return []

    sorted_pts = sorted(points, key=lambda p: p.timecode_sec)
    leaks: list[RetentionLeak] = []

    i = 0
    while i < len(sorted_pts) - 1:
        start = sorted_pts[i]
        # Buscar el primer punto fuera de la ventana, retroceder al último dentro
        j = i + 1
        while j < len(sorted_pts) and sorted_pts[j].timecode_sec - start.timecode_sec < window_sec:
            j += 1
        # j ahora es el primero fuera; usamos el último dentro de la ventana
        # (o el último disponible si nos pasamos del final)
        j = min(j, len(sorted_pts) - 1)
        if j <= i:
            i += 1
            continue
        end = sorted_pts[j]
        drop = (start.relative_retention - end.relative_retention) * 100
        if drop >= drop_threshold_pct:
            section = _nearest_section(section_map, start.timecode_sec) if section_map else None
            sorted_pts[i] = start.model_copy(update={"is_leak": True})
            leaks.append(
                RetentionLeak(
                    start_sec=start.timecode_sec,
                    end_sec=end.timecode_sec,
                    drop_pct=round(drop, 2),
                    related_section=section,
                    suggested_fix=_suggest_fix(drop, section),
                )
            )
            i = j  # Saltar al final del leak para no contar dos veces
        else:
            i += 1

    return leaks


def _nearest_section(section_map: dict[int, str], tc_sec: int) -> str | None:
    if not section_map:
        return None
    # Encontrar la sección cuyo timecode_start es el mayor <= tc_sec
    candidates = [(start, name) for start, name in section_map.items() if start <= tc_sec]
    if not candidates:
        return None
    return max(candidates)[1]


def _suggest_fix(drop_pct: float, section: str | None) -> str:
    location = f"al inicio de '{section}'" if section else "en este tramo"
    if drop_pct >= 15:
        return (
            f"Caída crítica ({drop_pct:.0f}%) {location}. Sospecha de hook fallido "
            f"o promesa no entregada. Reescribir esta sección con un pattern interrupt "
            f"y un loop nuevo. Considerar mover este contenido más adelante."
        )
    if drop_pct >= 8:
        return (
            f"Caída fuerte ({drop_pct:.0f}%) {location}. Probable fricción narrativa. "
            f"Insertar B-roll, cifra impactante o cambio de plano. Acortar la sección."
        )
    return (
        f"Caída moderada ({drop_pct:.0f}%) {location}. Añadir un pattern interrupt "
        f"o variación visual cada 3 segundos."
    )


def load_csv(path: Path, *, total_duration_sec: int) -> list[RetentionPoint]:
    return parse_retention_csv(path.read_text("utf-8"), total_duration_sec=total_duration_sec)
