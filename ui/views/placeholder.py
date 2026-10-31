from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget


class PlaceholderView(QWidget):
    def __init__(self, title: str, description: str, sprint_note: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        panel = QFrame()
        panel.setObjectName("GlassPanel")
        inner = QVBoxLayout(panel)
        heading = QLabel(title.upper())
        heading.setObjectName("TitleLabel")
        body = QLabel(description)
        body.setObjectName("MutedLabel")
        body.setWordWrap(True)
        note = QLabel(sprint_note)
        note.setObjectName("CyanLabel")
        note.setWordWrap(True)
        inner.addWidget(heading)
        inner.addWidget(body)
        inner.addWidget(note)
        inner.addStretch(1)
        layout.addWidget(panel)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
