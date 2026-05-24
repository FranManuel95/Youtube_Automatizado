"""Orquestador del pipeline end-to-end.

Filosofía (anti-purga): automatiza lo repetitivo SIN criterio (audio,
packaging, tracking) y marca como `manual_required` lo que da valor humano
y protege de la purga de YouTube 2026 (guion verificado, screencast real,
montaje, revisión anti-AI-Slop).

NO es generación de video 100% automática — eso es exactamente el perfil
que YouTube purga. Es "producción asistida": el pipeline deja todo listo
excepto lo que requiere tu criterio y tu pantalla.

Etapas:
- script: AUTOMATED si se pasa un ScriptReport ya generado; si no,
  MANUAL_REQUIRED (genera el prompt para Claude y espera tu ingest).
- audio: AUTOMATED (genera el plan de bloques; la síntesis real con
  ElevenLabs es un paso aparte con `audio synth`).
- packaging: AUTOMATED (descripción + afiliados + UTMs deterministas).
- screencast / editing / thumbnail: MANUAL_REQUIRED siempre (tu foso).
"""

from __future__ import annotations

from pydantic import BaseModel

from yt_auto.pipeline.project import Stage, StageStatus, VideoProject
from yt_auto.publishing.niche_profile import resolve_profile


class PipelinePlan(BaseModel):
    """Resultado de un `pipeline run`: estado de cada etapa + próximos pasos."""

    project_id: str
    automated_stages: list[str]
    manual_stages: list[str]
    next_actions: list[str]


def start_project(*, topic: str, niche_profile_id: str | None = None) -> VideoProject:
    """Crea un VideoProject nuevo con todas las etapas en pending."""
    if niche_profile_id is None:
        niche_profile_id = resolve_profile(topic).id
    project = VideoProject(topic=topic, niche_profile_id=niche_profile_id)
    for stage in Stage:
        project.set_stage(stage, StageStatus.pending)
    project.save()
    return project


def plan_pipeline(project: VideoProject, *, has_script: bool) -> PipelinePlan:
    """Calcula qué etapas son automatizables y cuáles requieren intervención.

    `has_script`: si el usuario ya ha provisto un ScriptReport (vía la etapa
    script-ingest), el guion se considera listo. Si no, queda manual.
    """
    automated: list[str] = []
    manual: list[str] = []
    actions: list[str] = []

    # script
    if has_script:
        project.set_stage(Stage.script, StageStatus.done, note="ScriptReport provisto")
        automated.append("script")
    else:
        project.set_stage(
            Stage.script,
            StageStatus.manual_required,
            note="Genera el guion (Claude) y haz `script ingest`",
        )
        manual.append("script")
        actions.append(
            "Generar guion: `yt-auto script prompt <topic> --niche <n>` → "
            "pegar a Claude → `yt-auto script ingest <respuesta.json>`"
        )

    # audio (automatizable: plan determinista; synth requiere API key aparte)
    project.set_stage(
        Stage.audio,
        StageStatus.automated if has_script else StageStatus.pending,
        note="audio plan determinista; synth con ElevenLabs aparte",
    )
    if has_script:
        automated.append("audio")
        actions.append(
            "Sintetizar voz: `yt-auto audio synth <plan.json>` "
            "(requiere ELEVENLABS_API_KEY)"
        )

    # packaging (100% automatizable: descripción + afiliados + UTMs)
    project.set_stage(
        Stage.publishing,
        StageStatus.automated if has_script else StageStatus.pending,
        note="descripción + afiliados + UTMs deterministas",
    )
    if has_script:
        automated.append("packaging")

    # MANUALES siempre (foso anti-purga)
    for stage, note, action in [
        (
            Stage.screencast,
            "Grabar pantalla real (OBS). NO automatizable sin caer en purga.",
            "Grabar screencast del workflow en OBS (~1.5h)",
        ),
        (
            Stage.editing,
            "Montaje voz + screencast + subtítulos (DaVinci).",
            "Montar en DaVinci Resolve",
        ),
        (
            Stage.thumbnail,
            "Generar con Ideogram (semi-auto) + revisión humana.",
            "Generar thumbnail con Ideogram (prompt en el packaging)",
        ),
    ]:
        project.set_stage(stage, StageStatus.manual_required, note=note)
        manual.append(stage.value)
        actions.append(action)

    project.save()
    return PipelinePlan(
        project_id=project.project_id,
        automated_stages=automated,
        manual_stages=manual,
        next_actions=actions,
    )
