"""
Mesh Generation Panel - Mesh configuration and generation

Provides controls for configuring mesh generation parameters
including base grid, boundary layers, and buffer layers.
"""

from pathlib import Path

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QGroupBox, QGridLayout, QLineEdit,
    QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from common.app_data import app_data
from common.case_data import case_data


class MeshGenerationPanel(QWidget):
    """
    Panel for mesh generation settings.

    Features:
    - Base grid configuration (X, Y, Z cells)
    - Boundary layer settings
    - Buffer layer settings
    - Generate mesh button
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
        Initialize mesh generation panel.

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
        self.vtk_pre = context.get("vtk_pre") if context else None

        # Setup UI
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Setup the UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        # Title
        title = QLabel("Mesh Generation")
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

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        # Content widget
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Fonts
        group_font = QFont()
        group_font.setPointSize(9)
        group_font.setBold(True)

        label_font = QFont()
        label_font.setPointSize(9)

        # ===== Block Mesh Group =====
        block_mesh_group = QGroupBox("Block Mesh")
        block_mesh_group.setFont(group_font)
        block_mesh_group.setStyleSheet(self.GROUPBOX_STYLE)
        block_mesh_group.setMaximumHeight(150)

        block_layout = QVBoxLayout(block_mesh_group)

        # Base Grid SubGroup
        basegrid_group = QGroupBox("Base Grid")
        basegrid_group.setFont(label_font)
        basegrid_group.setStyleSheet(self.GROUPBOX_STYLE)

        basegrid_layout = QGridLayout(basegrid_group)

        # X cells
        label_x = QLabel("X:")
        label_x.setFont(label_font)
        basegrid_layout.addWidget(label_x, 0, 0)

        self.edit_basegrid_x = QLineEdit()
        self.edit_basegrid_x.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_basegrid_x.setFont(label_font)
        self.edit_basegrid_x.setPlaceholderText("100")
        basegrid_layout.addWidget(self.edit_basegrid_x, 0, 1)

        # Y cells
        label_y = QLabel("Y:")
        label_y.setFont(label_font)
        basegrid_layout.addWidget(label_y, 1, 0)

        self.edit_basegrid_y = QLineEdit()
        self.edit_basegrid_y.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_basegrid_y.setFont(label_font)
        self.edit_basegrid_y.setPlaceholderText("100")
        basegrid_layout.addWidget(self.edit_basegrid_y, 1, 1)

        # Z cells
        label_z = QLabel("Z:")
        label_z.setFont(label_font)
        basegrid_layout.addWidget(label_z, 2, 0)

        self.edit_basegrid_z = QLineEdit()
        self.edit_basegrid_z.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_basegrid_z.setFont(label_font)
        self.edit_basegrid_z.setPlaceholderText("100")
        basegrid_layout.addWidget(self.edit_basegrid_z, 2, 1)

        basegrid_layout.setColumnStretch(0, 1)
        basegrid_layout.setColumnStretch(1, 1)

        block_layout.addWidget(basegrid_group)
        content_layout.addWidget(block_mesh_group)

        # ===== Boundary Layer Group =====
        boundary_group = QGroupBox("Boundary Layer")
        boundary_group.setFont(group_font)
        boundary_group.setStyleSheet(self.GROUPBOX_STYLE)

        boundary_layout = QGridLayout(boundary_group)

        # Total Layer Number
        label_total_layers = QLabel("Total Layer Number:")
        label_total_layers.setFont(label_font)
        boundary_layout.addWidget(label_total_layers, 0, 0)

        self.edit_total_layers = QLineEdit()
        self.edit_total_layers.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_total_layers.setFont(label_font)
        self.edit_total_layers.setPlaceholderText("5")
        boundary_layout.addWidget(self.edit_total_layers, 0, 1)

        # First Layer Height
        label_first_height = QLabel("First Layer Height:")
        label_first_height.setFont(label_font)
        boundary_layout.addWidget(label_first_height, 1, 0)

        self.edit_first_height = QLineEdit()
        self.edit_first_height.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_first_height.setFont(label_font)
        self.edit_first_height.setPlaceholderText("0.001")
        boundary_layout.addWidget(self.edit_first_height, 1, 1)

        # Expansion Ratio 1
        label_expansion1 = QLabel("Expansion Ratio 1:")
        label_expansion1.setFont(label_font)
        boundary_layout.addWidget(label_expansion1, 2, 0)

        self.edit_expansion1 = QLineEdit()
        self.edit_expansion1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_expansion1.setFont(label_font)
        self.edit_expansion1.setPlaceholderText("1.2")
        boundary_layout.addWidget(self.edit_expansion1, 2, 1)

        # Expansion Ratio 2
        label_expansion2 = QLabel("Expansion Ratio 2:")
        label_expansion2.setFont(label_font)
        boundary_layout.addWidget(label_expansion2, 3, 0)

        self.edit_expansion2 = QLineEdit()
        self.edit_expansion2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_expansion2.setFont(label_font)
        self.edit_expansion2.setPlaceholderText("1.2")
        boundary_layout.addWidget(self.edit_expansion2, 3, 1)

        # Total Layer Height (calculated, disabled)
        label_total_height = QLabel("Total Layer Height:")
        label_total_height.setFont(label_font)
        label_total_height.setEnabled(False)
        boundary_layout.addWidget(label_total_height, 4, 0)

        self.edit_total_height = QLineEdit()
        self.edit_total_height.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_total_height.setFont(label_font)
        self.edit_total_height.setEnabled(False)
        self.edit_total_height.setPlaceholderText("(calculated)")
        boundary_layout.addWidget(self.edit_total_height, 4, 1)

        boundary_layout.setColumnStretch(0, 1)
        boundary_layout.setColumnStretch(1, 1)

        content_layout.addWidget(boundary_group)

        # ===== Buffer Layer Group =====
        buffer_group = QGroupBox("Buffer Layer")
        buffer_group.setFont(group_font)
        buffer_group.setStyleSheet(self.GROUPBOX_STYLE)

        buffer_layout = QGridLayout(buffer_group)

        # Number of Buffer Layer 1
        label_buffer1_num = QLabel("Buffer Layer 1 Number:")
        label_buffer1_num.setFont(label_font)
        buffer_layout.addWidget(label_buffer1_num, 0, 0)

        self.edit_buffer1_num = QLineEdit()
        self.edit_buffer1_num.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_buffer1_num.setFont(label_font)
        self.edit_buffer1_num.setPlaceholderText("3")
        buffer_layout.addWidget(self.edit_buffer1_num, 0, 1)

        # Number of Buffer Layer 2
        label_buffer2_num = QLabel("Buffer Layer 2 Number:")
        label_buffer2_num.setFont(label_font)
        buffer_layout.addWidget(label_buffer2_num, 1, 0)

        self.edit_buffer2_num = QLineEdit()
        self.edit_buffer2_num.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_buffer2_num.setFont(label_font)
        self.edit_buffer2_num.setPlaceholderText("2")
        buffer_layout.addWidget(self.edit_buffer2_num, 1, 1)

        # Last Layer Octree Ratio 1
        label_octree1 = QLabel("Octree Ratio 1:")
        label_octree1.setFont(label_font)
        buffer_layout.addWidget(label_octree1, 2, 0)

        self.edit_octree1 = QLineEdit()
        self.edit_octree1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_octree1.setFont(label_font)
        self.edit_octree1.setPlaceholderText("0.5")
        buffer_layout.addWidget(self.edit_octree1, 2, 1)

        # Last Layer Octree Ratio 2
        label_octree2 = QLabel("Octree Ratio 2:")
        label_octree2.setFont(label_font)
        buffer_layout.addWidget(label_octree2, 3, 0)

        self.edit_octree2 = QLineEdit()
        self.edit_octree2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_octree2.setFont(label_font)
        self.edit_octree2.setPlaceholderText("0.5")
        buffer_layout.addWidget(self.edit_octree2, 3, 1)

        buffer_layout.setColumnStretch(0, 1)
        buffer_layout.setColumnStretch(1, 1)

        content_layout.addWidget(buffer_group)

        # Spacer
        content_layout.addStretch()

        scroll.setWidget(content)

        # ===== Bottom buttons =====
        # Separator
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line2)

        # Button row
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btn_generate = QPushButton("Generate Mesh")
        self.btn_generate.setMinimumHeight(30)
        self.btn_generate.setMinimumWidth(120)
        btn_layout.addWidget(self.btn_generate)

        layout.addLayout(btn_layout)

    def _connect_signals(self) -> None:
        """Connect UI signals."""
        self.btn_generate.clicked.connect(self._on_generate_clicked)

        # Connect boundary layer inputs to calculate total height
        self.edit_total_layers.textChanged.connect(self._calculate_total_height)
        self.edit_first_height.textChanged.connect(self._calculate_total_height)
        self.edit_expansion1.textChanged.connect(self._calculate_total_height)

    def _on_generate_clicked(self) -> None:
        """Handle Generate Mesh button click."""
        # Get base grid values
        x = self.edit_basegrid_x.text() or "100"
        y = self.edit_basegrid_y.text() or "100"
        z = self.edit_basegrid_z.text() or "100"

        print(f"Generating mesh with base grid: ({x}, {y}, {z})")

        # TODO: Update blockMeshDict with values
        # TODO: Run mesh generation command

        if self.exec_widget:
            # Example command - would need to be adapted for actual OpenFOAM
            cmd = "./Allrun"
            self.exec_widget.run(cmd)

    def _calculate_total_height(self) -> None:
        """Calculate and display total boundary layer height."""
        try:
            n_layers = int(self.edit_total_layers.text()) if self.edit_total_layers.text() else 0
            first_height = float(self.edit_first_height.text()) if self.edit_first_height.text() else 0.0
            expansion = float(self.edit_expansion1.text()) if self.edit_expansion1.text() else 1.0

            if n_layers > 0 and first_height > 0 and expansion > 0:
                # Calculate total height using geometric series
                if abs(expansion - 1.0) < 1e-6:
                    total = first_height * n_layers
                else:
                    total = first_height * (1 - expansion ** n_layers) / (1 - expansion)

                self.edit_total_height.setText(f"{total:.6f}")
            else:
                self.edit_total_height.clear()
        except (ValueError, ZeroDivisionError):
            self.edit_total_height.clear()

    def load_data(self) -> None:
        """Load mesh settings from case_data."""
        # TODO: Load values from OpenFOAM dict files
        pass

    def save_data(self) -> None:
        """Save mesh settings to case_data."""
        # TODO: Save values to OpenFOAM dict files
        pass
