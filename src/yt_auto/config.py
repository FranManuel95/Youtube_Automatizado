"""Carga centralizada de configuración desde variables de entorno."""

from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Anthropic
    anthropic_api_key: str = ""
    anthropic_model_sonnet: str = "claude-sonnet-4-6"
    anthropic_model_opus: str = "claude-opus-4-7"

    # Gemini
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-pro"

    # ElevenLabs
    elevenlabs_api_key: str = ""
    elevenlabs_voice_id: str = ""
    elevenlabs_model_id: str = "eleven_multilingual_v2"

    # Visuales
    nanobanana_api_key: str = ""
    seedance_api_key: str = ""
    topmedia_api_key: str = ""

    # YouTube
    youtube_client_secrets_file: str = "client_secret.json"
    youtube_token_file: str = "token.json"
    youtube_channel_id: str = ""

    # Proyecto
    project_name: str = "canal_demo"
    default_language: str = "es"
    target_markets: str = "US-Hispanic,EN-US"
    default_niche: str = ""
    content_format: str = "long_form"  # long_form | masterclass | shorts | mixed
    target_duration_min: int = 12

    @property
    def target_markets_list(self) -> list[str]:
        return [m.strip() for m in self.target_markets.split(",") if m.strip()]

    @property
    def assets_dir(self) -> Path:
        return ROOT_DIR / "assets"

    @property
    def output_dir(self) -> Path:
        return ROOT_DIR / "output"


def get_settings() -> Settings:
    return Settings()
