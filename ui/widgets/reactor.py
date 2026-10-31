from __future__ import annotations

import math

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QConicalGradient, QPainter, QPainterPath, QPen, QRadialGradient
from PySide6.QtWidgets import QWidget

from core.constants import COLOR_BACKGROUND, COLOR_CRIMSON, COLOR_CYAN, COLOR_ELECTRIC


class ReactorWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("ReactorWidget")
        self.setMinimumSize(220, 220)
        self._angle = 0.0
        self._pulse = 0.0
        self._emergency = False
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(33)

    def set_emergency(self, active: bool) -> None:
        self._emergency = active
        self.update()

    def _tick(self) -> None:
        self._angle = (self._angle + 1.8) % 360
        self._pulse = (self._pulse + 0.08) % (math.pi * 2)
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        del event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        side = min(self.width(), self.height())
        painter.translate(self.width() / 2, self.height() / 2)
        radius = side / 2 - 8

        core = QColor(COLOR_ELECTRIC if self._emergency else COLOR_CRIMSON)
        accent = QColor(COLOR_CYAN)
        bg = QColor(COLOR_BACKGROUND)

        glow = QRadialGradient(QPointF(0, 0), radius)
        glow.setColorAt(0.0, QColor(core.red(), core.green(), core.blue(), 90))
        glow.setColorAt(0.55, QColor(core.red(), core.green(), core.blue(), 24))
        glow.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(glow)
        painter.drawEllipse(QPointF(0, 0), radius, radius)

        ring = QConicalGradient(QPointF(0, 0), self._angle)
        ring.setColorAt(0.0, core)
        ring.setColorAt(0.35, accent)
        ring.setColorAt(0.7, core)
        ring.setColorAt(1.0, accent)
        pen = QPen()
        pen.setBrush(ring)
        pen.setWidthF(4.5)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QPointF(0, 0), radius * 0.82, radius * 0.82)

        inner_pen = QPen(QColor(accent.red(), accent.green(), accent.blue(), 140))
        inner_pen.setWidthF(1.5)
        painter.setPen(inner_pen)
        pulse_r = radius * (0.48 + 0.04 * math.sin(self._pulse))
        painter.drawEllipse(QPointF(0, 0), pulse_r, pulse_r)

        painter.setPen(Qt.PenStyle.NoPen)
        core_fill = QRadialGradient(QPointF(0, 0), radius * 0.28)
        core_fill.setColorAt(0.0, QColor(255, 255, 255, 180))
        core_fill.setColorAt(0.35, core)
        core_fill.setColorAt(1.0, bg)
        painter.setBrush(core_fill)
        painter.drawEllipse(QPointF(0, 0), radius * 0.22, radius * 0.22)

        scan = QPainterPath()
        scan.moveTo(0, 0)
        sweep = 38
        scan.arcTo(QRectF(-radius * 0.72, -radius * 0.72, radius * 1.44, radius * 1.44), -self._angle, sweep)
        scan.closeSubpath()
        painter.fillPath(scan, QColor(accent.red(), accent.green(), accent.blue(), 28))
        painter.end()
