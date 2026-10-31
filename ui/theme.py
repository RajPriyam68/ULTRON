from __future__ import annotations

from PySide6.QtWidgets import QApplication

from core.constants import (
    COLOR_BACKGROUND,
    COLOR_BORDER,
    COLOR_CRIMSON,
    COLOR_CYAN,
    COLOR_ELECTRIC,
    COLOR_MUTED,
    COLOR_PANEL,
    COLOR_PANEL_ALT,
    COLOR_WHITE,
)

STYLESHEET = f"""
QWidget {{
    background-color: {COLOR_BACKGROUND};
    color: {COLOR_WHITE};
    font-family: "Segoe UI", "Noto Sans", "DejaVu Sans", sans-serif;
    font-size: 13px;
}}
QMainWindow, QDialog {{
    background-color: {COLOR_BACKGROUND};
}}
QFrame#Sidebar, QFrame#RightRail, QFrame#StatusBar, QFrame#CenterStage {{
    background-color: {COLOR_PANEL};
    border: 1px solid {COLOR_BORDER};
    border-radius: 14px;
}}
QFrame#GlassPanel {{
    background-color: rgba(21, 25, 35, 220);
    border: 1px solid {COLOR_BORDER};
    border-radius: 12px;
}}
QPushButton {{
    background-color: {COLOR_PANEL_ALT};
    color: {COLOR_WHITE};
    border: 1px solid {COLOR_BORDER};
    border-radius: 8px;
    padding: 8px 14px;
}}
QPushButton:hover {{
    border-color: {COLOR_CYAN};
    color: {COLOR_CYAN};
}}
QPushButton:pressed {{
    background-color: {COLOR_BACKGROUND};
}}
QPushButton#PrimaryButton {{
    background-color: {COLOR_CRIMSON};
    border-color: {COLOR_ELECTRIC};
    color: {COLOR_WHITE};
    font-weight: 600;
}}
QPushButton#PrimaryButton:hover {{
    background-color: {COLOR_ELECTRIC};
    color: {COLOR_WHITE};
}}
QPushButton#DangerButton {{
    background-color: transparent;
    border: 1px solid {COLOR_CRIMSON};
    color: {COLOR_ELECTRIC};
    font-weight: 700;
    letter-spacing: 1px;
}}
QPushButton#DangerButton:hover {{
    background-color: {COLOR_CRIMSON};
    color: {COLOR_WHITE};
}}
QPushButton#NavButton {{
    text-align: left;
    padding: 10px 14px;
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 10px;
    color: {COLOR_MUTED};
}}
QPushButton#NavButton:hover {{
    background-color: {COLOR_PANEL_ALT};
    color: {COLOR_WHITE};
    border-color: {COLOR_BORDER};
}}
QPushButton#NavButton[active="true"] {{
    background-color: {COLOR_PANEL_ALT};
    color: {COLOR_WHITE};
    border-color: {COLOR_CRIMSON};
}}
QLineEdit {{
    background-color: {COLOR_BACKGROUND};
    border: 1px solid {COLOR_BORDER};
    border-radius: 10px;
    padding: 10px 14px;
    color: {COLOR_WHITE};
    selection-background-color: {COLOR_CRIMSON};
}}
QLineEdit:focus {{
    border-color: {COLOR_CYAN};
}}
QLabel#MutedLabel {{
    color: {COLOR_MUTED};
}}
QLabel#TitleLabel {{
    color: {COLOR_WHITE};
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 2px;
}}
QLabel#BrandLabel {{
    color: {COLOR_ELECTRIC};
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 4px;
}}
QLabel#CyanLabel {{
    color: {COLOR_CYAN};
}}
QScrollArea {{
    border: none;
    background: transparent;
}}
QScrollBar:vertical {{
    background: {COLOR_BACKGROUND};
    width: 8px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {COLOR_BORDER};
    border-radius: 4px;
    min-height: 24px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QStatusBar {{
    background-color: {COLOR_PANEL};
    color: {COLOR_MUTED};
    border-top: 1px solid {COLOR_BORDER};
}}
"""


def apply_theme(app: QApplication) -> None:
    app.setStyle("Fusion")
    app.setStyleSheet(STYLESHEET)
