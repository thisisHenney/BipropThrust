from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Signal, Qt


class StepItem(QWidget):
    """단일 단계 버튼 위젯."""

    clicked = Signal(str)

    STATUS_NONE    = "none"
    STATUS_CURRENT = "current"
    STATUS_DONE    = "done"

    def __init__(self, step_key: str, number: int, name: str, parent=None):
        super().__init__(parent)
        self.step_key = step_key
        self._status = self.STATUS_NONE
        self._setup_ui(number, name)
        self._apply_style()

    def _setup_ui(self, number: int, name: str):
        self.setFixedHeight(52)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # 왼쪽 액센트 바
        self._accent = QFrame(self)
        self._accent.setFixedWidth(3)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addWidget(self._accent)

        inner = QHBoxLayout()
        inner.setContentsMargins(10, 6, 10, 6)
        inner.setSpacing(10)
        outer.addLayout(inner)

        # 단계 번호 원형
        self._circle = QLabel(str(number))
        self._circle.setFixedSize(26, 26)
        self._circle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inner.addWidget(self._circle)

        # 단계 이름
        self._name_label = QLabel(name)
        inner.addWidget(self._name_label, 1)

        # 상태 아이콘
        self._status_label = QLabel("○")
        self._status_label.setFixedWidth(14)
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inner.addWidget(self._status_label)

    def set_status(self, status: str):
        self._status = status
        self._apply_style()

    def _apply_style(self):
        if self._status == self.STATUS_CURRENT:
            self._accent.setStyleSheet("background-color: #3a7bd5;")
            self._circle.setStyleSheet(
                "background-color: #3a7bd5; border-radius: 13px;"
                " color: white; font-weight: bold; font-size: 12px;"
            )
            self._name_label.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 11px;")
            self._status_label.setText("●")
            self._status_label.setStyleSheet("color: #3a7bd5; font-size: 10px;")
            self.setStyleSheet("StepItem { background-color: rgba(58,123,213,0.12); }")
        elif self._status == self.STATUS_DONE:
            self._accent.setStyleSheet("background-color: transparent;")
            self._circle.setStyleSheet(
                "background-color: #2d4a2d; border-radius: 13px;"
                " color: #5cb85c; font-weight: bold; font-size: 12px;"
            )
            self._name_label.setStyleSheet("color: #888888; font-size: 11px;")
            self._status_label.setText("✓")
            self._status_label.setStyleSheet("color: #5cb85c; font-size: 10px;")
            self.setStyleSheet("StepItem { background-color: transparent; }")
        else:
            self._accent.setStyleSheet("background-color: transparent;")
            self._circle.setStyleSheet(
                "background-color: #2d2d2d; border-radius: 13px;"
                " color: #666666; font-size: 12px;"
            )
            self._name_label.setStyleSheet("color: #777777; font-size: 11px;")
            self._status_label.setText("○")
            self._status_label.setStyleSheet("color: #555555; font-size: 10px;")
            self.setStyleSheet("StepItem { background-color: transparent; }")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.step_key)
        super().mousePressEvent(event)

    def enterEvent(self, event):
        if self._status != self.STATUS_CURRENT:
            self.setStyleSheet("StepItem { background-color: rgba(255,255,255,0.06); }")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._apply_style()
        super().leaveEvent(event)


class StepNavWidget(QWidget):
    """Workflow Step/Wizard 네비게이션 위젯."""

    step_clicked = Signal(str)

    STEPS = [
        ("geometry", "Geometry"),
        ("mesh",     "Mesh Gen."),
        ("run",      "Run"),
        ("post",     "Post"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._step_items: dict[str, StepItem] = {}
        self._setup_ui()

    def _setup_ui(self):
        self.setFixedWidth(160)
        self.setObjectName("StepNavWidget")
        self.setStyleSheet(
            "QWidget#StepNavWidget { background-color: #1e1e1e;"
            " border-right: 1px solid #333333; }"
        )

        layout = QVBoxLayout(self)
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

        for i, (key, name) in enumerate(self.STEPS):
            # 단계 연결선 (첫 번째 제외)
            if i > 0:
                connector = QFrame()
                connector.setFixedSize(2, 10)
                connector.setStyleSheet("background-color: #2e2e2e;")
                wrapper = QHBoxLayout()
                wrapper.setContentsMargins(28, 0, 0, 0)
                wrapper.addWidget(connector)
                wrapper.addStretch()
                layout.addLayout(wrapper)

            item = StepItem(key, i + 1, name)
            item.clicked.connect(self.step_clicked.emit)
            self._step_items[key] = item
            layout.addWidget(item)

        layout.addStretch(1)

    def set_current(self, step_key: str):
        """현재 활성 단계 설정. 이전 단계는 done, 이후 단계는 none."""
        keys = [k for k, _ in self.STEPS]
        try:
            current_idx = keys.index(step_key)
        except ValueError:
            return

        for i, key in enumerate(keys):
            item = self._step_items.get(key)
            if item is None:
                continue
            if i < current_idx:
                item.set_status(StepItem.STATUS_DONE)
            elif i == current_idx:
                item.set_status(StepItem.STATUS_CURRENT)
            else:
                item.set_status(StepItem.STATUS_NONE)

    def mark_done(self, step_key: str):
        """특정 단계를 완료 상태로 표시."""
        item = self._step_items.get(step_key)
        if item:
            item.set_status(StepItem.STATUS_DONE)
