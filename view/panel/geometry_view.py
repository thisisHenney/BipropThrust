
import traceback
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QToolBar, QLabel, QComboBox, QSlider, QPushButton,
    QProgressDialog, QHeaderView, QDoubleSpinBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


def _get_progress_color(progress: float) -> str:
    # Gradient color stops (Blue → Green → Yellow → Orange)
    GRAD = [
        (0,   (59, 130, 246)),   # Blue
        (33,  (34, 197, 94)),    # Green
        (66,  (234, 179, 8)),    # Yellow
        (100, (249, 115, 22)),   # Orange
    ]

    # Find the two stops to interpolate between
    for i in range(len(GRAD) - 1):
        p1, c1 = GRAD[i]
        p2, c2 = GRAD[i + 1]
        if p1 <= progress <= p2:
            t = (progress - p1) / (p2 - p1) if p2 != p1 else 0
            r = int(c1[0] + (c2[0] - c1[0]) * t)
            g = int(c1[1] + (c2[1] - c1[1]) * t)
            b = int(c1[2] + (c2[2] - c1[2]) * t)
            return f"rgb({r}, {g}, {b})"

    # Fallback to last color
    return f"rgb({GRAD[-1][1][0]}, {GRAD[-1][1][1]}, {GRAD[-1][1][2]})"


def _get_progress_stylesheet(progress: float) -> str:
    color = _get_progress_color(progress)
    return f"""
        QProgressBar {{
            border: 1px solid #888;
            border-radius: 5px;
            background-color: #d0d0dd;
            text-align: center;
            color: #333;
            font-weight: bold;
            font-size: 12px;
        }}
        QProgressBar::chunk {{
            background-color: {color};
            border-radius: 4px;
        }}
    """

from nextlib.dialogbox.dialogbox import FileDialogBox
from nextlib.widgets.tree import TreeWidget
from nextlib.vtk.core import MeshLoader

from common.app_data import app_data
from common.case_data import case_data


class GeometryView:

    # Visibility icons (Unicode)
    ICON_VISIBLE = "\U0001F441"  # 👁
    ICON_HIDDEN = "\u25CB"  # ○ (empty circle)

    def __init__(self, parent):
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

        # Track visibility state per object
        self._visibility_state = {}  # {name: bool}

        # Track flat/planar geometries (any axis extent < 1e-6)
        self._flat_geometries = set()

        # Initialize mesh loader for async loading
        self.mesh_loader = MeshLoader()
        self._loading_signals_connected = False
        self._loading_total = 0

        # Disable individual outlines in VTK (show only combined bbox)
        if self.vtk_pre:
            self.vtk_pre.obj_manager.show_individual_outlines = False

        # Red sphere marker for probe position (shown when picking mode is off)
        self._probe_marker_actor = None
        self._saved_view_style = None  # view style saved before entering picking mode

        # Setup tree for visibility column
        self._setup_visibility_tree()

        # Create slice controls widget (will be shown/hidden by center_widget)
        self.slice_widget = self._create_slice_widget()

        # Connect signals
        self._init_connect()

    def _setup_visibility_tree(self):
        tree_widget = self.tree.widget

        # Set 2 columns
        tree_widget.setColumnCount(2)
        tree_widget.setHeaderHidden(True)

        # Configure column sizes
        header = tree_widget.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        tree_widget.setColumnWidth(1, 30)

        # Connect item click for visibility toggle
        tree_widget.itemClicked.connect(self._on_tree_item_clicked)

    def _create_slice_widget(self):
        if not self.vtk_pre:
            return None

        # Create toolbar
        clip_toolbar = QToolBar("Clip Controls", self.vtk_pre)
        clip_toolbar.setObjectName("vtkBottomBar")
        clip_toolbar.setFloatable(True)
        clip_toolbar.setMovable(True)

        # Clip mode selection
        clip_toolbar.addWidget(QLabel("Clip:"))

        self._clip_combo = QComboBox()
        self._clip_combo.addItems(["Off", "X", "Y", "Z", "Custom"])
        self._clip_combo.setCurrentText("Off")
        self._clip_combo.setFixedWidth(70)
        clip_toolbar.addWidget(self._clip_combo)

        # Normal vector spinboxes
        clip_toolbar.addWidget(QLabel(" n=("))

        self._clip_spin_nx = QDoubleSpinBox()
        self._clip_spin_nx.setRange(-1.0, 1.0)
        self._clip_spin_nx.setSingleStep(0.1)
        self._clip_spin_nx.setValue(1.0)
        self._clip_spin_nx.setMaximumWidth(60)
        self._clip_spin_nx.setEnabled(False)
        clip_toolbar.addWidget(self._clip_spin_nx)

        clip_toolbar.addWidget(QLabel(","))

        self._clip_spin_ny = QDoubleSpinBox()
        self._clip_spin_ny.setRange(-1.0, 1.0)
        self._clip_spin_ny.setSingleStep(0.1)
        self._clip_spin_ny.setValue(0.0)
        self._clip_spin_ny.setMaximumWidth(60)
        self._clip_spin_ny.setEnabled(False)
        clip_toolbar.addWidget(self._clip_spin_ny)

        clip_toolbar.addWidget(QLabel(","))

        self._clip_spin_nz = QDoubleSpinBox()
        self._clip_spin_nz.setRange(-1.0, 1.0)
        self._clip_spin_nz.setSingleStep(0.1)
        self._clip_spin_nz.setValue(0.0)
        self._clip_spin_nz.setMaximumWidth(60)
        self._clip_spin_nz.setEnabled(False)
        clip_toolbar.addWidget(self._clip_spin_nz)

        clip_toolbar.addWidget(QLabel(")"))

        # Position slider
        clip_toolbar.addWidget(QLabel(" Pos:"))

        self._clip_slider = QSlider(Qt.Horizontal)
        self._clip_slider.setMinimum(0)
        self._clip_slider.setMaximum(100)
        self._clip_slider.setValue(50)
        self._clip_slider.setMinimumWidth(200)
        self._clip_slider.setEnabled(False)
        clip_toolbar.addWidget(self._clip_slider)

        self._lbl_pos_value = QLabel("50%")
        self._lbl_pos_value.setMinimumWidth(40)
        clip_toolbar.addWidget(self._lbl_pos_value)

        # Flip button
        self._clip_flip_btn = QPushButton("Flip")
        self._clip_flip_btn.setFixedWidth(50)
        self._clip_flip_btn.setCheckable(True)
        self._clip_flip_btn.setEnabled(False)
        clip_toolbar.addWidget(self._clip_flip_btn)

        # Reset button
        self._clip_reset_btn = QPushButton("Reset")
        self._clip_reset_btn.setFixedWidth(60)
        self._clip_reset_btn.setEnabled(False)
        clip_toolbar.addWidget(self._clip_reset_btn)

        # Hide toolbar initially
        clip_toolbar.hide()

        # Add to VTK widget as bottom toolbar (QMainWindow 기반)
        self.vtk_pre.addToolBar(Qt.BottomToolBarArea, clip_toolbar)

        return clip_toolbar

    def _init_connect(self):
        # Clip controls
        self._clip_combo.currentTextChanged.connect(self._on_clip_mode_changed)
        self._clip_slider.valueChanged.connect(self._on_clip_slider_changed)
        self._clip_slider.sliderReleased.connect(self._on_clip_slider_released)
        self._clip_flip_btn.toggled.connect(self._on_clip_flip_toggled)
        self._clip_reset_btn.clicked.connect(self._on_clip_reset_clicked)
        self._clip_spin_nx.valueChanged.connect(self._on_clip_normal_changed)
        self._clip_spin_ny.valueChanged.connect(self._on_clip_normal_changed)
        self._clip_spin_nz.valueChanged.connect(self._on_clip_normal_changed)

        # Button clicks
        self.ui.button_geometry_add.clicked.connect(self._on_add_clicked)
        self.ui.button_geometry_remove.clicked.connect(self._on_remove_clicked)
        self.ui.button_geometry_reset.clicked.connect(self._on_reset_clicked)
        self.ui.button_geometry_apply.clicked.connect(self._on_set_apply_clicked)
        self.ui.button_geometry_cancel.clicked.connect(self._on_cancel_clicked)

        # Change button text to "Position Picking Mode" - disabled until tree item selected
        self.ui.button_geometry_apply.setText("Position Picking Mode")
        self.ui.button_geometry_apply.setEnabled(False)

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

    def _on_tree_item_clicked(self, item, column):
        if column != 1:
            return

        name = item.text(0)
        current_visible = self._visibility_state.get(name, True)
        new_visible = not current_visible

        self._set_object_visibility(name, new_visible)

    def _set_object_visibility(self, name: str, visible: bool):
        self._visibility_state[name] = visible

        # Update tree icon
        for i in range(self.tree.widget.topLevelItemCount()):
            item = self.tree.widget.topLevelItem(i)
            if item and item.text(0) == name:
                item.setText(1, self.ICON_VISIBLE if visible else self.ICON_HIDDEN)
                break

        # Update VTK actor visibility
        if self.vtk_pre:
            obj = self.vtk_pre.obj_manager.find_by_name(name)
            if obj:
                obj.actor.SetVisibility(visible)
                self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    def set_all_visible(self, visible: bool):
        for i in range(self.tree.widget.topLevelItemCount()):
            item = self.tree.widget.topLevelItem(i)
            if item:
                name = item.text(0)
                self._set_object_visibility(name, visible)

    def _add_tree_item_with_visibility(self, name: str, visible: bool = True):
        self.tree.insert([], name)
        self._visibility_state[name] = visible

        # Find the newly added item and set visibility icon
        for i in range(self.tree.widget.topLevelItemCount()):
            item = self.tree.widget.topLevelItem(i)
            if item and item.text(0) == name:
                item.setText(1, self.ICON_VISIBLE if visible else self.ICON_HIDDEN)
                # Center align the visibility icon
                item.setTextAlignment(1, Qt.AlignmentFlag.AlignCenter)
                break

    def _on_add_clicked(self):
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
                traceback.print_exc()
                continue

            # Add to case_data and tree
            name = dst_file.stem
            self.case_data.add_geometry(dst_file)
            # Only add tree item if not already present in the tree
            tree_names = [
                self.tree.widget.topLevelItem(i).text(0)
                for i in range(self.tree.widget.topLevelItemCount())
            ]
            if name not in tree_names:
                self._add_tree_item_with_visibility(name, visible=True)
            copied_files.append(str(dst_file))

        # Load STL files asynchronously to prevent GUI lock
        if self.vtk_pre and copied_files:
            self._start_async_loading(copied_files)
        else:
            self.case_data.save()

    def _start_async_loading(self, files: list):
        self._loading_total = len(files)

        # Create QProgressDialog
        self._progress_dialog = QProgressDialog(
            "Loading geometry files...", "Cancel", 0, len(files), self.parent
        )
        self._progress_dialog.setWindowTitle("Loading")
        self._progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self._progress_dialog.setMinimumDuration(0)
        self._progress_dialog.setValue(0)
        self._progress_dialog.setStyleSheet(_get_progress_stylesheet(0))
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
        if self.vtk_pre and actor:
            self.vtk_pre.obj_manager.add(actor, name=name, group="geometry")

            # Set default probe_position to object center
            bounds = actor.GetBounds()
            center_x = (bounds[0] + bounds[1]) / 2
            center_y = (bounds[2] + bounds[3]) / 2
            center_z = (bounds[4] + bounds[5]) / 2

            # Detect flat/planar geometry (any axis extent < 1e-6)
            dx = bounds[1] - bounds[0]
            dy = bounds[3] - bounds[2]
            dz = bounds[5] - bounds[4]
            if dx < 1e-6 or dy < 1e-6 or dz < 1e-6:
                self._flat_geometries.add(name)

            # Only set probe_position to geometry center if not already set
            # (e.g. loaded from snappyHexMeshDict or case_data.json)
            existing = self.case_data.get_geometry_probe_position(name)
            if not existing or existing == (0.0, 0.0, 0.0):
                self.case_data.set_geometry_probe_position(name, center_x, center_y, center_z)

    def _on_loading_progress(self, current: int, total: int):
        try:
            dialog = getattr(self, '_progress_dialog', None)
            if dialog is not None:
                progress_pct = (current / total) * 100 if total > 0 else 0
                dialog.setValue(current)
                dialog.setLabelText(f"Loading geometry files... ({current}/{total})")
                dialog.setStyleSheet(_get_progress_stylesheet(progress_pct))
        except (RuntimeError, AttributeError):
            # Dialog may have been closed during progress update
            pass

    def _on_loading_error(self, file_path: str, error_msg: str):
        pass

    def _on_loading_canceled(self):
        self.mesh_loader.cancel_async()
        self._cleanup_loading_signals()
        if hasattr(self, '_progress_dialog') and self._progress_dialog:
            self._progress_dialog.close()
            self._progress_dialog = None

    def _on_loading_finished(self):
        # Close progress dialog
        if hasattr(self, '_progress_dialog') and self._progress_dialog:
            self._progress_dialog.close()
            self._progress_dialog = None

        # Disconnect signals
        self._cleanup_loading_signals()

        # Apply saved transforms to all loaded objects
        if self.vtk_pre:
            self._apply_saved_transforms()

            # Set fluid's default probe position to center of combined geometry bounds
            self._update_fluid_probe_position()

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

            # Re-enable picking button based on current selection
            # (fluid needs geometry bounds, flat geometries stay disabled)
            selected_items = self.tree.widget.selectedItems()
            if selected_items:
                selected_name = selected_items[0].text(0)
                if selected_name in self._flat_geometries:
                    self.ui.button_geometry_apply.setEnabled(False)
                elif selected_name == "fluid" and self._get_combined_geometry_bounds() is not None:
                    self.ui.button_geometry_apply.setEnabled(True)
                elif selected_name not in ("fluid",):
                    self.ui.button_geometry_apply.setEnabled(True)

        self.case_data.save()

    def _apply_saved_transforms(self):
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

    def _get_combined_geometry_bounds(self):
        if not self.vtk_pre:
            return None
        all_objs = self.vtk_pre.obj_manager.get_all()
        geom_objs = [o for o in all_objs
                     if hasattr(o, 'group') and o.group == "geometry"]
        if not geom_objs:
            return None
        combined = [float('inf'), float('-inf'),
                    float('inf'), float('-inf'),
                    float('inf'), float('-inf')]
        for go in geom_objs:
            gb = go.actor.GetBounds()
            combined[0] = min(combined[0], gb[0])
            combined[1] = max(combined[1], gb[1])
            combined[2] = min(combined[2], gb[2])
            combined[3] = max(combined[3], gb[3])
            combined[4] = min(combined[4], gb[4])
            combined[5] = max(combined[5], gb[5])
        return tuple(combined)

    def _update_fluid_probe_position(self):
        bounds = self._get_combined_geometry_bounds()
        if bounds is None:
            return
        cx = (bounds[0] + bounds[1]) / 2
        cy = (bounds[2] + bounds[3]) / 2
        cz = (bounds[4] + bounds[5]) / 2
        self.case_data.set_geometry_probe_position("fluid", cx, cy, cz)

    def _cleanup_loading_signals(self):
        if not getattr(self, '_loading_signals_connected', False):
            return

        self._loading_signals_connected = False
        self.mesh_loader.file_loaded.disconnect(self._on_file_loaded)
        self.mesh_loader.progress.disconnect(self._on_loading_progress)
        self.mesh_loader.all_finished.disconnect(self._on_loading_finished)
        self.mesh_loader.error.disconnect(self._on_loading_error)

    def _on_remove_clicked(self):
        # Get all selected items
        selected_items = self.tree.widget.selectedItems()
        if not selected_items:
            return

        # Collect names to remove (excluding "fluid")
        names_to_remove = []
        for item in selected_items:
            name = item.text(0)
            if name != "fluid":
                names_to_remove.append(name)

        if not names_to_remove:
            return

        model_path = Path(self.case_data.path) / "1.model_Mhead" / "scale0"

        # Remove each item
        for obj_name in names_to_remove:
            # Remove from tree (find item by name since positions change after each removal)
            for i in range(self.tree.widget.topLevelItemCount()):
                item = self.tree.widget.topLevelItem(i)
                if item and item.text(0) == obj_name:
                    self.tree.widget.takeTopLevelItem(i)
                    break

            # Remove from VTK
            if self.vtk_pre:
                obj = self.vtk_pre.obj_manager.find_by_name(obj_name)
                if obj:
                    self.vtk_pre.obj_manager.remove(obj.id)

            # Remove STL file from model directory
            stl_file = model_path / f"{obj_name}.stl"
            if stl_file.exists():
                try:
                    stl_file.unlink()
                except Exception:
                    traceback.print_exc()

            # Remove from case_data and visibility state
            self.case_data.remove_geometry(obj_name)
            if obj_name in self._visibility_state:
                del self._visibility_state[obj_name]

        # Refresh VTK view once after all removals
        if self.vtk_pre:
            self.vtk_pre.vtk_widget.GetRenderWindow().Render()

        # Save case_data once after all removals
        self.case_data.save()

    def _on_set_apply_clicked(self):
        current_text = self.ui.button_geometry_apply.text()

        if current_text == "Position Picking Mode":
            # Save current view style before entering picking mode
            if self.vtk_pre:
                self._saved_view_style = self.vtk_pre._current_view_style

            # Activate point_probe and change button to "Apply"
            if self.vtk_pre:
                probe_tool = self.vtk_pre._optional_tools.get("point_probe")
                if probe_tool:
                    # Get current selection
                    pos = self.tree.get_current_pos()
                    if pos is not None:
                        obj_name = self.tree.get_text(pos)

                        # Get selected object bounds
                        # fluid uses combined bounds of all geometries
                        if obj_name == "fluid":
                            self.vtk_pre.obj_manager.blockSignals(True)
                            self.vtk_pre.obj_manager.clear_selection()
                            self.vtk_pre.obj_manager.blockSignals(False)
                            bounds = self._get_combined_geometry_bounds()
                            if bounds is None:
                                return
                            # Make all geometry objects transparent for fluid picking
                            self._set_geometry_opacity(0.3)
                        else:
                            obj = self.vtk_pre.obj_manager.find_by_name(obj_name)
                            if obj:
                                bounds = obj.actor.GetBounds()
                            else:
                                return

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
                        # fluid는 VTK 객체가 없으므로 선택 ID를 비워서 이전 선택 상태 방지
                        if obj_name == "fluid":
                            probe_tool._saved_selection_ids = set()
                        else:
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
                    self._set_geometry_opacity(1.0)
                    self.ui.button_geometry_apply.setText("Position Picking Mode")
                    self.ui.button_geometry_cancel.hide()
                    self.ui.button_geometry_reset.hide()

                    # Restore view style that was active before picking mode
                    if self.vtk_pre and hasattr(self, '_saved_view_style') and self._saved_view_style:
                        self.vtk_pre.set_visibility_mode(self.vtk_pre._visibility_mode, apply_visibility=False)
                        self.vtk_pre.obj_manager.all().style(self._saved_view_style)
                        self.vtk_pre._view_combo.setCurrentText(self._saved_view_style)

                    # Show red sphere at saved probe position
                    if probe_center:
                        self._show_probe_marker(*probe_center)

    def _on_cancel_clicked(self):
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
                        # No saved position - use object center or combined bounds
                        if obj_name == "fluid":
                            bounds = self._get_combined_geometry_bounds()
                        else:
                            obj = self.vtk_pre.obj_manager.find_by_name(obj_name)
                            bounds = obj.actor.GetBounds() if obj else None
                        if bounds:
                            x = (bounds[0] + bounds[1]) / 2
                            y = (bounds[2] + bounds[3]) / 2
                            z = (bounds[4] + bounds[5]) / 2
                        else:
                            x, y, z = 0.0, 0.0, 0.0

                    # Update line editors
                    self.ui.edit_input_position_x.setText(f"{x:.4f}")
                    self.ui.edit_input_position_y.setText(f"{y:.4f}")
                    self.ui.edit_input_position_z.setText(f"{z:.4f}")

                # Deactivate probe
                probe_tool.hide()
                self._set_geometry_opacity(1.0)
                self.ui.button_geometry_apply.setText("Position Picking Mode")
                self.ui.button_geometry_cancel.hide()
                self.ui.button_geometry_reset.hide()

                # Restore view style that was active before picking mode
                if self.vtk_pre and hasattr(self, '_saved_view_style') and self._saved_view_style:
                    self.vtk_pre.obj_manager.all().style(self._saved_view_style)
                    self.vtk_pre._view_combo.setCurrentText(self._saved_view_style)

                # Show red sphere at restored position
                self._show_probe_marker(x, y, z)

    def _on_reset_clicked(self):
        # Get selected object
        pos = self.tree.get_current_pos()
        if pos is None:
            return

        obj_name = self.tree.get_text(pos)

        # Get object bounds from VTK (fluid uses combined bounds)
        if self.vtk_pre:
            if obj_name == "fluid":
                bounds = self._get_combined_geometry_bounds()
            else:
                obj = self.vtk_pre.obj_manager.find_by_name(obj_name)
                bounds = obj.actor.GetBounds() if obj else None
            if bounds:
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
                        probe_tool._update_cursor_from_bounds(new_bounds)
                        probe_tool._saved_bounds = new_bounds
                        probe_tool._saved_transform = None
                        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    def _on_tree_selection_changed(self):
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
            # Disable Position Picking button when nothing is selected
            self.ui.AdvancedGroupBox.setEnabled(True)
            self.ui.button_geometry_apply.setEnabled(False)
            self._hide_probe_marker()
        elif selected_count == 1:
            # Enable Input Position group and Set button for single selection
            self.ui.AdvancedGroupBox.setEnabled(True)
            # Disable picking for flat geometries or fluid with no geometry objects
            sel_name = selected_names[0]
            if sel_name in self._flat_geometries:
                self.ui.button_geometry_apply.setEnabled(False)
            elif sel_name == "fluid" and self._get_combined_geometry_bounds() is None:
                self.ui.button_geometry_apply.setEnabled(False)
            else:
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

                # Update red sphere marker if not in picking mode (flat objects excluded)
                is_picking = (self.ui.button_geometry_apply.text() == "Apply")
                is_flat = selected_names[0] in self._flat_geometries
                if not is_picking and not is_flat:
                    self._show_probe_marker(x, y, z)
                else:
                    self._hide_probe_marker()

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
                # No saved probe position - hide marker and show geometry position
                self._hide_probe_marker()
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
        # Selection visual is now handled by ObjectManager._update_selection_visual()
        # which also fades edge colors for wireframe/surface with edge modes
        pass

    def _highlight_multiple_objects(self, obj_names: list):
        # Selection visual is now handled by ObjectManager._update_selection_visual()
        pass

    def _restore_all_opacity(self):
        # Selection visual is now handled by ObjectManager._update_selection_visual()
        pass

    def _set_geometry_opacity(self, opacity: float):
        if not self.vtk_pre:
            return
        for obj in self.vtk_pre.obj_manager.get_all():
            if hasattr(obj, 'group') and obj.group == "geometry":
                obj.actor.GetProperty().SetOpacity(opacity)
        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    def _sync_vtk_selection(self, selected_names: list):
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
            # Disable Position Picking button when nothing is selected
            self.ui.AdvancedGroupBox.setEnabled(True)
            self.ui.button_geometry_apply.setEnabled(False)
            self._hide_probe_marker()
        elif selected_count == 1:
            # Enable Input Position group and Set button for single selection
            self.ui.AdvancedGroupBox.setEnabled(True)
            # Disable picking for flat geometries or fluid with no geometry objects
            sel_name = selected_names[0]
            if sel_name in self._flat_geometries:
                self.ui.button_geometry_apply.setEnabled(False)
            elif sel_name == "fluid" and self._get_combined_geometry_bounds() is None:
                self.ui.button_geometry_apply.setEnabled(False)
            else:
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

                # Update red sphere marker if not in picking mode (flat objects excluded)
                is_picking = (self.ui.button_geometry_apply.text() == "Apply")
                is_flat = selected_names[0] in self._flat_geometries
                if not is_picking and not is_flat:
                    self._show_probe_marker(x, y, z)
                else:
                    self._hide_probe_marker()

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
                # No saved probe position - hide marker and show geometry position
                self._hide_probe_marker()
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
        if is_visible:
            # Probe activated: hide marker, disable tree/buttons
            self._hide_probe_marker()
            self.tree.widget.setEnabled(False)
            self.ui.button_geometry_add.setEnabled(False)
            self.ui.button_geometry_remove.setEnabled(False)
        else:
            # Probe deactivated: enable tree/buttons
            self.tree.widget.setEnabled(True)
            self.ui.button_geometry_add.setEnabled(True)
            self.ui.button_geometry_remove.setEnabled(True)

    def _get_probe_marker_radius(self) -> float:
        """개별 STL 오브젝트(fluid 제외) 중 첫 번째 것의 대각선 1.5%를 공통 반지름으로 반환."""
        if not self.vtk_pre:
            return 0.005
        try:
            for name, geo in self.case_data.objects.items():
                if name == "fluid":
                    continue
                obj = self.vtk_pre.obj_manager.find_by_name(name)
                if obj and obj.actor:
                    bounds = obj.actor.GetBounds()
                    dx = bounds[1] - bounds[0]
                    dy = bounds[3] - bounds[2]
                    dz = bounds[5] - bounds[4]
                    diag = (dx**2 + dy**2 + dz**2) ** 0.5
                    if diag > 0:
                        return diag * 0.015
        except Exception:
            pass
        return 0.005

    def _show_probe_marker(self, x: float, y: float, z: float):
        """빨간 구를 표시한다. 크기는 모든 오브젝트에서 공통으로 사용."""
        if not self.vtk_pre:
            return

        try:
            from vtkmodules.vtkFiltersSources import vtkSphereSource
            from vtkmodules.vtkRenderingCore import vtkPolyDataMapper, vtkActor
        except ImportError:
            try:
                from vtk import vtkSphereSource, vtkPolyDataMapper, vtkActor
            except ImportError:
                return

        # Remove existing marker
        self._hide_probe_marker()

        radius = self._get_probe_marker_radius()

        sphere = vtkSphereSource()
        sphere.SetCenter(x, y, z)
        sphere.SetRadius(radius)
        sphere.SetThetaResolution(24)
        sphere.SetPhiResolution(24)

        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(sphere.GetOutputPort())

        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(1.0, 0.1, 0.1)   # 빨간색
        actor.GetProperty().SetOpacity(0.85)

        self.vtk_pre.renderer.AddActor(actor)
        self.vtk_pre.vtk_widget.GetRenderWindow().Render()
        self._probe_marker_actor = actor

    def _hide_probe_marker(self):
        """빨간 구 마커를 제거한다."""
        if self._probe_marker_actor and self.vtk_pre:
            try:
                self.vtk_pre.renderer.RemoveActor(self._probe_marker_actor)
                self.vtk_pre.vtk_widget.GetRenderWindow().Render()
            except Exception:
                pass
        self._probe_marker_actor = None

    def _on_clip_mode_changed(self, mode: str):
        mode_lower = mode.lower()
        is_clipping = (mode_lower != "off")
        is_custom = (mode_lower == "custom")

        self._clip_slider.setEnabled(is_clipping)
        self._clip_flip_btn.setEnabled(is_clipping)
        self._clip_reset_btn.setEnabled(is_clipping)
        self._clip_spin_nx.setEnabled(is_custom)
        self._clip_spin_ny.setEnabled(is_custom)
        self._clip_spin_nz.setEnabled(is_custom)

        # Set normal spinbox values for fixed axes
        for spin, val in zip(
            [self._clip_spin_nx, self._clip_spin_ny, self._clip_spin_nz],
            {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}.get(mode_lower, (None, None, None))
        ):
            if val is not None:
                spin.blockSignals(True)
                spin.setValue(val)
                spin.blockSignals(False)

        if not is_clipping:
            self._clip_flip_btn.blockSignals(True)
            self._clip_flip_btn.setChecked(True)   # 기본: 반전 상태
            self._clip_flip_btn.blockSignals(False)

        if is_clipping:
            self._clip_slider.blockSignals(True)
            self._clip_slider.setValue(50)
            self._clip_slider.blockSignals(False)
            if hasattr(self, '_lbl_pos_value'):
                self._lbl_pos_value.setText("50%")
            # 클립 활성화 시 기본 flip=True 적용
            self._clip_flip_btn.blockSignals(True)
            self._clip_flip_btn.setChecked(True)
            self._clip_flip_btn.blockSignals(False)
            if self.vtk_pre:
                self.vtk_pre.set_clip_invert(True)

        if self.vtk_pre:
            if is_custom:
                nx = self._clip_spin_nx.value()
                ny = self._clip_spin_ny.value()
                nz = self._clip_spin_nz.value()
                self.vtk_pre.set_clip_custom_normal(nx, ny, nz)
            self.vtk_pre.set_clip_mode(mode_lower, preview=is_clipping)

    def _on_clip_flip_toggled(self, checked: bool):
        if self.vtk_pre:
            self.vtk_pre.set_clip_invert(checked)

    def _on_clip_reset_clicked(self):
        if self.vtk_pre:
            self._clip_flip_btn.blockSignals(True)
            self._clip_flip_btn.setChecked(True)   # 리셋 시 기본 반전 상태로
            self._clip_flip_btn.blockSignals(False)
            self.vtk_pre.set_clip_invert(True)
            self.vtk_pre.reset_clip()

    def _on_clip_normal_changed(self):
        if self.vtk_pre and self._clip_combo.currentText().lower() == "custom":
            nx = self._clip_spin_nx.value()
            ny = self._clip_spin_ny.value()
            nz = self._clip_spin_nz.value()
            self.vtk_pre.set_clip_custom_normal(nx, ny, nz)

    def _on_clip_slider_changed(self, value: int):
        if hasattr(self, '_lbl_pos_value'):
            self._lbl_pos_value.setText(f"{value}%")
        if self.vtk_pre:
            self.vtk_pre.set_clip_position(value, preview=True)

    def _on_clip_slider_released(self):
        if self.vtk_pre:
            self.vtk_pre.apply_clip()

    def load_data(self):
        self.tree.clear_all()
        self._visibility_state.clear()

        # Add "fluid" as fixed first item (cannot be removed)
        self._add_tree_item_with_visibility("fluid", visible=True)
        # Ensure fluid exists in case_data (no STL file, path is empty)
        if not self.case_data.get_geometry("fluid"):
            from common.case_data import GeometryData
            self.case_data.objects["fluid"] = GeometryData(
                name="fluid", path="", is_visible=True
            )

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
                self._add_tree_item_with_visibility(name, visible=True)
            # Add to case_data if not already there
            if not self.case_data.get_geometry(name):
                self.case_data.add_geometry(stl_file)

        # Load STL files asynchronously to VTK
        if self.vtk_pre and stl_files:
            self._start_async_loading([str(f) for f in stl_files])
        else:
            self.case_data.save()
