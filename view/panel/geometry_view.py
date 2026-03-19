
import traceback

from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QToolBar, QLabel, QComboBox, QSlider, QPushButton,
    QHeaderView, QDoubleSpinBox
)

from PySide6.QtCore import Qt

from PySide6.QtGui import QFont

def _get_progress_color(progress: float) -> str:

    GRAD = [
        (0,   (59, 130, 246)),
        (33,  (34, 197, 94)),
        (66,  (234, 179, 8)),
        (100, (249, 115, 22)),
    ]

    for i in range(len(GRAD) - 1):

        p1, c1 = GRAD[i]

        p2, c2 = GRAD[i + 1]

        if p1 <= progress <= p2:

            t = (progress - p1) / (p2 - p1) if p2 != p1 else 0

            r = int(c1[0] + (c2[0] - c1[0]) * t)

            g = int(c1[1] + (c2[1] - c1[1]) * t)

            b = int(c1[2] + (c2[2] - c1[2]) * t)

            return f"rgb({r}, {g}, {b})"

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

    ICON_VISIBLE = "\U0001F441"

    ICON_HIDDEN = "\u25CB"

    def __init__(self, parent):

        self.parent = parent

        self.ui = self.parent.ui

        self.ctx = self.parent.context

        self.exec_widget = self.ctx.get("exec")

        self.vtk_pre = self.ctx.get("vtk_pre")

        self.app_data = app_data

        self.case_data = case_data

        self.tree = TreeWidget(self.parent, self.ui.tree_geometry)

        self._visibility_state = {}

        self._flat_geometries = set()

        self.mesh_loader = MeshLoader()

        self._loading_signals_connected = False

        self._loading_total = 0

        if self.vtk_pre:

            self.vtk_pre.obj_manager.show_individual_outlines = False

        self._probe_marker_actors: list = []

        self._saved_view_style = None

        self._setup_visibility_tree()

        self.slice_widget = self._create_slice_widget()

        self._init_connect()

    def _setup_visibility_tree(self):

        tree_widget = self.tree.widget

        tree_widget.setColumnCount(2)

        tree_widget.setHeaderHidden(True)

        header = tree_widget.header()

        header.setStretchLastSection(False)

        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)

        tree_widget.setColumnWidth(1, 30)

        tree_widget.itemClicked.connect(self._on_tree_item_clicked)

    def _create_slice_widget(self):

        if not self.vtk_pre:

            return None

        clip_toolbar = QToolBar("Clip Controls", self.vtk_pre)

        clip_toolbar.setObjectName("vtkBottomBar")

        clip_toolbar.setFloatable(True)

        clip_toolbar.setMovable(True)

        clip_toolbar.addWidget(QLabel("Clip:"))

        self._clip_combo = QComboBox()

        self._clip_combo.addItems(["Off", "X", "Y", "Z", "Custom"])

        self._clip_combo.setCurrentText("Off")

        self._clip_combo.setFixedWidth(70)

        clip_toolbar.addWidget(self._clip_combo)

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

        self._clip_flip_btn = QPushButton("Flip")

        self._clip_flip_btn.setFixedWidth(50)

        self._clip_flip_btn.setCheckable(True)

        self._clip_flip_btn.setEnabled(False)

        clip_toolbar.addWidget(self._clip_flip_btn)

        self._clip_reset_btn = QPushButton("Reset")

        self._clip_reset_btn.setFixedWidth(60)

        self._clip_reset_btn.setEnabled(False)

        clip_toolbar.addWidget(self._clip_reset_btn)

        clip_toolbar.hide()

        self.vtk_pre.addToolBar(Qt.BottomToolBarArea, clip_toolbar)

        return clip_toolbar

    def _init_connect(self):

        self._clip_combo.currentTextChanged.connect(self._on_clip_mode_changed)

        self._clip_slider.valueChanged.connect(self._on_clip_slider_changed)

        self._clip_slider.sliderReleased.connect(self._on_clip_slider_released)

        self._clip_flip_btn.toggled.connect(self._on_clip_flip_toggled)

        self._clip_reset_btn.clicked.connect(self._on_clip_reset_clicked)

        self._clip_spin_nx.valueChanged.connect(self._on_clip_normal_changed)

        self._clip_spin_ny.valueChanged.connect(self._on_clip_normal_changed)

        self._clip_spin_nz.valueChanged.connect(self._on_clip_normal_changed)

        self.ui.button_geometry_add.clicked.connect(self._on_add_clicked)

        self.ui.button_geometry_remove.clicked.connect(self._on_remove_clicked)

        self.ui.button_geometry_reset.clicked.connect(self._on_reset_clicked)

        self.ui.button_geometry_apply.clicked.connect(self._on_set_apply_clicked)

        self.ui.button_geometry_cancel.clicked.connect(self._on_cancel_clicked)

        self.ui.button_geometry_apply.setText("Position Picking Mode")

        self.ui.button_geometry_apply.setEnabled(False)

        self.ui.button_geometry_cancel.hide()

        self.ui.button_geometry_reset.hide()

        self.tree.widget.header().setVisible(False)

        self.tree.widget.itemSelectionChanged.connect(self._on_tree_selection_changed)

        if self.vtk_pre:

            self.vtk_pre.obj_manager.selection_changed.connect(self._on_vtk_selection_changed)

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

        for i in range(self.tree.widget.topLevelItemCount()):

            item = self.tree.widget.topLevelItem(i)

            if item and item.text(0) == name:

                item.setText(1, self.ICON_VISIBLE if visible else self.ICON_HIDDEN)

                break

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

        for i in range(self.tree.widget.topLevelItemCount()):

            item = self.tree.widget.topLevelItem(i)

            if item and item.text(0) == name:

                item.setText(1, self.ICON_VISIBLE if visible else self.ICON_HIDDEN)

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

        model_path = Path(self.case_data.path) / "1.model_Mhead" / "scale0"

        model_path.mkdir(parents=True, exist_ok=True)

        copied_files = []

        for f in add_files:

            src_file = Path(f)

            dst_file = model_path / src_file.name

            import shutil

            try:

                shutil.copy2(src_file, dst_file)

            except Exception:

                traceback.print_exc()

                continue

            name = dst_file.stem

            self.case_data.add_geometry(dst_file)

            tree_names = [
                self.tree.widget.topLevelItem(i).text(0)
                for i in range(self.tree.widget.topLevelItemCount())
            ]

            if name not in tree_names:

                self._add_tree_item_with_visibility(name, visible=True)

            copied_files.append(str(dst_file))

        if self.vtk_pre and copied_files:

            self._start_async_loading(copied_files)

        else:

            self.case_data.save()

    def _start_async_loading(self, files: list):

        self._loading_total = len(files)

        if self.vtk_pre:

            self.vtk_pre.show_progress(
                f"Loading geometry... (0/{len(files)})", value=0, maximum=len(files)
            )

        self._loading_signals_connected = True

        self.mesh_loader.file_loaded.connect(self._on_file_loaded)

        self.mesh_loader.progress.connect(self._on_loading_progress)

        self.mesh_loader.all_finished.connect(self._on_loading_finished)

        self.mesh_loader.error.connect(self._on_loading_error)

        self.mesh_loader.load_async(files)

    def _on_file_loaded(self, file_path: str, name: str, actor):

        if self.vtk_pre and actor:

            self.vtk_pre.obj_manager.add(actor, name=name, group="geometry")

            bounds = actor.GetBounds()

            center_x = (bounds[0] + bounds[1]) / 2

            center_y = (bounds[2] + bounds[3]) / 2

            center_z = (bounds[4] + bounds[5]) / 2

            dx = bounds[1] - bounds[0]

            dy = bounds[3] - bounds[2]

            dz = bounds[5] - bounds[4]

            if dx < 1e-6 or dy < 1e-6 or dz < 1e-6:

                self._flat_geometries.add(name)

            existing = self.case_data.get_geometry_probe_position(name)

            if not existing or existing == (0.0, 0.0, 0.0):

                self.case_data.set_geometry_probe_position(name, center_x, center_y, center_z)

    def _on_loading_progress(self, current: int, total: int):

        try:

            if self.vtk_pre:

                self.vtk_pre.update_progress(
                    current, label=f"Loading geometry... ({current}/{total})"
                )

        except (RuntimeError, AttributeError):

            pass

    def _on_loading_error(self, file_path: str, error_msg: str):

        pass

    def _on_loading_canceled(self):

        self.mesh_loader.cancel_async()

        self._cleanup_loading_signals()

        if self.vtk_pre:

            self.vtk_pre.hide_progress()

    def _on_loading_finished(self):

        if self.vtk_pre:

            self.vtk_pre.hide_progress()

        self._cleanup_loading_signals()

        if self.vtk_pre:

            self._apply_saved_transforms()

            self._update_fluid_probe_position()

            current_page = self.parent.ui.stackedWidget.currentWidget()

            is_geometry_tab = (current_page == self.parent.ui.page_geometry)

            all_objs = self.vtk_pre.obj_manager.get_all()

            for obj in all_objs:

                if hasattr(obj, 'group') and obj.group == "geometry":

                    obj.actor.SetVisibility(is_geometry_tab)

            if is_geometry_tab:

                self.vtk_pre.show_clip_actors_for_group("geometry")

            else:

                self.vtk_pre.hide_clip_actors_for_group("geometry")

            if is_geometry_tab:

                self.vtk_pre.camera.fit()

            self.vtk_pre.vtk_widget.GetRenderWindow().Render()

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

            position = self.case_data.get_geometry_position(obj.name)

            rotation = self.case_data.get_geometry_rotation(obj.name)

            if position or rotation:

                x, y, z = position if position else (0.0, 0.0, 0.0)

                rx, ry, rz = rotation if rotation else (0.0, 0.0, 0.0)

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

        selected_items = self.tree.widget.selectedItems()

        if not selected_items:

            return

        names_to_remove = []

        for item in selected_items:

            name = item.text(0)

            if name != "fluid":

                names_to_remove.append(name)

        if not names_to_remove:

            return

        model_path = Path(self.case_data.path) / "1.model_Mhead" / "scale0"

        for obj_name in names_to_remove:

            for i in range(self.tree.widget.topLevelItemCount()):

                item = self.tree.widget.topLevelItem(i)

                if item and item.text(0) == obj_name:

                    self.tree.widget.takeTopLevelItem(i)

                    break

            if self.vtk_pre:

                obj = self.vtk_pre.obj_manager.find_by_name(obj_name)

                if obj:

                    self.vtk_pre.obj_manager.remove(obj.id)

            stl_file = model_path / f"{obj_name}.stl"

            if stl_file.exists():

                try:

                    stl_file.unlink()

                except Exception:

                    traceback.print_exc()

            self.case_data.remove_geometry(obj_name)

            if obj_name in self._visibility_state:

                del self._visibility_state[obj_name]

        if self.vtk_pre:

            self.vtk_pre.vtk_widget.GetRenderWindow().Render()

        self.case_data.save()

    def _on_set_apply_clicked(self):

        current_text = self.ui.button_geometry_apply.text()

        if current_text == "Position Picking Mode":

            if self.vtk_pre:

                self._saved_view_style = self.vtk_pre._current_view_style

            if self.vtk_pre:

                probe_tool = self.vtk_pre._optional_tools.get("point_probe")

                if probe_tool:

                    pos = self.tree.get_current_pos()

                    if pos is not None:

                        obj_name = self.tree.get_text(pos)

                        if obj_name == "fluid":

                            self.vtk_pre.obj_manager.blockSignals(True)

                            self.vtk_pre.obj_manager.clear_selection()

                            self.vtk_pre.obj_manager.blockSignals(False)

                            bounds = self._get_combined_geometry_bounds()

                            if bounds is None:

                                return

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

                        scale = 1.4

                        probe_box_size = tuple(s * scale for s in obj_size)

                        probe_pos = self.case_data.get_geometry_probe_position(obj_name)

                        if not probe_pos or probe_pos == (0.0, 0.0, 0.0):

                            probe_pos = (
                                (bounds[0] + bounds[1]) / 2,
                                (bounds[2] + bounds[3]) / 2,
                                (bounds[4] + bounds[5]) / 2
                            )

                        if probe_tool.is_visible:

                            probe_tool.hide()

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

                        if hasattr(probe_tool, '_rep'):

                            probe_tool._rep.PlaceWidget(new_bounds)

                        from vtkmodules.vtkCommonTransforms import vtkTransform

                        probe_tool._saved_bounds = new_bounds

                        probe_tool._saved_transform = vtkTransform()

                        if obj_name == "fluid":

                            probe_tool._saved_selection_ids = set()

                        else:

                            probe_tool._saved_selection_ids = self.vtk_pre.obj_manager.selected_ids.copy()

                        probe_tool.show()

                        if hasattr(probe_tool, '_rep'):

                            verify_bounds = probe_tool._rep.GetBounds()

                            verify_size = (
                                verify_bounds[1] - verify_bounds[0],
                                verify_bounds[3] - verify_bounds[2],
                                verify_bounds[5] - verify_bounds[4]
                            )

                        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

            if self.vtk_pre:
                self._saved_projection = self.vtk_pre.camera.is_parallel_projection()
                if not self._saved_projection:
                    self.vtk_pre.camera.set_parallel_projection(True)
                    self.vtk_pre._projection_action.setChecked(True)
                self.vtk_pre.fit_to_scene()
                self.vtk_pre.escape_pressed.connect(self._on_cancel_clicked)

            self.ui.button_geometry_apply.setText("Apply")

            self.ui.button_geometry_cancel.show()

            self.ui.button_geometry_reset.show()

        elif current_text == "Apply":

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

                    probe_tool.hide()

                    self._set_geometry_opacity(1.0)

                    self.ui.button_geometry_apply.setText("Position Picking Mode")

                    self.ui.button_geometry_cancel.hide()

                    self.ui.button_geometry_reset.hide()

                    if self.vtk_pre and hasattr(self, '_saved_projection'):
                        if not self._saved_projection:
                            self.vtk_pre.camera.set_parallel_projection(False)
                            self.vtk_pre._projection_action.setChecked(False)
                        try:
                            self.vtk_pre.escape_pressed.disconnect(self._on_cancel_clicked)
                        except RuntimeError:
                            pass

                    if self.vtk_pre and hasattr(self, '_saved_view_style') and self._saved_view_style:

                        self.vtk_pre.set_visibility_mode(self.vtk_pre._visibility_mode, apply_visibility=False)

                        self.vtk_pre.obj_manager.all().style(self._saved_view_style)

                        self.vtk_pre._view_combo.setCurrentText(self._saved_view_style)

                    if probe_center:

                        self._show_probe_marker(*probe_center)

    def _on_cancel_clicked(self):

        if self.vtk_pre:

            probe_tool = self.vtk_pre._optional_tools.get("point_probe")

            if probe_tool:

                pos = self.tree.get_current_pos()

                if pos is not None:

                    obj_name = self.tree.get_text(pos)

                    probe_pos = self.case_data.get_geometry_probe_position(obj_name)

                    if probe_pos and probe_pos != (0.0, 0.0, 0.0):

                        x, y, z = probe_pos

                    else:

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

                    self.ui.edit_input_position_x.setText(f"{x:.4f}")

                    self.ui.edit_input_position_y.setText(f"{y:.4f}")

                    self.ui.edit_input_position_z.setText(f"{z:.4f}")

                probe_tool.hide()

                self._set_geometry_opacity(1.0)

                self.ui.button_geometry_apply.setText("Position Picking Mode")

                self.ui.button_geometry_cancel.hide()

                self.ui.button_geometry_reset.hide()

                if self.vtk_pre and hasattr(self, '_saved_projection'):
                    if not self._saved_projection:
                        self.vtk_pre.camera.set_parallel_projection(False)
                        self.vtk_pre._projection_action.setChecked(False)
                    try:
                        self.vtk_pre.escape_pressed.disconnect(self._on_cancel_clicked)
                    except RuntimeError:
                        pass

                if self.vtk_pre and hasattr(self, '_saved_view_style') and self._saved_view_style:

                    self.vtk_pre.obj_manager.all().style(self._saved_view_style)

                    self.vtk_pre._view_combo.setCurrentText(self._saved_view_style)

                self._show_probe_marker(x, y, z)

    def _on_reset_clicked(self):

        pos = self.tree.get_current_pos()

        if pos is None:

            return

        obj_name = self.tree.get_text(pos)

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

                self.ui.edit_input_position_x.setText(f"{center_x:.4f}")

                self.ui.edit_input_position_y.setText(f"{center_y:.4f}")

                self.ui.edit_input_position_z.setText(f"{center_z:.4f}")

                probe_tool = self.vtk_pre._optional_tools.get("point_probe")

                if probe_tool and probe_tool.is_visible:

                    obj_size = (
                        bounds[1] - bounds[0],
                        bounds[3] - bounds[2],
                        bounds[5] - bounds[4]
                    )

                    scale = 1.4

                    half_size_x = (obj_size[0] * scale) / 2

                    half_size_y = (obj_size[1] * scale) / 2

                    half_size_z = (obj_size[2] * scale) / 2

                    new_bounds = [
                        center_x - half_size_x,
                        center_x + half_size_x,
                        center_y - half_size_y,
                        center_y + half_size_y,
                        center_z - half_size_z,
                        center_z + half_size_z
                    ]

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

        self._sync_vtk_selection(selected_names)

        if "fluid" in selected_names:

            self.ui.button_geometry_remove.setEnabled(False)

        else:

            self.ui.button_geometry_remove.setEnabled(True)

        if selected_count == 0:

            self._restore_all_opacity()

            self.ui.edit_input_position_x.setText("0")

            self.ui.edit_input_position_y.setText("0")

            self.ui.edit_input_position_z.setText("0")

            self.ui.AdvancedGroupBox.setEnabled(True)

            self.ui.button_geometry_apply.setEnabled(False)

            self._hide_probe_marker()

        elif selected_count == 1:

            self.ui.AdvancedGroupBox.setEnabled(True)

            sel_name = selected_names[0]

            if sel_name in self._flat_geometries:

                self.ui.button_geometry_apply.setEnabled(False)

            elif sel_name == "fluid" and self._get_combined_geometry_bounds() is None:

                self.ui.button_geometry_apply.setEnabled(False)

            else:

                self.ui.button_geometry_apply.setEnabled(True)

            self._highlight_object(selected_names[0])

            if self.vtk_pre:

                obj = self.vtk_pre.obj_manager.find_by_name(selected_names[0])

                if obj:

                    bounds = obj.actor.GetBounds()

                    obj_size = (
                        bounds[1] - bounds[0],
                        bounds[3] - bounds[2],
                        bounds[5] - bounds[4]
                    )

            probe_tool = None

            if self.vtk_pre:

                probe_tool = self.vtk_pre._optional_tools.get("point_probe")

            probe_pos = self.case_data.get_geometry_probe_position(selected_names[0])

            if probe_pos is not None:

                x, y, z = probe_pos

                is_picking = (self.ui.button_geometry_apply.text() == "Apply")

                is_flat = selected_names[0] in self._flat_geometries

                if not is_picking and not is_flat:

                    self._show_probe_marker(x, y, z)

                else:

                    self._hide_probe_marker()

                self.ui.edit_input_position_x.setText(f"{x:.4f}")

                self.ui.edit_input_position_y.setText(f"{y:.4f}")

                self.ui.edit_input_position_z.setText(f"{z:.4f}")

                if probe_tool and probe_tool.is_visible:

                    if self.ui.button_geometry_apply.text() != "Apply":

                        probe_tool.set_center(*probe_pos)

            else:

                self._hide_probe_marker()

                position = self.case_data.get_geometry_position(selected_names[0])

                if position:

                    x, y, z = position

                    self.ui.edit_input_position_x.setText(f"{x:.4f}")

                    self.ui.edit_input_position_y.setText(f"{y:.4f}")

                    self.ui.edit_input_position_z.setText(f"{z:.4f}")

                else:

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

            self.ui.edit_input_position_x.setText("")

            self.ui.edit_input_position_y.setText("")

            self.ui.edit_input_position_z.setText("")

            self.ui.AdvancedGroupBox.setEnabled(False)

            self.ui.button_geometry_apply.setEnabled(False)

            self._hide_probe_marker()

            for name in selected_names:

                pos = self.case_data.get_geometry_probe_position(name)

                if pos is not None:

                    self._add_probe_marker(*pos)

    def _highlight_object(self, obj_name: str):

        pass

    def _highlight_multiple_objects(self, obj_names: list):

        pass

    def _restore_all_opacity(self):

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

        obj_manager = self.vtk_pre.obj_manager

        obj_manager.blockSignals(True)

        selected_ids = []

        for name in selected_names:

            obj = obj_manager.find_by_name(name)

            if obj:

                selected_ids.append(obj.id)

        if not selected_ids:

            if selected_names:

                obj_manager.fade_all()

            else:

                obj_manager.clear_selection()

        else:

            obj_manager.select_multiple(selected_ids)

        obj_manager.blockSignals(False)

        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    def _on_vtk_selection_changed(self, info: dict):

        selected_objects = info.get("selected_objects", [])

        selected_names = [obj["name"] for obj in selected_objects]

        selected_count = len(selected_names)

        self.tree.widget.blockSignals(True)

        self.tree.widget.clearSelection()

        for i in range(self.tree.widget.topLevelItemCount()):

            item = self.tree.widget.topLevelItem(i)

            if item and item.text(0) in selected_names:

                item.setSelected(True)

        self.tree.widget.blockSignals(False)

        if selected_count == 0:

            self._restore_all_opacity()

            self.ui.edit_input_position_x.setText("0")

            self.ui.edit_input_position_y.setText("0")

            self.ui.edit_input_position_z.setText("0")

            self.ui.AdvancedGroupBox.setEnabled(True)

            self.ui.button_geometry_apply.setEnabled(False)

            self._hide_probe_marker()

        elif selected_count == 1:

            self.ui.AdvancedGroupBox.setEnabled(True)

            sel_name = selected_names[0]

            if sel_name in self._flat_geometries:

                self.ui.button_geometry_apply.setEnabled(False)

            elif sel_name == "fluid" and self._get_combined_geometry_bounds() is None:

                self.ui.button_geometry_apply.setEnabled(False)

            else:

                self.ui.button_geometry_apply.setEnabled(True)

            self._highlight_object(selected_names[0])

            if self.vtk_pre:

                obj = self.vtk_pre.obj_manager.find_by_name(selected_names[0])

                if obj:

                    bounds = obj.actor.GetBounds()

                    obj_size = (
                        bounds[1] - bounds[0],
                        bounds[3] - bounds[2],
                        bounds[5] - bounds[4]
                    )

            probe_tool = None

            if self.vtk_pre:

                probe_tool = self.vtk_pre._optional_tools.get("point_probe")

            probe_pos = self.case_data.get_geometry_probe_position(selected_names[0])

            if probe_pos is not None:

                x, y, z = probe_pos

                is_picking = (self.ui.button_geometry_apply.text() == "Apply")

                is_flat = selected_names[0] in self._flat_geometries

                if not is_picking and not is_flat:

                    self._show_probe_marker(x, y, z)

                else:

                    self._hide_probe_marker()

                self.ui.edit_input_position_x.setText(f"{x:.4f}")

                self.ui.edit_input_position_y.setText(f"{y:.4f}")

                self.ui.edit_input_position_z.setText(f"{z:.4f}")

                if probe_tool and probe_tool.is_visible:

                    if self.ui.button_geometry_apply.text() != "Apply":

                        probe_tool.set_center(*probe_pos)

            else:

                self._hide_probe_marker()

                position = self.case_data.get_geometry_position(selected_names[0])

                if position:

                    x, y, z = position

                    self.ui.edit_input_position_x.setText(f"{x:.4f}")

                    self.ui.edit_input_position_y.setText(f"{y:.4f}")

                    self.ui.edit_input_position_z.setText(f"{z:.4f}")

                else:

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

            self.ui.edit_input_position_x.setText("")

            self.ui.edit_input_position_y.setText("")

            self.ui.edit_input_position_z.setText("")

            self.ui.AdvancedGroupBox.setEnabled(False)

            self.ui.button_geometry_apply.setEnabled(False)

            self._hide_probe_marker()

            for name in selected_names:

                pos = self.case_data.get_geometry_probe_position(name)

                if pos is not None:

                    self._add_probe_marker(*pos)

    def _on_probe_visibility_changed(self, is_visible: bool):

        if is_visible:

            self._hide_probe_marker()

            self.tree.widget.setEnabled(False)

            self.ui.button_geometry_add.setEnabled(False)

            self.ui.button_geometry_remove.setEnabled(False)

        else:

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

    def _add_probe_marker(self, x: float, y: float, z: float):

        """빨간 구를 하나 추가한다 (기존 마커 유지). 다중 선택 지원."""

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

        actor.GetProperty().SetColor(1.0, 0.1, 0.1)

        actor.GetProperty().SetOpacity(0.85)

        self.vtk_pre.renderer.AddActor(actor)

        self._probe_marker_actors.append(actor)

        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    def _show_probe_marker(self, x: float, y: float, z: float):

        """기존 마커를 모두 지우고 빨간 구 하나를 표시한다 (단일 선택용)."""

        self._hide_probe_marker()

        self._add_probe_marker(x, y, z)

    def _hide_probe_marker(self):

        """모든 빨간 구 마커를 제거한다."""

        if not self.vtk_pre:

            self._probe_marker_actors.clear()

            return

        for actor in self._probe_marker_actors:

            try:

                self.vtk_pre.renderer.RemoveActor(actor)

            except Exception:

                pass

        if self._probe_marker_actors:

            self.vtk_pre.vtk_widget.GetRenderWindow().Render()

        self._probe_marker_actors.clear()

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

            self._clip_flip_btn.setChecked(True)

            self._clip_flip_btn.blockSignals(False)

        if is_clipping:

            self._clip_slider.blockSignals(True)

            self._clip_slider.setValue(50)

            self._clip_slider.blockSignals(False)

            if hasattr(self, '_lbl_pos_value'):

                self._lbl_pos_value.setText("50%")

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

            self._clip_flip_btn.setChecked(True)

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

        self._add_tree_item_with_visibility("fluid", visible=True)

        if not self.case_data.get_geometry("fluid"):

            from common.case_data import GeometryData

            self.case_data.objects["fluid"] = GeometryData(
                name="fluid", path="", is_visible=True
            )

        model_path = Path(self.case_data.path) / "1.model_Mhead" / "scale0"

        if not model_path.exists():

            return

        stl_files = []

        for stl_file in model_path.glob("*.stl"):

            if stl_file.name.lower() != "mesh.stl":

                stl_files.append(stl_file)

        if not stl_files:

            return

        for stl_file in stl_files:

            name = stl_file.stem

            if name != "fluid":

                self._add_tree_item_with_visibility(name, visible=True)

            if not self.case_data.get_geometry(name):

                self.case_data.add_geometry(stl_file)

        if self.vtk_pre and stl_files:

            self._start_async_loading([str(f) for f in stl_files])

        else:

            self.case_data.save()

