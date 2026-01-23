"""
Initial Conditions Panel - Set initial field values

Configures fluid and solid initial conditions for the simulation.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGroupBox, QGridLayout, QLineEdit, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from common.app_data import app_data
from common.case_data import case_data


class InitialConditionsPanel(QWidget):
    """
    Panel for setting initial conditions.

    Features:
    - Fluid initial conditions (pressure, temperature, velocity)
    - Solid boundary conditions (temperature, heat transfer)
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
        title = QLabel("Initial Conditions")
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

        # ===== Fluid Group =====
        fluid_group = QGroupBox("Fluid")
        fluid_group.setFont(group_font)
        fluid_group.setStyleSheet(self.GROUPBOX_STYLE)

        fluid_layout = QGridLayout(fluid_group)

        # Pressure
        label_pressure = QLabel("Pressure [atm]:")
        label_pressure.setFont(label_font)
        fluid_layout.addWidget(label_pressure, 0, 0)

        self.edit_pressure = QLineEdit("1")
        self.edit_pressure.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_pressure.setFont(label_font)
        fluid_layout.addWidget(self.edit_pressure, 0, 1)

        # Temperature
        label_temp = QLabel("Temperature [K]:")
        label_temp.setFont(label_font)
        fluid_layout.addWidget(label_temp, 1, 0)

        self.edit_temperature = QLineEdit("310")
        self.edit_temperature.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_temperature.setFont(label_font)
        fluid_layout.addWidget(self.edit_temperature, 1, 1)

        # Velocity (x, y, z)
        label_velocity = QLabel("Velocity [m/s]:")
        label_velocity.setFont(label_font)
        fluid_layout.addWidget(label_velocity, 2, 0)

        vel_layout = QHBoxLayout()
        self.edit_vel_x = QLineEdit("0")
        self.edit_vel_x.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_vel_x.setFont(label_font)
        vel_layout.addWidget(self.edit_vel_x)

        self.edit_vel_y = QLineEdit("0")
        self.edit_vel_y.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_vel_y.setFont(label_font)
        vel_layout.addWidget(self.edit_vel_y)

        self.edit_vel_z = QLineEdit("0")
        self.edit_vel_z.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_vel_z.setFont(label_font)
        vel_layout.addWidget(self.edit_vel_z)

        fluid_layout.addLayout(vel_layout, 2, 1)
        fluid_layout.setColumnStretch(0, 1)
        fluid_layout.setColumnStretch(1, 1)

        layout.addWidget(fluid_group)

        # ===== Solid Group =====
        solid_group = QGroupBox("Solid")
        solid_group.setFont(group_font)
        solid_group.setStyleSheet(self.GROUPBOX_STYLE)

        solid_layout = QGridLayout(solid_group)

        # Temperature
        label_solid_temp = QLabel("Temperature [K]:")
        label_solid_temp.setFont(label_font)
        solid_layout.addWidget(label_solid_temp, 0, 0)

        self.edit_solid_temp = QLineEdit("300")
        self.edit_solid_temp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_solid_temp.setFont(label_font)
        solid_layout.addWidget(self.edit_solid_temp, 0, 1)

        # Heat coefficient
        label_heat_coeff = QLabel("Heat coefficient [W/(m²K)]:")
        label_heat_coeff.setFont(label_font)
        solid_layout.addWidget(label_heat_coeff, 1, 0)

        self.edit_heat_coeff = QLineEdit("1000")
        self.edit_heat_coeff.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_heat_coeff.setFont(label_font)
        solid_layout.addWidget(self.edit_heat_coeff, 1, 1)

        # External Type
        label_ext_type = QLabel("External Type:")
        label_ext_type.setFont(label_font)
        solid_layout.addWidget(label_ext_type, 2, 0)

        self.combo_ext_type = QComboBox()
        self.combo_ext_type.setFont(label_font)
        self.combo_ext_type.addItems([
            "externalWallHeatFluxTemperature",
            "Convective Heat Transfer",
            "wallHeatTransfer"
        ])
        solid_layout.addWidget(self.combo_ext_type, 2, 1)

        solid_layout.setColumnStretch(0, 1)
        solid_layout.setColumnStretch(1, 1)

        layout.addWidget(solid_group)

        # Spacer
        layout.addStretch()

    def load_data(self) -> None:
        """Load initial conditions from case_data."""
        pass

    def save_data(self) -> None:
        """Save initial conditions to case_data."""
        pass
