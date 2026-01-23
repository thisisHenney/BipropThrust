"""
Run Panel - Simulation execution control

Provides controls for running, pausing, and stopping simulations.
"""

from datetime import datetime

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QGroupBox, QGridLayout, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from common.app_data import app_data
from common.case_data import case_data


class RunPanel(QWidget):
    """
    Panel for controlling simulation execution.

    Features:
    - Display case info (ID, creation time, status)
    - Run/Pause/Stop buttons
    - Status monitoring
    """

    # Style constants
    GROUPBOX_STYLE = """
        QGroupBox {
            border: 1px solid;
            border-radius: 6px;
            margin-top: 9px;
            border-color: #c8c8c8;
            padding: 3px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 10px;
            padding: 2px 3px;
        }
    """

    def __init__(self, parent=None, context=None):
        """
        Initialize run panel.

        Args:
            parent: Parent widget
            context: Application context for service access
        """
        super().__init__(parent)

        self.context = context
        self.app_data = app_data
        self.case_data = case_data

        # Get services from context
        self.exec_widget = context.get("exec") if context else None

        # Setup UI
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Setup the UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        # Title
        title = QLabel("Run")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # Fonts
        group_font = QFont()
        group_font.setPointSize(9)
        group_font.setBold(True)

        label_font = QFont()
        label_font.setPointSize(9)

        # ===== Case Info Group =====
        info_group = QGroupBox("Case Information")
        info_group.setFont(group_font)
        info_group.setStyleSheet(self.GROUPBOX_STYLE)

        info_layout = QGridLayout(info_group)

        # Case ID
        label_id = QLabel("Case ID:")
        label_id.setFont(label_font)
        info_layout.addWidget(label_id, 0, 0)

        self.label_case_id = QLabel("-")
        self.label_case_id.setFont(label_font)
        self.label_case_id.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(self.label_case_id, 0, 1)

        # Creation Time
        label_time = QLabel("Created:")
        label_time.setFont(label_font)
        info_layout.addWidget(label_time, 1, 0)

        self.label_create_time = QLabel("-")
        self.label_create_time.setFont(label_font)
        self.label_create_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(self.label_create_time, 1, 1)

        # Status
        label_status = QLabel("Status:")
        label_status.setFont(label_font)
        info_layout.addWidget(label_status, 2, 0)

        self.label_status = QLabel("Ready")
        self.label_status.setFont(label_font)
        self.label_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(self.label_status, 2, 1)

        info_layout.setColumnStretch(1, 1)

        layout.addWidget(info_group)

        # Separator
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line2)

        # ===== Control Buttons =====
        btn_layout = QHBoxLayout()

        self.btn_run = QPushButton("Run")
        self.btn_run.setMinimumHeight(35)
        self.btn_run.setFont(group_font)
        btn_layout.addWidget(self.btn_run)

        self.btn_pause = QPushButton("Pause")
        self.btn_pause.setMinimumHeight(35)
        self.btn_pause.setFont(label_font)
        self.btn_pause.setEnabled(False)
        btn_layout.addWidget(self.btn_pause)

        self.btn_stop = QPushButton("Stop")
        self.btn_stop.setMinimumHeight(35)
        self.btn_stop.setFont(label_font)
        self.btn_stop.setEnabled(False)
        btn_layout.addWidget(self.btn_stop)

        layout.addLayout(btn_layout)

        # Spacer
        layout.addStretch()

    def _connect_signals(self) -> None:
        """Connect UI signals."""
        self.btn_run.clicked.connect(self._on_run_clicked)
        self.btn_pause.clicked.connect(self._on_pause_clicked)
        self.btn_stop.clicked.connect(self._on_stop_clicked)

    def _on_run_clicked(self) -> None:
        """Handle Run button click."""
        print("Starting simulation...")
        self._update_status("Running")
        self._update_button_states(running=True)

        if self.exec_widget:
            # Run the simulation
            cmd = "./Allrun"
            self.exec_widget.run(cmd)

    def _on_pause_clicked(self) -> None:
        """Handle Pause button click."""
        print("Pausing simulation...")
        self._update_status("Paused")

        if self.exec_widget:
            self.exec_widget.pause()

    def _on_stop_clicked(self) -> None:
        """Handle Stop button click."""
        print("Stopping simulation...")
        self._update_status("Stopped")
        self._update_button_states(running=False)

        if self.exec_widget:
            self.exec_widget.stop()

    def _update_status(self, status: str) -> None:
        """Update status display."""
        self.label_status.setText(status)

        # Color coding for status
        color_map = {
            "Ready": "#333333",
            "Running": "#2e7d32",  # Green
            "Paused": "#f57c00",   # Orange
            "Stopped": "#c62828",  # Red
            "Completed": "#1565c0", # Blue
        }
        color = color_map.get(status, "#333333")
        self.label_status.setStyleSheet(f"color: {color}; font-weight: bold;")

    def _update_button_states(self, running: bool) -> None:
        """Update button enabled states based on running status."""
        self.btn_run.setEnabled(not running)
        self.btn_pause.setEnabled(running)
        self.btn_stop.setEnabled(running)

    def load_data(self) -> None:
        """Load case info from case_data."""
        if self.case_data.path:
            from pathlib import Path
            case_path = Path(self.case_data.path)

            # Case ID (folder name)
            self.label_case_id.setText(case_path.name)

            # Creation time (from folder stats)
            try:
                create_time = datetime.fromtimestamp(case_path.stat().st_ctime)
                self.label_create_time.setText(create_time.strftime("%Y-%m-%d %H:%M:%S"))
            except Exception:
                self.label_create_time.setText("-")

            # Status
            self._update_status("Ready")
