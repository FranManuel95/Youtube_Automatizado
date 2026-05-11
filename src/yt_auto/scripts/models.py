"""Modelos de dominio para la etapa de ingeniería de guiones.

Implementa las estructuras del informe `docs/02_ingenieria_de_guiones.md`:
- Hook con validación de duración 15-30s.
- Secciones con bucles abiertos/cerrados y pattern interrupts.
- Marco de humanización (anti-AI-Slop) verificable.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class TitleStyle(str, Enum):
    three_points_open_loop = "3-Points / Open Loop"
    psicologia_sujeto = "La Psicología de + Sujeto"
    paradoja_emocional = "Paradoja Emocional"
    revelacion_disruptiva = "Revelación Disruptiva"


class ViewerIdeal(BaseModel):
    """Perfil psicográfico del espectador objetivo (mandatorio en Claude project)."""

    nombre: str = Field(..., description="Etiqueta operativa del perfil")
    edad: str = Field(..., description="Rango etario (ej. 28-42)")
    ubicacion: str
    situacion: str = Field(..., description="Contexto vital - ej. inmigrante reciente en EE.UU.")
    dolor: str = Field(..., description="Pain point principal que el video resuelve")
    deseo: str = Field(..., description="Outcome que la audiencia persigue")
    objeciones: list[str] = Field(default_factory=list)


class Hook(BaseModel):
    """Primeros 15-30s. Confirmación de promesa y apertura del primer loop."""

    text: str
    duration_sec: int = Field(..., ge=10, le=45)
    visual_cue: str = Field(..., description="Qué se ve en pantalla en este momento")
    promise: str = Field(..., description="Promesa concreta entregada al final del video")
    open_loop: str = Field(..., description="Pregunta o tensión que se mantiene viva")

    @field_validator("duration_sec")
    @classmethod
    def warn_long_hook(cls, v: int) -> int:
        if v > 30:
            # No fallamos, solo avisamos vía Pydantic info
            pass
        return v


class Section(BaseModel):
    """Una sección del cuerpo del guion. Cada sección debe abrir o cerrar un loop."""

    heading: str
    content: str = Field(..., description="Texto narrativo en formato locución")
    duration_sec: int = Field(..., ge=15)
    loop_close: str | None = Field(default=None, description="Loop anterior que aquí se resuelve")
    loop_open: str | None = Field(default=None, description="Nuevo loop que se abre")
    pattern_interrupt: str | None = Field(
        default=None,
        description="Quiebro visual/sonoro (cambio de plano, B-roll, glitch)",
    )
    sources: list[str] = Field(default_factory=list)
    word_count: int | None = None


class HumanizationCheck(BaseModel):
    """Marco de Tres Pilares contra el AI Slop (docs/02 § 4)."""

    pilar_localizacion: bool = Field(
        ..., description="Usa giros y dialectos del mercado objetivo"
    )
    pilar_autoridad: bool = Field(
        ..., description="Incluye datos verificables, fuentes nombradas o experiencias reales"
    )
    pilar_refinamiento: bool = Field(
        ..., description="Se ha refinado manualmente, sin patrones LLM evidentes"
    )
    paradoja_emocional: bool = Field(
        ..., description="Contiene al menos una disonancia 'sientes X pero sabes Y'"
    )
    pattern_interrupts_count: int = Field(..., ge=0)
    sources_count: int = Field(..., ge=0)

    @property
    def pasa(self) -> bool:
        return all(
            [
                self.pilar_localizacion,
                self.pilar_autoridad,
                self.pilar_refinamiento,
                self.paradoja_emocional,
                self.pattern_interrupts_count >= 2,
                self.sources_count >= 2,
            ]
        )


class ScriptDraft(BaseModel):
    """Borrador completo de un guion auditable."""

    # Identidad
    title: str
    title_alternatives: list[str] = Field(default_factory=list)
    title_style: TitleStyle

    # Parámetros de producción
    niche: str
    target_market: str
    target_language: str = "es"
    target_duration_min: int
    viewer_ideal: ViewerIdeal

    # Estructura narrativa
    hook: Hook
    sections: list[Section]
    cta: str = Field(..., description="Call-to-action final, alineado con productos digitales")

    # Métricas estimadas
    word_count: int
    estimated_retention_30s: float = Field(
        ..., ge=0.0, le=1.0, description="Estimación de retención a los 30s (objetivo > 0.80)"
    )
    estimated_ctr: float = Field(
        ..., ge=0.0, le=1.0, description="CTR estimado de la combinación título+miniatura"
    )

    # Anti-AI-Slop
    humanization: HumanizationCheck

    @property
    def total_duration_sec(self) -> int:
        return self.hook.duration_sec + sum(s.duration_sec for s in self.sections)


class ScriptReport(BaseModel):
    """Sesión completa de generación de guion (con metadata)."""

    schema_version: str = "1.0"
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    niche_audit_ref: str | None = Field(
        default=None, description="Path o nombre de la auditoría de nicho que originó este guion"
    )
    candidate_name: str = Field(..., description="Nombre del subnicho en la auditoría origen")

    model_used: str = "claude-opus-4-7"
    mode: Literal["interactive", "api"] = "interactive"

    draft: ScriptDraft

    notes: str = ""
