from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea
from PySide6.QtCore import Signal, Qt

from view.style.theme import get_colors


# ─────────────────────────────────────────────────────────────────────────────
# 단계 구조 정의  (key, 표시이름, 하위항목 리스트)
# ─────────────────────────────────────────────────────────────────────────────
STEP_TREE = [
    ("geometry",  "Geometry",  []),
    ("setup",     "Setup", [
        ("models",             "Models"),
        ("initial_conditions", "Initial Conditions"),
        ("spray_mmh",          "Spray - MMH"),
        ("spray_nto",          "Spray - NTO"),
    ]),
    ("solution",  "Solution", [
        ("numerical", "Numerical Conditions"),
        ("run_cond",  "Run Conditions"),
    ]),
    ("run",       "Run",      []),
    ("results",   "Results",  [
        ("residual", "Residual"),
        ("post",     "Post"),
    ]),
]


def _c():
    """현재 테마 색상 반환."""
    return get_colors()


# ─────────────────────────────────────────────────────────────────────────────
# SubItem – 하위 항목 버튼
# ─────────────────────────────────────────────────────────────────────────────
class SubItem(QWidget):
    clicked = Signal(str)

    def __init__(self, key: str, name: str, parent=None):
        super().__init__(parent)
        self.key = key
        self._active = False
        self._setup_ui(name)

    def _setup_ui(self, name: str):
        self.setFixedHeight(26)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._accent = QFrame(self)
        self._accent.setFixedWidth(3)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addWidget(self._accent)

        inner = QHBoxLayout()
        inner.setContentsMargins(28, 0, 8, 0)
        inner.setSpacing(4)
        outer.addLayout(inner)

        self._label = QLabel(name)
        self._label.setStyleSheet(f"font-size: 10px; color: {_c()['text_dim']};")
        inner.addWidget(self._label, 1)

        self._apply_style()

    def set_active(self, active: bool):
        self._active = active
        self._apply_style()

    def _apply_style(self):
        c = _c()
        if self._active:
            self._accent.setStyleSheet(f"background-color: {c['accent']};")
            self._label.setStyleSheet(
                f"font-size: 10px; color: {c['highlight_text']}; font-weight: bold;"
            )
            self.setStyleSheet(
                f"SubItem {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:1,"
                f" stop:0 {c['tree_sel_start']}, stop:1 {c['tree_sel_end']}); }}"
            )
        else:
            self._accent.setStyleSheet("background-color: transparent;")
            self._label.setStyleSheet(f"font-size: 10px; color: {c['text_dim']};")
            self.setStyleSheet("SubItem { background-color: transparent; }")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.key)
        super().mousePressEvent(event)

    def enterEvent(self, event):
        if not self._active:
            c = _c()
            self.setStyleSheet(f"SubItem {{ background-color: {c['tree_hover']}; }}")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._apply_style()
        super().leaveEvent(event)


# ─────────────────────────────────────────────────────────────────────────────
# StepItem – 상위 단계 버튼 (하위 항목 포함 가능)
# ─────────────────────────────────────────────────────────────────────────────
class StepItem(QWidget):
    clicked     = Signal(str)
    sub_clicked = Signal(str)

    STATUS_NONE    = "none"
    STATUS_CURRENT = "current"
    STATUS_DONE    = "done"

    def __init__(self, step_key: str, number: int, name: str,
                 sub_items: list, parent=None):
        super().__init__(parent)
        self.step_key = step_key
        self._status = self.STATUS_NONE
        self._expanded = False
        self._sub_items: dict[str, SubItem] = {}
        self._setup_ui(number, name, sub_items)
        self._apply_style()

    def _setup_ui(self, number: int, name: str, sub_items: list):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── 헤더 행 ──────────────────────────────────────────────
        self._header = QWidget()
        self._header.setFixedHeight(30)
        self._header.setCursor(Qt.CursorShape.PointingHandCursor)

        self._accent = QFrame(self._header)
        self._accent.setFixedWidth(3)

        h_outer = QHBoxLayout(self._header)
        h_outer.setContentsMargins(0, 0, 0, 0)
        h_outer.setSpacing(0)
        h_outer.addWidget(self._accent)

        h_inner = QHBoxLayout()
        h_inner.setContentsMargins(6, 2, 8, 2)
        h_inner.setSpacing(6)
        h_outer.addLayout(h_inner)

        # 단계 번호 (작은 원형)
        self._circle = QLabel(str(number))
        self._circle.setFixedSize(18, 18)
        self._circle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h_inner.addWidget(self._circle)

        self._name_label = QLabel(name)
        h_inner.addWidget(self._name_label, 1)

        if sub_items:
            self._expand_label = QLabel("▶")
            self._expand_label.setFixedWidth(10)
            self._expand_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            h_inner.addWidget(self._expand_label)
            self._status_label = None
        else:
            self._expand_label = None
            self._status_label = QLabel("○")
            self._status_label.setFixedWidth(12)
            self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            h_inner.addWidget(self._status_label)

        root.addWidget(self._header)

        # ── 하위 항목 컨테이너 ──────────────────────────────────
        self._sub_container = QWidget()
        sub_layout = QVBoxLayout(self._sub_container)
        sub_layout.setContentsMargins(0, 0, 0, 0)
        sub_layout.setSpacing(0)

        for sub_key, sub_name in sub_items:
            sub = SubItem(sub_key, sub_name)
            sub.clicked.connect(self.sub_clicked.emit)
            self._sub_items[sub_key] = sub
            sub_layout.addWidget(sub)

        self._sub_container.setVisible(False)
        root.addWidget(self._sub_container)

        self._header.mousePressEvent = self._on_header_click

    def _on_header_click(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self._sub_items:
                self._toggle_expand()
            self.clicked.emit(self.step_key)

    def _toggle_expand(self):
        self._expanded = not self._expanded
        self._sub_container.setVisible(self._expanded)
        if self._expand_label:
            self._expand_label.setText("▼" if self._expanded else "▶")

    def set_expanded(self, expanded: bool):
        if self._expanded != expanded:
            self._expanded = expanded
            self._sub_container.setVisible(expanded)
            if self._expand_label:
                self._expand_label.setText("▼" if expanded else "▶")

    def set_sub_active(self, sub_key: str):
        for key, item in self._sub_items.items():
            item.set_active(key == sub_key)

    def clear_sub_active(self):
        for item in self._sub_items.values():
            item.set_active(False)

    def set_status(self, status: str):
        self._status = status
        self._apply_style()

    def _apply_style(self):
        c = _c()
        has_sub = bool(self._sub_items)

        if self._status == self.STATUS_CURRENT:
            self._accent.setStyleSheet(f"background-color: {c['accent']};")
            self._circle.setStyleSheet(
                f"background-color: {c['accent']}; border-radius: 9px;"
                f" color: {c['highlight_text']}; font-weight: bold; font-size: 10px;"
            )
            self._name_label.setStyleSheet(
                f"color: {c['highlight_text']}; font-weight: bold; font-size: 11px;"
            )
            self._header.setStyleSheet(
                f"QWidget {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:1,"
                f" stop:0 {c['tree_sel_start']}, stop:1 {c['tree_sel_end']}); }}"
            )
            if has_sub and self._expand_label:
                self._expand_label.setStyleSheet(
                    f"color: {c['highlight_text']}; font-size: 8px;"
                )
            elif self._status_label:
                self._status_label.setText("●")
                self._status_label.setStyleSheet(f"color: {c['highlight_text']}; font-size: 9px;")

        elif self._status == self.STATUS_DONE:
            self._accent.setStyleSheet("background-color: transparent;")
            self._circle.setStyleSheet(
                f"background-color: {c['mid']}; border-radius: 9px;"
                f" color: {c['accent']}; font-weight: bold; font-size: 10px;"
            )
            self._name_label.setStyleSheet(
                f"color: {c['text_dim']}; font-size: 11px;"
            )
            self._header.setStyleSheet("")
            if has_sub and self._expand_label:
                self._expand_label.setStyleSheet(f"color: {c['text_dim']}; font-size: 8px;")
            elif self._status_label:
                self._status_label.setText("✓")
                self._status_label.setStyleSheet(f"color: {c['accent']}; font-size: 9px;")

        else:  # NONE
            self._accent.setStyleSheet("background-color: transparent;")
            self._circle.setStyleSheet(
                f"background-color: {c['mid']}; border-radius: 9px;"
                f" color: {c['text_dim']}; font-size: 10px;"
            )
            self._name_label.setStyleSheet(
                f"color: {c['text_dim']}; font-size: 11px;"
            )
            self._header.setStyleSheet("")
            if has_sub and self._expand_label:
                self._expand_label.setStyleSheet(f"color: {c['text_dim']}; font-size: 8px;")
            elif self._status_label:
                self._status_label.setText("○")
                self._status_label.setStyleSheet(f"color: {c['text_dim']}; font-size: 9px;")

    def enterEvent(self, event):
        if self._status != self.STATUS_CURRENT:
            c = _c()
            self._header.setStyleSheet(f"QWidget {{ background-color: {c['tree_hover']}; }}")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._apply_style()
        super().leaveEvent(event)


# ─────────────────────────────────────────────────────────────────────────────
# StepNavWidget – 전체 네비게이션 패널
# ─────────────────────────────────────────────────────────────────────────────
class StepNavWidget(QWidget):
    step_clicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._step_items: dict[str, StepItem] = {}
        self._sub_parent: dict[str, str] = {}
        self._setup_ui()

    def _setup_ui(self):
        c = _c()
        self.setFixedWidth(180)
        self.setObjectName("StepNavWidget")
        self.setStyleSheet(
            f"QWidget#StepNavWidget {{ background-color: {c['base']};"
            f" border-right: 1px solid {c['border_light']}; }}"
        )

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        outer_layout.addWidget(scroll)

        container = QWidget()
        container.setStyleSheet(f"background-color: {c['base']};")
        scroll.setWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 4, 0, 8)
        layout.setSpacing(0)

        for i, (key, name, subs) in enumerate(STEP_TREE):
            item = StepItem(key, i + 1, name, subs)
            item.clicked.connect(self._on_step_clicked)
            item.sub_clicked.connect(self._on_sub_clicked)
            self._step_items[key] = item

            for sub_key, _ in subs:
                self._sub_parent[sub_key] = key

            layout.addWidget(item)

            # 구분선 (하위 항목 없는 단계 사이)
            if i < len(STEP_TREE) - 1:
                sep = QFrame()
                sep.setFrameShape(QFrame.Shape.HLine)
                sep.setStyleSheet(f"color: {c['border_light']}; margin: 0px 8px;")
                sep.setFixedHeight(1)
                layout.addWidget(sep)

        layout.addStretch(1)

    # ── 내부 핸들러 ───────────────────────────────────────────────

    def _on_step_clicked(self, step_key: str):
        step = self._step_items.get(step_key)
        if step and not step._sub_items:
            self._activate_step(step_key)
        self.step_clicked.emit(step_key)

    def _on_sub_clicked(self, sub_key: str):
        parent_key = self._sub_parent.get(sub_key)
        if parent_key:
            self._activate_sub(parent_key, sub_key)
        self.step_clicked.emit(sub_key)

    # ── 공개 API ──────────────────────────────────────────────────

    def set_current(self, key: str):
        if key in self._step_items:
            self._activate_step(key)
        elif key in self._sub_parent:
            self._activate_sub(self._sub_parent[key], key)

    def _activate_step(self, step_key: str):
        step_keys = [k for k, _, _ in STEP_TREE]
        try:
            current_idx = step_keys.index(step_key)
        except ValueError:
            return

        for i, key in enumerate(step_keys):
            item = self._step_items.get(key)
            if item is None:
                continue
            item.clear_sub_active()
            if i < current_idx:
                item.set_status(StepItem.STATUS_DONE)
            elif i == current_idx:
                item.set_status(StepItem.STATUS_CURRENT)
            else:
                item.set_status(StepItem.STATUS_NONE)

    def _activate_sub(self, parent_key: str, sub_key: str):
        step_keys = [k for k, _, _ in STEP_TREE]
        try:
            parent_idx = step_keys.index(parent_key)
        except ValueError:
            return

        for i, key in enumerate(step_keys):
            item = self._step_items.get(key)
            if item is None:
                continue
            item.clear_sub_active()
            if i < parent_idx:
                item.set_status(StepItem.STATUS_DONE)
            elif i == parent_idx:
                item.set_status(StepItem.STATUS_CURRENT)
                item.set_expanded(True)
                item.set_sub_active(sub_key)
            else:
                item.set_status(StepItem.STATUS_NONE)
