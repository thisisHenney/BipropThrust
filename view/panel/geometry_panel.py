"""
Geometry Panel - STL geometry file management

Allows users to add, remove, and configure geometry files for the simulation.
"""

from pathlib import Path

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QTreeWidget, QTreeWidgetItem, QGroupBox,
    QGridLayout, QLineEdit, QSpacerItem, QSizePolicy,
    QApplication, QProgressDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from nextlib.dialogbox.dialogbox import FileDialogBox
from nextlib.widgets.tree import TreeWidget
from nextlib.vtk.core import MeshLoader

from common.app_data import app_data
from common.case_data import case_data


class GeometryPanel(QWidget):
    """
    Panel for managing geometry files (STL).

    Features:
    - Add/Remove STL files
    - Display geometry list in tree view
    - Configure geometry position
    - Preview in VTK widget
    """

    # Style constants
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

    TREE_STYLE = """
        QTreeWidget {
            show-decoration-selected: 1;
        }
        QTreeWidget::item {
            height: 24px;
        }
        QTreeWidget::item:hover {
            border: 1px solid #567dbc;
            border-radius: 6px;
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e7effd, stop:1 #cbdaf1);
        }
        QTreeWidget::item:selected:active {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6ea1f1, stop:1 #3d87bf);
            border-radius: 6px;
        }
        QTreeWidget::item:selected:!active {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6b9be8, stop:1 #577fbf);
            border-radius: 6px;
        }
    """

    def __init__(self, parent=None, context=None):
        """
        Initialize geometry panel.

        Args:
            parent: Parent widget
            context: Application context for service access
        """
        super().__init__(parent)

        self.context = context
        self.app_data = app_data
        self.case_data = case_data

        # Get VTK widget from context
        self.vtk_pre = context.get("vtk_pre") if context else None

        # Mesh loader for STL files
        self.mesh_loader = MeshLoader()

        # Track selected geometry for highlight effect
        self._selected_obj_name = None

        # Disable individual outlines in VTK (show only combined bbox)
        if self.vtk_pre:
            self.vtk_pre.obj_manager.show_individual_outlines = False

        # Setup UI
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Setup the UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        # Title
        title = QLabel("Geometry")
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

        # Button row
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btn_add = QPushButton("Add")
        self.btn_add.setMinimumHeight(30)
        btn_layout.addWidget(self.btn_add)

        self.btn_remove = QPushButton("Remove")
        self.btn_remove.setMinimumHeight(30)
        btn_layout.addWidget(self.btn_remove)

        layout.addLayout(btn_layout)

        # Geometry tree
        self.tree_geometry = QTreeWidget()
        self.tree_geometry.setHeaderHidden(True)
        self.tree_geometry.setAlternatingRowColors(True)
        tree_font = QFont()
        tree_font.setPointSize(10)
        self.tree_geometry.setFont(tree_font)
        self.tree_geometry.setStyleSheet(self.TREE_STYLE)
        layout.addWidget(self.tree_geometry)

        # TreeWidget wrapper for convenience
        self.tree = TreeWidget(self, self.tree_geometry)

        # Hide header again (TreeWidget wrapper enables it in _setup_style)
        self.tree_geometry.setHeaderHidden(True)

        # Disable editing in tree (name changes not allowed)
        self.tree_geometry.setEditTriggers(QTreeWidget.EditTrigger.NoEditTriggers)

        # Position GroupBox
        self.position_group = QGroupBox("Position")
        group_font = QFont()
        group_font.setPointSize(9)
        group_font.setBold(True)
        self.position_group.setFont(group_font)
        self.position_group.setStyleSheet(self.GROUPBOX_STYLE)
        self.position_group.setMaximumHeight(100)

        pos_layout = QGridLayout(self.position_group)

        label_font = QFont()
        label_font.setPointSize(9)

        # Position X, Y, Z
        pos_label = QLabel("Position (x, y, z):")
        pos_label.setFont(label_font)
        pos_layout.addWidget(pos_label, 0, 0)

        pos_edit_layout = QHBoxLayout()

        self.edit_pos_x = QLineEdit()
        self.edit_pos_x.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_pos_x.setFont(label_font)
        pos_edit_layout.addWidget(self.edit_pos_x)

        self.edit_pos_y = QLineEdit()
        self.edit_pos_y.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_pos_y.setFont(label_font)
        pos_edit_layout.addWidget(self.edit_pos_y)

        self.edit_pos_z = QLineEdit()
        self.edit_pos_z.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_pos_z.setFont(label_font)
        pos_edit_layout.addWidget(self.edit_pos_z)

        pos_layout.addLayout(pos_edit_layout, 0, 1)

        layout.addWidget(self.position_group)

        # Separator
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line2)

        # Apply button row
        apply_layout = QHBoxLayout()
        apply_layout.addStretch()

        self.btn_apply = QPushButton("Apply")
        self.btn_apply.setMinimumHeight(30)
        apply_layout.addWidget(self.btn_apply)

        layout.addLayout(apply_layout)

        # Spacer
        layout.addStretch()

    def _connect_signals(self) -> None:
        """Connect UI signals."""
        self.btn_add.clicked.connect(self._on_add_clicked)
        self.btn_remove.clicked.connect(self._on_remove_clicked)
        self.btn_apply.clicked.connect(self._on_apply_clicked)

        # Allow multiple selection in tree (sync with VTK selection)
        self.tree_geometry.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)

        # Use itemSelectionChanged for detecting selection changes including deselection
        self.tree_geometry.itemSelectionChanged.connect(self._on_tree_selection_changed)

        # Connect VTK selection changed signal
        if self.vtk_pre:
            self.vtk_pre.obj_manager.selection_changed.connect(self._on_vtk_selection_changed)

    def _on_add_clicked(self) -> None:
        """Handle Add button click - open file dialog for STL files."""
        add_files = FileDialogBox.open_files(
            self, "Select STL files",
            "STL Files (*.stl);;All Files (*)",
            self.case_data.path
        )

        if not add_files:
            return

        # Add files to case_data and tree first
        for f in add_files:
            file = Path(f)
            self.case_data.add_geometry(file)
            name = file.stem
            self.tree.insert([], name)

        # Load STL files asynchronously to prevent GUI lock
        if self.vtk_pre:
            self._pending_files = add_files
            self._start_async_loading(add_files)
        else:
            self.case_data.save()

    def _start_async_loading(self, files: list) -> None:
        """Start async loading of STL files."""
        # Show progress dialog
        self._progress_dialog = QProgressDialog(
            "Loading STL files...", "Cancel", 0, len(files), self
        )
        self._progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self._progress_dialog.setMinimumDuration(0)
        self._progress_dialog.canceled.connect(self._on_loading_canceled)
        self._progress_dialog.show()

        # Connect mesh_loader signals
        self._loading_signals_connected = True
        self.mesh_loader.file_loaded.connect(self._on_file_loaded)
        self.mesh_loader.progress.connect(self._on_loading_progress)
        self.mesh_loader.all_finished.connect(self._on_loading_finished)
        self.mesh_loader.error.connect(self._on_loading_error)

        # Start async loading
        self.mesh_loader.load_async(files)

    def _on_file_loaded(self, file_path: str, name: str, actor) -> None:
        """Handle single file loaded from async loading."""
        if self.vtk_pre and actor:
            self.vtk_pre.obj_manager.add(actor, name=name, group="geometry")

    def _on_loading_progress(self, current: int, total: int) -> None:
        """Handle loading progress update."""
        if hasattr(self, '_progress_dialog') and self._progress_dialog:
            self._progress_dialog.setValue(current)

    def _on_loading_error(self, file_path: str, error_msg: str) -> None:
        """Handle loading error."""
        print(f"Error loading {file_path}: {error_msg}")

    def _on_loading_canceled(self) -> None:
        """Handle loading canceled by user."""
        self.mesh_loader.cancel_async()
        self._cleanup_loading_signals()

    def _on_loading_finished(self) -> None:
        """Handle all files loaded."""
        # Close progress dialog
        if hasattr(self, '_progress_dialog') and self._progress_dialog:
            self._progress_dialog.close()
            self._progress_dialog = None

        # Disconnect signals
        self._cleanup_loading_signals()

        # Update VTK view after all files loaded
        if self.vtk_pre:
            self.vtk_pre.camera.fit()
            self.vtk_pre.vtk_widget.GetRenderWindow().Render()

        self.case_data.save()

    def _cleanup_loading_signals(self) -> None:
        """Disconnect mesh_loader signals safely."""
        if not getattr(self, '_loading_signals_connected', False):
            return

        self._loading_signals_connected = False
        self.mesh_loader.file_loaded.disconnect(self._on_file_loaded)
        self.mesh_loader.progress.disconnect(self._on_loading_progress)
        self.mesh_loader.all_finished.disconnect(self._on_loading_finished)
        self.mesh_loader.error.disconnect(self._on_loading_error)

    def _on_remove_clicked(self) -> None:
        """Handle Remove button click - remove selected geometry."""
        pos = self.tree.get_current_pos()
        if pos is None:
            return

        obj_name = self.tree.get_text(pos)
        self.tree.remove_item(pos)

        # Remove from VTK
        if self.vtk_pre:
            obj = self.vtk_pre.obj_manager.find_by_name(obj_name)
            if obj:
                self.vtk_pre.obj_manager.remove(obj.id)
            # Refresh view
            self.vtk_pre.vtk_widget.GetRenderWindow().Render()

        self.case_data.remove_geometry(obj_name)
        self.case_data.save()

    def _on_apply_clicked(self) -> None:
        """Handle Apply button click - apply position changes."""
        pos = self.tree.get_current_pos()
        if pos is None:
            return

        # Get position values
        try:
            x = float(self.edit_pos_x.text()) if self.edit_pos_x.text() else 0.0
            y = float(self.edit_pos_y.text()) if self.edit_pos_y.text() else 0.0
            z = float(self.edit_pos_z.text()) if self.edit_pos_z.text() else 0.0
        except ValueError:
            print("Invalid position values")
            return

        obj_name = self.tree.get_text(pos)

        # Save position to case data only (no VTK update)
        self.case_data.set_geometry_position(obj_name, x, y, z)
        self.case_data.save()

    def _on_tree_selection_changed(self) -> None:
        """Handle tree selection changed - sync VTK selection, update opacity and position fields."""
        # Get all selected items
        selected_items = self.tree_geometry.selectedItems()
        selected_count = len(selected_items)
        selected_names = [item.text(0) for item in selected_items]

        # Enable Position group only when exactly one item is selected
        self.position_group.setEnabled(selected_count == 1)

        # Sync VTK selection
        if self.vtk_pre:
            self._sync_vtk_selection(selected_names)

        if selected_count == 0:
            # No selection - restore all objects to full opacity
            self._restore_all_opacity()
            # Reset position fields to default (0,0,0)
            self.edit_pos_x.setText("0")
            self.edit_pos_y.setText("0")
            self.edit_pos_z.setText("0")
            return

        if selected_count == 1:
            # Single selection - highlight and show position
            obj_name = selected_names[0]
            self._highlight_object(obj_name)

            # Load position values for selected geometry (default: 0,0,0)
            position = self.case_data.get_geometry_position(obj_name)
            x, y, z = position if position else (0.0, 0.0, 0.0)
            self.edit_pos_x.setText(f"{x:.6g}")
            self.edit_pos_y.setText(f"{y:.6g}")
            self.edit_pos_z.setText(f"{z:.6g}")
        else:
            # Multiple selection - highlight all selected, clear position fields
            self._highlight_multiple_objects(selected_names)
            self.edit_pos_x.setText("")
            self.edit_pos_y.setText("")
            self.edit_pos_z.setText("")

    def _highlight_object(self, obj_name: str) -> None:
        """Highlight selected object by making others semi-transparent."""
        if not self.vtk_pre:
            return

        # Store selected object name
        self._selected_obj_name = obj_name

        # Get all objects and set opacity
        all_objs = self.vtk_pre.obj_manager.get_all()

        for obj in all_objs:
            if obj.name == obj_name:
                # Selected object - full opacity
                obj.actor.GetProperty().SetOpacity(1.0)
            else:
                # Other objects - semi-transparent
                obj.actor.GetProperty().SetOpacity(0.3)

        # Force render update
        self.vtk_pre.vtk_widget.GetRenderWindow().Modified()
        self.vtk_pre.vtk_widget.GetRenderWindow().Render()
        self.vtk_pre.vtk_widget.update()

    def _highlight_multiple_objects(self, obj_names: list) -> None:
        """Highlight multiple selected objects by making others semi-transparent."""
        if not self.vtk_pre:
            return

        # Clear single selected object name
        self._selected_obj_name = None

        # Get all objects and set opacity
        all_objs = self.vtk_pre.obj_manager.get_all()

        for obj in all_objs:
            if obj.name in obj_names:
                # Selected objects - full opacity
                obj.actor.GetProperty().SetOpacity(1.0)
            else:
                # Other objects - semi-transparent
                obj.actor.GetProperty().SetOpacity(0.3)

        # Force render update
        self.vtk_pre.vtk_widget.GetRenderWindow().Modified()
        self.vtk_pre.vtk_widget.GetRenderWindow().Render()
        self.vtk_pre.vtk_widget.update()

    def _restore_all_opacity(self) -> None:
        """Restore all objects to full opacity."""
        if not self.vtk_pre:
            return

        self._selected_obj_name = None

        # Restore all objects to full opacity
        all_objs = self.vtk_pre.obj_manager.get_all()
        for obj in all_objs:
            obj.actor.GetProperty().SetOpacity(1.0)

        # Force render update
        self.vtk_pre.vtk_widget.GetRenderWindow().Modified()
        self.vtk_pre.vtk_widget.GetRenderWindow().Render()
        self.vtk_pre.vtk_widget.update()

    def _sync_vtk_selection(self, selected_names: list) -> None:
        """Sync VTK object selection with tree selection."""
        if not self.vtk_pre:
            return

        # Block VTK obj_manager signals to prevent feedback loop
        obj_manager = self.vtk_pre.obj_manager
        obj_manager.blockSignals(True)

        # Find object IDs for selected names
        selected_ids = []

        for name in selected_names:
            obj = obj_manager.find_by_name(name)
            if obj:
                selected_ids.append(obj.id)

        # Update VTK selection
        if not selected_ids:
            obj_manager.clear_selection()
        else:
            obj_manager.select_multiple(selected_ids)

        # Unblock signals
        obj_manager.blockSignals(False)

        # Force render update
        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    def _on_vtk_selection_changed(self, info: dict) -> None:
        """Handle VTK selection changed - sync tree widget selection."""
        selected_objects = info.get("selected_objects", [])
        selected_names = [obj["name"] for obj in selected_objects]
        selected_count = len(selected_names)

        # Enable Position group only when exactly one item is selected
        self.position_group.setEnabled(selected_count == 1)

        # Block signals to prevent feedback loop
        self.tree_geometry.blockSignals(True)

        # Clear current selection
        self.tree_geometry.clearSelection()

        # Select matching items in tree
        for i in range(self.tree_geometry.topLevelItemCount()):
            item = self.tree_geometry.topLevelItem(i)
            if item and item.text(0) in selected_names:
                item.setSelected(True)

        self.tree_geometry.blockSignals(False)

        # Update opacity based on selection
        if selected_count == 0:
            self._restore_all_opacity()
            self.edit_pos_x.setText("0")
            self.edit_pos_y.setText("0")
            self.edit_pos_z.setText("0")
        elif selected_count == 1:
            self._selected_obj_name = selected_names[0]
            self._highlight_object(selected_names[0])
            # Update position fields for single selected object
            position = self.case_data.get_geometry_position(selected_names[0])
            x, y, z = position if position else (0.0, 0.0, 0.0)
            self.edit_pos_x.setText(f"{x:.6g}")
            self.edit_pos_y.setText(f"{y:.6g}")
            self.edit_pos_z.setText(f"{z:.6g}")
        else:
            self._selected_obj_name = None
            self._highlight_multiple_objects(selected_names)
            # Multiple selection - clear position fields
            self.edit_pos_x.setText("")
            self.edit_pos_y.setText("")
            self.edit_pos_z.setText("")

    def rename_geometry(self, old_name: str, new_name: str) -> bool:
        """
        Rename geometry across tree, VTK, and case_data.

        Args:
            old_name: Current geometry name
            new_name: New geometry name

        Returns:
            True if renamed successfully, False otherwise
        """
        # Check if new name already exists
        if self.case_data.get_geometry(new_name):
            print(f"Geometry '{new_name}' already exists")
            return False

        # Rename in case_data
        geom = self.case_data.get_geometry(old_name)
        if not geom:
            print(f"Geometry '{old_name}' not found")
            return False

        # Update case_data (remove old, add with new name)
        self.case_data.objects[new_name] = geom
        self.case_data.objects[new_name].name = new_name
        del self.case_data.objects[old_name]

        # Rename in VTK obj_manager
        if self.vtk_pre:
            obj = self.vtk_pre.obj_manager.find_by_name(old_name)
            if obj:
                obj.name = new_name

        # Update tree item text
        for i in range(self.tree_geometry.topLevelItemCount()):
            item = self.tree_geometry.topLevelItem(i)
            if item and item.text(0) == old_name:
                item.setText(0, new_name)
                break

        self.case_data.save()
        return True

    def load_data(self) -> None:
        """Load geometry data from case_data."""
        self.tree_geometry.clear()

        for geom in self.case_data.geometry.files:
            name = Path(geom).stem
            self.tree.insert([], name)
