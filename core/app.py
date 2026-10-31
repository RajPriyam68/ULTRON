from __future__ import annotations

import logging
import sys
from pathlib import Path

from PySide6.QtGui import QFont, QGuiApplication
from PySide6.QtWidgets import QApplication

from config.paths import PathLayout, resolve_paths
from config.settings import Settings, get_settings
from core.constants import APP_NAME, ORGANIZATION_DOMAIN, ORGANIZATION_NAME
from core.logging import setup_logging
from core.signals import AppSignals
from core.state import AppState
from ui.theme import apply_theme

LOGGER = logging.getLogger("ultron.app")


class UltronApplication(QApplication):
    def __init__(
        self,
        argv: list[str],
        settings: Settings | None = None,
        paths: PathLayout | None = None,
    ) -> None:
        super().__init__(argv)
        self.setApplicationName(APP_NAME)
        self.setOrganizationName(ORGANIZATION_NAME)
        self.setOrganizationDomain(ORGANIZATION_DOMAIN)
        self.setQuitOnLastWindowClosed(True)

        self.settings = settings or get_settings()
        self.paths = paths or resolve_paths(self.settings)
        self.state = AppState()
        self.signals = AppSignals()
        self.logger = setup_logging(self.settings, self.paths)

        apply_theme(self)
        self._configure_font()
        LOGGER.info("ULTRON Sprint %s starting", self.settings.sprint)

    def _configure_font(self) -> None:
        font = QFont("Segoe UI")
        if not font.exactMatch():
            font = QFont("Noto Sans")
        if not font.exactMatch():
            font = QFont("DejaVu Sans")
        font.setPointSize(10)
        self.setFont(font)

    def engage_emergency_stop(self) -> None:
        if self.state.emergency_stopped:
            return
        self.state.trigger_emergency_stop()
        self.signals.emergency_stop.emit()
        self.signals.status_message.emit("Emergency stop engaged")
        LOGGER.warning("Emergency stop engaged")


def create_application(argv: list[str] | None = None) -> UltronApplication:
    args = argv if argv is not None else sys.argv
    settings = get_settings()
    paths = resolve_paths(settings)
    return UltronApplication(args, settings=settings, paths=paths)


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def screens() -> int:
    return len(QGuiApplication.screens())
