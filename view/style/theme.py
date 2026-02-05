"""
Application Theme - Light/Dark Theme Toggle

Supports switching between professional light and dark themes at runtime.
"""

import tempfile
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor, QPixmap, QPainter, QPolygonF, QPen
from PySide6.QtCore import Qt, QPointF


# Current theme mode
_current_mode = "light"


# ===== Light Theme Colors =====
_LIGHT = {
    "window":         "#f0f0f0",
    "base":           "#ffffff",
    "alt_base":       "#f5f7fa",
    "text":           "#1e1e1e",
    "text_dim":       "#888888",
    "text_disabled":  "#a0a0a0",
    "button":         "#e8e8e8",
    "button_hover":   "#d0d8e0",
    "border":         "#c0c0c0",
    "border_light":   "#d8d8d8",
    "accent":         "#3574c4",
    "accent_hover":   "#4a8ad4",
    "highlight":      "#3574c4",
    "highlight_text": "#ffffff",
    "link":           "#2a6cb6",
    "status_bg":      "#3574c4",
    "light":          "#ffffff",
    "midlight":       "#e8ecf0",
    "mid":            "#c0c0c0",
    "dark":           "#a0a0a0",
    "shadow":         "#808080",
    "tooltip_bg":     "#ffffee",
    "tree_hover":       "#e0eaf5",
    "tree_sel_start":   "#6ea1f1",
    "tree_sel_end":     "#3d87bf",
    "tree_sel2_start":  "#6b9be8",
    "tree_sel2_end":    "#577fbf",
    "btn_grad_top":     "#fcfcfc",
    "btn_grad_bot":     "#e8e8e8",
    "btn_hover_top":    "#e5f1fb",
    "btn_hover_bot":    "#c1d8f0",
    "btn_disabled_bg":  "#eeeeee",
    "btn_disabled_text":"#a0a0a0",
    "btn_pressed_bg":   "#2a5fa0",
    "prog_start":       "#1c76c1",
    "prog_end":         "#8ccbff",
    "scroll_handle":    "#b0b0b0",
    "scroll_hover":     "#909090",
    "tool_pressed":     "#b0c8e0",
    "tool_checked":     "#cce0f0",
    "panel_bg":         "#f8f8f8",
    "base_disabled":    "#f0f0f0",
    "btn_disabled_base":"#e0e0e0",
    # VTK
    "vtk_bg1": (0.32, 0.34, 0.43),
    "vtk_bg2": (0.82, 0.87, 0.97),
    "vtk_post_bg1": (0.65, 0.65, 0.70),
    "vtk_post_bg2": (0.40, 0.40, 0.50),
    # Graph
    "graph_bg":   "w",
    "graph_axis": "#333333",
}

# ===== Dark Theme Colors =====
_DARK = {
    "window":         "#2d2d30",
    "base":           "#1e1e1e",
    "alt_base":       "#2d2d30",
    "text":           "#cccccc",
    "text_dim":       "#808080",
    "text_disabled":  "#707070",
    "button":         "#3c3c3c",
    "button_hover":   "#505050",
    "border":         "#555555",
    "border_light":   "#666666",
    "accent":         "#3574c4",
    "accent_hover":   "#4a8ad4",
    "highlight":      "#264f78",
    "highlight_text": "#ffffff",
    "link":           "#4a9cd6",
    "status_bg":      "#3574c4",
    "light":          "#505050",
    "midlight":       "#404040",
    "mid":            "#353535",
    "dark":           "#1a1a1a",
    "shadow":         "#141414",
    "tooltip_bg":     "#2d2d30",
    "tree_hover":       "#505050",
    "tree_sel_start":   "#264f78",
    "tree_sel_end":     "#264f78",
    "tree_sel2_start":  "#264f78",
    "tree_sel2_end":    "#264f78",
    "btn_grad_top":     "#444444",
    "btn_grad_bot":     "#3c3c3c",
    "btn_hover_top":    "#505050",
    "btn_hover_bot":    "#484848",
    "btn_disabled_bg":  "#333333",
    "btn_disabled_text":"#707070",
    "btn_pressed_bg":   "#264f78",
    "prog_start":       "#3574c4",
    "prog_end":         "#5ba3d9",
    "scroll_handle":    "#555555",
    "scroll_hover":     "#777777",
    "tool_pressed":     "#264f78",
    "tool_checked":     "#264f78",
    "panel_bg":         "#252528",
    "base_disabled":    "#282828",
    "btn_disabled_base":"#333333",
    # VTK
    "vtk_bg1": (0.15, 0.15, 0.18),
    "vtk_bg2": (0.25, 0.27, 0.33),
    "vtk_post_bg1": (0.15, 0.15, 0.18),
    "vtk_post_bg2": (0.25, 0.27, 0.33),
    # Graph
    "graph_bg":   "#1e1e1e",
    "graph_axis": "#cccccc",
}

_THEMES = {"light": _LIGHT, "dark": _DARK}


def get_current_mode() -> str:
    return _current_mode


def get_colors(mode: str = None) -> dict:
    return _THEMES[mode or _current_mode]


def apply_theme(app: QApplication, mode: str = "light") -> None:
    global _current_mode
    _current_mode = mode
    c = _THEMES[mode]
    app.setStyle("Fusion")
    _apply_palette(app, c)
    app.setStyleSheet(_build_stylesheet(c))


def toggle_theme(app: QApplication) -> str:
    new_mode = "dark" if _current_mode == "light" else "light"
    apply_theme(app, new_mode)
    return new_mode


def _apply_palette(app: QApplication, c: dict) -> None:
    p = QPalette()
    p.setColor(QPalette.ColorRole.Window, QColor(c["window"]))
    p.setColor(QPalette.ColorRole.WindowText, QColor(c["text"]))
    p.setColor(QPalette.ColorRole.Base, QColor(c["base"]))
    p.setColor(QPalette.ColorRole.AlternateBase, QColor(c["alt_base"]))
    p.setColor(QPalette.ColorRole.ToolTipBase, QColor(c["tooltip_bg"]))
    p.setColor(QPalette.ColorRole.ToolTipText, QColor(c["text"]))
    p.setColor(QPalette.ColorRole.PlaceholderText, QColor(c["text_dim"]))
    p.setColor(QPalette.ColorRole.Text, QColor(c["text"]))
    p.setColor(QPalette.ColorRole.Button, QColor(c["button"]))
    p.setColor(QPalette.ColorRole.ButtonText, QColor(c["text"]))
    p.setColor(QPalette.ColorRole.BrightText, QColor("#ffffff"))
    p.setColor(QPalette.ColorRole.Link, QColor(c["link"]))
    p.setColor(QPalette.ColorRole.Highlight, QColor(c["highlight"]))
    p.setColor(QPalette.ColorRole.HighlightedText, QColor(c["highlight_text"]))
    p.setColor(QPalette.ColorRole.Light, QColor(c["light"]))
    p.setColor(QPalette.ColorRole.Midlight, QColor(c["midlight"]))
    p.setColor(QPalette.ColorRole.Mid, QColor(c["mid"]))
    p.setColor(QPalette.ColorRole.Dark, QColor(c["dark"]))
    p.setColor(QPalette.ColorRole.Shadow, QColor(c["shadow"]))
    p.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(c["text_disabled"]))
    p.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(c["text_disabled"]))
    p.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(c["text_disabled"]))
    p.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, QColor(c["base_disabled"]))
    p.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, QColor(c["btn_disabled_base"]))
    app.setPalette(p)


def _generate_combo_arrows(c: dict) -> dict:
    """Generate small combobox arrow PNGs for the current theme."""
    tmp = Path(tempfile.gettempdir()) / "bipropthrust_theme"
    tmp.mkdir(exist_ok=True)
    arrows = {}
    for key, color in [("normal", c["text"]), ("disabled", c["text_disabled"])]:
        sz = 10
        pixmap = QPixmap(sz, sz)
        pixmap.fill(QColor(0, 0, 0, 0))
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        painter.setBrush(QColor(color))
        painter.drawPolygon(QPolygonF([
            QPointF(2, 3), QPointF(sz - 2, 3), QPointF(sz / 2, sz - 3)
        ]))
        painter.end()
        path = tmp / f"combo_arrow_{key}.png"
        pixmap.save(str(path))
        arrows[key] = str(path).replace('\\', '/')
    return arrows


def _build_stylesheet(c: dict) -> str:
    arrows = _generate_combo_arrows(c)
    return f"""
        /* ===== QGroupBox ===== */
        QGroupBox {{
            border: 1px solid {c["border_light"]};
            border-radius: 6px;
            margin-top: 7px;
            padding: 4px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 16px;
            padding: 0 3px;
            color: {c["text"]};
        }}

        /* ===== QTreeWidget ===== */
        QTreeWidget {{
            background-color: {c["base"]};
            alternate-background-color: {c["alt_base"]};
            show-decoration-selected: 1;
            border: 1px solid {c["border_light"]};
            outline: none;
        }}
        QTreeWidget::item {{
            height: 26px;
            border-right: 1px dotted {c["border_light"]};
            color: {c["text"]};
        }}
        QTreeWidget::item:hover {{
            background-color: {c["tree_hover"]};
            border-radius: 4px;
        }}
        QTreeWidget::item:selected:active {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {c["tree_sel_start"]}, stop:1 {c["tree_sel_end"]});
            border-radius: 4px;
            color: {c["highlight_text"]};
        }}
        QTreeWidget::item:selected:!active {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {c["tree_sel2_start"]}, stop:1 {c["tree_sel2_end"]});
            border-radius: 4px;
            color: {c["highlight_text"]};
        }}

        /* ===== QLineEdit ===== */
        QLineEdit {{
            background-color: {c["base"]};
            border: 1px solid {c["border"]};
            border-radius: 3px;
            padding: 3px 6px;
            color: {c["text"]};
            selection-background-color: {c["highlight"]};
            selection-color: {c["highlight_text"]};
        }}
        QLineEdit:focus {{
            border: 1px solid {c["accent"]};
        }}

        /* ===== QComboBox ===== */
        QComboBox {{
            background-color: {c["base"]};
            border: 1px solid {c["border"]};
            border-radius: 3px;
            padding: 3px 8px;
            color: {c["text"]};
            combobox-popup: 0;
        }}
        QComboBox:hover {{
            border: 1px solid {c["accent"]};
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: center right;
            width: 18px;
            border: none;
        }}
        QComboBox::down-arrow {{
            image: url({arrows["normal"]});
            width: 10px;
            height: 10px;
        }}
        QComboBox::down-arrow:disabled {{
            image: url({arrows["disabled"]});
        }}
        QComboBox QAbstractItemView {{
            background-color: {c["base"]};
            border: 1px solid {c["border"]};
            selection-background-color: {c["highlight"]};
            selection-color: {c["highlight_text"]};
            color: {c["text"]};
        }}

        /* ===== QPushButton ===== */
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {c["btn_grad_top"]}, stop:1 {c["btn_grad_bot"]});
            border: 1px solid {c["border"]};
            border-radius: 4px;
            padding: 4px 16px;
            color: {c["text"]};
            min-height: 20px;
        }}
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {c["btn_hover_top"]}, stop:1 {c["btn_hover_bot"]});
            border: 1px solid {c["accent"]};
        }}
        QPushButton:pressed {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {c["btn_hover_bot"]}, stop:1 {c["btn_hover_top"]});
        }}
        QPushButton:disabled {{
            background-color: {c["btn_disabled_bg"]};
            color: {c["btn_disabled_text"]};
            border: 1px solid {c["border_light"]};
        }}

        /* ===== Primary Button ===== */
        QPushButton[cssClass="primary"] {{
            background-color: {c["accent"]};
            border: 1px solid {c["accent"]};
            color: {c["highlight_text"]};
        }}
        QPushButton[cssClass="primary"]:hover {{
            background-color: {c["accent_hover"]};
            border: 1px solid {c["accent_hover"]};
        }}
        QPushButton[cssClass="primary"]:pressed {{
            background-color: {c["btn_pressed_bg"]};
        }}

        /* ===== QProgressBar ===== */
        QProgressBar {{
            border: 1px solid {c["border"]};
            border-radius: 4px;
            text-align: center;
            background-color: {c["base"]};
            color: {c["text"]};
        }}
        QProgressBar::chunk {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {c["prog_start"]}, stop:1 {c["prog_end"]});
            border-radius: 3px;
        }}

        /* ===== QScrollBar (vertical) ===== */
        QScrollBar:vertical {{
            background: {c["window"]};
            width: 12px;
            margin: 0;
        }}
        QScrollBar::handle:vertical {{
            background: {c["scroll_handle"]};
            min-height: 30px;
            border-radius: 4px;
            margin: 2px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {c["scroll_hover"]};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}

        /* ===== QScrollBar (horizontal) ===== */
        QScrollBar:horizontal {{
            background: {c["window"]};
            height: 12px;
            margin: 0;
        }}
        QScrollBar::handle:horizontal {{
            background: {c["scroll_handle"]};
            min-width: 30px;
            border-radius: 4px;
            margin: 2px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background: {c["scroll_hover"]};
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0;
        }}
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
            background: none;
        }}

        /* ===== QTextEdit ===== */
        QTextEdit {{
            background-color: {c["base"]};
            color: {c["text"]};
            border: 1px solid {c["border_light"]};
            border-radius: 3px;
            selection-background-color: {c["highlight"]};
            selection-color: {c["highlight_text"]};
        }}

        /* ===== QStackedWidget (center panel pages) ===== */
        QStackedWidget {{
            background-color: {c["panel_bg"]};
        }}
        QStackedWidget > QWidget {{
            background-color: {c["panel_bg"]};
        }}

        /* ===== QScrollArea ===== */
        QScrollArea {{
            border: none;
            background-color: {c["panel_bg"]};
        }}
        QScrollArea > QWidget > QWidget {{
            background-color: {c["panel_bg"]};
        }}

        /* ===== QSplitter ===== */
        QSplitter::handle {{
            background-color: {c["border_light"]};
        }}
        QSplitter::handle:horizontal {{
            width: 2px;
        }}
        QSplitter::handle:vertical {{
            height: 2px;
        }}

        /* ===== QMenuBar ===== */
        QMenuBar {{
            background-color: {c["window"]};
            color: {c["text"]};
            border-bottom: 1px solid {c["border_light"]};
        }}
        QMenuBar::item:selected {{
            background-color: {c["button_hover"]};
        }}

        /* ===== QMenu ===== */
        QMenu {{
            background-color: {c["base"]};
            color: {c["text"]};
            border: 1px solid {c["border"]};
        }}
        QMenu::item:selected {{
            background-color: {c["highlight"]};
            color: {c["highlight_text"]};
        }}
        QMenu::separator {{
            height: 1px;
            background-color: {c["border_light"]};
            margin: 4px 8px;
        }}

        /* ===== QStatusBar ===== */
        QStatusBar {{
            background-color: {c["status_bg"]};
            color: {c["highlight_text"]};
            font-size: 8pt;
        }}

        /* ===== QHeaderView ===== */
        QHeaderView::section {{
            background-color: {c["window"]};
            color: {c["text"]};
            border: 1px solid {c["border_light"]};
            padding: 4px;
        }}

        /* ===== QToolBar ===== */
        QToolBar {{
            background-color: {c["window"]};
            border: none;
            spacing: 2px;
        }}
        QToolButton {{
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 3px;
            padding: 3px;
            color: {c["text"]};
        }}
        QToolButton:hover {{
            background-color: {c["button_hover"]};
            border: 1px solid {c["border"]};
        }}
        QToolButton:pressed {{
            background-color: {c["tool_pressed"]};
        }}
        QToolButton:checked {{
            background-color: {c["tool_checked"]};
            border: 1px solid {c["accent"]};
        }}

        /* ===== VTK Bottom Toolbar (clip/slice controls) ===== */
        QToolBar#vtkBottomBar {{
            background-color: {c["window"]};
            border-top: 1px solid {c["border_light"]};
            spacing: 4px;
            padding: 1px 4px;
            font-size: 9pt;
        }}
        QToolBar#vtkBottomBar QLabel {{
            font-size: 9pt;
            color: {c["text"]};
            padding: 0px 2px;
        }}
        QToolBar#vtkBottomBar QComboBox {{
            font-size: 9pt;
            padding: 1px 4px;
            min-height: 18px;
            max-height: 22px;
        }}
        QToolBar#vtkBottomBar QCheckBox {{
            font-size: 9pt;
            spacing: 3px;
        }}
        QToolBar#vtkBottomBar QPushButton {{
            font-size: 9pt;
            padding: 1px 8px;
            min-height: 18px;
            max-height: 22px;
        }}
        QToolBar#vtkBottomBar QDoubleSpinBox {{
            font-size: 9pt;
            padding: 1px 2px;
            min-height: 18px;
            max-height: 22px;
        }}
        QToolBar#vtkBottomBar QSlider::groove:horizontal {{
            height: 4px;
            background: {c["border"]};
            border-radius: 2px;
        }}
        QToolBar#vtkBottomBar QSlider::handle:horizontal {{
            background: {c["accent"]};
            width: 12px;
            height: 12px;
            margin: -4px 0;
            border-radius: 6px;
        }}
        QToolBar#vtkBottomBar QSlider::handle:horizontal:hover {{
            background: {c["accent_hover"]};
        }}
        QToolBar#vtkBottomBar QLineEdit {{
            font-size: 9pt;
            padding: 1px 4px;
            min-height: 18px;
            max-height: 22px;
        }}

        /* ===== QTabWidget / QTabBar ===== */
        QTabWidget::pane {{
            border: 1px solid {c["border_light"]};
            background-color: {c["base"]};
        }}
        QTabBar::tab {{
            background-color: {c["window"]};
            color: {c["text"]};
            border: 1px solid {c["border_light"]};
            padding: 6px 12px;
            margin-right: 1px;
        }}
        QTabBar::tab:selected {{
            background-color: {c["base"]};
            border-bottom-color: {c["base"]};
        }}
        QTabBar::tab:hover {{
            background-color: {c["button_hover"]};
        }}

        /* ===== QCheckBox ===== */
        QCheckBox {{
            color: {c["text"]};
            spacing: 6px;
        }}
        QCheckBox:hover {{
            color: {c["accent"]};
        }}

        /* ===== QSpinBox / QDoubleSpinBox ===== */
        QSpinBox, QDoubleSpinBox {{
            background-color: {c["base"]};
            border: 1px solid {c["border"]};
            border-radius: 3px;
            padding: 3px 6px;
            color: {c["text"]};
        }}
        QSpinBox:focus, QDoubleSpinBox:focus {{
            border: 1px solid {c["accent"]};
        }}
    """
