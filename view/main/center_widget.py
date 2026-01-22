"""
Center Widget - Main Content Area with Navigation Tree and Panel Stack

This module provides the central widget containing navigation tree
and stacked panels for different settings.
"""

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QSplitter,
    QTreeWidget, QTreeWidgetItem, QStackedWidget, QLabel,
    QScrollArea, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from common.app_context import AppContext
from view.panel.geometry_panel import GeometryPanel
from view.panel.mesh_generation_panel import MeshGenerationPanel
from view.panel.initial_conditions_panel import InitialConditionsPanel
from view.panel.models_panel import ModelsPanel
from view.panel.numerical_conditions_panel import NumericalConditionsPanel
from view.panel.materials_panel import MaterialsPanel
from view.panel.spray_mmh_panel import SprayMMHPanel
from view.panel.spray_nto_panel import SprayNTOPanel
from view.panel.run_panel import RunPanel


class CenterWidget(QWidget):
    """
    Central widget with navigation tree and stacked panels.

    Layout:
    +------------------+---------------------------+
    |                  |                           |
    |  Navigation      |   Stacked Panel Area      |
    |  Tree            |   (Geometry, Mesh, etc.)  |
    |                  |                           |
    +------------------+---------------------------+
    """

    # Navigation tree structure
    TREE_STRUCTURE = [
        ("Geometry", []),
        ("Mesh Generation", []),
        ("Setup", [
            "Initial Conditions",
            "Models",
            "Numerical Conditions",
            "Materials",
        ]),
        ("Spray Properties", [
            "MMH",
            "NTO",
        ]),
        ("Run", []),
        ("Post-Processing", [
            "Residuals",
            "Visualization",
        ]),
    ]

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

        # Get services from context
        self.exec_widget = context.get("exec") if context else None
        self.vtk_pre = context.get("vtk_pre") if context else None
        self.vtk_post = context.get("vtk_post") if context else None
        self.dock_manager = context.get("dock") if context else None

        # Panel views (will be initialized later)
        self.panel_views = {}

        # Setup UI
        self._setup_ui()
        self._setup_tree()
        self._setup_panels()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Setup the UI layout."""
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Splitter for tree and content
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(self.splitter)

        # Left side: Navigation tree
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabel("Navigation")
        self.tree_widget.setMinimumWidth(150)
        self.tree_widget.setMaximumWidth(250)

        # Tree style
        font = QFont()
        font.setPointSize(10)
        self.tree_widget.setFont(font)
        self.tree_widget.setStyleSheet("""
            QTreeWidget {
                show-decoration-selected: 1;
                border: none;
            }
            QTreeWidget::item {
                height: 26px;
            }
            QTreeWidget::item:hover {
                background-color: #e7effd;
                border-radius: 4px;
            }
            QTreeWidget::item:selected {
                background-color: #cce4ff;
                border-radius: 4px;
            }
        """)

        self.splitter.addWidget(self.tree_widget)

        # Right side: Stacked widget for panels
        self.stacked_widget = QStackedWidget()
        self.splitter.addWidget(self.stacked_widget)

        # Set splitter sizes (tree: 180, content: remaining)
        self.splitter.setSizes([180, 600])

    def _setup_tree(self) -> None:
        """Setup navigation tree items."""
        self.tree_items = {}

        for idx, (name, children) in enumerate(self.TREE_STRUCTURE):
            # Create parent item
            parent_item = QTreeWidgetItem([name])
            font = QFont()
            font.setPointSize(10)
            font.setBold(True if not children else False)
            parent_item.setFont(0, font)

            self.tree_widget.addTopLevelItem(parent_item)
            self.tree_items[(idx,)] = parent_item

            # Create child items
            for child_idx, child_name in enumerate(children):
                child_item = QTreeWidgetItem([child_name])
                child_font = QFont()
                child_font.setPointSize(10)
                child_item.setFont(0, child_font)
                parent_item.addChild(child_item)
                self.tree_items[(idx, child_idx)] = child_item

        # Expand all items
        self.tree_widget.expandAll()

    def _setup_panels(self) -> None:
        """Setup panel pages in stacked widget."""
        # Panel index mapping
        self.panel_indices = {}
        panel_idx = 0

        # Helper to add panel
        def add_panel(panel_id: str, panel: QWidget):
            nonlocal panel_idx
            self.stacked_widget.addWidget(panel)
            self.panel_indices[panel_id] = panel_idx
            self.panel_views[panel_id] = panel
            panel_idx += 1

        # Geometry Panel
        add_panel("geometry", GeometryPanel(self, self.context))

        # Mesh Generation Panel
        add_panel("mesh", MeshGenerationPanel(self, self.context))

        # Setup section panels
        add_panel("initial_conditions", InitialConditionsPanel(self, self.context))
        add_panel("models", ModelsPanel(self, self.context))
        add_panel("numerical", NumericalConditionsPanel(self, self.context))
        add_panel("materials", MaterialsPanel(self, self.context))

        # Spray Properties panels
        add_panel("spray_mmh", SprayMMHPanel(self, self.context))
        add_panel("spray_nto", SprayNTOPanel(self, self.context))

        # Run Panel
        add_panel("run", RunPanel(self, self.context))

        # Post-processing placeholders (switch dock tabs instead)
        post_configs = [
            ("post_residuals", "Residuals", "View convergence history"),
            ("post_viz", "Visualization", "Post-processing visualization"),
        ]

        for panel_id, title, description in post_configs:
            panel = self._create_placeholder_panel(title, description)
            self.stacked_widget.addWidget(panel)
            self.panel_indices[panel_id] = panel_idx
            panel_idx += 1

    def _create_placeholder_panel(self, title: str, description: str) -> QWidget:
        """
        Create a placeholder panel widget.

        Args:
            title: Panel title
            description: Panel description

        Returns:
            Placeholder panel widget
        """
        # Scroll area for panel content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        # Content widget
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16pt; font-weight: bold; color: #333;")
        layout.addWidget(title_label)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #ddd;")
        layout.addWidget(separator)

        # Description
        desc_label = QLabel(description)
        desc_label.setStyleSheet("font-size: 11pt; color: #666; margin-top: 10px;")
        layout.addWidget(desc_label)

        # Placeholder content
        placeholder = QLabel("\n\n(Panel content will be implemented here)")
        placeholder.setStyleSheet("color: #999; font-style: italic;")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(placeholder)

        # Spacer
        layout.addStretch()

        scroll.setWidget(content)
        return scroll

    def _connect_signals(self) -> None:
        """Connect tree selection signals."""
        self.tree_widget.itemSelectionChanged.connect(self._on_tree_selection_changed)

    def _on_tree_selection_changed(self) -> None:
        """Handle tree item selection change."""
        selected_items = self.tree_widget.selectedItems()
        if not selected_items:
            return

        item = selected_items[0]
        pos = self._get_item_position(item)

        if pos is None:
            return

        # Map tree position to panel index
        self._navigate_to_panel(pos)

    def _get_item_position(self, item: QTreeWidgetItem) -> tuple:
        """
        Get the position tuple for a tree item.

        Args:
            item: Tree widget item

        Returns:
            Position tuple (parent_idx,) or (parent_idx, child_idx)
        """
        parent = item.parent()
        if parent is None:
            # Top-level item
            idx = self.tree_widget.indexOfTopLevelItem(item)
            return (idx,)
        else:
            # Child item
            parent_idx = self.tree_widget.indexOfTopLevelItem(parent)
            child_idx = parent.indexOfChild(item)
            return (parent_idx, child_idx)

    def _navigate_to_panel(self, pos: tuple) -> None:
        """
        Navigate to the appropriate panel based on tree position.

        Args:
            pos: Tree position tuple
        """
        # Map positions to panel indices
        # (0,) -> Geometry
        # (1,) -> Mesh Generation
        # (2, 0) -> Initial Conditions
        # (2, 1) -> Models
        # (2, 2) -> Numerical Conditions
        # (2, 3) -> Materials
        # (3, 0) -> Spray MMH
        # (3, 1) -> Spray NTO
        # (4,) -> Run
        # (5, 0) -> Post Residuals (switch to Residuals dock tab)
        # (5, 1) -> Post Visualization (switch to Post dock tab)

        panel_map = {
            (0,): "geometry",
            (1,): "mesh",
            (2, 0): "initial_conditions",
            (2, 1): "models",
            (2, 2): "numerical",
            (2, 3): "materials",
            (3, 0): "spray_mmh",
            (3, 1): "spray_nto",
            (4,): "run",
            (5, 0): "post_residuals",
            (5, 1): "post_viz",
        }

        panel_id = panel_map.get(pos)
        if panel_id is None:
            return

        # Handle special cases for post-processing (switch dock tabs)
        if pos == (5, 0):  # Residuals
            if self.dock_manager:
                self.dock_manager.change_dock_tab(0)
            return
        elif pos == (5, 1):  # Visualization
            if self.dock_manager:
                self.dock_manager.change_dock_tab(3)
            return

        # Switch to appropriate panel
        if panel_id in self.panel_indices:
            idx = self.panel_indices[panel_id]
            self.stacked_widget.setCurrentIndex(idx)

    def set_panel(self, panel_id: str, widget: QWidget) -> None:
        """
        Replace a placeholder panel with an actual panel widget.

        Args:
            panel_id: Panel identifier
            widget: Panel widget to set
        """
        if panel_id not in self.panel_indices:
            print(f"Warning: Unknown panel ID: {panel_id}")
            return

        idx = self.panel_indices[panel_id]

        # Remove old widget
        old_widget = self.stacked_widget.widget(idx)
        if old_widget:
            self.stacked_widget.removeWidget(old_widget)
            old_widget.deleteLater()

        # Insert new widget
        self.stacked_widget.insertWidget(idx, widget)
        self.panel_views[panel_id] = widget

    def get_panel(self, panel_id: str) -> QWidget:
        """
        Get a panel widget by ID.

        Args:
            panel_id: Panel identifier

        Returns:
            Panel widget or None
        """
        return self.panel_views.get(panel_id)

    def select_tree_item(self, pos: tuple) -> None:
        """
        Programmatically select a tree item.

        Args:
            pos: Position tuple
        """
        item = self.tree_items.get(pos)
        if item:
            self.tree_widget.setCurrentItem(item)
