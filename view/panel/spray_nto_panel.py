"""
Spray NTO Panel - NTO spray injection properties

Configures NTO (Nitrogen Tetroxide) spray injection parameters.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGroupBox, QGridLayout, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from common.app_data import app_data
from common.case_data import case_data


class SprayNTOPanel(QWidget):
    """
    Panel for NTO spray properties.

    Features:
    - Operating conditions (mass, duration, velocity, parcels, SMD)
    - Geometric conditions (position, direction, diameters)
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
        title = QLabel("Spray Property - NTO")
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

        # ===== Operating Condition Group =====
        oper_group = QGroupBox("Operating Condition")
        oper_group.setFont(group_font)
        oper_group.setStyleSheet(self.GROUPBOX_STYLE)

        oper_layout = QGridLayout(oper_group)

        # Total Mass
        label_mass = QLabel("Total Mass [kg]:")
        label_mass.setFont(label_font)
        oper_layout.addWidget(label_mass, 0, 0)

        self.edit_mass = QLineEdit("2.18e-4")
        self.edit_mass.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_mass.setFont(label_font)
        oper_layout.addWidget(self.edit_mass, 0, 1)

        # Duration
        label_duration = QLabel("Duration [sec]:")
        label_duration.setFont(label_font)
        oper_layout.addWidget(label_duration, 1, 0)

        self.edit_duration = QLineEdit("0.1")
        self.edit_duration.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_duration.setFont(label_font)
        oper_layout.addWidget(self.edit_duration, 1, 1)

        # Velocity
        label_velocity = QLabel("Velocity [m/s]:")
        label_velocity.setFont(label_font)
        oper_layout.addWidget(label_velocity, 2, 0)

        self.edit_velocity = QLineEdit("18")
        self.edit_velocity.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_velocity.setFont(label_font)
        oper_layout.addWidget(self.edit_velocity, 2, 1)

        # Parcels Per Second
        label_parcels = QLabel("Parcels Per Second:")
        label_parcels.setFont(label_font)
        oper_layout.addWidget(label_parcels, 3, 0)

        self.edit_parcels = QLineEdit("5000000")
        self.edit_parcels.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_parcels.setFont(label_font)
        oper_layout.addWidget(self.edit_parcels, 3, 1)

        # SMD
        label_smd = QLabel("SMD [um]:")
        label_smd.setFont(label_font)
        oper_layout.addWidget(label_smd, 4, 0)

        self.edit_smd = QLineEdit("26")
        self.edit_smd.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_smd.setFont(label_font)
        oper_layout.addWidget(self.edit_smd, 4, 1)

        oper_layout.setColumnStretch(0, 1)
        oper_layout.setColumnStretch(1, 1)

        layout.addWidget(oper_group)

        # ===== Geometric Condition Group =====
        geom_group = QGroupBox("Geometric Condition")
        geom_group.setFont(group_font)
        geom_group.setStyleSheet(self.GROUPBOX_STYLE)

        geom_layout = QGridLayout(geom_group)

        # Position (x, y, z)
        label_pos = QLabel("Position (x,y,z) [m]:")
        label_pos.setFont(label_font)
        geom_layout.addWidget(label_pos, 0, 0)

        pos_layout = QHBoxLayout()
        self.edit_pos_x = QLineEdit("0.0001")
        self.edit_pos_x.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pos_layout.addWidget(self.edit_pos_x)

        self.edit_pos_y = QLineEdit("0.0")
        self.edit_pos_y.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pos_layout.addWidget(self.edit_pos_y)

        self.edit_pos_z = QLineEdit("0.0")
        self.edit_pos_z.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pos_layout.addWidget(self.edit_pos_z)

        geom_layout.addLayout(pos_layout, 0, 1)

        # Direction (x, y, z)
        label_dir = QLabel("Direction (x,y,z):")
        label_dir.setFont(label_font)
        geom_layout.addWidget(label_dir, 1, 0)

        dir_layout = QHBoxLayout()
        self.edit_dir_x = QLineEdit("1")
        self.edit_dir_x.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dir_layout.addWidget(self.edit_dir_x)

        self.edit_dir_y = QLineEdit("0")
        self.edit_dir_y.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dir_layout.addWidget(self.edit_dir_y)

        self.edit_dir_z = QLineEdit("0")
        self.edit_dir_z.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dir_layout.addWidget(self.edit_dir_z)

        geom_layout.addLayout(dir_layout, 1, 1)

        # Outer Diameter
        label_outer = QLabel("Outer Diameter [m]:")
        label_outer.setFont(label_font)
        geom_layout.addWidget(label_outer, 2, 0)

        self.edit_outer_dia = QLineEdit("1.5e-3")
        self.edit_outer_dia.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_outer_dia.setFont(label_font)
        geom_layout.addWidget(self.edit_outer_dia, 2, 1)

        # Inner Diameter
        label_inner = QLabel("Inner Diameter [m]:")
        label_inner.setFont(label_font)
        geom_layout.addWidget(label_inner, 3, 0)

        self.edit_inner_dia = QLineEdit("9.8e-4")
        self.edit_inner_dia.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_inner_dia.setFont(label_font)
        geom_layout.addWidget(self.edit_inner_dia, 3, 1)

        geom_layout.setColumnStretch(0, 1)
        geom_layout.setColumnStretch(1, 1)

        layout.addWidget(geom_group)

        # Spacer
        layout.addStretch()

    def load_data(self) -> None:
        """Load NTO spray properties from case_data."""
        pass

    def save_data(self) -> None:
        """Save NTO spray properties to case_data."""
        pass
