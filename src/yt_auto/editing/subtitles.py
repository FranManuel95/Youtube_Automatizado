"""Segmentación de subtítulos dinámicos con keywords destacados.

Toma el texto limpio de cada bloque de audio y lo divide en chunks de
2-4 segundos basándose en puntuación natural. Detecta heurísticamente
keywords merecedores de destacado cromático (números, cifras dólar,
nombres propios identificables, palabras clave del nicho).
"""

from __future__ import annotations

import re

from yt_auto.editing.models import SubtitleSegment

# ~150 palabras por minuto = 2.5 palabras/segundo
WORDS_PER_SECOND = 2.5
MIN_SEG_WORDS = 5
MAX_SEG_WORDS = 12
MAX_SEG_DURATION_SEC = 4.0

_NUMBER_PATTERN = re.compile(r"\b\d{1,3}(?:[\.,]\d{3})*(?:[\.,]\d+)?\b")
_DOLLAR_PATTERN = re.compile(r"\$\d[\d\.,]*")
_PERCENT_PATTERN = re.compile(r"\b\d+\s?%")
_PROPER_NOUN_PATTERN = re.compile(r"\b[A-Z][a-záéíóúñ]+(?:\s[A-Z][a-záéíóúñ]+)*\b")
_ACRONYM_PATTERN = re.compile(r"\b[A-Z]{2,5}\b")

# Palabras clave del dominio financiero que merece destacar.
DOMAIN_KEYWORDS = {
    "ITIN", "Social Security", "FICO", "W-7", "IRS", "CFPB", "Experian",
    "Equifax", "TransUnion", "FHA", "LLC", "Capital One", "Discover",
    "Self Inc", "Kikoff", "Credit Strong", "secured", "credit builder",
    "utilization", "statement date", "due date",
}


def _split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[\.\?!])\s+(?=[A-ZÁÉÍÓÚÑ¿¡])", text.strip())
    return [p.strip() for p in parts if p.strip()]


def _chunk_words(words: list[str], max_words: int, min_words: int) -> list[list[str]]:
    if len(words) <= max_words:
        return [words]
    chunks: list[list[str]] = []
    i = 0
    while i < len(words):
        remaining = len(words) - i
        if remaining <= max_words:
            chunks.append(words[i:])
            break
        # Buscar la coma o pausa natural más cercana entre min y max
        cut = i + max_words
        for j in range(i + min_words, min(i + max_words + 1, len(words))):
            if words[j - 1].endswith((",", ";", ":")):
                cut = j
        chunks.append(words[i:cut])
        i = cut
    return chunks


def detect_keywords(text: str) -> list[str]:
    """Extrae keywords que merecen destacado visual en el subtítulo."""
    found: set[str] = set()

    for pattern in (_NUMBER_PATTERN, _DOLLAR_PATTERN, _PERCENT_PATTERN):
        found.update(pattern.findall(text))

    for kw in DOMAIN_KEYWORDS:
        if kw.lower() in text.lower():
            # Recuperar la grafía real del texto si la encontramos
            m = re.search(re.escape(kw), text, re.IGNORECASE)
            if m:
                found.add(m.group(0))

    # Siglas en mayúsculas
    for m in _ACRONYM_PATTERN.findall(text):
        if m not in {"EE", "UU"} and len(m) >= 2:
            found.add(m)

    return sorted(found)


def segment_block(
    *,
    text: str,
    block_start_sec: int,
    block_duration_sec: int,
    starting_seg_id: int = 1,
) -> list[SubtitleSegment]:
    """Segmenta el texto de un bloque de audio en chunks de subtítulo."""
    sentences = _split_sentences(text)
    if not sentences:
        return []

    total_words = sum(len(s.split()) for s in sentences)
    if total_words == 0:
        return []

    sec_per_word = block_duration_sec / total_words
    segments: list[SubtitleSegment] = []
    seg_id = starting_seg_id
    cursor_sec = float(block_start_sec)

    for sentence in sentences:
        words = sentence.split()
        for chunk in _chunk_words(words, MAX_SEG_WORDS, MIN_SEG_WORDS):
            chunk_text = " ".join(chunk)
            duration = min(MAX_SEG_DURATION_SEC, max(1.0, len(chunk) * sec_per_word))
            keywords = detect_keywords(chunk_text)
            segments.append(
                SubtitleSegment(
                    seg_id=seg_id,
                    timecode_start_sec=round(cursor_sec, 2),
                    duration_sec=round(duration, 2),
                    text=chunk_text,
                    highlight_keywords=keywords,
                    motion_style="pop" if keywords else "none",
                )
            )
            seg_id += 1
            cursor_sec += duration

    return segments
