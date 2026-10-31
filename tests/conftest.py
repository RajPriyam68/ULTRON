from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("ULTRON_LOG_LEVEL", "INFO")


@pytest.fixture(autouse=True)
def _reset_settings(tmp_path, monkeypatch):
    monkeypatch.setenv("ULTRON_DATA_DIR", str(tmp_path / "data"))
    from config.settings import reset_settings
    from core.logging import reset_logging

    reset_settings()
    reset_logging()
    yield
    reset_settings()
    reset_logging()
