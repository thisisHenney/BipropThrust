"""
Numerical Conditions Panel - Configure numerical settings

Sets discretization schemes and PIMPLE algorithm parameters.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame,
    QGroupBox, QGridLayout, QLineEdit, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from common.app_data import app_data
from common.case_data import case_data


class NumericalConditionsPanel(QWidget):
    """
    Panel for numerical condition settings.

    Features:
    - Discretization schemes (time, momentum, energy, turbulence, mass fraction)
    - PIMPLE settings (correctors, flux scheme)
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
        title = QLabel("Numerical Conditions")
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

        # ===== Discretization Schemes Group =====
        disc_group = QGroupBox("Discretization Schemes")
        disc_group.setFont(group_font)
        disc_group.setStyleSheet(self.GROUPBOX_STYLE)

        disc_layout = QGridLayout(disc_group)

        # Time
        label_time = QLabel("Time:")
        label_time.setFont(label_font)
        disc_layout.addWidget(label_time, 0, 0)

        self.combo_time = QComboBox()
        self.combo_time.setFont(label_font)
        self.combo_time.addItems(["Euler", "Steady"])
        disc_layout.addWidget(self.combo_time, 0, 1)

        # Momentum
        label_momentum = QLabel("Momentum:")
        label_momentum.setFont(label_font)
        disc_layout.addWidget(label_momentum, 1, 0)

        self.combo_momentum = QComboBox()
        self.combo_momentum.setFont(label_font)
        self.combo_momentum.addItems(["Minmod", "MinmodV", "vanLeer"])
        self.combo_momentum.setCurrentIndex(1)
        disc_layout.addWidget(self.combo_momentum, 1, 1)

        # Energy
        label_energy = QLabel("Energy:")
        label_energy.setFont(label_font)
        disc_layout.addWidget(label_energy, 2, 0)

        self.combo_energy = QComboBox()
        self.combo_energy.setFont(label_font)
        self.combo_energy.addItems(["Minmod", "MinmodV", "vanLeer"])
        disc_layout.addWidget(self.combo_energy, 2, 1)

        # Turbulence
        label_turb = QLabel("Turbulence:")
        label_turb.setFont(label_font)
        disc_layout.addWidget(label_turb, 3, 0)

        self.combo_turbulence = QComboBox()
        self.combo_turbulence.setFont(label_font)
        self.combo_turbulence.addItems(["upwind", "Minmod"])
        disc_layout.addWidget(self.combo_turbulence, 3, 1)

        # Mass Fraction
        label_mass = QLabel("Mass Fraction:")
        label_mass.setFont(label_font)
        disc_layout.addWidget(label_mass, 4, 0)

        self.combo_mass_fraction = QComboBox()
        self.combo_mass_fraction.setFont(label_font)
        self.combo_mass_fraction.addItems(["Minmod", "MinmodV", "vanLeer"])
        disc_layout.addWidget(self.combo_mass_fraction, 4, 1)

        disc_layout.setColumnStretch(0, 1)
        disc_layout.setColumnStretch(1, 1)

        layout.addWidget(disc_group)

        # ===== PIMPLE Group =====
        pimple_group = QGroupBox("PIMPLE")
        pimple_group.setFont(group_font)
        pimple_group.setStyleSheet(self.GROUPBOX_STYLE)

        pimple_layout = QGridLayout(pimple_group)

        # nCorrectors
        label_ncorr = QLabel("nCorrectors:")
        label_ncorr.setFont(label_font)
        pimple_layout.addWidget(label_ncorr, 0, 0)

        self.edit_ncorrectors = QLineEdit("2")
        self.edit_ncorrectors.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_ncorrectors.setFont(label_font)
        pimple_layout.addWidget(self.edit_ncorrectors, 0, 1)

        # nOuterCorrectors
        label_nouter = QLabel("nOuterCorrectors:")
        label_nouter.setFont(label_font)
        pimple_layout.addWidget(label_nouter, 1, 0)

        self.edit_nouter = QLineEdit("1")
        self.edit_nouter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_nouter.setFont(label_font)
        pimple_layout.addWidget(self.edit_nouter, 1, 1)

        # nonOrthogonality
        label_nonortho = QLabel("nonOrthogonality:")
        label_nonortho.setFont(label_font)
        pimple_layout.addWidget(label_nonortho, 2, 0)

        self.edit_nonortho = QLineEdit("60")
        self.edit_nonortho.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_nonortho.setFont(label_font)
        pimple_layout.addWidget(self.edit_nonortho, 2, 1)

        # fluxScheme
        label_flux = QLabel("fluxScheme:")
        label_flux.setFont(label_font)
        pimple_layout.addWidget(label_flux, 3, 0)

        self.combo_flux = QComboBox()
        self.combo_flux.setFont(label_font)
        self.combo_flux.addItems(["Kurganov", "Tamdor"])
        pimple_layout.addWidget(self.combo_flux, 3, 1)

        pimple_layout.setColumnStretch(0, 1)
        pimple_layout.setColumnStretch(1, 1)

        layout.addWidget(pimple_group)

        # Spacer
        layout.addStretch()

    def load_data(self) -> None:
        """Load numerical settings from case_data."""
        pass

    def save_data(self) -> None:
        """Save numerical settings to case_data."""
        pass
