"""
Models Panel - Physics model selection

Configures turbulence, phase change, and reaction models.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame,
    QGroupBox, QGridLayout, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from common.app_data import app_data
from common.case_data import case_data


class ModelsPanel(QWidget):
    """
    Panel for selecting physics models.

    Features:
    - RANS turbulence model selection
    - Film model on/off
    - Phase change model
    - Chemical reaction model
    - Species selection
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
        title = QLabel("Models")
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

        # ===== Properties Group =====
        props_group = QGroupBox("Properties")
        props_group.setFont(group_font)
        props_group.setStyleSheet(self.GROUPBOX_STYLE)

        props_layout = QGridLayout(props_group)

        # RANS
        label_rans = QLabel("RANS:")
        label_rans.setFont(label_font)
        props_layout.addWidget(label_rans, 0, 0)

        self.combo_rans = QComboBox()
        self.combo_rans.setFont(label_font)
        self.combo_rans.addItems(["kEpsilon", "kOmega", "kOmegaSST"])
        self.combo_rans.setCurrentIndex(2)
        props_layout.addWidget(self.combo_rans, 0, 1)

        # Film
        label_film = QLabel("Film:")
        label_film.setFont(label_font)
        props_layout.addWidget(label_film, 1, 0)

        self.combo_film = QComboBox()
        self.combo_film.setFont(label_font)
        self.combo_film.addItems(["On", "Off"])
        props_layout.addWidget(self.combo_film, 1, 1)

        # Phase Change Model
        label_phase = QLabel("Phase Change Model:")
        label_phase.setFont(label_font)
        props_layout.addWidget(label_phase, 2, 0)

        self.combo_phase = QComboBox()
        self.combo_phase.setFont(label_font)
        self.combo_phase.addItems(["On", "Off"])
        props_layout.addWidget(self.combo_phase, 2, 1)

        # Thermophysical Property
        label_thermo = QLabel("Thermophysical Property:")
        label_thermo.setFont(label_font)
        props_layout.addWidget(label_thermo, 3, 0)

        self.combo_thermo = QComboBox()
        self.combo_thermo.setFont(label_font)
        self.combo_thermo.addItems(["NASA polynomial"])
        props_layout.addWidget(self.combo_thermo, 3, 1)

        # Chemical Reaction
        label_chem = QLabel("Chemical Reaction:")
        label_chem.setFont(label_font)
        props_layout.addWidget(label_chem, 4, 0)

        self.combo_chemical = QComboBox()
        self.combo_chemical.setFont(label_font)
        self.combo_chemical.addItems(["On", "Off"])
        props_layout.addWidget(self.combo_chemical, 4, 1)

        # Reaction Model (indented)
        label_reaction = QLabel("  └ Reaction Model:")
        label_reaction.setFont(label_font)
        props_layout.addWidget(label_reaction, 5, 0)

        self.combo_reaction = QComboBox()
        self.combo_reaction.setFont(label_font)
        self.combo_reaction.addItems(["31Reaction", "31Reaction+global", "51Reaction"])
        props_layout.addWidget(self.combo_reaction, 5, 1)

        # Species
        label_species = QLabel("Species:")
        label_species.setFont(label_font)
        props_layout.addWidget(label_species, 6, 0)

        self.combo_species = QComboBox()
        self.combo_species.setFont(label_font)
        self.combo_species.addItems(["MMH+NTO"])
        props_layout.addWidget(self.combo_species, 6, 1)

        props_layout.setColumnStretch(0, 1)
        props_layout.setColumnStretch(1, 1)

        layout.addWidget(props_group)

        # Spacer
        layout.addStretch()

    def load_data(self) -> None:
        """Load model settings from case_data."""
        pass

    def save_data(self) -> None:
        """Save model settings to case_data."""
        pass
