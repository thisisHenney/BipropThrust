"""
Center Widget - Main Content Area with Navigation Tree and Panel Stack

This module provides the central widget containing navigation tree
and stacked panels for different settings.
Uses Qt Designer generated UI file (center_form_ui.py).
"""

from pathlib import Path

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

from common.app_context import AppContext
from common.case_data import case_data
from view.main.center_form_ui import Ui_Center
from view.panel.geometry_view import GeometryView
from view.panel.mesh_generation_view import MeshGenerationView
from view.panel.run_view import RunView
from view.panel.post_view import PostView


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
        self.residual_graph = context.get("residual_graph") if context else None
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

        # Run View
        self.panel_views["run"] = RunView(self)

        # Post View
        self.panel_views["post"] = PostView(self)

        # Slice controls are already added to VTK toolbar in mesh view
        # They will be shown/hidden based on active tab

        # TODO: Add other views
        # self.panel_views["initial_conditions"] = InitialConditionsView(self)
        # self.panel_views["models"] = ModelsView(self)
        # self.panel_views["numerical"] = NumericalConditionsView(self)
        # self.panel_views["materials"] = MaterialsView(self)
        # self.panel_views["spray_mmh"] = SprayMMHView(self)
        # self.panel_views["spray_nto"] = SprayNTOView(self)

    def _connect_signals(self) -> None:
        """Connect tree selection signals."""
        self.ui.treeWidget.itemSelectionChanged.connect(self._on_tree_selection_changed)

    def select_default_tab(self) -> None:
        """Select the default tab (Geometry) on startup."""
        # Select the first top-level item (Geometry)
        geometry_item = self.ui.treeWidget.topLevelItem(0)
        if geometry_item:
            self.ui.treeWidget.setCurrentItem(geometry_item)
            # This will trigger _on_tree_selection_changed which handles visibility

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
                # Results submenu - switch to corresponding dock tabs
                if item_text == "Residual":
                    if self.dock_manager:
                        self.dock_manager.change_dock_tab(4)
                    # Load residual log file
                    self._load_residual_log()
                elif item_text == "Post":
                    if self.dock_manager:
                        self.dock_manager.change_dock_tab(3)
                    # Load post-processing results
                    post_view = self.panel_views.get("post")
                    if post_view:
                        post_view.load_results()
                # Update visibility for Results tabs (show mesh, hide geometry)
                if self.vtk_pre:
                    self._show_mesh_objects_only()
                return
        else:
            # Top-level item
            page = page_map.get(item_text)

        if page:
            self.ui.stackedWidget.setCurrentWidget(page)

            # Toggle visibility based on active tab
            if self.vtk_pre:
                # Check if this is a top-level item or submenu item
                # For submenu items, always show mesh and hide geometry
                if parent_text:
                    # Submenu item (Setup, Solution) - show mesh, hide geometry
                    self._show_mesh_objects_only()
                    self._hide_slice_toolbar()
                elif item_text == "Geometry":
                    # Show geometry STL, hide mesh
                    self._show_geometry_objects()
                    # Hide slice toolbar
                    self._hide_slice_toolbar()
                elif item_text == "Mesh Generation":
                    # Hide geometry STL, show mesh
                    self._show_mesh_objects()
                    # Show slice toolbar
                    self._show_slice_toolbar()
                else:
                    # Other top-level tabs (Run, etc.) - show mesh, hide STL and slice controls
                    self._show_mesh_objects_only()
                    # Hide slice toolbar
                    self._hide_slice_toolbar()

    def _show_geometry_objects(self):
        """Show geometry group objects, hide mesh group objects."""
        all_objs = self.vtk_pre.obj_manager.get_all()

        geom_count = 0
        mesh_count = 0

        for obj in all_objs:
            # Check if object has group attribute
            if hasattr(obj, 'group'):
                if obj.group == "geometry":
                    obj.actor.SetVisibility(True)
                    geom_count += 1
                elif obj.group == "mesh":
                    obj.actor.SetVisibility(False)
                    mesh_count += 1

        # Hide slice/clip actors when switching to Geometry tab
        mesh_view = self.panel_views.get("mesh")
        if mesh_view:
            mesh_view._hide_slice_clip_actors()

        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    def _show_mesh_objects(self):
        """Show mesh group objects, hide geometry group objects."""
        all_objs = self.vtk_pre.obj_manager.get_all()

        geom_count = 0
        mesh_count = 0

        for obj in all_objs:
            # Check if object has group attribute
            if hasattr(obj, 'group'):
                if obj.group == "geometry":
                    obj.actor.SetVisibility(False)
                    geom_count += 1
                elif obj.group == "mesh":
                    obj.actor.SetVisibility(True)
                    mesh_count += 1

        # Show slice/clip actors when switching to Mesh Generation tab
        mesh_view = self.panel_views.get("mesh")
        if mesh_view:
            mesh_view._show_slice_clip_actors()

        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    def _show_mesh_objects_only(self):
        """Show mesh objects, hide geometry and slice/clip actors (for Run and other tabs)."""
        all_objs = self.vtk_pre.obj_manager.get_all()

        geom_count = 0
        mesh_count = 0

        for obj in all_objs:
            # Check if object has group attribute
            if hasattr(obj, 'group'):
                if obj.group == "geometry":
                    obj.actor.SetVisibility(False)
                    geom_count += 1
                elif obj.group == "mesh":
                    obj.actor.SetVisibility(True)
                    mesh_count += 1

        # Hide slice/clip actors (no slicing on Run and other tabs)
        mesh_view = self.panel_views.get("mesh")
        if mesh_view:
            mesh_view._hide_slice_clip_actors()

        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    def _show_slice_toolbar(self):
        """Show slice controls widget (Mesh Generation tab)."""
        mesh_view = self.panel_views.get("mesh")
        if mesh_view and hasattr(mesh_view, "slice_widget"):
            mesh_view.slice_widget.show()

    def _hide_slice_toolbar(self):
        """Hide slice controls widget (other tabs)."""
        mesh_view = self.panel_views.get("mesh")
        if mesh_view and hasattr(mesh_view, "slice_widget"):
            mesh_view.slice_widget.hide()

    def _load_residual_log(self):
        """Load residual log file from 5.CHTFCase folder."""
        if not self.residual_graph:
            return

        if not case_data.path:
            return

        # Look for log.solver in 5.CHTFCase folder
        chtf_case = Path(case_data.path) / "5.CHTFCase"
        log_file = chtf_case / "log.solver"

        if log_file.exists():
            self.residual_graph.load_file(str(log_file))

    def get_panel(self, panel_id: str):
        """
        Get a panel view by ID.

        Args:
            panel_id: Panel identifier

        Returns:
            Panel view instance or None
        """
        return self.panel_views.get(panel_id)
