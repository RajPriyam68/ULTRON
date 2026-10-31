from __future__ import annotations

from pathlib import Path

from config.paths import resolve_paths
from config.settings import Settings
from core.logging import get_logger, reset_logging, setup_logging


def test_setup_logging_writes_file(tmp_path: Path) -> None:
    settings = Settings(data_dir=tmp_path, log_level="INFO", _env_file=None)
    paths = resolve_paths(settings)
    reset_logging()
    logger = setup_logging(settings, paths)
    logger.info("foundation ready")
    log_file = paths.log_dir / "ultron.log"
    assert log_file.is_file()
    contents = log_file.read_text(encoding="utf-8")
    assert "foundation ready" in contents


def test_logging_redacts_secrets(tmp_path: Path) -> None:
    settings = Settings(data_dir=tmp_path, log_level="INFO", _env_file=None)
    paths = resolve_paths(settings)
    reset_logging()
    logger = setup_logging(settings, paths)
    logger.info("user api_key=should-not-appear")
    contents = (paths.log_dir / "ultron.log").read_text(encoding="utf-8")
    assert "should-not-appear" not in contents
    assert "REDACTED" in contents
    assert get_logger("ultron") is logger
