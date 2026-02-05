"""
Application Theme - Professional Dark Theme

Sets Fusion style with custom dark QPalette and global stylesheet.
"""

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt


# Color constants
_WINDOW = "#2d2d30"
_WINDOW_DARKER = "#252526"
_BASE = "#1e1e1e"
_ALT_BASE = "#2d2d30"
_TEXT = "#cccccc"
_TEXT_BRIGHT = "#ffffff"
_TEXT_DIM = "#808080"
_BUTTON = "#3c3c3c"
_BUTTON_HOVER = "#505050"
_BORDER = "#555555"
_BORDER_LIGHT = "#666666"
_ACCENT = "#3574c4"
_ACCENT_HOVER = "#4a8ad4"
_HIGHLIGHT = "#264f78"
_LINK = "#4a9cd6"
_ERROR = "#f44747"
_SUCCESS = "#4ec9b0"


def apply_theme(app: QApplication) -> None:
    """Apply professional dark theme to the application."""
    app.setStyle("Fusion")
    _apply_palette(app)
    app.setStyleSheet(_build_stylesheet())


def _apply_palette(app: QApplication) -> None:
    """Set custom dark QPalette."""
    p = QPalette()

    # Active colors
    p.setColor(QPalette.ColorRole.Window, QColor(_WINDOW))
    p.setColor(QPalette.ColorRole.WindowText, QColor(_TEXT))
    p.setColor(QPalette.ColorRole.Base, QColor(_BASE))
    p.setColor(QPalette.ColorRole.AlternateBase, QColor(_ALT_BASE))
    p.setColor(QPalette.ColorRole.ToolTipBase, QColor(_WINDOW))
    p.setColor(QPalette.ColorRole.ToolTipText, QColor(_TEXT))
    p.setColor(QPalette.ColorRole.PlaceholderText, QColor(_TEXT_DIM))
    p.setColor(QPalette.ColorRole.Text, QColor(_TEXT))
    p.setColor(QPalette.ColorRole.Button, QColor(_BUTTON))
    p.setColor(QPalette.ColorRole.ButtonText, QColor(_TEXT))
    p.setColor(QPalette.ColorRole.BrightText, QColor(_TEXT_BRIGHT))
    p.setColor(QPalette.ColorRole.Link, QColor(_LINK))
    p.setColor(QPalette.ColorRole.Highlight, QColor(_HIGHLIGHT))
    p.setColor(QPalette.ColorRole.HighlightedText, QColor(_TEXT_BRIGHT))

    # Fusion-specific palette roles
    p.setColor(QPalette.ColorRole.Light, QColor("#505050"))
    p.setColor(QPalette.ColorRole.Midlight, QColor("#404040"))
    p.setColor(QPalette.ColorRole.Mid, QColor("#353535"))
    p.setColor(QPalette.ColorRole.Dark, QColor("#1a1a1a"))
    p.setColor(QPalette.ColorRole.Shadow, QColor("#141414"))

    # Disabled colors
    p.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor("#707070"))
    p.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor("#707070"))
    p.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor("#707070"))
    p.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, QColor("#282828"))
    p.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, QColor("#333333"))

    app.setPalette(p)


def _build_stylesheet() -> str:
    """Build global stylesheet string."""
    return f"""
        /* ===== QToolTip ===== */
        QToolTip {{
            background-color: {_WINDOW_DARKER};
            color: {_TEXT};
            border: 1px solid {_BORDER};
            padding: 4px;
        }}

        /* ===== QGroupBox ===== */
        QGroupBox {{
            border: 1px solid {_BORDER};
            border-radius: 6px;
            margin-top: 7px;
            padding: 4px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 16px;
            padding: 0 3px;
            color: {_TEXT};
        }}

        /* ===== QTreeWidget (navigation) ===== */
        QTreeWidget {{
            background-color: {_BASE};
            alternate-background-color: {_ALT_BASE};
            show-decoration-selected: 1;
            border: none;
            outline: none;
        }}
        QTreeWidget::item {{
            height: 26px;
            border-right: 1px dotted {_BORDER};
            color: {_TEXT};
        }}
        QTreeWidget::item:hover {{
            background-color: {_BUTTON_HOVER};
            border-radius: 4px;
        }}
        QTreeWidget::item:selected:active {{
            background-color: {_HIGHLIGHT};
            border-radius: 4px;
            color: {_TEXT_BRIGHT};
        }}
        QTreeWidget::item:selected:!active {{
            background-color: {_HIGHLIGHT};
            border-radius: 4px;
            color: {_TEXT};
        }}
        QTreeWidget::branch:hover {{
            background-color: {_BUTTON_HOVER};
        }}

        /* ===== QLineEdit ===== */
        QLineEdit {{
            background-color: {_BASE};
            border: 1px solid {_BORDER};
            border-radius: 3px;
            padding: 3px 6px;
            color: {_TEXT};
            selection-background-color: {_HIGHLIGHT};
        }}
        QLineEdit:focus {{
            border: 1px solid {_ACCENT};
        }}

        /* ===== QComboBox ===== */
        QComboBox {{
            background-color: {_BUTTON};
            border: 1px solid {_BORDER};
            border-radius: 3px;
            padding: 3px 8px;
            color: {_TEXT};
            combobox-popup: 0;
        }}
        QComboBox:hover {{
            border: 1px solid {_ACCENT};
        }}
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        QComboBox QAbstractItemView {{
            background-color: {_WINDOW_DARKER};
            border: 1px solid {_BORDER};
            selection-background-color: {_HIGHLIGHT};
            color: {_TEXT};
        }}

        /* ===== QPushButton ===== */
        QPushButton {{
            background-color: {_BUTTON};
            border: 1px solid {_BORDER};
            border-radius: 4px;
            padding: 4px 16px;
            color: {_TEXT};
            min-height: 20px;
        }}
        QPushButton:hover {{
            background-color: {_BUTTON_HOVER};
            border: 1px solid {_ACCENT};
        }}
        QPushButton:pressed {{
            background-color: {_HIGHLIGHT};
        }}
        QPushButton:disabled {{
            background-color: #333333;
            color: #707070;
            border: 1px solid #444444;
        }}

        /* ===== Primary Button (Generate, Run, etc.) ===== */
        QPushButton[cssClass="primary"] {{
            background-color: {_ACCENT};
            border: 1px solid {_ACCENT};
            color: {_TEXT_BRIGHT};
        }}
        QPushButton[cssClass="primary"]:hover {{
            background-color: {_ACCENT_HOVER};
            border: 1px solid {_ACCENT_HOVER};
        }}
        QPushButton[cssClass="primary"]:pressed {{
            background-color: #2a5fa0;
        }}

        /* ===== QProgressBar ===== */
        QProgressBar {{
            border: 1px solid {_BORDER};
            border-radius: 4px;
            text-align: center;
            background-color: {_BASE};
            color: {_TEXT};
        }}
        QProgressBar::chunk {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {_ACCENT}, stop:1 #5ba3d9);
            border-radius: 3px;
        }}

        /* ===== QScrollBar (vertical) ===== */
        QScrollBar:vertical {{
            background: {_WINDOW_DARKER};
            width: 12px;
            margin: 0;
        }}
        QScrollBar::handle:vertical {{
            background: #555555;
            min-height: 30px;
            border-radius: 4px;
            margin: 2px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: #777777;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}

        /* ===== QScrollBar (horizontal) ===== */
        QScrollBar:horizontal {{
            background: {_WINDOW_DARKER};
            height: 12px;
            margin: 0;
        }}
        QScrollBar::handle:horizontal {{
            background: #555555;
            min-width: 30px;
            border-radius: 4px;
            margin: 2px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background: #777777;
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0;
        }}
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
            background: none;
        }}

        /* ===== QTextEdit ===== */
        QTextEdit {{
            background-color: {_BASE};
            color: {_TEXT};
            border: 1px solid {_BORDER};
            border-radius: 3px;
            selection-background-color: {_HIGHLIGHT};
        }}

        /* ===== QScrollArea ===== */
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}

        /* ===== QSplitter ===== */
        QSplitter::handle {{
            background-color: {_BORDER};
        }}
        QSplitter::handle:horizontal {{
            width: 2px;
        }}
        QSplitter::handle:vertical {{
            height: 2px;
        }}

        /* ===== QMenuBar ===== */
        QMenuBar {{
            background-color: {_WINDOW};
            color: {_TEXT};
            border-bottom: 1px solid {_BORDER};
        }}
        QMenuBar::item:selected {{
            background-color: {_BUTTON_HOVER};
        }}

        /* ===== QMenu ===== */
        QMenu {{
            background-color: {_WINDOW_DARKER};
            color: {_TEXT};
            border: 1px solid {_BORDER};
        }}
        QMenu::item:selected {{
            background-color: {_HIGHLIGHT};
        }}
        QMenu::separator {{
            height: 1px;
            background-color: {_BORDER};
            margin: 4px 8px;
        }}

        /* ===== QStatusBar ===== */
        QStatusBar {{
            background-color: {_ACCENT};
            color: {_TEXT_BRIGHT};
        }}

        /* ===== QHeaderView ===== */
        QHeaderView::section {{
            background-color: {_BUTTON};
            color: {_TEXT};
            border: 1px solid {_BORDER};
            padding: 4px;
        }}

        /* ===== QToolBar ===== */
        QToolBar {{
            background-color: {_WINDOW};
            border: none;
            spacing: 2px;
        }}
        QToolButton {{
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 3px;
            padding: 3px;
            color: {_TEXT};
        }}
        QToolButton:hover {{
            background-color: {_BUTTON_HOVER};
            border: 1px solid {_BORDER};
        }}
        QToolButton:pressed {{
            background-color: {_HIGHLIGHT};
        }}
        QToolButton:checked {{
            background-color: {_HIGHLIGHT};
            border: 1px solid {_ACCENT};
        }}

        /* ===== QTabWidget / QTabBar ===== */
        QTabWidget::pane {{
            border: 1px solid {_BORDER};
            background-color: {_WINDOW};
        }}
        QTabBar::tab {{
            background-color: {_BUTTON};
            color: {_TEXT};
            border: 1px solid {_BORDER};
            padding: 6px 12px;
            margin-right: 1px;
        }}
        QTabBar::tab:selected {{
            background-color: {_WINDOW};
            border-bottom-color: {_WINDOW};
        }}
        QTabBar::tab:hover {{
            background-color: {_BUTTON_HOVER};
        }}

        /* ===== QCheckBox ===== */
        QCheckBox {{
            color: {_TEXT};
            spacing: 6px;
        }}
        QCheckBox:hover {{
            color: {_ACCENT_HOVER};
        }}

        /* ===== QLabel ===== */
        QLabel {{
            color: {_TEXT};
        }}

        /* ===== QSpinBox / QDoubleSpinBox ===== */
        QSpinBox, QDoubleSpinBox {{
            background-color: {_BASE};
            border: 1px solid {_BORDER};
            border-radius: 3px;
            padding: 3px 6px;
            color: {_TEXT};
        }}
        QSpinBox:focus, QDoubleSpinBox:focus {{
            border: 1px solid {_ACCENT};
        }}
    """


def clear_widget_styles(widget):
    """Recursively clear hardcoded stylesheets from a widget tree.

    This is needed to remove auto-generated Qt Designer styles
    that conflict with the dark theme.
    """
    # Clear this widget's stylesheet
    if widget.styleSheet():
        widget.setStyleSheet("")

    # Recurse into children
    for child in widget.findChildren(type(widget).__mro__[1]):
        if child.styleSheet():
            child.setStyleSheet("")
