from __future__ import annotations

from PySide6.QtCore import QObject, Signal


class AppSignals(QObject):
    emergency_stop = Signal()
    navigation_changed = Signal(str)
    command_submitted = Signal(str)
    status_message = Signal(str)
    log_event = Signal(str, str)
    resource_updated = Signal(float, float)
    listening_changed = Signal(bool)
    task_cancelled = Signal()
