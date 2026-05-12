from yt_auto.config import Settings


def test_settings_defaults():
    s = Settings(_env_file=None)
    assert s.anthropic_model_sonnet == "claude-sonnet-4-6"
    assert s.anthropic_model_opus == "claude-opus-4-7"
    assert s.elevenlabs_model_id == "eleven_v3"
    assert "US-Hispanic" in s.target_markets_list
