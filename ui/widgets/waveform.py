from __future__ import annotations

import math

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPen
from PySide6.QtWidgets import QWidget

from core.constants import COLOR_CYAN, COLOR_ELECTRIC, COLOR_MUTED


class WaveformWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("WaveformWidget")
        self.setMinimumHeight(72)
        self.setMaximumHeight(96)
        self._phase = 0.0
        self._active = False
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(40)

    def set_active(self, active: bool) -> None:
        self._active = active
        self.update()

    def _tick(self) -> None:
        self._phase += 0.18 if self._active else 0.05
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        del event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        width = self.width()
        height = self.height()
        mid = height / 2
        bars = 48
        gap = width / bars
        color = QColor(COLOR_ELECTRIC if self._active else COLOR_CYAN)
        muted = QColor(COLOR_MUTED)
        for index in range(bars):
            x = index * gap + gap / 2
            wave = math.sin(self._phase + index * 0.28)
            amp = 0.55 if self._active else 0.18
            bar_h = max(6.0, abs(wave) * (height * amp) + 6)
            gradient = QLinearGradient(x, mid - bar_h / 2, x, mid + bar_h / 2)
            gradient.setColorAt(0.0, color)
            gradient.setColorAt(1.0, muted)
            pen = QPen()
            pen.setBrush(gradient)
            pen.setWidthF(2.4)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            painter.drawLine(int(x), int(mid - bar_h / 2), int(x), int(mid + bar_h / 2))
        painter.end()
