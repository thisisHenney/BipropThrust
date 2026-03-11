from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea
from PySide6.QtCore import Signal, Qt, QPropertyAnimation, QEasingCurve


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
        self.setFixedHeight(32)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # 왼쪽 액센트 바 (active 시 표시)
        self._accent = QFrame(self)
        self._accent.setFixedWidth(3)
        self._accent.setStyleSheet("background-color: transparent;")

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addWidget(self._accent)

        inner = QHBoxLayout()
        inner.setContentsMargins(22, 0, 10, 0)   # 들여쓰기
        inner.setSpacing(6)
        outer.addLayout(inner)

        dot = QLabel("·")
        dot.setStyleSheet("color: #555; font-size: 14px;")
        dot.setFixedWidth(10)
        inner.addWidget(dot)

        self._label = QLabel(name)
        self._label.setStyleSheet("color: #777777; font-size: 10px;")
        inner.addWidget(self._label, 1)

        self.setStyleSheet("SubItem { background-color: transparent; }")

    def set_active(self, active: bool):
        self._active = active
        if active:
            self._accent.setStyleSheet("background-color: #3a7bd5;")
            self._label.setStyleSheet("color: #ffffff; font-size: 10px; font-weight: bold;")
            self.setStyleSheet("SubItem { background-color: rgba(58,123,213,0.10); }")
        else:
            self._accent.setStyleSheet("background-color: transparent;")
            self._label.setStyleSheet("color: #777777; font-size: 10px;")
            self.setStyleSheet("SubItem { background-color: transparent; }")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.key)
        super().mousePressEvent(event)

    def enterEvent(self, event):
        if not self._active:
            self.setStyleSheet("SubItem { background-color: rgba(255,255,255,0.05); }")
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self._active:
            self.setStyleSheet("SubItem { background-color: rgba(58,123,213,0.10); }")
        else:
            self.setStyleSheet("SubItem { background-color: transparent; }")
        super().leaveEvent(event)


# ─────────────────────────────────────────────────────────────────────────────
# StepItem – 상위 단계 버튼 (하위 항목 포함 가능)
# ─────────────────────────────────────────────────────────────────────────────
class StepItem(QWidget):
    clicked    = Signal(str)   # step_key
    sub_clicked = Signal(str)  # sub_key

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
        self._header.setFixedHeight(48)
        self._header.setCursor(Qt.CursorShape.PointingHandCursor)

        self._accent = QFrame(self._header)
        self._accent.setFixedWidth(3)

        h_outer = QHBoxLayout(self._header)
        h_outer.setContentsMargins(0, 0, 0, 0)
        h_outer.setSpacing(0)
        h_outer.addWidget(self._accent)

        h_inner = QHBoxLayout()
        h_inner.setContentsMargins(10, 4, 10, 4)
        h_inner.setSpacing(8)
        h_outer.addLayout(h_inner)

        self._circle = QLabel(str(number))
        self._circle.setFixedSize(26, 26)
        self._circle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h_inner.addWidget(self._circle)

        self._name_label = QLabel(name)
        h_inner.addWidget(self._name_label, 1)

        if sub_items:
            self._expand_label = QLabel("▶")
            self._expand_label.setFixedWidth(12)
            self._expand_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._expand_label.setStyleSheet("color: #555; font-size: 8px;")
            h_inner.addWidget(self._expand_label)
        else:
            self._expand_label = None
            self._status_label = QLabel("○")
            self._status_label.setFixedWidth(14)
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

        # 헤더 클릭 이벤트
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
        has_sub = bool(self._sub_items)
        if self._status == self.STATUS_CURRENT:
            self._accent.setStyleSheet("background-color: #3a7bd5;")
            self._circle.setStyleSheet(
                "background-color: #3a7bd5; border-radius: 13px;"
                " color: white; font-weight: bold; font-size: 12px;"
            )
            self._name_label.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 11px;")
            self._header.setStyleSheet("QWidget { background-color: rgba(58,123,213,0.12); }")
            if not has_sub:
                self._status_label.setText("●")
                self._status_label.setStyleSheet("color: #3a7bd5; font-size: 10px;")
        elif self._status == self.STATUS_DONE:
            self._accent.setStyleSheet("background-color: transparent;")
            self._circle.setStyleSheet(
                "background-color: #2d4a2d; border-radius: 13px;"
                " color: #5cb85c; font-weight: bold; font-size: 12px;"
            )
            self._name_label.setStyleSheet("color: #888888; font-size: 11px;")
            self._header.setStyleSheet("")
            if not has_sub:
                self._status_label.setText("✓")
                self._status_label.setStyleSheet("color: #5cb85c; font-size: 10px;")
        else:
            self._accent.setStyleSheet("background-color: transparent;")
            self._circle.setStyleSheet(
                "background-color: #2d2d2d; border-radius: 13px;"
                " color: #666666; font-size: 12px;"
            )
            self._name_label.setStyleSheet("color: #777777; font-size: 11px;")
            self._header.setStyleSheet("")
            if not has_sub:
                self._status_label.setText("○")
                self._status_label.setStyleSheet("color: #555555; font-size: 10px;")

    def enterEvent(self, event):
        if self._status != self.STATUS_CURRENT:
            self._header.setStyleSheet("QWidget { background-color: rgba(255,255,255,0.05); }")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._apply_style()
        super().leaveEvent(event)


# ─────────────────────────────────────────────────────────────────────────────
# StepNavWidget – 전체 네비게이션 패널
# ─────────────────────────────────────────────────────────────────────────────
class StepNavWidget(QWidget):
    step_clicked = Signal(str)   # step_key 또는 sub_key

    def __init__(self, parent=None):
        super().__init__(parent)
        self._step_items: dict[str, StepItem] = {}
        # sub_key → parent step_key 매핑
        self._sub_parent: dict[str, str] = {}
        self._setup_ui()

    def _setup_ui(self):
        self.setFixedWidth(175)
        self.setObjectName("StepNavWidget")
        self.setStyleSheet(
            "QWidget#StepNavWidget { background-color: #1e1e1e;"
            " border-right: 1px solid #333333; }"
        )

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        # 스크롤 가능하도록 감싸기
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        outer_layout.addWidget(scroll)

        container = QWidget()
        container.setStyleSheet("background-color: #1e1e1e;")
        scroll.setWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 16, 0, 16)
        layout.setSpacing(0)

        # 타이틀
        title = QLabel("WORKFLOW")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "color: #555555; font-size: 9px; font-weight: bold;"
            " letter-spacing: 2px; padding-bottom: 14px;"
        )
        layout.addWidget(title)

        for i, (key, name, subs) in enumerate(STEP_TREE):
            # 단계 사이 연결선
            if i > 0:
                connector = QFrame()
                connector.setFixedSize(2, 8)
                connector.setStyleSheet("background-color: #2e2e2e;")
                wrapper = QHBoxLayout()
                wrapper.setContentsMargins(31, 0, 0, 0)
                wrapper.addWidget(connector)
                wrapper.addStretch()
                layout.addLayout(wrapper)

            item = StepItem(key, i + 1, name, subs)
            item.clicked.connect(self._on_step_clicked)
            item.sub_clicked.connect(self._on_sub_clicked)
            self._step_items[key] = item

            for sub_key, _ in subs:
                self._sub_parent[sub_key] = key

            layout.addWidget(item)

        layout.addStretch(1)

    # ── 내부 핸들러 ───────────────────────────────────────────────

    def _on_step_clicked(self, step_key: str):
        # 하위 항목이 없는 단계 → 활성화
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
        """step_key 또는 sub_key를 활성 상태로 설정."""
        if key in self._step_items:
            self._activate_step(key)
        elif key in self._sub_parent:
            self._activate_sub(self._sub_parent[key], key)

    def _activate_step(self, step_key: str):
        """하위 없는 단계를 current로, 순서에 따라 done/none 설정."""
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
        """하위 항목을 활성화, 부모 단계를 current로 설정."""
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
