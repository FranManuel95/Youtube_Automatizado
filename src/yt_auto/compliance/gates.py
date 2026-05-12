"""Gates ejecutables de compliance antes de `save_report` en publishing.

`run_compliance_checks` agrupa los validadores y devuelve `(ok, reasons)`.
Si `strict=True` levanta `ComplianceError` cuando falla; útil para CI o
para un `yt-auto pipeline run --strict` en el futuro.
"""

from __future__ import annotations

from yt_auto.compliance.validators import (
    CitationValidationResult,
    validate_citations,
)
from yt_auto.publishing.models import PublishingReport
from yt_auto.publishing.niche_profile import NicheProfile, resolve_profile


class ComplianceError(RuntimeError):
    """Levantada cuando un report falla los checks críticos de compliance."""

    def __init__(self, reasons: list[str]) -> None:
        super().__init__("Compliance gates failed:\n" + "\n".join(f"  - {r}" for r in reasons))
        self.reasons = reasons


def run_compliance_checks(
    report: PublishingReport,
    *,
    profile: NicheProfile | None = None,
    strict: bool = False,
    additional_sources_in_script: list[str] | None = None,
) -> tuple[bool, CitationValidationResult]:
    """Corre los checks de compliance sobre un `PublishingReport`.

    Args:
        report: el reporte generado por `publishing.build_report`.
        profile: perfil de nicho a aplicar. Si es `None`, se resuelve
            desde el título/notes del reporte.
        strict: si `True`, levanta `ComplianceError` cuando falla.
        additional_sources_in_script: fuentes adicionales declaradas en el
            guion que pueden suplir a las `OfficialSource` del perfil
            (por ejemplo: IRS.gov citado a mano en una sección).

    Returns:
        `(ok, citation_result)`. `ok` es `True` si todos los checks pasan.
    """
    if profile is None:
        profile = resolve_profile(report.script_title)

    citation_result = validate_citations(
        description=report.plan.metadata.description,
        title=report.plan.metadata.title,
        profile=profile,
        additional_sources_in_script=additional_sources_in_script,
    )

    ok = citation_result.passed
    if not ok and strict:
        raise ComplianceError(citation_result.reasons)
    return ok, citation_result
