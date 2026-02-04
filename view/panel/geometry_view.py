"""
Geometry View - Handles geometry management logic

This view connects to UI widgets defined in center_form_ui.py
and implements geometry file management functionality.
"""

from pathlib import Path
from PySide6.QtWidgets import (
    QProgressDialog, QApplication, QHBoxLayout, QLabel, QComboBox, QSlider, QWidget, QCheckBox, QPushButton
)
from PySide6.QtCore import Qt

from nextlib.dialogbox.dialogbox import FileDialogBox
from nextlib.widgets.tree import TreeWidget
from nextlib.vtk.core import MeshLoader

from common.app_data import app_data
from common.case_data import case_data


class GeometryView:
    """
    Geometry management view.

    Manages STL file loading, VTK visualization, and geometry tree.
    """

    def __init__(self, parent):
        """
        Initialize geometry view.

        Args:
            parent: CenterWidget instance (contains ui and context)
        """
        self.parent = parent
        self.ui = self.parent.ui
        self.ctx = self.parent.context

        # Get services from context
        self.exec_widget = self.ctx.get("exec")
        self.vtk_pre = self.ctx.get("vtk_pre")

        # Get data instances
        self.app_data = app_data
        self.case_data = case_data

        # Wrap tree widget with TreeWidget helper
        self.tree = TreeWidget(self.parent, self.ui.tree_geometry)

        # Initialize mesh loader for async loading
        self.mesh_loader = MeshLoader()
        self._loading_signals_connected = False
        self._progress_dialog = None

        # Disable individual outlines in VTK (show only combined bbox)
        if self.vtk_pre:
            self.vtk_pre.obj_manager.show_individual_outlines = False

        # Create slice controls widget (will be shown/hidden by center_widget)
        self.slice_widget = self._create_slice_widget()

        # Connect signals
        self._init_connect()

    def _create_slice_widget(self):
        """
        Create clip controls as a separate widget to be added below VTK viewer.

        Returns:
            QWidget containing clip controls
        """
        if not self.vtk_pre:
            return None

        # Create container widget
        slice_widget = QWidget()
        layout = QHBoxLayout(slice_widget)
        layout.setContentsMargins(6, 3, 6, 3)
        layout.setSpacing(6)

        # Clip mode selection
        lbl_clip = QLabel("Clip:")
        layout.addWidget(lbl_clip)

        self._clip_combo = QComboBox()
        self._clip_combo.addItems(["Off", "X", "Y", "Z"])
        self._clip_combo.setCurrentText("Off")
        self._clip_combo.setFixedWidth(60)
        layout.addWidget(self._clip_combo)

        # Position slider
        lbl_pos = QLabel("Pos:")
        layout.addWidget(lbl_pos)

        self._clip_slider = QSlider(Qt.Horizontal)
        self._clip_slider.setMinimum(0)
        self._clip_slider.setMaximum(100)
        self._clip_slider.setValue(50)
        self._clip_slider.setMinimumWidth(200)
        self._clip_slider.setEnabled(False)
        layout.addWidget(self._clip_slider)

        self._lbl_pos_value = QLabel("50%")
        self._lbl_pos_value.setMinimumWidth(40)
        layout.addWidget(self._lbl_pos_value)

        # Preview checkbox (shows outline instead of real-time clip)
        self._clip_preview_check = QCheckBox("Preview")
        self._clip_preview_check.setChecked(True)  # Default to preview mode
        self._clip_preview_check.setEnabled(False)
        layout.addWidget(self._clip_preview_check)

        # Apply button (applies the clip when in preview mode)
        self._clip_apply_btn = QPushButton("Apply")
        self._clip_apply_btn.setFixedWidth(60)
        self._clip_apply_btn.setEnabled(False)
        layout.addWidget(self._clip_apply_btn)

        # Reset button (restores original state)
        self._clip_reset_btn = QPushButton("Reset")
        self._clip_reset_btn.setFixedWidth(60)
        self._clip_reset_btn.setEnabled(False)
        layout.addWidget(self._clip_reset_btn)

        # Add spacer to push controls to the left
        layout.addStretch()

        # Hide widget initially
        slice_widget.hide()

        # Add to VTK widget layout (below vtk_widget)
        vtk_layout = self.vtk_pre.layout()
        vtk_layout.addWidget(slice_widget)

        return slice_widget

    def _init_connect(self):
        """Initialize signal connections."""
        # Clip controls
        self._clip_combo.currentTextChanged.connect(self._on_clip_mode_changed)
        self._clip_slider.valueChanged.connect(self._on_clip_slider_changed)
        self._clip_preview_check.toggled.connect(self._on_clip_preview_toggled)
        self._clip_apply_btn.clicked.connect(self._on_clip_apply_clicked)
        self._clip_reset_btn.clicked.connect(self._on_clip_reset_clicked)

        # Button clicks
        self.ui.button_geometry_add.clicked.connect(self._on_add_clicked)
        self.ui.button_geometry_remove.clicked.connect(self._on_remove_clicked)
        self.ui.button_geometry_reset.clicked.connect(self._on_reset_clicked)
        self.ui.button_geometry_apply.clicked.connect(self._on_set_apply_clicked)
        self.ui.button_geometry_cancel.clicked.connect(self._on_cancel_clicked)

        # Change button text to "Position Picking Mode" and keep enabled
        self.ui.button_geometry_apply.setText("Position Picking Mode")
        self.ui.button_geometry_apply.setEnabled(True)

        # Hide Cancel and Reset buttons by default
        self.ui.button_geometry_cancel.hide()
        self.ui.button_geometry_reset.hide()

        # Tree selection
        self.tree.widget.header().setVisible(False)
        self.tree.widget.itemSelectionChanged.connect(self._on_tree_selection_changed)

        # VTK selection
        if self.vtk_pre:
            self.vtk_pre.obj_manager.selection_changed.connect(self._on_vtk_selection_changed)

            # Point probe visibility changed signal
            probe_tool = self.vtk_pre._optional_tools.get("point_probe")
            if probe_tool:
                probe_tool.visibility_changed.connect(self._on_probe_visibility_changed)

    def _on_add_clicked(self):
        """Handle Add button click - open file dialog and copy STL files to model directory."""
        add_files = FileDialogBox.open_files(
            self.parent, "Select STL files",
            "STL Files (*.stl);;All Files (*)",
            self.case_data.path
        )

        if not add_files:
            return

        # Get model directory
        model_path = Path(self.case_data.path) / "1.model_Mhead" / "scale0"
        model_path.mkdir(parents=True, exist_ok=True)

        # Copy files to model directory and add to tree
        copied_files = []
        for f in add_files:
            src_file = Path(f)
            dst_file = model_path / src_file.name

            # Copy file to model directory
            import shutil
            try:
                shutil.copy2(src_file, dst_file)
            except Exception:
                continue

            # Add to case_data and tree
            self.case_data.add_geometry(dst_file)
            name = dst_file.stem
            self.tree.insert([], name)
            copied_files.append(str(dst_file))

        # Load STL files asynchronously to prevent GUI lock
        if self.vtk_pre and copied_files:
            self._start_async_loading(copied_files)
        else:
            self.case_data.save()

    def _start_async_loading(self, files: list):
        """Start async loading of STL files."""
        # Show progress dialog
        self._progress_dialog = QProgressDialog(
            "Loading STL files...", "Cancel", 0, len(files), self.parent
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

    def _on_file_loaded(self, file_path: str, name: str, actor):
        """Handle single file loaded from async loading."""
        if self.vtk_pre and actor:
            self.vtk_pre.obj_manager.add(actor, name=name, group="geometry")

            # Set default probe_position to object center
            bounds = actor.GetBounds()
            center_x = (bounds[0] + bounds[1]) / 2
            center_y = (bounds[2] + bounds[3]) / 2
            center_z = (bounds[4] + bounds[5]) / 2

            self.case_data.set_geometry_probe_position(name, center_x, center_y, center_z)

    def _on_loading_progress(self, current: int, total: int):
        """Handle loading progress update."""
        if hasattr(self, '_progress_dialog') and self._progress_dialog:
            self._progress_dialog.setValue(current)

    def _on_loading_error(self, file_path: str, error_msg: str):
        """Handle loading error."""

    def _on_loading_canceled(self):
        """Handle loading canceled by user."""
        self.mesh_loader.cancel_async()
        self._cleanup_loading_signals()

    def _on_loading_finished(self):
        """Handle all files loaded."""
        # Close progress dialog
        if hasattr(self, '_progress_dialog') and self._progress_dialog:
            self._progress_dialog.close()
            self._progress_dialog = None

        # Disconnect signals
        self._cleanup_loading_signals()

        # Apply saved transforms to all loaded objects
        if self.vtk_pre:
            self._apply_saved_transforms()

            # Set geometry visibility based on current tab
            # Check if we're on Geometry tab
            current_page = self.parent.ui.stackedWidget.currentWidget()
            is_geometry_tab = (current_page == self.parent.ui.page_geometry)

            # Set visibility for geometry objects
            all_objs = self.vtk_pre.obj_manager.get_all()
            for obj in all_objs:
                if hasattr(obj, 'group') and obj.group == "geometry":
                    obj.actor.SetVisibility(is_geometry_tab)

            # Also update clip actor visibility for geometry group
            if is_geometry_tab:
                self.vtk_pre.show_clip_actors_for_group("geometry")
            else:
                self.vtk_pre.hide_clip_actors_for_group("geometry")

            # Update VTK view after all files loaded
            # Only fit camera if we're on Geometry tab
            if is_geometry_tab:
                self.vtk_pre.camera.fit()
            self.vtk_pre.vtk_widget.GetRenderWindow().Render()

        self.case_data.save()

    def _apply_saved_transforms(self):
        """Apply saved position and rotation to all VTK objects."""
        if not self.vtk_pre:
            return

        import vtk
        all_objs = self.vtk_pre.obj_manager.get_all()

        for obj in all_objs:
            # Get saved position and rotation from case_data
            position = self.case_data.get_geometry_position(obj.name)
            rotation = self.case_data.get_geometry_rotation(obj.name)

            if position or rotation:
                # Default values if not found
                x, y, z = position if position else (0.0, 0.0, 0.0)
                rx, ry, rz = rotation if rotation else (0.0, 0.0, 0.0)

                # Apply transform to actor
                transform = vtk.vtkTransform()
                transform.PostMultiply()
                transform.RotateX(rx)
                transform.RotateY(ry)
                transform.RotateZ(rz)
                transform.Translate(x, y, z)

                obj.actor.SetUserTransform(transform)

    def _cleanup_loading_signals(self):
        """Disconnect mesh_loader signals safely."""
        if not getattr(self, '_loading_signals_connected', False):
            return

        self._loading_signals_connected = False
        self.mesh_loader.file_loaded.disconnect(self._on_file_loaded)
        self.mesh_loader.progress.disconnect(self._on_loading_progress)
        self.mesh_loader.all_finished.disconnect(self._on_loading_finished)
        self.mesh_loader.error.disconnect(self._on_loading_error)

    def _on_remove_clicked(self):
        """Handle Remove button click - remove selected geometry from tree, VTK, and model directory."""
        pos = self.tree.get_current_pos()
        if pos is None:
            return

        obj_name = self.tree.get_text(pos)

        # Prevent removing "fluid" (fixed item)
        if obj_name == "fluid":
            return

        self.tree.remove_item(pos)

        # Remove from VTK
        if self.vtk_pre:
            obj = self.vtk_pre.obj_manager.find_by_name(obj_name)
            if obj:
                self.vtk_pre.obj_manager.remove(obj.id)
            # Refresh view
            self.vtk_pre.vtk_widget.GetRenderWindow().Render()

        # Remove STL file from model directory
        model_path = Path(self.case_data.path) / "1.model_Mhead" / "scale0"
        stl_file = model_path / f"{obj_name}.stl"

        if stl_file.exists():
            try:
                stl_file.unlink()
            except Exception:
                pass

        self.case_data.remove_geometry(obj_name)
        self.case_data.save()

    def _on_set_apply_clicked(self):
        """Handle Set/Apply button click - toggle probe and save position."""
        current_text = self.ui.button_geometry_apply.text()

        if current_text == "Position Picking Mode":
            # Activate point_probe and change button to "Apply"
            if self.vtk_pre:
                probe_tool = self.vtk_pre._optional_tools.get("point_probe")
                if probe_tool:
                    # Get current selection
                    pos = self.tree.get_current_pos()
                    if pos is not None:
                        obj_name = self.tree.get_text(pos)

                        # Get selected object bounds
                        obj = self.vtk_pre.obj_manager.find_by_name(obj_name)
                        if obj:
                            bounds = obj.actor.GetBounds()
                            obj_size = (
                                bounds[1] - bounds[0],
                                bounds[3] - bounds[2],
                                bounds[5] - bounds[4]
                            )

                            # Calculate probe box size as 140% of object bounds
                            scale = 1.4
                            probe_box_size = tuple(s * scale for s in obj_size)

                        # Get saved probe position, or use object center if none
                        probe_pos = self.case_data.get_geometry_probe_position(obj_name)
                        if not probe_pos or probe_pos == (0.0, 0.0, 0.0):
                            # No saved position - use object center
                            probe_pos = (
                                (bounds[0] + bounds[1]) / 2,
                                (bounds[2] + bounds[3]) / 2,
                                (bounds[4] + bounds[5]) / 2
                            )
                        # else: Use saved probe position

                        # Ensure probe is hidden first
                        if probe_tool.is_visible:
                            probe_tool.hide()

                        # Calculate new bounds centered at probe_pos with 140% size
                        half_size_x = probe_box_size[0] / 2
                        half_size_y = probe_box_size[1] / 2
                        half_size_z = probe_box_size[2] / 2

                        new_bounds = [
                            probe_pos[0] - half_size_x,
                            probe_pos[0] + half_size_x,
                            probe_pos[1] - half_size_y,
                            probe_pos[1] + half_size_y,
                            probe_pos[2] - half_size_z,
                            probe_pos[2] + half_size_z
                        ]


                        # Set position while widget is Off
                        if hasattr(probe_tool, '_rep'):
                            probe_tool._rep.PlaceWidget(new_bounds)

                        # CRITICAL: Set saved state to match what we just set
                        # This makes show() restore exactly our desired position/size
                        from vtkmodules.vtkCommonTransforms import vtkTransform
                        probe_tool._saved_bounds = new_bounds
                        probe_tool._saved_transform = vtkTransform()  # Identity (no rotation)
                        probe_tool._saved_selection_ids = self.vtk_pre.obj_manager.selected_ids.copy()

                        # Now show() will restore our saved state with correct position
                        probe_tool.show()

                        # Verify final size
                        if hasattr(probe_tool, '_rep'):
                            verify_bounds = probe_tool._rep.GetBounds()
                            verify_size = (
                                verify_bounds[1] - verify_bounds[0],
                                verify_bounds[3] - verify_bounds[2],
                                verify_bounds[5] - verify_bounds[4]
                            )

                        # Force render to show changes
                        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

            # Update button state (must be OUTSIDE all if blocks to always show buttons)
            self.ui.button_geometry_apply.setText("Apply")
            self.ui.button_geometry_cancel.show()
            self.ui.button_geometry_reset.show()

        elif current_text == "Apply":
            # Save probe position and change button back to "Position Picking Mode"
            if self.vtk_pre:
                probe_tool = self.vtk_pre._optional_tools.get("point_probe")
                if probe_tool:
                    probe_center = probe_tool.get_center()
                    if probe_center:
                        pos = self.tree.get_current_pos()
                        if pos is not None:
                            obj_name = self.tree.get_text(pos)
                            self.case_data.set_geometry_probe_position(obj_name, *probe_center)
                        self.case_data.save()

                    # Deactivate probe and change button to "Position Picking Mode"
                    probe_tool.hide()
                    self.ui.button_geometry_apply.setText("Position Picking Mode")
                    self.ui.button_geometry_cancel.hide()
                    self.ui.button_geometry_reset.hide()

    def _on_cancel_clicked(self):
        """Handle Cancel button click - cancel position picking without saving."""
        if self.vtk_pre:
            probe_tool = self.vtk_pre._optional_tools.get("point_probe")
            if probe_tool:
                # Restore line editors to saved position (or object center if never saved)
                pos = self.tree.get_current_pos()
                if pos is not None:
                    obj_name = self.tree.get_text(pos)
                    probe_pos = self.case_data.get_geometry_probe_position(obj_name)

                    # If saved position exists and is not (0,0,0), use it
                    # Otherwise use object center
                    if probe_pos and probe_pos != (0.0, 0.0, 0.0):
                        x, y, z = probe_pos
                    else:
                        # No saved position - use object center
                        obj = self.vtk_pre.obj_manager.find_by_name(obj_name)
                        if obj:
                            bounds = obj.actor.GetBounds()
                            x = (bounds[0] + bounds[1]) / 2
                            y = (bounds[2] + bounds[3]) / 2
                            z = (bounds[4] + bounds[5]) / 2

                    # Update line editors
                    self.ui.edit_input_position_x.setText(f"{x:.4f}")
                    self.ui.edit_input_position_y.setText(f"{y:.4f}")
                    self.ui.edit_input_position_z.setText(f"{z:.4f}")

                # Deactivate probe
                probe_tool.hide()
                self.ui.button_geometry_apply.setText("Position Picking Mode")
                self.ui.button_geometry_cancel.hide()
                self.ui.button_geometry_reset.hide()

    def _on_reset_clicked(self):
        """Handle Reset button click - reset position to object center."""
        # Get selected object
        pos = self.tree.get_current_pos()
        if pos is None:
            return

        obj_name = self.tree.get_text(pos)

        # Get object center from VTK
        if self.vtk_pre:
            obj = self.vtk_pre.obj_manager.find_by_name(obj_name)
            if obj:
                bounds = obj.actor.GetBounds()
                center_x = (bounds[0] + bounds[1]) / 2
                center_y = (bounds[2] + bounds[3]) / 2
                center_z = (bounds[4] + bounds[5]) / 2

                # Update line editors with center coordinates (4 decimal places)
                self.ui.edit_input_position_x.setText(f"{center_x:.4f}")
                self.ui.edit_input_position_y.setText(f"{center_y:.4f}")
                self.ui.edit_input_position_z.setText(f"{center_z:.4f}")

                # If probe tool is active, reset to object center with correct size
                probe_tool = self.vtk_pre._optional_tools.get("point_probe")
                if probe_tool and probe_tool.is_visible:
                    # Calculate probe box size as 140% of object bounds (same as initial setup)
                    obj_size = (
                        bounds[1] - bounds[0],
                        bounds[3] - bounds[2],
                        bounds[5] - bounds[4]
                    )
                    scale = 1.4
                    half_size_x = (obj_size[0] * scale) / 2
                    half_size_y = (obj_size[1] * scale) / 2
                    half_size_z = (obj_size[2] * scale) / 2

                    # Calculate new bounds centered at object center
                    new_bounds = [
                        center_x - half_size_x,
                        center_x + half_size_x,
                        center_y - half_size_y,
                        center_y + half_size_y,
                        center_z - half_size_z,
                        center_z + half_size_z
                    ]

                    # Set bounds directly to preserve size
                    if hasattr(probe_tool, '_rep'):
                        probe_tool._rep.PlaceWidget(new_bounds)
                        probe_tool._saved_bounds = new_bounds
                        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    def _on_tree_selection_changed(self):
        """Handle tree selection changed - sync VTK and update position fields."""
        selected_items = self.tree.widget.selectedItems()
        selected_names = [item.text(0) for item in selected_items]
        selected_count = len(selected_names)

        # Sync VTK selection
        self._sync_vtk_selection(selected_names)

        # Disable Remove button if "fluid" is selected (fluid is fixed)
        if "fluid" in selected_names:
            self.ui.button_geometry_remove.setEnabled(False)
        else:
            self.ui.button_geometry_remove.setEnabled(True)

        # Update opacity based on selection
        if selected_count == 0:
            self._restore_all_opacity()
            self.ui.edit_input_position_x.setText("0")
            self.ui.edit_input_position_y.setText("0")
            self.ui.edit_input_position_z.setText("0")
            # Enable Input Position group and Set button
            self.ui.AdvancedGroupBox.setEnabled(True)
            self.ui.button_geometry_apply.setEnabled(True)
        elif selected_count == 1:
            # Enable Input Position group and Set button for single selection
            self.ui.AdvancedGroupBox.setEnabled(True)
            self.ui.button_geometry_apply.setEnabled(True)
            self._highlight_object(selected_names[0])

            # Print selected object size
            if self.vtk_pre:
                obj = self.vtk_pre.obj_manager.find_by_name(selected_names[0])
                if obj:
                    bounds = obj.actor.GetBounds()
                    obj_size = (
                        bounds[1] - bounds[0],
                        bounds[3] - bounds[2],
                        bounds[5] - bounds[4]
                    )

            # Check if point_probe is visible
            probe_tool = None
            if self.vtk_pre:
                probe_tool = self.vtk_pre._optional_tools.get("point_probe")

            # Try to load saved probe position first
            probe_pos = self.case_data.get_geometry_probe_position(selected_names[0])

            if probe_pos is not None:
                # Display saved probe position in line editors
                x, y, z = probe_pos
                self.ui.edit_input_position_x.setText(f"{x:.4f}")
                self.ui.edit_input_position_y.setText(f"{y:.4f}")
                self.ui.edit_input_position_z.setText(f"{z:.4f}")

                # Only update probe position if visible AND not in Position Picking Mode
                # (to avoid size reset during manual positioning)
                if probe_tool and probe_tool.is_visible:
                    # Check if we're in Position Picking Mode (Apply button is showing)
                    if self.ui.button_geometry_apply.text() != "Apply":
                        probe_tool.set_center(*probe_pos)
            else:
                # No saved probe position - show geometry position
                position = self.case_data.get_geometry_position(selected_names[0])
                if position:
                    x, y, z = position
                    self.ui.edit_input_position_x.setText(f"{x:.4f}")
                    self.ui.edit_input_position_y.setText(f"{y:.4f}")
                    self.ui.edit_input_position_z.setText(f"{z:.4f}")
                else:
                    # Fallback to object center if no saved position
                    if self.vtk_pre:
                        obj = self.vtk_pre.obj_manager.find_by_name(selected_names[0])
                        if obj:
                            bounds = obj.actor.GetBounds()
                            center_x = (bounds[0] + bounds[1]) / 2
                            center_y = (bounds[2] + bounds[3]) / 2
                            center_z = (bounds[4] + bounds[5]) / 2

                            self.ui.edit_input_position_x.setText(f"{center_x:.2f}")
                            self.ui.edit_input_position_y.setText(f"{center_y:.2f}")
                            self.ui.edit_input_position_z.setText(f"{center_z:.2f}")
        else:
            self._highlight_multiple_objects(selected_names)
            # Multiple selection - clear position fields and disable Input Position group and Set button
            self.ui.edit_input_position_x.setText("")
            self.ui.edit_input_position_y.setText("")
            self.ui.edit_input_position_z.setText("")
            self.ui.AdvancedGroupBox.setEnabled(False)
            self.ui.button_geometry_apply.setEnabled(False)

    def _highlight_object(self, obj_name: str):
        """Highlight selected object - handled by ObjectManager."""
        # Selection visual is now handled by ObjectManager._update_selection_visual()
        # which also fades edge colors for wireframe/surface with edge modes
        pass

    def _highlight_multiple_objects(self, obj_names: list):
        """Highlight multiple selected objects - handled by ObjectManager."""
        # Selection visual is now handled by ObjectManager._update_selection_visual()
        pass

    def _restore_all_opacity(self):
        """Restore all objects to full opacity - handled by ObjectManager."""
        # Selection visual is now handled by ObjectManager._update_selection_visual()
        pass

    def _sync_vtk_selection(self, selected_names: list):
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
            # 트리에서 선택이 있지만 VTK 객체가 없으면 모든 객체 반투명하게
            if selected_names:
                obj_manager.fade_all()
            else:
                obj_manager.clear_selection()
        else:
            obj_manager.select_multiple(selected_ids)

        # Unblock signals
        obj_manager.blockSignals(False)

        # Force render update
        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    def _on_vtk_selection_changed(self, info: dict):
        """Handle VTK selection changed - sync tree widget selection."""
        selected_objects = info.get("selected_objects", [])
        selected_names = [obj["name"] for obj in selected_objects]
        selected_count = len(selected_names)

        # Block signals to prevent feedback loop
        self.tree.widget.blockSignals(True)

        # Clear current selection
        self.tree.widget.clearSelection()

        # Select matching items in tree
        for i in range(self.tree.widget.topLevelItemCount()):
            item = self.tree.widget.topLevelItem(i)
            if item and item.text(0) in selected_names:
                item.setSelected(True)

        self.tree.widget.blockSignals(False)

        # Update opacity based on selection
        if selected_count == 0:
            self._restore_all_opacity()
            self.ui.edit_input_position_x.setText("0")
            self.ui.edit_input_position_y.setText("0")
            self.ui.edit_input_position_z.setText("0")
            # Enable Input Position group and Set button
            self.ui.AdvancedGroupBox.setEnabled(True)
            self.ui.button_geometry_apply.setEnabled(True)
        elif selected_count == 1:
            # Enable Input Position group and Set button for single selection
            self.ui.AdvancedGroupBox.setEnabled(True)
            self.ui.button_geometry_apply.setEnabled(True)
            self._highlight_object(selected_names[0])

            # Print selected object size
            if self.vtk_pre:
                obj = self.vtk_pre.obj_manager.find_by_name(selected_names[0])
                if obj:
                    bounds = obj.actor.GetBounds()
                    obj_size = (
                        bounds[1] - bounds[0],
                        bounds[3] - bounds[2],
                        bounds[5] - bounds[4]
                    )

            # Check if point_probe is visible
            probe_tool = None
            if self.vtk_pre:
                probe_tool = self.vtk_pre._optional_tools.get("point_probe")

            # Try to load saved probe position first
            probe_pos = self.case_data.get_geometry_probe_position(selected_names[0])

            if probe_pos is not None:
                # Display saved probe position in line editors
                x, y, z = probe_pos
                self.ui.edit_input_position_x.setText(f"{x:.4f}")
                self.ui.edit_input_position_y.setText(f"{y:.4f}")
                self.ui.edit_input_position_z.setText(f"{z:.4f}")

                # Only update probe position if visible AND not in Position Picking Mode
                # (to avoid size reset during manual positioning)
                if probe_tool and probe_tool.is_visible:
                    # Check if we're in Position Picking Mode (Apply button is showing)
                    if self.ui.button_geometry_apply.text() != "Apply":
                        probe_tool.set_center(*probe_pos)
            else:
                # No saved probe position - show geometry position
                position = self.case_data.get_geometry_position(selected_names[0])
                if position:
                    x, y, z = position
                    self.ui.edit_input_position_x.setText(f"{x:.4f}")
                    self.ui.edit_input_position_y.setText(f"{y:.4f}")
                    self.ui.edit_input_position_z.setText(f"{z:.4f}")
                else:
                    # Fallback to object center if no saved position
                    if self.vtk_pre:
                        obj = self.vtk_pre.obj_manager.find_by_name(selected_names[0])
                        if obj:
                            bounds = obj.actor.GetBounds()
                            center_x = (bounds[0] + bounds[1]) / 2
                            center_y = (bounds[2] + bounds[3]) / 2
                            center_z = (bounds[4] + bounds[5]) / 2

                            self.ui.edit_input_position_x.setText(f"{center_x:.2f}")
                            self.ui.edit_input_position_y.setText(f"{center_y:.2f}")
                            self.ui.edit_input_position_z.setText(f"{center_z:.2f}")
        else:
            self._highlight_multiple_objects(selected_names)
            # Multiple selection - clear position fields and disable Input Position group and Set button
            self.ui.edit_input_position_x.setText("")
            self.ui.edit_input_position_y.setText("")
            self.ui.edit_input_position_z.setText("")
            self.ui.AdvancedGroupBox.setEnabled(False)
            self.ui.button_geometry_apply.setEnabled(False)

    def _on_probe_visibility_changed(self, is_visible: bool):
        """Handle point_probe visibility changed - enable/disable tree widget and buttons."""
        if is_visible:
            # Probe activated - disable tree widget and Add/Remove buttons
            self.tree.widget.setEnabled(False)
            self.ui.button_geometry_add.setEnabled(False)
            self.ui.button_geometry_remove.setEnabled(False)
            # Set/Apply button remains enabled (controlled by selection logic)
        else:
            # Probe deactivated - enable tree widget and Add/Remove buttons
            self.tree.widget.setEnabled(True)
            self.ui.button_geometry_add.setEnabled(True)
            self.ui.button_geometry_remove.setEnabled(True)
            # Set/Apply button remains enabled (controlled by selection logic)

    def _on_clip_mode_changed(self, mode: str):
        """Handle clip mode combo box change."""
        mode_lower = mode.lower()
        is_clipping = (mode_lower != "off")

        # Enable/disable controls based on mode
        self._clip_slider.setEnabled(is_clipping)
        self._clip_preview_check.setEnabled(is_clipping)
        self._clip_apply_btn.setEnabled(is_clipping and self._clip_preview_check.isChecked())
        self._clip_reset_btn.setEnabled(is_clipping)

        # Reset slider to center when mode changes
        if is_clipping:
            self._clip_slider.blockSignals(True)
            self._clip_slider.setValue(50)
            self._clip_slider.blockSignals(False)
            # Update position label manually since signals are blocked
            if hasattr(self, '_lbl_pos_value'):
                self._lbl_pos_value.setText("50%")

        # Apply clip to VTK widget (preview or real-time based on checkbox)
        if self.vtk_pre:
            is_preview = self._clip_preview_check.isChecked() if is_clipping else False
            self.vtk_pre.set_clip_mode(mode_lower, preview=is_preview)

    def _on_clip_preview_toggled(self, checked: bool):
        """Handle preview checkbox toggle."""
        # Enable/disable apply button based on preview mode
        mode_lower = self._clip_combo.currentText().lower()
        is_clipping = (mode_lower != "off")
        self._clip_apply_btn.setEnabled(is_clipping and checked)

        # Update VTK clip mode with new preview state
        if self.vtk_pre and is_clipping:
            self.vtk_pre.set_clip_mode(mode_lower, preview=checked)
            # Also update position to refresh the view
            self.vtk_pre.set_clip_position(self._clip_slider.value(), preview=checked)

    def _on_clip_apply_clicked(self):
        """Handle Apply button click - apply the clip."""
        if self.vtk_pre:
            self.vtk_pre.apply_clip()

    def _on_clip_reset_clicked(self):
        """Handle Reset button click - reset clip to original state (keep preview plane)."""
        if self.vtk_pre:
            self.vtk_pre.reset_clip()
            # Ensure preview checkbox is checked
            self._clip_preview_check.blockSignals(True)
            self._clip_preview_check.setChecked(True)
            self._clip_preview_check.blockSignals(False)
            # Enable apply button since we're back in preview mode
            self._clip_apply_btn.setEnabled(True)

    def _on_clip_slider_changed(self, value: int):
        """Handle clip slider value change."""
        # Update position label
        if hasattr(self, '_lbl_pos_value'):
            self._lbl_pos_value.setText(f"{value}%")

        if self.vtk_pre:
            is_preview = self._clip_preview_check.isChecked()
            self.vtk_pre.set_clip_position(value, preview=is_preview)

    def load_data(self):
        """Load geometry data from model folder."""
        self.tree.clear_all()

        # Add "fluid" as fixed first item (cannot be removed)
        self.tree.insert([], "fluid")

        # Get model directory path
        model_path = Path(self.case_data.path) / "1.model_Mhead" / "scale0"

        if not model_path.exists():
            return

        # Find all STL files in model directory (excluding mesh.stl)
        stl_files = []
        for stl_file in model_path.glob("*.stl"):
            if stl_file.name.lower() != "mesh.stl":
                stl_files.append(stl_file)

        if not stl_files:
            return

        # Add files to tree and case_data
        for stl_file in stl_files:
            name = stl_file.stem
            if name != "fluid":  # Skip if fluid (already added)
                self.tree.insert([], name)
            # Add to case_data if not already there
            if not self.case_data.get_geometry(name):
                self.case_data.add_geometry(stl_file)

        # Load STL files asynchronously to VTK
        if self.vtk_pre and stl_files:
            self._start_async_loading([str(f) for f in stl_files])
        else:
            self.case_data.save()
