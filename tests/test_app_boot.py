from __future__ import annotations

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from core.app import UltronApplication
from core.signals import AppSignals
from core.state import AppState
from ui.main_window import MainWindow


def test_application_window_shows(qtbot) -> None:
    window = MainWindow(AppState(), AppSignals())
    qtbot.addWidget(window)
    window.show()
    assert window.isVisible()
    assert window.reactor.isVisible()
    assert window.waveform.isVisible()
    assert window.emergency_button.text() == "EMERGENCY STOP"
    assert len(window._nav_buttons) == 11


def test_ultron_application_class_is_qapplication_subclass() -> None:
    assert issubclass(UltronApplication, QApplication)
    assert hasattr(UltronApplication, "engage_emergency_stop")


def test_quit_timer_pattern() -> None:
    timer = QTimer()
    timer.setSingleShot(True)
    assert timer.isSingleShot()
