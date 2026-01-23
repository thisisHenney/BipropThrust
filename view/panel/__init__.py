"""
Panel Views - Settings Views for Main Window

Each view provides logic for different aspects of the simulation setup.
UI widgets are defined in center_form_ui.py (Qt Designer generated).
"""

from .geometry_view import GeometryView
from .mesh_generation_view import MeshGenerationView

# TODO: Add other view imports when implemented
# from .initial_conditions_view import InitialConditionsView
# from .models_view import ModelsView
# from .numerical_conditions_view import NumericalConditionsView
# from .materials_view import MaterialsView
# from .spray_mmh_view import SprayMMHView
# from .spray_nto_view import SprayNTOView
# from .run_view import RunView

__all__ = [
    "GeometryView",
    "MeshGenerationView",
    # "InitialConditionsView",
    # "ModelsView",
    # "NumericalConditionsView",
    # "MaterialsView",
    # "SprayMMHView",
    # "SprayNTOView",
    # "RunView",
]
