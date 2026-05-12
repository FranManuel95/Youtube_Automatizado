"""Modo API de la etapa de audio.

Recoge un `AudioReport` ya generado por `build_report` (modo interactivo) y
materializa los MP3 llamando a la API de ElevenLabs, bloque a bloque.

Diseño:
- Idempotente por bloque: si el `.mp3` ya existe en disco y `--overwrite`
  no está activo, se salta esa llamada (ahorra créditos al reintentar).
- Pre-check de cuota: antes de sintetizar consulta `/v1/user/subscription`
  y aborta si los caracteres pendientes no caben en el ciclo actual.
- Compatible con la salida del modo interactivo: los MP3 se guardan en
  `output/audio/<base>/mp3/NN_<role>.mp3`, junto a los `.txt` que ya
  genera `storage.save_report`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from yt_auto.audio.client import ElevenLabsClient, Subscription
from yt_auto.audio.models import AudioReport, NarrationBlock


@dataclass(frozen=True)
class BlockSynthesisResult:
    block_id: int
    role: str
    path: Path
    characters_used: int
    skipped: bool  # True si el MP3 ya existía y no se regeneró


@dataclass(frozen=True)
class SynthesisReport:
    blocks: list[BlockSynthesisResult]
    total_characters_used: int
    subscription_before: Subscription | None
    output_dir: Path

    @property
    def generated_count(self) -> int:
        return sum(1 for b in self.blocks if not b.skipped)

    @property
    def skipped_count(self) -> int:
        return sum(1 for b in self.blocks if b.skipped)


class QuotaExceededError(RuntimeError):
    """Los chars pendientes superan los disponibles en el ciclo Free/Starter."""


def mp3_dir_for(report_base: Path) -> Path:
    """Directorio donde van los MP3 de un AudioReport ya persistido.

    `report_base` es el directorio sin extensión del reporte (el mismo
    que `storage.save_report` usa para `blocks/`).
    """
    return report_base / "mp3"


def synthesize_report(
    report: AudioReport,
    *,
    client: ElevenLabsClient,
    voice_id: str,
    output_base: Path,
    block_ids: list[int] | None = None,
    overwrite: bool = False,
    skip_quota_check: bool = False,
) -> SynthesisReport:
    """Sintetiza el `AudioReport` a MP3.

    Args:
        report: plan de audio generado por `build_report`.
        client: cliente de ElevenLabs ya configurado.
        voice_id: ID de voz del catálogo del usuario (no es `voice_preset_key`).
        output_base: directorio raíz del reporte (lo que devuelve
            `save_report` como `blocks_dir.parent`).
        block_ids: si se da, solo se sintetizan esos bloques (útil para probar
            con un único hook antes de gastar créditos en el plan completo).
        overwrite: si `False`, los MP3 ya presentes en disco se respetan.
        skip_quota_check: salta la consulta a `/v1/user/subscription`. Útil
            para tests, no para producción.
    """
    blocks = _select_blocks(report.plan.blocks, block_ids)
    if not blocks:
        raise ValueError("Ningún bloque seleccionado para sintetizar.")

    mp3_dir = mp3_dir_for(output_base)
    mp3_dir.mkdir(parents=True, exist_ok=True)

    pending_chars = sum(
        b.character_count for b in blocks if overwrite or not _mp3_path(mp3_dir, b).exists()
    )

    subscription: Subscription | None = None
    if not skip_quota_check:
        subscription = client.get_subscription()
        if pending_chars > subscription.characters_remaining:
            raise QuotaExceededError(
                f"Necesitas {pending_chars} chars pero quedan "
                f"{subscription.characters_remaining} en el ciclo "
                f"({subscription.tier}). Reduce con --block N o sube de plan."
            )

    results: list[BlockSynthesisResult] = []
    for block in blocks:
        path = _mp3_path(mp3_dir, block)
        if path.exists() and not overwrite:
            results.append(
                BlockSynthesisResult(
                    block_id=block.block_id,
                    role=block.role.value,
                    path=path,
                    characters_used=0,
                    skipped=True,
                )
            )
            continue

        audio_bytes = client.text_to_speech(
            voice_id=voice_id,
            text=block.text,
            model_id=report.plan.model_id,
            settings=block.suggested_settings,
        )
        path.write_bytes(audio_bytes)
        results.append(
            BlockSynthesisResult(
                block_id=block.block_id,
                role=block.role.value,
                path=path,
                characters_used=block.character_count,
                skipped=False,
            )
        )

    return SynthesisReport(
        blocks=results,
        total_characters_used=sum(r.characters_used for r in results),
        subscription_before=subscription,
        output_dir=mp3_dir,
    )


def _select_blocks(
    blocks: list[NarrationBlock], block_ids: list[int] | None
) -> list[NarrationBlock]:
    if block_ids is None:
        return list(blocks)
    wanted = set(block_ids)
    selected = [b for b in blocks if b.block_id in wanted]
    missing = wanted - {b.block_id for b in selected}
    if missing:
        raise ValueError(f"Bloques inexistentes en el plan: {sorted(missing)}")
    return selected


def _mp3_path(mp3_dir: Path, block: NarrationBlock) -> Path:
    return mp3_dir / f"{block.block_id:02d}_{block.role.value}.mp3"
