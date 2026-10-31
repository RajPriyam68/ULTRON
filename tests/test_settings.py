from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from config.paths import resolve_paths
from config.settings import Settings, get_settings, reset_settings


def test_default_settings() -> None:
    settings = Settings(_env_file=None)
    assert settings.app_name == "ULTRON"
    assert settings.sprint == 0
    assert settings.log_level == "INFO"
    assert settings.window_width >= 1024


def test_log_level_is_validated() -> None:
    with pytest.raises(ValidationError):
        Settings(log_level="NOISE", _env_file=None)


def test_get_settings_is_cached(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ULTRON_LOG_LEVEL", "DEBUG")
    reset_settings()
    first = get_settings()
    second = get_settings()
    assert first is second
    assert first.log_level == "DEBUG"


def test_resolve_paths_creates_directories(tmp_path: Path) -> None:
    settings = Settings(data_dir=tmp_path / "ultron-data", _env_file=None)
    layout = resolve_paths(settings)
    assert layout.log_dir.is_dir()
    assert layout.audit_dir.is_dir()
    assert layout.db_path.parent == layout.data_dir
