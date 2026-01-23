"""
Center Widget - Main Content Area with Navigation Tree and Panel Stack

This module provides the central widget containing navigation tree
and stacked panels for different settings.
Uses Qt Designer generated UI file (center_form_ui.py).
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

from common.app_context import AppContext
from view.main.center_form_ui import Ui_Center
from view.panel.geometry_view import GeometryView
from view.panel.mesh_generation_view import MeshGenerationView


class CenterWidget(QWidget):
    """
    Central widget with navigation tree and stacked panels.
    Uses Qt Designer generated UI.

    Layout:
    +------------------+---------------------------+
    |                  |                           |
    |  Navigation      |   Stacked Panel Area      |
    |  Tree            |   (Geometry, Mesh, etc.)  |
    |                  |                           |
    +------------------+---------------------------+
    """

    def __init__(self, parent=None, context: AppContext = None):
        """
        Initialize center widget.

        Args:
            parent: Parent widget (MainWindow)
            context: Application context for service access
        """
        super().__init__(parent)

        self.main_window = parent
        self.context = context

        # Setup UI from Qt Designer file
        self.ui = Ui_Center()
        self.ui.setupUi(self)

        # Get services from context
        self.exec_widget = context.get("exec") if context else None
        self.vtk_pre = context.get("vtk_pre") if context else None
        self.vtk_post = context.get("vtk_post") if context else None
        self.dock_manager = context.get("dock") if context else None

        # Panel views (will be initialized)
        self.panel_views = {}

        # Setup panels and signals
        self._setup_panels()
        self._connect_signals()

    def _setup_panels(self) -> None:
        """Setup panel view instances."""
        # Geometry View
        self.panel_views["geometry"] = GeometryView(self)

        # Mesh Generation View
        self.panel_views["mesh"] = MeshGenerationView(self)

        # TODO: Add other views
        # self.panel_views["initial_conditions"] = InitialConditionsView(self)
        # self.panel_views["models"] = ModelsView(self)
        # self.panel_views["numerical"] = NumericalConditionsView(self)
        # self.panel_views["materials"] = MaterialsView(self)
        # self.panel_views["spray_mmh"] = SprayMMHView(self)
        # self.panel_views["spray_nto"] = SprayNTOView(self)
        # self.panel_views["run"] = RunView(self)

    def _connect_signals(self) -> None:
        """Connect tree selection signals."""
        self.ui.treeWidget.itemSelectionChanged.connect(self._on_tree_selection_changed)

    def _on_tree_selection_changed(self) -> None:
        """Handle tree item selection change."""
        selected_items = self.ui.treeWidget.selectedItems()
        if not selected_items:
            return

        item = selected_items[0]

        # Get item text to determine which page to show
        item_text = item.text(0)
        parent = item.parent()
        parent_text = parent.text(0) if parent else None

        # Map tree items to stackedWidget pages
        # Top-level pages
        page_map = {
            "Geometry": self.ui.page_geometry,
            "Mesh Generation": self.ui.page_mesh_generation,
            "Run": self.ui.page_run,
        }

        # Setup submenu pages
        setup_pages = {
            "Models": self.ui.page_models,
            "Initial Conditions": self.ui.page_initial_conditions,
            "Spray - NMH": self.ui.page_mmh,
            "Spray - NTO": self.ui.page_nto,
        }

        # Solution submenu pages
        solution_pages = {
            "Numerical Conditions": self.ui.page_numerical_conditions,
            "Run Conditions": self.ui.page_run_conditions,
        }

        # Find the page to display
        page = None
        if parent_text:
            # Child item - check parent to determine which submenu
            if parent_text == "Setup":
                page = setup_pages.get(item_text)
            elif parent_text == "Solution":
                page = solution_pages.get(item_text)
            elif parent_text == "Results":
                # Results submenu - handle later (Residual, Post)
                # Switch dock tabs instead of pages
                if item_text == "Residual":
                    if self.dock_manager:
                        self.dock_manager.change_dock_tab(0)
                elif item_text == "Post":
                    if self.dock_manager:
                        self.dock_manager.change_dock_tab(3)
                return
        else:
            # Top-level item
            page = page_map.get(item_text)

        if page:
            self.ui.stackedWidget.setCurrentWidget(page)

    def get_panel(self, panel_id: str):
        """
        Get a panel view by ID.

        Args:
            panel_id: Panel identifier

        Returns:
            Panel view instance or None
        """
        return self.panel_views.get(panel_id)
