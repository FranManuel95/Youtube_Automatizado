"""Cliente HTTP de ElevenLabs.

Wrapper fino sobre `httpx.Client` para los tres endpoints que necesita el
pipeline: listar voces, consultar la suscripción (chars disponibles) y
sintetizar texto a MP3. No usa la lib oficial `elevenlabs` para mantener
control de errores, timeouts y testabilidad con `httpx.MockTransport`.
"""

from __future__ import annotations

from typing import Self

import httpx
from pydantic import BaseModel, Field
from tenacity import (
    Retrying,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from yt_auto.audio.models import VoiceSettings

_DEFAULT_BASE_URL = "https://api.elevenlabs.io"
_DEFAULT_TIMEOUT = 120.0
_RETRYABLE_STATUS = {429, 500, 502, 503, 504}


class ElevenLabsError(RuntimeError):
    """Error devuelto por la API de ElevenLabs."""

    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(f"ElevenLabs {status_code}: {message}")
        self.status_code = status_code
        self.message = message


class RemoteVoice(BaseModel):
    """Voz tal y como la devuelve `GET /v1/voices`."""

    voice_id: str
    name: str
    category: str | None = None
    description: str | None = None
    labels: dict[str, str] = Field(default_factory=dict)
    preview_url: str | None = None

    @property
    def language(self) -> str | None:
        return self.labels.get("language") or self.labels.get("accent")

    @property
    def gender(self) -> str | None:
        return self.labels.get("gender")


class Subscription(BaseModel):
    """Subconjunto de `GET /v1/user/subscription` que nos interesa."""

    tier: str
    character_count: int = Field(..., description="Caracteres consumidos en el ciclo")
    character_limit: int = Field(..., description="Tope del ciclo")

    @property
    def characters_remaining(self) -> int:
        return max(0, self.character_limit - self.character_count)


class ElevenLabsClient:
    """Cliente sincrónico para ElevenLabs.

    Diseñado para ser inyectable en tests: el caller puede pasar un
    `transport` (p. ej. `httpx.MockTransport`) en vez de hablar con la
    red real.

    Reintenta automáticamente 429 y 5xx con backoff exponencial. Los 4xx
    no-429 se propagan inmediatamente (key inválida, voice_id inválido).
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = _DEFAULT_TIMEOUT,
        transport: httpx.BaseTransport | None = None,
        max_attempts: int = 4,
    ) -> None:
        if not api_key:
            raise ValueError("ELEVENLABS_API_KEY vacía. Configúrala en .env.")
        self._client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            transport=transport,
            headers={
                "xi-api-key": api_key,
                "accept": "application/json",
            },
        )
        self._max_attempts = max_attempts

    def _retrying(self) -> Retrying:
        return Retrying(
            stop=stop_after_attempt(self._max_attempts),
            wait=wait_exponential(multiplier=1, min=2, max=30),
            retry=retry_if_exception(
                lambda e: isinstance(e, ElevenLabsError)
                and e.status_code in _RETRYABLE_STATUS
            ),
            reraise=True,
        )

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def close(self) -> None:
        self._client.close()

    # ------------------------------------------------------------------
    # Endpoints
    # ------------------------------------------------------------------

    def list_voices(self) -> list[RemoteVoice]:
        for attempt in self._retrying():
            with attempt:
                response = self._client.get("/v1/voices")
                self._raise_for_status(response)
        payload = response.json()
        return [RemoteVoice.model_validate(v) for v in payload.get("voices", [])]

    def get_subscription(self) -> Subscription:
        for attempt in self._retrying():
            with attempt:
                response = self._client.get("/v1/user/subscription")
                self._raise_for_status(response)
        return Subscription.model_validate(response.json())

    def text_to_speech(
        self,
        *,
        voice_id: str,
        text: str,
        model_id: str,
        settings: VoiceSettings,
    ) -> bytes:
        """Sintetiza `text` con la voz dada y devuelve los bytes del MP3."""
        if not voice_id:
            raise ValueError(
                "voice_id vacío. Fíjalo en .env como ELEVENLABS_VOICE_ID "
                "o pásalo explícito (usa `yt-auto audio voices --remote` para verlos)."
            )
        body = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": settings.stability,
                "similarity_boost": settings.similarity_boost,
                "style": settings.style,
                "use_speaker_boost": settings.use_speaker_boost,
            },
        }
        for attempt in self._retrying():
            with attempt:
                response = self._client.post(
                    f"/v1/text-to-speech/{voice_id}",
                    json=body,
                    headers={"accept": "audio/mpeg"},
                )
                self._raise_for_status(response)
        return response.content

    # ------------------------------------------------------------------
    # Internos
    # ------------------------------------------------------------------

    @staticmethod
    def _raise_for_status(response: httpx.Response) -> None:
        if response.is_success:
            return
        message = ""
        try:
            data = response.json()
            detail = data.get("detail") if isinstance(data, dict) else None
            if isinstance(detail, dict):
                message = detail.get("message") or detail.get("status") or str(detail)
            elif isinstance(detail, str):
                message = detail
            else:
                message = response.text
        except ValueError:
            message = response.text
        raise ElevenLabsError(response.status_code, message or response.reason_phrase)
