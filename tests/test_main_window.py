from __future__ import annotations

from PySide6.QtCore import Qt

from core.signals import AppSignals
from core.state import AppState
from ui.main_window import MainWindow


def test_main_window_navigation(qtbot) -> None:
    state = AppState()
    signals = AppSignals()
    window = MainWindow(state, signals)
    qtbot.addWidget(window)
    window.show()
    assert window.windowTitle().startswith("ULTRON")
    window._navigate("settings")
    assert state.current_view == "settings"
    assert window._views.currentIndex() == window._view_index["settings"]


def test_command_submission_updates_conversation(qtbot) -> None:
    state = AppState()
    signals = AppSignals()
    window = MainWindow(state, signals)
    qtbot.addWidget(window)
    window.command_input.setText("status report")
    window._submit_command()
    assert state.last_command == "status report"
    assert "status report" in window.conversation.text()
    assert window.command_input.text() == ""


def test_emergency_stop_blocks_commands(qtbot) -> None:
    state = AppState()
    signals = AppSignals()
    window = MainWindow(state, signals)
    qtbot.addWidget(window)
    qtbot.mouseClick(window.emergency_button, Qt.MouseButton.LeftButton)
    assert state.emergency_stopped is True
    window.command_input.setText("open notepad")
    window._submit_command()
    assert state.last_command == ""
    assert "Emergency stop" in window.conversation.text()


def test_microphone_toggle_is_ui_only(qtbot) -> None:
    state = AppState()
    signals = AppSignals()
    window = MainWindow(state, signals)
    qtbot.addWidget(window)
    window._toggle_listening()
    assert state.listening is True
    window._stop_listening()
    assert state.listening is False
    assert state.microphone_status == "idle"
