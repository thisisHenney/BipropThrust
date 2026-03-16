"""
Panel Views - Settings Views for Main Window

Each view provides logic for different aspects of the simulation setup.
UI widgets are defined in center_form_ui.py (Qt Designer generated).
"""

from .geometry_view import GeometryView
from .mesh_generation_view import MeshGenerationView
from .run_view import RunView


__all__ = [
    "GeometryView",
    "MeshGenerationView",
    "RunView",
]
