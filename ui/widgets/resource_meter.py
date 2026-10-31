from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QProgressBar, QVBoxLayout, QWidget

from core.constants import COLOR_BORDER, COLOR_CRIMSON, COLOR_CYAN, COLOR_PANEL_ALT


class ResourceMeter(QWidget):
    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        header = QHBoxHeader(title)
        self._bar = QProgressBar()
        self._bar.setRange(0, 100)
        self._bar.setValue(0)
        self._bar.setTextVisible(False)
        self._bar.setFixedHeight(8)
        self._bar.setStyleSheet(
            f"""
            QProgressBar {{
                background: {COLOR_PANEL_ALT};
                border: 1px solid {COLOR_BORDER};
                border-radius: 4px;
            }}
            QProgressBar::chunk {{
                background: {COLOR_CYAN};
                border-radius: 4px;
            }}
            """
        )
        self._value = header.value
        layout.addWidget(header)
        layout.addWidget(self._bar)

    def set_percent(self, value: float) -> None:
        clamped = max(0, min(100, int(round(value))))
        self._bar.setValue(clamped)
        self._value.setText(f"{clamped}%")
        chunk = COLOR_CRIMSON if clamped >= 85 else COLOR_CYAN
        self._bar.setStyleSheet(
            f"""
            QProgressBar {{
                background: {COLOR_PANEL_ALT};
                border: 1px solid {COLOR_BORDER};
                border-radius: 4px;
            }}
            QProgressBar::chunk {{
                background: {chunk};
                border-radius: 4px;
            }}
            """
        )


class QHBoxHeader(QWidget):
    def __init__(self, title: str) -> None:
        super().__init__()
        from PySide6.QtWidgets import QHBoxLayout

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel(title.upper())
        label.setObjectName("MutedLabel")
        self.value = QLabel("0%")
        self.value.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(label)
        layout.addWidget(self.value)
