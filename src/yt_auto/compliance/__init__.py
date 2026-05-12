"""Etapa transversal - Compliance anti-AI-Slop y disclosure de IA.

Defensa contra la oleada de purgas YouTube 2026 (4.7B views borradas en
enero 2026). Tres componentes:

1. **AIDisclosureRenderer**: bloque normalizado de transparencia que se
   inyecta en la descripción y se declara en metadata Studio
   (`altered_content=true` cuando publishing/api.py exista).
2. **CitationValidator**: bloquea reportes que NO citen al menos una
   `OfficialSource` del perfil de nicho. Sello agregador-educador.
3. **HumanReviewLog**: registro persistente de las horas reales de
   edición humana por video. Trazabilidad para apelaciones futuras.

Esta etapa no produce un artefacto independiente: se invoca desde
`publishing/builder.py` como gate previo al `save_report`. Si falla,
levanta `ComplianceError` con la lista de problemas.
"""

from __future__ import annotations

from yt_auto.compliance.disclosures import (
    DEFAULT_AI_DISCLOSURE_ES,
    AIDisclosure,
    render_disclosure_block,
)
from yt_auto.compliance.gates import ComplianceError, run_compliance_checks
from yt_auto.compliance.human_review import (
    HumanReviewEntry,
    HumanReviewLog,
    append_review_entry,
    load_review_log,
)
from yt_auto.compliance.validators import (
    CitationValidationResult,
    validate_citations,
)

__all__ = [
    "AIDisclosure",
    "CitationValidationResult",
    "ComplianceError",
    "DEFAULT_AI_DISCLOSURE_ES",
    "HumanReviewEntry",
    "HumanReviewLog",
    "append_review_entry",
    "load_review_log",
    "render_disclosure_block",
    "run_compliance_checks",
    "validate_citations",
]
