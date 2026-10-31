from __future__ import annotations

from datetime import UTC, datetime

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from core.constants import APP_NAME, APP_VERSION, CURRENT_SPRINT, NAV_ITEMS
from core.signals import AppSignals
from core.state import AppState
from ui.views.placeholder import PlaceholderView
from ui.widgets.reactor import ReactorWidget
from ui.widgets.resource_meter import ResourceMeter
from ui.widgets.status_chip import StatusChip
from ui.widgets.waveform import WaveformWidget

try:
    import psutil
except ImportError:  # pragma: no cover - optional at import time
    psutil = None


VIEW_NOTES = {
    "dashboard": "Sprint 0 command center is live. Later sprints add voice, tools, and memory.",
    "voice": "Voice capture, Faster-Whisper, and Piper TTS arrive in Sprint 1.",
    "chat": "Hybrid Ollama and cloud routing arrive in Sprint 3.",
    "files": "Approved file operations arrive in Sprint 2.",
    "apps": "Registered application launch and window control arrive in Sprint 2.",
    "automation": "Multi-step task planning and verification arrive in Sprint 4.",
    "developer": "Project registry, Git, and approved servers arrive in Sprint 5.",
    "memory": "SQLite memory and conversation history arrive in Sprint 6.",
    "history": "Task and conversation history arrive in Sprint 6.",
    "monitor": "Live process inspection expands in Sprint 2. CPU/RAM meters are active now.",
    "settings": "Preferences, voice, and security controls expand through Sprint 7.",
}


class MainWindow(QMainWindow):
    def __init__(self, state: AppState, signals: AppSignals, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.state = state
        self.signals = signals
        self._nav_buttons: dict[str, QPushButton] = {}
        self.setWindowTitle(f"{APP_NAME}  //  Sprint {CURRENT_SPRINT}")
        self.setMinimumSize(1180, 740)
        self.resize(1440, 900)

        root = QWidget()
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(16, 16, 16, 12)
        outer.setSpacing(12)

        body = QHBoxLayout()
        body.setSpacing(12)
        body.addWidget(self._build_sidebar(), 0)
        body.addWidget(self._build_center(), 1)
        body.addWidget(self._build_right_rail(), 0)
        outer.addLayout(body, 1)
        outer.addWidget(self._build_status_bar())

        self.signals.emergency_stop.connect(self._on_emergency_stop)
        self.signals.navigation_changed.connect(self._on_navigation)
        self.signals.status_message.connect(self._set_status)
        self.signals.command_submitted.connect(self._on_command)
        self.signals.resource_updated.connect(self._on_resources)

        self._resource_timer = QTimer(self)
        self._resource_timer.timeout.connect(self._poll_resources)
        self._resource_timer.start(2000)
        self._poll_resources()
        self._navigate("dashboard")

    def _build_sidebar(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("Sidebar")
        frame.setFixedWidth(236)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 18, 16, 16)
        layout.setSpacing(6)
        brand = QLabel(APP_NAME)
        brand.setObjectName("BrandLabel")
        subtitle = QLabel("COMMAND CENTER")
        subtitle.setObjectName("MutedLabel")
        layout.addWidget(brand)
        layout.addWidget(subtitle)
        layout.addSpacing(12)

        for key, title, _hint in NAV_ITEMS:
            button = QPushButton(title)
            button.setObjectName("NavButton")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setProperty("nav_key", key)
            button.clicked.connect(lambda _checked=False, item=key: self._navigate(item))
            self._nav_buttons[key] = button
            layout.addWidget(button)
        layout.addStretch(1)
        version = QLabel(f"v{APP_VERSION}  ·  S{CURRENT_SPRINT}")
        version.setObjectName("MutedLabel")
        layout.addWidget(version)
        return frame

    def _build_center(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("CenterStage")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)

        header = QHBoxLayout()
        title = QLabel("AI CORE")
        title.setObjectName("TitleLabel")
        self._scan_label = QLabel("SCANNING LOCAL SYSTEMS")
        self._scan_label.setObjectName("CyanLabel")
        header.addWidget(title)
        header.addStretch(1)
        header.addWidget(self._scan_label)
        layout.addLayout(header)

        self.reactor = ReactorWidget()
        layout.addWidget(self.reactor, 0, Qt.AlignmentFlag.AlignHCenter)

        self.waveform = WaveformWidget()
        layout.addWidget(self.waveform)

        self.conversation = QLabel("ULTRON online. Voice and tools are staged for later sprints.")
        self.conversation.setWordWrap(True)
        self.conversation.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.conversation)

        self._views = QStackedWidget()
        self._view_index: dict[str, int] = {}
        for key, title, hint in NAV_ITEMS:
            view = PlaceholderView(title, hint, VIEW_NOTES[key])
            index = self._views.addWidget(view)
            self._view_index[key] = index
        layout.addWidget(self._views, 1)

        command_row = QHBoxLayout()
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Enter a command. Voice arrives in Sprint 1.")
        self.command_input.returnPressed.connect(self._submit_command)
        self.mic_button = QPushButton("MIC")
        self.mic_button.setObjectName("PrimaryButton")
        self.mic_button.setFixedWidth(88)
        self.mic_button.clicked.connect(self._toggle_listening)
        self.stop_listen_button = QPushButton("STOP")
        self.stop_listen_button.setFixedWidth(88)
        self.stop_listen_button.clicked.connect(self._stop_listening)
        command_row.addWidget(self.command_input, 1)
        command_row.addWidget(self.mic_button)
        command_row.addWidget(self.stop_listen_button)
        layout.addLayout(command_row)
        return frame

    def _build_right_rail(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("RightRail")
        frame.setFixedWidth(268)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 18, 16, 16)
        layout.setSpacing(12)

        heading = QLabel("STATUS")
        heading.setObjectName("TitleLabel")
        layout.addWidget(heading)
        self.model_chip = StatusChip("AI model", "offline")
        self.mic_chip = StatusChip("Microphone", "idle")
        self.link_chip = StatusChip("Link", "offline-local")
        layout.addWidget(self.model_chip)
        layout.addWidget(self.mic_chip)
        layout.addWidget(self.link_chip)

        self.cpu_meter = ResourceMeter("CPU")
        self.ram_meter = ResourceMeter("RAM")
        layout.addWidget(self.cpu_meter)
        layout.addWidget(self.ram_meter)

        tasks_label = QLabel("ACTIVE TASKS")
        tasks_label.setObjectName("MutedLabel")
        self.tasks_value = QLabel("None")
        self.tasks_value.setObjectName("CyanLabel")
        layout.addWidget(tasks_label)
        layout.addWidget(self.tasks_value)

        ops_label = QLabel("RECENT OPERATIONS")
        ops_label.setObjectName("MutedLabel")
        layout.addWidget(ops_label)
        self.ops_list = QLabel("System boot")
        self.ops_list.setObjectName("MutedLabel")
        self.ops_list.setWordWrap(True)
        self.ops_list.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.ops_list)
        scroll.setFixedHeight(160)
        layout.addWidget(scroll)
        layout.addStretch(1)
        return frame

    def _build_status_bar(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("StatusBar")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(16, 8, 16, 8)
        self.status_label = QLabel("Systems nominal  ·  Sprint 0 foundation")
        self.status_label.setObjectName("MutedLabel")
        self.clock_label = QLabel("")
        self.clock_label.setObjectName("CyanLabel")
        self.emergency_button = QPushButton("EMERGENCY STOP")
        self.emergency_button.setObjectName("DangerButton")
        self.emergency_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.emergency_button.clicked.connect(self._engage_emergency_stop)
        layout.addWidget(self.status_label, 1)
        layout.addWidget(self.clock_label)
        layout.addWidget(self.emergency_button)
        self._clock_timer = QTimer(self)
        self._clock_timer.timeout.connect(self._tick_clock)
        self._clock_timer.start(1000)
        self._tick_clock()
        return frame

    def _navigate(self, key: str) -> None:
        if key not in self._view_index:
            return
        self.state.current_view = key
        self._views.setCurrentIndex(self._view_index[key])
        for nav_key, button in self._nav_buttons.items():
            button.setProperty("active", "true" if nav_key == key else "false")
            button.style().unpolish(button)
            button.style().polish(button)
        self.state.record_operation(f"Opened {key}")
        self._refresh_operations()
        self.signals.navigation_changed.emit(key)

    def _submit_command(self) -> None:
        text = self.command_input.text().strip()
        if not text:
            return
        if self.state.emergency_stopped:
            self._set_status("Emergency stop is engaged. Command ignored.")
            return
        self.command_input.clear()
        self.state.last_command = text
        self.state.record_operation(f"Command: {text}")
        self.conversation.setText(f"Acknowledged: {text}")
        self._refresh_operations()
        self.signals.command_submitted.emit(text)
        self._set_status("Command received. Automation arrives in later sprints.")

    def _toggle_listening(self) -> None:
        if self.state.emergency_stopped:
            self._set_status("Emergency stop is engaged.")
            return
        self.state.listening = not self.state.listening
        self.state.microphone_status = "listening" if self.state.listening else "idle"
        self.waveform.set_active(self.state.listening)
        self.mic_chip.set_value(self.state.microphone_status)
        self.signals.listening_changed.emit(self.state.listening)
        self._set_status("Microphone armed (UI only until Sprint 1)." if self.state.listening else "Microphone idle.")

    def _stop_listening(self) -> None:
        self.state.listening = False
        self.state.microphone_status = "idle"
        self.waveform.set_active(False)
        self.mic_chip.set_value("idle")
        self.signals.listening_changed.emit(False)

    def _engage_emergency_stop(self) -> None:
        if self.state.emergency_stopped:
            return
        self.state.trigger_emergency_stop()
        self.signals.emergency_stop.emit()
        self.signals.task_cancelled.emit()

    def _on_emergency_stop(self) -> None:
        self.reactor.set_emergency(True)
        self.waveform.set_active(False)
        self.mic_chip.set_value("stopped")
        self.tasks_value.setText("Cancelled")
        self.conversation.setText("Emergency stop engaged. All pending actions halted.")
        self._refresh_operations()
        self._set_status("EMERGENCY STOP")

    def _on_navigation(self, key: str) -> None:
        self._set_status(f"View: {key}")

    def _on_command(self, text: str) -> None:
        self._set_status(f"Queued: {text}")

    def _on_resources(self, cpu: float, ram: float) -> None:
        self.cpu_meter.set_percent(cpu)
        self.ram_meter.set_percent(ram)

    def _poll_resources(self) -> None:
        cpu = 0.0
        ram = 0.0
        if psutil is not None:
            cpu = float(psutil.cpu_percent(interval=None))
            ram = float(psutil.virtual_memory().percent)
        self.signals.resource_updated.emit(cpu, ram)

    def _refresh_operations(self) -> None:
        if self.state.recent_operations:
            self.ops_list.setText("\n".join(self.state.recent_operations))
        else:
            self.ops_list.setText("No operations yet")

    def _set_status(self, message: str) -> None:
        self.status_label.setText(message)

    def _tick_clock(self) -> None:
        self.clock_label.setText(datetime.now(UTC).strftime("%H:%M:%S UTC"))

    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802
        self._resource_timer.stop()
        self._clock_timer.stop()
        super().closeEvent(event)
