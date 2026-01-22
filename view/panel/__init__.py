"""
Panel Views - Settings Panels for Main Window

Each panel provides specific configuration UI for different aspects
of the simulation setup.
"""

from .geometry_panel import GeometryPanel
from .mesh_generation_panel import MeshGenerationPanel
from .initial_conditions_panel import InitialConditionsPanel
from .models_panel import ModelsPanel
from .numerical_conditions_panel import NumericalConditionsPanel
from .materials_panel import MaterialsPanel
from .spray_mmh_panel import SprayMMHPanel
from .spray_nto_panel import SprayNTOPanel
from .run_panel import RunPanel

__all__ = [
    "GeometryPanel",
    "MeshGenerationPanel",
    "InitialConditionsPanel",
    "ModelsPanel",
    "NumericalConditionsPanel",
    "MaterialsPanel",
    "SprayMMHPanel",
    "SprayNTOPanel",
    "RunPanel",
]
