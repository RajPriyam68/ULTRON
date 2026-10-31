from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config.paths import PathLayout
from config.settings import Settings

_SECRET_KEYS = ("api_key", "apikey", "password", "token", "secret", "authorization")
_configured = False


class RedactingFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        lowered = message.lower()
        if any(key in lowered for key in _SECRET_KEYS):
            return "[REDACTED] potential secret content omitted from log"
        return message


def setup_logging(settings: Settings, paths: PathLayout) -> logging.Logger:
    global _configured
    logger = logging.getLogger("ultron")
    logger.setLevel(getattr(logging, settings.log_level, logging.INFO))
    if _configured:
        return logger

    formatter = RedactingFormatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    console.setLevel(logger.level)

    log_file = paths.log_dir / "ultron.log"
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=2_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logger.level)

    logger.addHandler(console)
    logger.addHandler(file_handler)
    logger.propagate = False
    _configured = True
    logger.info("Logging initialized at %s", settings.log_level)
    return logger


def get_logger(name: str = "ultron") -> logging.Logger:
    return logging.getLogger(name)


def reset_logging() -> None:
    global _configured
    logger = logging.getLogger("ultron")
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)
    _configured = False


def log_path(paths: PathLayout) -> Path:
    return paths.log_dir / "ultron.log"
