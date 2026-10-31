from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget

from core.constants import COLOR_CYAN, COLOR_MUTED, COLOR_SUCCESS, COLOR_WARNING


class StatusChip(QWidget):
    def __init__(self, label: str, value: str = "offline", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("StatusChip")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        self._dot = QLabel("●")
        self._name = QLabel(label.upper())
        self._name.setObjectName("MutedLabel")
        self._value = QLabel(value)
        self._value.setObjectName("CyanLabel")
        layout.addWidget(self._dot)
        layout.addWidget(self._name)
        layout.addWidget(self._value, 1, Qt.AlignmentFlag.AlignRight)
        self.set_value(value)

    def set_value(self, value: str) -> None:
        self._value.setText(value)
        lowered = value.lower()
        if lowered in {"online", "ready", "idle", "ok", "connected"}:
            color = COLOR_SUCCESS
        elif lowered in {"listening", "active", "running"}:
            color = COLOR_CYAN
        elif lowered in {"stopped", "error", "offline"}:
            color = COLOR_WARNING if lowered == "offline" else COLOR_MUTED
        else:
            color = COLOR_CYAN
        self._dot.setStyleSheet(f"color: {color};")
