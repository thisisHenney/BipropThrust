"""
Materials Panel - Define material properties

Configures material properties for the simulation.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame,
    QGroupBox, QGridLayout, QLineEdit, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from common.app_data import app_data
from common.case_data import case_data


class MaterialsPanel(QWidget):
    """
    Panel for material properties.

    Features:
    - Fluid material properties
    - Solid material properties
    """

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
        super().__init__(parent)
        self.context = context
        self.app_data = app_data
        self.case_data = case_data
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        # Title
        title = QLabel("Materials")
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

        # ===== Fluid Properties Group =====
        fluid_group = QGroupBox("Fluid Properties")
        fluid_group.setFont(group_font)
        fluid_group.setStyleSheet(self.GROUPBOX_STYLE)

        fluid_layout = QGridLayout(fluid_group)

        # Material Database
        label_db = QLabel("Material Database:")
        label_db.setFont(label_font)
        fluid_layout.addWidget(label_db, 0, 0)

        self.combo_fluid_db = QComboBox()
        self.combo_fluid_db.setFont(label_font)
        self.combo_fluid_db.addItems(["NASA CEA", "User Defined"])
        fluid_layout.addWidget(self.combo_fluid_db, 0, 1)

        # Density
        label_density = QLabel("Density [kg/m³]:")
        label_density.setFont(label_font)
        fluid_layout.addWidget(label_density, 1, 0)

        self.edit_fluid_density = QLineEdit("1.225")
        self.edit_fluid_density.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_fluid_density.setFont(label_font)
        fluid_layout.addWidget(self.edit_fluid_density, 1, 1)

        # Viscosity
        label_visc = QLabel("Dynamic Viscosity [Pa·s]:")
        label_visc.setFont(label_font)
        fluid_layout.addWidget(label_visc, 2, 0)

        self.edit_fluid_viscosity = QLineEdit("1.8e-5")
        self.edit_fluid_viscosity.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_fluid_viscosity.setFont(label_font)
        fluid_layout.addWidget(self.edit_fluid_viscosity, 2, 1)

        # Specific Heat
        label_cp = QLabel("Specific Heat [J/(kg·K)]:")
        label_cp.setFont(label_font)
        fluid_layout.addWidget(label_cp, 3, 0)

        self.edit_fluid_cp = QLineEdit("1005")
        self.edit_fluid_cp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_fluid_cp.setFont(label_font)
        fluid_layout.addWidget(self.edit_fluid_cp, 3, 1)

        # Thermal Conductivity
        label_k = QLabel("Thermal Conductivity [W/(m·K)]:")
        label_k.setFont(label_font)
        fluid_layout.addWidget(label_k, 4, 0)

        self.edit_fluid_k = QLineEdit("0.026")
        self.edit_fluid_k.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_fluid_k.setFont(label_font)
        fluid_layout.addWidget(self.edit_fluid_k, 4, 1)

        fluid_layout.setColumnStretch(0, 1)
        fluid_layout.setColumnStretch(1, 1)

        layout.addWidget(fluid_group)

        # ===== Solid Properties Group =====
        solid_group = QGroupBox("Solid Properties")
        solid_group.setFont(group_font)
        solid_group.setStyleSheet(self.GROUPBOX_STYLE)

        solid_layout = QGridLayout(solid_group)

        # Material
        label_mat = QLabel("Material:")
        label_mat.setFont(label_font)
        solid_layout.addWidget(label_mat, 0, 0)

        self.combo_solid_mat = QComboBox()
        self.combo_solid_mat.setFont(label_font)
        self.combo_solid_mat.addItems(["Steel", "Aluminum", "Copper", "User Defined"])
        solid_layout.addWidget(self.combo_solid_mat, 0, 1)

        # Density
        label_solid_density = QLabel("Density [kg/m³]:")
        label_solid_density.setFont(label_font)
        solid_layout.addWidget(label_solid_density, 1, 0)

        self.edit_solid_density = QLineEdit("7850")
        self.edit_solid_density.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_solid_density.setFont(label_font)
        solid_layout.addWidget(self.edit_solid_density, 1, 1)

        # Specific Heat
        label_solid_cp = QLabel("Specific Heat [J/(kg·K)]:")
        label_solid_cp.setFont(label_font)
        solid_layout.addWidget(label_solid_cp, 2, 0)

        self.edit_solid_cp = QLineEdit("500")
        self.edit_solid_cp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_solid_cp.setFont(label_font)
        solid_layout.addWidget(self.edit_solid_cp, 2, 1)

        # Thermal Conductivity
        label_solid_k = QLabel("Thermal Conductivity [W/(m·K)]:")
        label_solid_k.setFont(label_font)
        solid_layout.addWidget(label_solid_k, 3, 0)

        self.edit_solid_k = QLineEdit("50")
        self.edit_solid_k.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_solid_k.setFont(label_font)
        solid_layout.addWidget(self.edit_solid_k, 3, 1)

        solid_layout.setColumnStretch(0, 1)
        solid_layout.setColumnStretch(1, 1)

        layout.addWidget(solid_group)

        # Spacer
        layout.addStretch()

    def load_data(self) -> None:
        """Load material properties from case_data."""
        pass

    def save_data(self) -> None:
        """Save material properties to case_data."""
        pass
