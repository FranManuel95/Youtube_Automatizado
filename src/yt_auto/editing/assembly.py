"""Ensamblaje determinista del plan de edición.

Toma `ScriptReport`, `AudioReport` y `VisualReport` y construye un
`EditingReport` con:
- Timeline ordenado de eventos.
- Subtítulos dinámicos sincronizados.
- DAI anchors detectados entre secciones.
- Auditoría de la regla de 3 segundos.
"""

from __future__ import annotations

from yt_auto.audio.models import AudioReport, BlockRole
from yt_auto.editing.models import (
    DAIAnchor,
    EditingPlan,
    EditingReport,
    EventType,
    Importance,
    ThreeSecondRuleViolation,
    TimelineEvent,
    TransitionStyle,
)
from yt_auto.editing.subtitles import segment_block
from yt_auto.scripts.models import ScriptReport
from yt_auto.visuals.models import VisualReport

THREE_SECOND_THRESHOLD = 3


def _build_timeline(
    audio: AudioReport,
    visuals: VisualReport | None,
) -> tuple[list[TimelineEvent], list[TimelineEvent]]:
    """Genera eventos de timeline + transiciones."""
    events: list[TimelineEvent] = []
    transitions: list[TimelineEvent] = []
    cursor = 0
    event_id = 1

    # Capa de audio: orden estricto por block_id
    for block in audio.plan.blocks:
        events.append(
            TimelineEvent(
                event_id=event_id,
                timecode_sec=cursor,
                duration_sec=block.target_duration_sec,
                event_type=EventType.audio_block,
                description=f"Audio {block.heading} ({block.character_count} chars)",
                source_ref=f"audio.block_{block.block_id:02d}",
                importance=Importance.critical,
            )
        )
        event_id += 1
        cursor += block.target_duration_sec

    # Capa de video: usa los timecodes de cada shot
    if visuals:
        prev_end = 0
        for shot in visuals.shots:
            events.append(
                TimelineEvent(
                    event_id=event_id,
                    timecode_sec=shot.timecode_start_sec,
                    duration_sec=shot.duration_sec,
                    event_type=EventType.video_clip,
                    description=f"{shot.shot_type.value}: {shot.description[:80]}",
                    source_ref=f"visuals.shot_{shot.shot_id:02d}",
                    importance=Importance.critical if shot.pattern_interrupt else Importance.recommended,
                )
            )
            event_id += 1

            # Transición entre shots
            if shot.timecode_start_sec > 0:
                style = TransitionStyle.glitch if shot.pattern_interrupt else TransitionStyle.cut
                transitions.append(
                    TimelineEvent(
                        event_id=event_id,
                        timecode_sec=shot.timecode_start_sec,
                        duration_sec=0,
                        event_type=EventType.transition,
                        description=f"Transición {style.value} desde shot anterior",
                        source_ref=f"transition.before_shot_{shot.shot_id:02d}",
                        importance=Importance.recommended,
                    )
                )
                event_id += 1
            prev_end = shot.timecode_start_sec + shot.duration_sec

    return events, transitions


def _build_subtitles(audio: AudioReport):
    segments = []
    seg_id = 1
    cursor = 0
    for block in audio.plan.blocks:
        block_segments = segment_block(
            text=block.text,
            block_start_sec=cursor,
            block_duration_sec=block.target_duration_sec,
            starting_seg_id=seg_id,
        )
        segments.extend(block_segments)
        seg_id += len(block_segments)
        cursor += block.target_duration_sec
    return segments


def _detect_dai_anchors(script: ScriptReport, audio: AudioReport) -> list[DAIAnchor]:
    """Identifica puntos naturales entre secciones donde insertar ads."""
    anchors: list[DAIAnchor] = []
    cursor = 0

    # Recorre los bloques de audio en orden
    for block in audio.plan.blocks:
        cursor += block.target_duration_sec
        # Solo entre secciones (no después del hook ni antes del CTA)
        if block.role == BlockRole.section:
            # No el último (CTA debería ser el último)
            anchors.append(
                DAIAnchor(
                    timecode_sec=cursor,
                    minimum_break_sec=5,
                    rationale=(
                        f"Punto natural tras '{block.heading}' donde un loop se "
                        f"acaba de cerrar antes de abrir el siguiente. Pausa de 5s "
                        f"no rompe la retención."
                    ),
                    section_after=f"sección siguiente",
                )
            )

    # Heurística: máximo 2 anchors por video largo, repartidos.
    # Quitamos el último (suele ser justo antes del CTA).
    if len(anchors) > 2:
        # Tomar el ~33% y ~66% del timeline
        n = len(anchors)
        keep = [anchors[n // 3], anchors[(2 * n) // 3]]
        anchors = keep

    return anchors


def _audit_three_second_rule(
    visuals: VisualReport | None,
    total_duration_sec: int,
) -> tuple[int, list[ThreeSecondRuleViolation]]:
    """Detecta tramos sin cambio visual >3s.

    Un cambio visual es: un nuevo shot, un pattern interrupt, o (idealmente)
    un B-roll/inserción. En modo estricto solo cuentan shots.
    """
    if not visuals or not visuals.shots:
        return total_duration_sec, [
            ThreeSecondRuleViolation(
                start_sec=0,
                end_sec=total_duration_sec,
                duration_sec=total_duration_sec,
                suggested_fix=(
                    "No hay shots definidos. Genera un plan visual en la etapa 4 "
                    "antes de editar."
                ),
            )
        ]

    # Ordenamos por timecode
    sorted_shots = sorted(visuals.shots, key=lambda s: s.timecode_start_sec)

    violations: list[ThreeSecondRuleViolation] = []
    longest_gap = 0

    for shot in sorted_shots:
        # Para shots largos asumimos que el editor introducirá B-roll cada 3s.
        # Pero si el shot dura >3s y NO es pattern_interrupt explícito, marcamos.
        if shot.duration_sec > THREE_SECOND_THRESHOLD and not shot.pattern_interrupt:
            longest_gap = max(longest_gap, shot.duration_sec)
            if shot.duration_sec > 8:
                violations.append(
                    ThreeSecondRuleViolation(
                        start_sec=shot.timecode_start_sec,
                        end_sec=shot.timecode_start_sec + shot.duration_sec,
                        duration_sec=shot.duration_sec,
                        suggested_fix=(
                            f"Shot {shot.shot_id:02d} dura {shot.duration_sec}s. "
                            f"Subdividir en sub-shots de ≤3s con zoom, B-roll, "
                            f"text overlay o pattern interrupt cada 3s en CapCut/Filmora."
                        ),
                    )
                )

    return longest_gap, violations


def build_report(
    *,
    script: ScriptReport,
    audio: AudioReport,
    visuals: VisualReport | None = None,
    script_ref: str,
    audio_ref: str | None = None,
    visuals_ref: str | None = None,
) -> EditingReport:
    timeline, transitions = _build_timeline(audio, visuals)
    subtitles = _build_subtitles(audio)
    dai_anchors = _detect_dai_anchors(script, audio)
    longest_gap, violations = _audit_three_second_rule(
        visuals, audio.plan.estimated_duration_sec
    )

    notes_parts: list[str] = []
    if violations:
        notes_parts.append(
            f"⚠ {len(violations)} tramos violan la regla de 3 segundos. "
            f"El más largo: {longest_gap}s. Subdividir manualmente en CapCut."
        )
    if not visuals:
        notes_parts.append(
            "No se proporcionó plan visual. La timeline solo contiene audio + subs."
        )

    plan = EditingPlan(
        timeline=timeline,
        subtitles=subtitles,
        dai_anchors=dai_anchors,
        transitions=transitions,
        longest_static_gap_sec=longest_gap,
        three_second_violations=violations,
    )

    return EditingReport(
        script_ref=script_ref,
        audio_ref=audio_ref,
        visuals_ref=visuals_ref,
        script_title=script.draft.title,
        plan=plan,
        notes="\n".join(notes_parts),
    )
