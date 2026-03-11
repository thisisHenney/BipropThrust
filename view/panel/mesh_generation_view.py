
import sys

import subprocess

import math

import re

import traceback

from datetime import datetime

from pathlib import Path

import vtk

from PySide6.QtCore import QThread, Qt, Signal, QTimer

from PySide6.QtWidgets import (
    QToolBar,
    QLabel,
    QComboBox,
    QSlider,
    QPushButton,
    QDoubleSpinBox,
    QMessageBox,
)

from nextlib.openfoam.PyFoamCase.foamfile import FoamFile

from common.app_data import app_data

from common.case_data import case_data

class PrepareMeshThread(QThread):

    finished_success = Signal()

    finished_error = Signal(str)

    def __init__(self, view, cells_x, cells_y, cells_z, bounds=None):

        super().__init__()

        self.view = view

        self.cells_x = cells_x

        self.cells_y = cells_y

        self.cells_z = cells_z

        self.bounds = bounds

    def run(self):

        try:

            if not self.view._update_blockmesh_dict(self.cells_x, self.cells_y, self.cells_z, bounds=self.bounds):

                self.finished_error.emit("Failed to update blockMeshDict")

                return

            if not self.view._update_snappyhex_dict():

                self.finished_error.emit("Failed to update snappyHexMeshDict locations")

                return

            if not self.view._update_surface_feature_extract_dict():

                self.finished_error.emit("Failed to update surfaceFeatureExtractDict")

                return

            if not self.view._update_castellation_settings():

                self.finished_error.emit("Failed to update castellation settings")

                return

            if not self.view._update_snap_settings():

                self.finished_error.emit("Failed to update snap settings")

                return

            if not self.view._update_boundary_layer_settings():

                self.finished_error.emit("Failed to update boundary layer settings")

                return

            self.finished_success.emit()

        except Exception as e:

            self.finished_error.emit(f"Unexpected error: {str(e)}")

class MeshGenerationView:

    def __init__(self, parent):

        self.parent = parent

        self.ui = self.parent.ui

        self.ctx = self.parent.context

        self.exec_widget = self.ctx.get("exec")

        self.vtk_pre = self.ctx.get("vtk_pre")

        self.app_data = app_data

        self.case_data = case_data

        self.foam_reader = None

        self.geom_output = None

        self.bounds = None

        self.center = None

        self.diagonal_length = None

        self.surface_actor = None

        self.clip_plane = None

        self.clip_actor = None

        self._clip_flip = True

        self._clip_clip_filter = None

        self._clip_geom_filter = None

        self._clip_preview_actor = None

        self._slice_update_timer = QTimer()

        self._slice_update_timer.setSingleShot(True)

        self._slice_update_timer.setInterval(150)

        self._slice_update_timer.timeout.connect(self.update_slice)

        self.slice_widget = self._create_slice_widget()

        self._init_connect()

    def _init_connect(self):

        self.ui.button_mesh_generate.clicked.connect(self._on_generate_clicked)

        self.ui.button_mesh_stop.clicked.connect(self._on_mesh_stop_clicked)

        self.ui.button_edit_hostfile_mesh.clicked.connect(self._on_edit_hostfile_clicked)

        self.ui.checkBox_host_1.toggled.connect(self._on_hostfile_mesh_toggled)

        self.ui.button_mesh_stop.setEnabled(False)

        self.combo_dir.currentTextChanged.connect(self._on_clip_dir_changed)

        self.slider_pos.valueChanged.connect(self._on_slider_changed)

        self.slider_pos.sliderReleased.connect(self._on_slider_released)

        self.clip_flip_btn.toggled.connect(self._on_clip_flip_toggled)

        self.clip_reset_btn.clicked.connect(self._on_clip_reset_clicked)

        self.spin_nx.valueChanged.connect(self._request_slice_update)

        self.spin_ny.valueChanged.connect(self._request_slice_update)

        self.spin_nz.valueChanged.connect(self._request_slice_update)

    def _create_slice_widget(self):

        if not self.vtk_pre:

            return None

        clip_toolbar = QToolBar("Clip Controls", self.vtk_pre)

        clip_toolbar.setObjectName("vtkBottomBar")

        clip_toolbar.setFloatable(True)

        clip_toolbar.setMovable(True)

        clip_toolbar.addWidget(QLabel("Clip:"))

        self.combo_dir = QComboBox()

        self.combo_dir.addItems(["Off", "X", "Y", "Z", "Custom"])

        self.combo_dir.setCurrentText("Off")

        self.combo_dir.setFixedWidth(70)

        clip_toolbar.addWidget(self.combo_dir)

        clip_toolbar.addWidget(QLabel(" n=("))

        self.spin_nx = QDoubleSpinBox()

        self.spin_nx.setRange(-1.0, 1.0)

        self.spin_nx.setSingleStep(0.1)

        self.spin_nx.setValue(1.0)

        self.spin_nx.setMaximumWidth(60)

        self.spin_nx.setEnabled(False)

        clip_toolbar.addWidget(self.spin_nx)

        clip_toolbar.addWidget(QLabel(","))

        self.spin_ny = QDoubleSpinBox()

        self.spin_ny.setRange(-1.0, 1.0)

        self.spin_ny.setSingleStep(0.1)

        self.spin_ny.setValue(0.0)

        self.spin_ny.setMaximumWidth(60)

        self.spin_ny.setEnabled(False)

        clip_toolbar.addWidget(self.spin_ny)

        clip_toolbar.addWidget(QLabel(","))

        self.spin_nz = QDoubleSpinBox()

        self.spin_nz.setRange(-1.0, 1.0)

        self.spin_nz.setSingleStep(0.1)

        self.spin_nz.setValue(0.0)

        self.spin_nz.setMaximumWidth(60)

        self.spin_nz.setEnabled(False)

        clip_toolbar.addWidget(self.spin_nz)

        clip_toolbar.addWidget(QLabel(")"))

        clip_toolbar.addWidget(QLabel(" Pos:"))

        self.slider_pos = QSlider(Qt.Horizontal)

        self.slider_pos.setRange(0, 100)

        self.slider_pos.setValue(50)

        self.slider_pos.setMinimumWidth(200)

        self.slider_pos.setEnabled(False)

        clip_toolbar.addWidget(self.slider_pos)

        self.lbl_pos_value = QLabel("50%")

        self.lbl_pos_value.setMinimumWidth(40)

        clip_toolbar.addWidget(self.lbl_pos_value)

        self.clip_flip_btn = QPushButton("Flip")

        self.clip_flip_btn.setFixedWidth(50)

        self.clip_flip_btn.setCheckable(True)

        self.clip_flip_btn.setEnabled(False)

        clip_toolbar.addWidget(self.clip_flip_btn)

        self.clip_reset_btn = QPushButton("Reset")

        self.clip_reset_btn.setFixedWidth(60)

        self.clip_reset_btn.setEnabled(False)

        clip_toolbar.addWidget(self.clip_reset_btn)

        clip_toolbar.hide()

        self.vtk_pre.addToolBar(Qt.BottomToolBarArea, clip_toolbar)

        return clip_toolbar

    def _on_hostfile_mesh_toggled(self, checked: bool):

        self.app_data.parallel_mesh_enabled = checked

        self.ui.button_edit_hostfile_mesh.setEnabled(checked)

    def _on_mesh_stop_clicked(self):

        if self.exec_widget:

            self.exec_widget.stop_process(kill=True)

        self.ui.button_mesh_generate.setEnabled(True)

        self.ui.button_mesh_generate.setText("Generate Mesh")

        self.ui.button_mesh_stop.setEnabled(False)

        self.ui.button_run.setEnabled(True)

        self.ui.button_stop.setEnabled(False)

        self.ui.edit_run_status.setText("Stopped")

        self.ui.edit_run_finished.setText(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def _highlight_error_widget(self, widget):

        from PySide6.QtWidgets import QScrollArea

        if not hasattr(self, '_error_highlighted_widget'):

            self._error_highlighted_widget = None

            self._error_original_style = ""

        self._error_highlighted_widget = widget

        self._error_original_style = widget.styleSheet()

        widget.setStyleSheet("border: 2px solid #ff4444; border-radius: 3px;")

        parent = widget.parent()

        while parent is not None:

            if isinstance(parent, QScrollArea):

                parent.ensureWidgetVisible(widget, 50, 50)

                break

            parent = parent.parent()

        widget.setFocus()

        widget.selectAll()

    def _clear_error_highlight(self):

        if hasattr(self, '_error_highlighted_widget') and self._error_highlighted_widget:

            self._error_highlighted_widget.setStyleSheet("")

            self._error_highlighted_widget.style().unpolish(self._error_highlighted_widget)

            self._error_highlighted_widget.style().polish(self._error_highlighted_widget)

            self._error_highlighted_widget.update()

            self._error_highlighted_widget = None

            self._error_original_style = ""

    def _on_edit_hostfile_clicked(self):

        hosts_path = Path(self.case_data.path) / "2.meshing_MheadBL" / "system" / "hosts"

        if not hosts_path.exists():

            hosts_path.parent.mkdir(parents=True, exist_ok=True)

            hosts_path.touch()

        try:

            if sys.platform == "win32":

                import os

                os.startfile(str(hosts_path))

            else:

                subprocess.Popen(["xdg-open", str(hosts_path)])

        except Exception:

            traceback.print_exc()

    def _on_generate_clicked(self):

        import os

        self._clear_error_highlight()

        try:

            n_procs = int(self.ui.edit_number_of_subdomains.text())

            cpu_count = os.cpu_count() or 1

            if n_procs > cpu_count:

                self._highlight_error_widget(self.ui.edit_number_of_subdomains)

                QMessageBox.critical(
                    self.parent,
                    "Error",
                    f"Number of Subdomains ({n_procs}) exceeds available CPU count ({cpu_count}).\n\n"
                    f"Please reduce the value to {cpu_count} or less."
                )

                return

        except (ValueError, AttributeError):

            pass

        self.ui.button_mesh_generate.setEnabled(False)

        self.ui.button_mesh_generate.setText("Preparing...")

        self.ui.button_run.setEnabled(False)

        self.ui.edit_run_name.setText("Mesh Generation")

        self.ui.edit_run_status.setText("Preparing...")

        self.ui.edit_run_started.setText(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        self.ui.edit_run_finished.setText("-")

        self._clear_existing_mesh()

        self._clear_mesh_files()

        x = self.ui.lineEdit_basegrid_x.text() or "100"

        y = self.ui.lineEdit_basegrid_y.text() or "100"

        z = self.ui.lineEdit_basegrid_z.text() or "100"

        geom_bounds = None

        if self.vtk_pre:

            all_objs = self.vtk_pre.obj_manager.get_all()

            geom_objects = [obj for obj in all_objs if hasattr(obj, 'group') and obj.group == "geometry"]

            if geom_objects:

                raw = [float('inf'), float('-inf'),
                       float('inf'), float('-inf'),
                       float('inf'), float('-inf')]

                for obj in geom_objects:

                    ob = obj.actor.GetBounds()

                    raw[0] = min(raw[0], ob[0])

                    raw[1] = max(raw[1], ob[1])

                    raw[2] = min(raw[2], ob[2])

                    raw[3] = max(raw[3], ob[3])

                    raw[4] = min(raw[4], ob[4])

                    raw[5] = max(raw[5], ob[5])

                geom_bounds = tuple(raw)

        geom_view = self.parent.panel_views.get("geometry")

        self._flat_geometries = geom_view._flat_geometries if geom_view else set()

        self.prepare_thread = PrepareMeshThread(self, x, y, z, bounds=geom_bounds)

        self.prepare_thread.finished_success.connect(self._on_preparation_finished)

        self.prepare_thread.finished_error.connect(self._on_preparation_error)

        self.prepare_thread.start()

    def _clear_existing_mesh(self):

        if not self.vtk_pre:

            return

        existing_mesh = self.vtk_pre.obj_manager.find_by_name("mesh")

        if existing_mesh:

            self.vtk_pre.obj_manager.remove(existing_mesh.id)

        self._clear_slice_clip()

        self.foam_reader = None

        self.geom_output = None

        self.bounds = None

        self.center = None

        self.diagonal_length = None

        self.surface_actor = None

        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    def _clear_mesh_files(self):

        import shutil

        meshing_path = Path(self.case_data.path) / "2.meshing_MheadBL"

        polymesh_path = meshing_path / "constant" / "polyMesh"

        if polymesh_path.exists():

            shutil.rmtree(polymesh_path, ignore_errors=True)

        constant_path = meshing_path / "constant"

        if constant_path.exists():

            for item in constant_path.iterdir():

                if item.is_dir() and item.name not in ["triSurface", "extendedFeatureEdgeMesh"]:

                    shutil.rmtree(item, ignore_errors=True)

        for log_file in meshing_path.glob("log.*"):

            log_file.unlink(missing_ok=True)

        for proc_folder in meshing_path.glob("processor*"):

            if proc_folder.is_dir():

                shutil.rmtree(proc_folder, ignore_errors=True)

        for item in meshing_path.iterdir():

            if item.is_dir():

                try:

                    float(item.name)

                    shutil.rmtree(item, ignore_errors=True)

                except ValueError:

                    pass

    def _on_preparation_finished(self):

        if not self.exec_widget:

            self.ui.button_mesh_generate.setEnabled(True)

            self.ui.button_mesh_generate.setText("Generate Mesh")

            self.ui.button_mesh_stop.setEnabled(False)

            self.ui.button_run.setEnabled(True)

            self.ui.button_stop.setEnabled(False)

            self.ui.button_pause.setEnabled(False)

            self.ui.edit_run_status.setText("Ready")

            return

        meshing_path = Path(self.case_data.path) / "2.meshing_MheadBL"

        self.exec_widget.set_working_path(str(meshing_path))

        self.exec_widget.set_function_after_finished(self._on_mesh_generated)

        self.exec_widget.set_function_restore_ui(self._restore_ui)

        self.ui.button_mesh_generate.setText("Generating...")

        self.ui.edit_run_status.setText("Running...")

        self.ui.button_mesh_stop.setEnabled(True)

        self.ui.button_stop.setEnabled(True)

        n_procs = 4

        try:

            n_procs = int(self.ui.edit_number_of_subdomains.text())

        except (ValueError, AttributeError):

            pass

        decompose_dict = meshing_path / "system" / "decomposeParDict"

        if decompose_dict.exists():

            try:

                content = decompose_dict.read_text()

                new_content = re.sub(
                    r'(numberOfSubdomains\s+)\d+',
                    rf'\g<1>{n_procs}',
                    content
                )

                decompose_dict.write_text(new_content)

            except Exception:

                traceback.print_exc()

        import shutil

        tri_surface_path = meshing_path / "constant" / "triSurface"

        tri_surface_path.mkdir(parents=True, exist_ok=True)

        for geom_name in self.case_data.list_geometries():

            geom_data = self.case_data.get_geometry(geom_name)

            if geom_data and geom_data.path:

                src_path = Path(geom_data.path)

                if src_path.exists():

                    dst_path = tri_surface_path / src_path.name

                    shutil.copy2(src_path, dst_path)

        shell_wrapper = meshing_path / "shell_cmd.sh"

        shell_wrapper.write_text('#!/bin/bash\neval "$@"\n', encoding='utf-8')

        shell_wrapper.chmod(0o755)

        of_wrapper = meshing_path / "of_cmd.sh"

        of_wrapper.write_text(
            '#!/bin/bash\n'
            'source /usr/lib/openfoam/openfoam2212/etc/bashrc\n'
            '. ${WM_PROJECT_DIR}/bin/tools/RunFunctions\n'
            '. ${WM_PROJECT_DIR}/bin/tools/CleanFunctions\n'
            '"$@"\n',
            encoding='utf-8'
        )

        of_wrapper.chmod(0o755)

        log_wrapper = meshing_path / "log_cmd.sh"

        log_wrapper.write_text(
            '#!/bin/bash\n'
            'set -o pipefail\n'
            'trap "kill 0" SIGTERM SIGINT\n'
            'LOG_FILE="$1"\n'
            'shift\n'
            '"$@" 2>&1 | stdbuf -oL tee "$LOG_FILE"\n',
            encoding='utf-8'
        )

        log_wrapper.chmod(0o755)

        self._log_dir = Path(self.case_data.path) / "log" / "GenerateMesh" / datetime.now().strftime("%Y%m%d_%H%M%S")

        self._log_dir.mkdir(parents=True, exist_ok=True)

        allclean = meshing_path / "Allclean"

        allrun = meshing_path / "Allrun"

        use_hostfile = self.ui.checkBox_host_1.isChecked()

        commands = []

        if allclean.exists():

            commands.extend(self._parse_script(allclean, n_procs, use_hostfile))

        if allrun.exists():

            commands.extend(self._parse_script(allrun, n_procs, use_hostfile))

        if not commands:

            QMessageBox.warning(
                None, "Mesh Generation",
                "Allclean/Allrun files not found in:\n"
                f"{meshing_path}"
            )

            self._restore_ui()

            return

        commands = self._wrap_commands_with_logging(commands)

        self._lock_vtk_toolbars(True)

        self.exec_widget.run(commands)

    def _wrap_commands_with_logging(self, commands: list) -> list:

        logged_commands = []

        for i, cmd in enumerate(commands, 1):

            display = self._get_display_cmd(cmd)

            if cmd.startswith("./shell_cmd.sh"):

                logged_commands.append((cmd, display))

            else:

                cmd_name = self._extract_command_name(cmd)

                log_file = self._log_dir / f"{i:02d}_{cmd_name}.log"

                logged_commands.append((f"./log_cmd.sh {log_file} {cmd}", display))

        return logged_commands

    @staticmethod

    def _get_display_cmd(cmd: str) -> str:

        if cmd.startswith("./shell_cmd.sh "):

            return cmd[len("./shell_cmd.sh "):]

        if cmd.startswith("./log_cmd.sh "):

            rest = cmd[len("./log_cmd.sh "):]

            parts = rest.split(" ", 1)

            rest = parts[1] if len(parts) == 2 else rest

            if rest.startswith("./of_cmd.sh "):

                return rest[len("./of_cmd.sh "):]

            return rest

        if cmd.startswith("./of_cmd.sh "):

            return cmd[len("./of_cmd.sh "):]

        return cmd

    @staticmethod

    def _extract_command_name(cmd: str) -> str:

        stripped = cmd

        for prefix in ("./of_cmd.sh ", "./shell_cmd.sh "):

            if stripped.startswith(prefix):

                stripped = stripped[len(prefix):]

                break

        parts = stripped.split()

        if not parts:

            return "unknown"

        i = 0

        if parts[0] in ("mpirun", "mpiexec"):

            i = 1

            while i < len(parts) and parts[i].startswith("-"):

                i += 1

                if i < len(parts) and not parts[i - 1].startswith("--"):

                    i += 1

        return parts[i] if i < len(parts) else parts[0]

    def _parse_script(self, script_path: Path, n_procs: int, use_hostfile: bool = False) -> list:

        SKIP_PREFIXES = (
            '#!',
            'cd "${0%/*}"',
            '. ${WM_PROJECT_DIR',
            'cp ../',
        )

        SKIP_CONTAINS = ('constant/triSurface',)

        SHELL_CMDS = {'rm', 'cp', 'mkdir', 'mv', 'ls', 'find', 'echo'}

        commands = []

        try:

            lines = script_path.read_text(encoding='utf-8').splitlines()

        except Exception:

            return commands

        for raw_line in lines:

            line = raw_line.strip()

            if not line or line.startswith('#'):

                continue

            if any(line.startswith(p) for p in SKIP_PREFIXES):

                continue

            if any(s in line for s in SKIP_CONTAINS):

                continue

            line = re.sub(r'>\s*/dev/null.*', '', line).strip()

            line = re.sub(r'#.*$', '', line).strip()

            if not line:

                continue

            if line.startswith('runApplication '):

                line = line[len('runApplication '):]

            if line.startswith('runParallel '):

                app_and_args = line[len('runParallel '):]

                if use_hostfile:

                    line = f"mpirun -np {n_procs} --hostfile system/hosts {app_and_args} -parallel"

                else:

                    line = f"mpirun -np {n_procs} --host localhost --oversubscribe {app_and_args} -parallel"

            line = line.replace('`getNumberOfProcessors`', str(n_procs))

            line = line.replace('$(getNumberOfProcessors)', str(n_procs))

            if 'mpirun' in line:

                if use_hostfile:

                    if '--host localhost' in line:

                        line = line.replace('--host localhost --oversubscribe', '--hostfile system/hosts')

                else:

                    if '--hostfile system/hosts' in line:

                        line = line.replace('--hostfile system/hosts', '--host localhost --oversubscribe')

            first_word = line.split()[0]

            if first_word in SHELL_CMDS:

                commands.append(f"./shell_cmd.sh {line}")

            else:

                commands.append(f"./of_cmd.sh {line}")

        return commands

    def _on_preparation_error(self, error_msg: str):

        self.ui.button_mesh_generate.setEnabled(True)

        self.ui.button_mesh_generate.setText("Generate Mesh")

        self.ui.button_mesh_stop.setEnabled(False)

        self.ui.button_run.setEnabled(True)

        self.ui.button_stop.setEnabled(False)

        self.ui.button_pause.setEnabled(False)

        self.ui.edit_run_status.setText("Error")

        self.ui.edit_run_finished.setText(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def _restore_ui(self):

        self.ui.button_mesh_generate.setEnabled(True)

        self.ui.button_mesh_generate.setText("Generate Mesh")

        self.ui.button_mesh_stop.setEnabled(False)

        self.ui.button_run.setEnabled(True)

        self.ui.button_stop.setEnabled(False)

        self.ui.button_pause.setEnabled(False)

        self.ui.edit_run_status.setText("Complete")

        self.ui.edit_run_finished.setText(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        self._lock_vtk_toolbars(False)

    def _lock_vtk_toolbars(self, lock: bool):

        if not self.vtk_pre:

            return

        for toolbar in self.vtk_pre.findChildren(QToolBar):

            toolbar.setFloatable(not lock)

            toolbar.setMovable(not lock)

    def _update_blockmesh_dict(self, cells_x: str, cells_y: str, cells_z: str, bounds=None) -> bool:

        if bounds is None:

            return False

        xmin, xmax, ymin, ymax, zmin, zmax = bounds

        x_size = xmax - xmin

        y_size = ymax - ymin

        z_size = zmax - zmin

        x_margin = max(x_size * 0.1, 0.005)

        y_margin = max(y_size * 0.1, 0.005)

        z_margin = max(z_size * 0.1, 0.005)

        xmin -= x_margin

        xmax += x_margin

        ymin -= y_margin

        ymax += y_margin

        zmin -= z_margin

        zmax += z_margin

        try:

            case_path = Path(self.case_data.path) / "2.meshing_MheadBL"

            blockmesh_path = case_path / "system" / "blockMeshDict"

            if not blockmesh_path.exists():

                return False

            foam_file = FoamFile(str(blockmesh_path))

            if not foam_file.load():

                return False

            vertices = [
                [round(xmin, 2), round(ymin, 2), round(zmin, 2)],
                [round(xmax, 2), round(ymin, 2), round(zmin, 2)],
                [round(xmax, 2), round(ymax, 2), round(zmin, 2)],
                [round(xmin, 2), round(ymax, 2), round(zmin, 2)],
                [round(xmin, 2), round(ymin, 2), round(zmax, 2)],
                [round(xmax, 2), round(ymin, 2), round(zmax, 2)],
                [round(xmax, 2), round(ymax, 2), round(zmax, 2)],
                [round(xmin, 2), round(ymax, 2), round(zmax, 2)],
            ]

            if not foam_file.has_key("vertices"):

                return False

            foam_file.set_value("vertices", vertices, show_type="list")

            foam_file.set_value("scale", 1.0)

            new_cells = [int(cells_x), int(cells_y), int(cells_z)]

            foam_file.set_value('blocks[0]', new_cells, map_key='cells')

            verify_cells = foam_file.get_value('blocks[0]', map_key='cells')

            foam_file.save()

            return True

        except Exception:

            traceback.print_exc()

            return False

    def _update_snappyhex_dict(self) -> bool:

        try:

            case_path = Path(self.case_data.path) / "2.meshing_MheadBL"

            snappy_path = case_path / "system" / "snappyHexMeshDict"

            if not snappy_path.exists():

                return False

            geometries = self.case_data.list_geometries()

            if not geometries:

                return False

            with open(snappy_path, 'r', encoding='utf-8') as f:

                content = f.read()

            geometry_entries = []

            for geom_name in geometries:

                if geom_name == "fluid":

                    continue

                entry = f'''    {geom_name}.stl
    {{
        type triSurfaceMesh;
        name {geom_name};
    }}'''

                geometry_entries.append(entry)

            new_geometry_block = "geometry\n{\n"

            new_geometry_block += "\n\n".join(geometry_entries)

            new_geometry_block += "\n}"

            geometry_pattern = r'geometry\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'

            if re.search(geometry_pattern, content, re.DOTALL):

                content = re.sub(geometry_pattern, new_geometry_block, content, flags=re.DOTALL)

            feature_lines = []

            for geom_name in geometries:

                if geom_name == "fluid":

                    continue

                feature_line = f'        {{ file "{geom_name}.eMesh"; level 0; }}'

                feature_lines.append(feature_line)

            new_features_block = "features\n    (\n"

            new_features_block += "\n".join(feature_lines)

            new_features_block += "\n    );"

            features_pattern = r'^(\s*)features\s*\(\s*(?:.*?)\s*\);'

            if re.search(features_pattern, content, re.DOTALL | re.MULTILINE):

                content = re.sub(features_pattern, r'\1' + new_features_block, content, flags=re.DOTALL | re.MULTILINE)

            refinement_entries = []

            for geom_name in geometries:

                if geom_name == "fluid":

                    continue

                if geom_name == "outlet":

                    entry = f'''        {geom_name}
        {{
            level (0 0);
            patchInfo
            {{
                type patch;
            }}
        }}'''

                else:

                    entry = f'''        {geom_name}
        {{
            level (0 0);
        }}'''

                refinement_entries.append(entry)

            new_refinement_block = "refinementSurfaces\n    {\n"

            new_refinement_block += "\n\n".join(refinement_entries)

            new_refinement_block += "\n    }"

            refinement_pattern = r'refinementSurfaces\s*\{[^{}]*(?:\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}[^{}]*)*\}'

            if re.search(refinement_pattern, content, re.DOTALL):

                content = re.sub(refinement_pattern, new_refinement_block, content, flags=re.DOTALL)

            geom_view = self.parent.panel_views.get("geometry")

            flat_geoms = geom_view._flat_geometries if geom_view else getattr(self, '_flat_geometries', set())

            location_lines = []

            for geom_name in geometries:

                if geom_name != "fluid" and geom_name in flat_geoms:

                    continue

                probe_pos = self.case_data.get_geometry_probe_position(geom_name)

                if probe_pos is None:

                    probe_pos = (0.0, 0.0, 0.0)

                x, y, z = probe_pos

                location_line = f"        (( {x:.4f}  {y:.4f}  {z:.4f} ) {geom_name})"

                location_lines.append(location_line)

            new_locations_block = "    locationsInMesh\n    (\n"

            new_locations_block += "\n".join(location_lines)

            new_locations_block += "\n    );"

            locations_pattern = r'[ \t]*locationsInMesh\s*\([\s\S]*?\);'

            if re.search(locations_pattern, content):

                content = re.sub(locations_pattern, new_locations_block, content)

            with open(snappy_path, 'w', encoding='utf-8') as f:

                f.write(content)

            return True

        except Exception:

            traceback.print_exc()

            return False

    def _update_surface_feature_extract_dict(self) -> bool:

        try:

            case_path = Path(self.case_data.path) / "2.meshing_MheadBL"

            dict_path = case_path / "system" / "surfaceFeatureExtractDict"

            if not dict_path.exists():

                return False

            geometries = self.case_data.list_geometries()

            if not geometries:

                return False

            header = '''/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\\\    /   O peration     | Version:  v2112                                 |
|   \\\\  /    A nd           | Website:  www.openfoam.com                      |
|    \\\\/     M anipulation  |                                                 |
\\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      surfaceFeatureExtractDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

'''

            entries = []

            for geom_name in geometries:

                if geom_name == "fluid":

                    continue

                entry = f'''{geom_name}.stl
{{
    extractionMethod    extractFromSurface;
    includedAngle       150;
    writeFeatureEdgeMesh    yes;
    writeObj                yes;
}}
'''

                entries.append(entry)

            content = header + "\n".join(entries) + "\n// ************************************************************************* //\n"

            with open(dict_path, 'w', encoding='utf-8') as f:

                f.write(content)

            return True

        except Exception:

            traceback.print_exc()

            return False

    def _on_mesh_generated(self):

        if not self.vtk_pre:

            return

        self._switch_to_mesh_tab()

        all_objs = self.vtk_pre.obj_manager.get_all()

        geom_count = 0

        for obj in all_objs:

            if hasattr(obj, 'group') and obj.group == "geometry":

                obj.actor.SetVisibility(False)

                geom_count += 1

        self.vtk_pre.hide_clip_actors_for_group("geometry")

        self.load_mesh_async()

    def _switch_to_mesh_tab(self):

        self.ui.stackedWidget.setCurrentWidget(self.ui.page_mesh_generation)

        tree = self.ui.treeWidget

        tree.blockSignals(True)

        for i in range(tree.topLevelItemCount()):

            item = tree.topLevelItem(i)

            if item and item.text(0) == "Mesh Generation":

                tree.setCurrentItem(item)

                break

        tree.blockSignals(False)

        if self.slice_widget:

            self.slice_widget.show()

        if hasattr(self.parent, 'geometry_view') and self.parent.geometry_view:

            geom_view = self.parent.geometry_view

            if geom_view.slice_widget:

                geom_view.slice_widget.hide()

    def load_mesh_async(self):

        mesh_case_path = Path(self.case_data.path) / "2.meshing_MheadBL"

        polymesh_folder = mesh_case_path / "constant" / "polyMesh"

        if not polymesh_folder.exists() or not (polymesh_folder / "points").exists():

            return

        class MeshLoadThread(QThread):

            def __init__(self, view, case_path):

                super().__init__()

                self.view = view

                self.case_path = case_path

                self.reader = None

                self.success = False

            def run(self):

                try:

                    foam_file = self.case_path / "case.foam"

                    if not foam_file.exists():

                        foam_file.write_text("", encoding="utf-8")

                    reader = vtk.vtkOpenFOAMReader()

                    reader.SetFileName(str(foam_file))

                    if hasattr(reader, "SetCreateCellToPointOn"):

                        reader.SetCreateCellToPointOn()

                    elif hasattr(reader, "SetCreateCellToPoint"):

                        reader.SetCreateCellToPoint(1)

                    if hasattr(reader, "DecomposePolyhedraOn"):

                        reader.DecomposePolyhedraOn()

                    elif hasattr(reader, "SetDecomposePolyhedra"):

                        reader.SetDecomposePolyhedra(1)

                    reader.Update()

                    self.reader = reader

                    self.success = True

                except Exception:

                    self.success = False

        self.mesh_thread = MeshLoadThread(self, mesh_case_path)

        self.mesh_thread.finished.connect(
            lambda: self._on_openfoam_case_loaded(
                self.mesh_thread.reader if self.mesh_thread.success else None
            )
        )

        self.mesh_thread.finished.connect(self.mesh_thread.deleteLater)

        self.mesh_thread.start()

    def _on_openfoam_case_loaded(self, reader):

        if not reader or not self.vtk_pre:

            return

        try:

            self.foam_reader = reader

            self._clear_slice_clip()

            geom = vtk.vtkCompositeDataGeometryFilter()

            geom.SetInputConnection(reader.GetOutputPort())

            geom.Update()

            polydata = geom.GetOutput()

            self.geom_output = polydata

            b = polydata.GetBounds()

            self.bounds = b

            cx = 0.5 * (b[0] + b[1])

            cy = 0.5 * (b[2] + b[3])

            cz = 0.5 * (b[4] + b[5])

            self.center = (cx, cy, cz)

            dx = b[1] - b[0]

            dy = b[3] - b[2]

            dz = b[5] - b[4]

            self.diagonal_length = math.sqrt(dx * dx + dy * dy + dz * dz)

            mapper = vtk.vtkPolyDataMapper()

            mapper.SetInputData(polydata)

            mapper.ScalarVisibilityOff()

            actor = vtk.vtkActor()

            actor.SetMapper(mapper)

            prop = actor.GetProperty()

            prop.SetRepresentationToSurface()

            prop.EdgeVisibilityOn()

            prop.SetColor(0.85, 0.85, 0.90)

            prop.SetEdgeColor(0.10, 0.10, 0.40)

            prop.SetLineWidth(1.0)

            existing_mesh = self.vtk_pre.obj_manager.find_by_name("mesh")

            if existing_mesh:

                self.vtk_pre.obj_manager.remove(existing_mesh.id)

            self.vtk_pre.obj_manager.add(actor, name="mesh", group="mesh")

            self.surface_actor = actor

            current_page = self.parent.ui.stackedWidget.currentWidget()

            page_name = None

            if current_page == self.parent.ui.page_mesh_generation:

                page_name = "Mesh Generation"

                actor.SetVisibility(True)

            else:

                actor.SetVisibility(False)

            self.vtk_pre.camera.fit()

            self.vtk_pre.vtk_widget.GetRenderWindow().Render()

            if actor.GetVisibility():

                self.update_slice()

        except Exception:

            traceback.print_exc()

    def _clear_slice_clip(self):

        if not self.vtk_pre:

            return

        renderer = self.vtk_pre.vtk_widget.GetRenderWindow().GetRenderers().GetFirstRenderer()

        if self.clip_actor is not None:

            renderer.RemoveActor(self.clip_actor)

            self.clip_actor = None

        self.clip_plane = None

        self._clip_clip_filter = None

        self._clip_geom_filter = None

    def _hide_slice_clip_actors(self):

        if not self.vtk_pre:

            return

        if self.clip_actor is not None:

            self.clip_actor.SetVisibility(False)

    def _show_slice_clip_actors(self):

        if not self.vtk_pre:

            return

        if self.clip_actor is not None and self.combo_dir.currentText() != "Off":

            self.clip_actor.SetVisibility(True)

    def _get_plane_params(self):

        if self.bounds is None or self.center is None:

            return None, None

        dir_text = self.combo_dir.currentText()

        if dir_text == "Off":

            return None, None

        xmin, xmax, ymin, ymax, zmin, zmax = self.bounds

        cx, cy, cz = self.center

        t = self.slider_pos.value() / 100.0

        if dir_text == "X":

            normal = (1.0, 0.0, 0.0)

            x = xmin + t * (xmax - xmin)

            origin = (x, cy, cz)

        elif dir_text == "Y":

            normal = (0.0, 1.0, 0.0)

            y = ymin + t * (ymax - ymin)

            origin = (cx, y, cz)

        elif dir_text == "Z":

            normal = (0.0, 0.0, 1.0)

            z = zmin + t * (zmax - zmin)

            origin = (cx, cy, z)

        else:

            nx = self.spin_nx.value()

            ny = self.spin_ny.value()

            nz = self.spin_nz.value()

            length = math.sqrt(nx * nx + ny * ny + nz * nz)

            if length < 1e-6:

                nx, ny, nz = 0.0, 0.0, 1.0

                length = 1.0

            normal = (nx / length, ny / length, nz / length)

            d = self.diagonal_length if self.diagonal_length else 1.0

            s = (t - 0.5) * d

            ox = cx + s * normal[0]

            oy = cy + s * normal[1]

            oz = cz + s * normal[2]

            origin = (ox, oy, oz)

        return origin, normal

    def _on_clip_dir_changed(self, direction: str):

        is_clipping = (direction != "Off")

        is_custom = (direction == "Custom")

        self.slider_pos.setEnabled(is_clipping)

        self.clip_flip_btn.setEnabled(is_clipping)

        self.clip_reset_btn.setEnabled(is_clipping)

        self.spin_nx.setEnabled(is_custom)

        self.spin_ny.setEnabled(is_custom)

        self.spin_nz.setEnabled(is_custom)

        normals = {"X": (1, 0, 0), "Y": (0, 1, 0), "Z": (0, 0, 1)}

        if direction in normals:

            for spin, val in zip([self.spin_nx, self.spin_ny, self.spin_nz], normals[direction]):

                spin.blockSignals(True)

                spin.setValue(val)

                spin.blockSignals(False)

        if not is_clipping:

            self.slider_pos.blockSignals(True)

            self.slider_pos.setValue(50)

            self.slider_pos.blockSignals(False)

            self.lbl_pos_value.setText("50%")

        self.clip_flip_btn.blockSignals(True)

        self.clip_flip_btn.setChecked(True)

        self.clip_flip_btn.blockSignals(False)

        self._clip_flip = True

        self._request_slice_update()

    def _on_clip_flip_toggled(self, checked: bool):

        self._clip_flip = checked

        self._request_slice_update()

    def _on_clip_reset_clicked(self):

        self.clip_flip_btn.blockSignals(True)

        self.clip_flip_btn.setChecked(True)

        self.clip_flip_btn.blockSignals(False)

        self._clip_flip = True

        self.slider_pos.blockSignals(True)

        self.slider_pos.setValue(50)

        self.slider_pos.blockSignals(False)

        self.lbl_pos_value.setText("50%")

        self._request_slice_update()

    def _on_slider_changed(self, value: int):

        self.lbl_pos_value.setText(f"{value}%")

        if self.slider_pos.isSliderDown():

            self._show_clip_preview_plane()

        else:

            self._request_slice_update()

    def _on_slider_released(self):

        """슬라이더 릴리즈 시 preview 제거 후 실제 clip 적용."""

        self._remove_clip_preview_plane()

        self._request_slice_update()

    def _show_clip_preview_plane(self):

        """현재 슬라이더 위치에 빨간 반투명 평면을 표시한다 (geometry view와 동일한 방식)."""

        if not self.vtk_pre or self.bounds is None:

            return

        origin, normal = self._get_plane_params()

        if origin is None or normal is None:

            self._remove_clip_preview_plane()

            return

        try:

            import vtk as _vtk

        except ImportError:

            return

        renderer = self.vtk_pre.vtk_widget.GetRenderWindow().GetRenderers().GetFirstRenderer()

        self._remove_clip_preview_plane()

        xmin, xmax, ymin, ymax, zmin, zmax = self.bounds

        margin = 0.1

        ext_xmin = xmin - (xmax - xmin) * margin

        ext_xmax = xmax + (xmax - xmin) * margin

        ext_ymin = ymin - (ymax - ymin) * margin

        ext_ymax = ymax + (ymax - ymin) * margin

        ext_zmin = zmin - (zmax - zmin) * margin

        ext_zmax = zmax + (zmax - zmin) * margin

        ox, oy, oz = origin

        dir_text = self.combo_dir.currentText()

        plane_src = _vtk.vtkPlaneSource()

        if dir_text == "X":

            plane_src.SetOrigin(ox, ext_ymin, ext_zmin)

            plane_src.SetPoint1(ox, ext_ymax, ext_zmin)

            plane_src.SetPoint2(ox, ext_ymin, ext_zmax)

        elif dir_text == "Y":

            plane_src.SetOrigin(ext_xmin, oy, ext_zmin)

            plane_src.SetPoint1(ext_xmax, oy, ext_zmin)

            plane_src.SetPoint2(ext_xmin, oy, ext_zmax)

        elif dir_text == "Z":

            plane_src.SetOrigin(ext_xmin, ext_ymin, oz)

            plane_src.SetPoint1(ext_xmax, ext_ymin, oz)

            plane_src.SetPoint2(ext_xmin, ext_ymax, oz)

        else:

            size = (((xmax-xmin)**2 + (ymax-ymin)**2 + (zmax-zmin)**2) ** 0.5) * 1.1

            nx, ny, nz = normal

            u = (0.0, nz, -ny) if abs(nx) < 0.9 else (nz, 0.0, -nx)

            ul = (u[0]**2 + u[1]**2 + u[2]**2) ** 0.5

            u = (u[0]/ul, u[1]/ul, u[2]/ul)

            v = (ny*u[2]-nz*u[1], nz*u[0]-nx*u[2], nx*u[1]-ny*u[0])

            half = size / 2.0

            plane_src.SetOrigin(ox-u[0]*half-v[0]*half, oy-u[1]*half-v[1]*half, oz-u[2]*half-v[2]*half)

            plane_src.SetPoint1(ox+u[0]*half-v[0]*half, oy+u[1]*half-v[1]*half, oz+u[2]*half-v[2]*half)

            plane_src.SetPoint2(ox-u[0]*half+v[0]*half, oy-u[1]*half+v[1]*half, oz-u[2]*half+v[2]*half)

        plane_src.SetResolution(1, 1)

        plane_src.Update()

        mapper = _vtk.vtkPolyDataMapper()

        mapper.SetInputConnection(plane_src.GetOutputPort())

        actor = _vtk.vtkActor()

        actor.SetMapper(mapper)

        prop = actor.GetProperty()

        prop.SetColor(1.0, 0.2, 0.2)

        prop.SetOpacity(0.4)

        prop.SetRepresentationToSurface()

        prop.EdgeVisibilityOn()

        prop.SetEdgeColor(1.0, 0.0, 0.0)

        prop.SetLineWidth(2.0)

        renderer.AddActor(actor)

        self._clip_preview_actor = actor

        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    def _remove_clip_preview_plane(self):

        """빨간 반투명 preview plane을 제거한다."""

        if self._clip_preview_actor and self.vtk_pre:

            try:

                renderer = self.vtk_pre.vtk_widget.GetRenderWindow().GetRenderers().GetFirstRenderer()

                renderer.RemoveActor(self._clip_preview_actor)

            except Exception:

                pass

        self._clip_preview_actor = None

    def _request_slice_update(self):

        self._slice_update_timer.start()

    def update_slice(self):

        if self.foam_reader is None or self.geom_output is None or not self.vtk_pre:

            return

        renderer = self.vtk_pre.vtk_widget.GetRenderWindow().GetRenderers().GetFirstRenderer()

        origin, normal = self._get_plane_params()

        if origin is None or normal is None:

            if self.clip_actor is not None:

                self.clip_actor.SetVisibility(False)

            if self.surface_actor is not None:

                self.surface_actor.SetVisibility(True)

            self.vtk_pre.vtk_widget.GetRenderWindow().Render()

            return

        all_objs = self.vtk_pre.obj_manager.get_all()

        for obj in all_objs:

            if hasattr(obj, 'group') and obj.group == "geometry":

                obj.actor.SetVisibility(False)

        if self.clip_plane is None:

            self.clip_plane = vtk.vtkPlane()

        self.clip_plane.SetOrigin(*origin)

        self.clip_plane.SetNormal(*normal)

        if self.surface_actor is not None:

            self.surface_actor.SetVisibility(False)

        if self._clip_clip_filter is None:

            self._clip_clip_filter = vtk.vtkClipDataSet()

            self._clip_clip_filter.SetInputConnection(self.foam_reader.GetOutputPort())

            self._clip_geom_filter = vtk.vtkCompositeDataGeometryFilter()

            self._clip_geom_filter.SetInputConnection(self._clip_clip_filter.GetOutputPort())

        self._clip_clip_filter.SetClipFunction(self.clip_plane)

        if self._clip_flip:

            self._clip_clip_filter.InsideOutOn()

        else:

            self._clip_clip_filter.InsideOutOff()

        if self.clip_actor is None:

            clip_mapper = vtk.vtkPolyDataMapper()

            clip_mapper.SetInputConnection(self._clip_geom_filter.GetOutputPort())

            self.clip_actor = vtk.vtkActor()

            self.clip_actor.SetMapper(clip_mapper)

            prop = self.clip_actor.GetProperty()

            prop.SetRepresentationToSurface()

            prop.EdgeVisibilityOn()

            prop.SetColor(0.80, 0.80, 0.90)

            prop.SetEdgeColor(0.0, 0.0, 0.0)

            prop.SetLineWidth(1.0)

            renderer.AddActor(self.clip_actor)

        self.clip_actor.SetVisibility(True)

        all_objs = self.vtk_pre.obj_manager.get_all()

        for obj in all_objs:

            if hasattr(obj, 'group') and obj.group == "geometry":

                obj.actor.SetVisibility(False)

        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    def _load_locations_from_snappyhex(self):

        try:

            case_path = Path(self.case_data.path) / "2.meshing_MheadBL"

            snappy_path = case_path / "system" / "snappyHexMeshDict"

            if not snappy_path.exists():

                return

            with open(snappy_path, 'r', encoding='utf-8') as f:

                content = f.read()

            pattern = r'locationsInMesh\s*\(\s*(.*?)\s*\);'

            match = re.search(pattern, content, re.DOTALL)

            if not match:

                return

            locations_block = match.group(1)

            line_pattern = r'\(\s*\(\s*([+-]?[\d\.e]+)\s+([+-]?[\d\.e]+)\s+([+-]?[\d\.e]+)\s*\)\s+(\w+)\s*\)'

            loaded_count = 0

            for line_match in re.finditer(line_pattern, locations_block):

                x = float(line_match.group(1))

                y = float(line_match.group(2))

                z = float(line_match.group(3))

                region_name = line_match.group(4)

                if not self.case_data.get_geometry(region_name):

                    from common.case_data import GeometryData

                    obj = GeometryData()

                    obj.name = region_name

                    self.case_data.objects[region_name] = obj

                if self.case_data.set_geometry_probe_position(region_name, x, y, z):

                    loaded_count += 1

            if loaded_count > 0:

                self.case_data.save()

        except Exception:

            traceback.print_exc()

    def load_data(self):

        self.ui.checkBox_host_1.setChecked(self.app_data.parallel_mesh_enabled)

        self.ui.button_edit_hostfile_mesh.setEnabled(self.app_data.parallel_mesh_enabled)

        default_cells = ["100", "100", "100"]

        self._load_number_of_subdomains()

        self._load_locations_from_snappyhex()

        self._load_castellation_settings()

        self._load_snap_settings()

        self._load_boundary_layer_settings()

        self.load_mesh_async()

        try:

            case_path = Path(self.case_data.path) / "2.meshing_MheadBL"

            blockmesh_path = case_path / "system" / "blockMeshDict"

            if not blockmesh_path.exists():

                self.ui.lineEdit_basegrid_x.setText(default_cells[0])

                self.ui.lineEdit_basegrid_y.setText(default_cells[1])

                self.ui.lineEdit_basegrid_z.setText(default_cells[2])

                return

            foam_file = FoamFile(str(blockmesh_path))

            load_result = foam_file.load()

            if not load_result:

                self.ui.lineEdit_basegrid_x.setText(default_cells[0])

                self.ui.lineEdit_basegrid_y.setText(default_cells[1])

                self.ui.lineEdit_basegrid_z.setText(default_cells[2])

                return

            cells = foam_file.get_value('blocks[0]', map_key='cells')

            if cells and isinstance(cells, list) and len(cells) > 0:

                actual_cells = cells[0] if isinstance(cells[0], list) else cells

                if isinstance(actual_cells, list) and len(actual_cells) >= 3:

                    self.ui.lineEdit_basegrid_x.setText(str(actual_cells[0]))

                    self.ui.lineEdit_basegrid_y.setText(str(actual_cells[1]))

                    self.ui.lineEdit_basegrid_z.setText(str(actual_cells[2]))

                else:

                    self.ui.lineEdit_basegrid_x.setText(default_cells[0])

                    self.ui.lineEdit_basegrid_y.setText(default_cells[1])

                    self.ui.lineEdit_basegrid_z.setText(default_cells[2])

            else:

                self.ui.lineEdit_basegrid_x.setText(default_cells[0])

                self.ui.lineEdit_basegrid_y.setText(default_cells[1])

                self.ui.lineEdit_basegrid_z.setText(default_cells[2])

        except Exception:

            self.ui.lineEdit_basegrid_x.setText(default_cells[0])

            self.ui.lineEdit_basegrid_y.setText(default_cells[1])

            self.ui.lineEdit_basegrid_z.setText(default_cells[2])

    def _load_number_of_subdomains(self):

        import os

        cpu_count = os.cpu_count() or 4

        default_value = max(1, cpu_count // 2)

        decompose_dict_path = Path(self.case_data.path) / "2.meshing_MheadBL" / "system" / "decomposeParDict"

        if decompose_dict_path.exists():

            try:

                content = decompose_dict_path.read_text()

                match = re.search(r'numberOfSubdomains\s+(\d+)', content)

                if match:

                    self.ui.edit_number_of_subdomains.setText(match.group(1))

                    return

            except Exception:

                traceback.print_exc()

        self.ui.edit_number_of_subdomains.setText(str(default_value))

    def _load_castellation_settings(self):

        try:

            case_path = Path(self.case_data.path) / "2.meshing_MheadBL"

            snappy_path = case_path / "system" / "snappyHexMeshDict"

            if not snappy_path.exists():

                return

            foam_file = FoamFile(str(snappy_path))

            if not foam_file.load():

                return

            n_cells = foam_file.get_value("castellatedMeshControls.nCellsBetweenLevels")

            if n_cells is not None:

                self.ui.edit_castellation_1.setText(str(n_cells))

            angle = foam_file.get_value("castellatedMeshControls.resolveFeatureAngle")

            if angle is not None:

                self.ui.edit_castellation_2.setText(str(angle))

            geometries = [g for g in self.case_data.list_geometries() if g != "fluid"]

            if geometries:

                first_geom = geometries[0]

                level = foam_file.get_value(
                    f"castellatedMeshControls.refinementSurfaces.{first_geom}.level"
                )

                if level is not None:

                    if isinstance(level, list):

                        actual_level = level[0] if isinstance(level[0], list) else level

                        if len(actual_level) >= 2:

                            self.ui.edit_castellation_3.setText(str(actual_level[0]))

                            self.ui.edit_castellation_4.setText(str(actual_level[1]))

        except Exception:

            traceback.print_exc()

    def _update_castellation_settings(self) -> bool:

        try:

            case_path = Path(self.case_data.path) / "2.meshing_MheadBL"

            snappy_path = case_path / "system" / "snappyHexMeshDict"

            if not snappy_path.exists():

                return False

            n_cells_between_levels = int(self.ui.edit_castellation_1.text() or "2")

            resolve_feature_angle = int(self.ui.edit_castellation_2.text() or "60")

            surface_min_level = int(self.ui.edit_castellation_3.text() or "0")

            surface_max_level = int(self.ui.edit_castellation_4.text() or "0")

            foam_file = FoamFile(str(snappy_path))

            if not foam_file.load():

                return False

            foam_file.set_value(
                "castellatedMeshControls.nCellsBetweenLevels",
                n_cells_between_levels
            )

            foam_file.set_value(
                "castellatedMeshControls.resolveFeatureAngle",
                resolve_feature_angle
            )

            foam_file.save()

            self._update_refinement_surfaces_level(snappy_path, surface_min_level, surface_max_level)

            return True

        except Exception:

            traceback.print_exc()

            return False

    def _update_refinement_surfaces_level(self, snappy_path: Path, min_level: int, max_level: int):

        try:

            with open(snappy_path, 'r', encoding='utf-8') as f:

                content = f.read()

            pattern = r'(level\s*\(\s*)\d+\s+\d+(\s*\);)'

            replacement = rf'\g<1>{min_level} {max_level}\2'

            new_content = re.sub(pattern, replacement, content)

            with open(snappy_path, 'w', encoding='utf-8') as f:

                f.write(new_content)

        except Exception:

            traceback.print_exc()

    def _load_snap_settings(self):

        try:

            case_path = Path(self.case_data.path) / "2.meshing_MheadBL"

            snappy_path = case_path / "system" / "snappyHexMeshDict"

            if not snappy_path.exists():

                return

            foam_file = FoamFile(str(snappy_path))

            if not foam_file.load():

                return

            val = foam_file.get_value("snapControls.nSmoothPatch")

            if val is not None:

                self.ui.edit_snap_1.setText(str(val))

            val = foam_file.get_value("snapControls.tolerance")

            if val is not None:

                self.ui.edit_snap_2.setText(str(val))

            val = foam_file.get_value("snapControls.nSolveIter")

            if val is not None:

                self.ui.edit_snap_3.setText(str(val))

            val = foam_file.get_value("snapControls.nFeatureSnapIter")

            if val is not None:

                self.ui.edit_snap_4.setText(str(val))

        except Exception:

            traceback.print_exc()

    def _update_snap_settings(self) -> bool:

        try:

            case_path = Path(self.case_data.path) / "2.meshing_MheadBL"

            snappy_path = case_path / "system" / "snappyHexMeshDict"

            if not snappy_path.exists():

                return False

            foam_file = FoamFile(str(snappy_path))

            if not foam_file.load():

                return False

            n_smooth_patch = int(self.ui.edit_snap_1.text() or "3")

            foam_file.set_value("snapControls.nSmoothPatch", n_smooth_patch)

            tolerance = float(self.ui.edit_snap_2.text() or "2.0")

            foam_file.set_value("snapControls.tolerance", tolerance)

            n_solve_iter = int(self.ui.edit_snap_3.text() or "30")

            foam_file.set_value("snapControls.nSolveIter", n_solve_iter)

            n_feature_snap_iter = int(self.ui.edit_snap_4.text() or "5")

            foam_file.set_value("snapControls.nFeatureSnapIter", n_feature_snap_iter)

            foam_file.save()

            return True

        except Exception:

            traceback.print_exc()

            return False

    def _load_boundary_layer_settings(self):

        try:

            case_path = Path(self.case_data.path) / "2.meshing_MheadBL"

            snappy_path = case_path / "system" / "snappyHexMeshDict"

            if not snappy_path.exists():

                return

            foam_file = FoamFile(str(snappy_path))

            if not foam_file.load():

                return

            val = foam_file.get_value("addLayersControls.firstLayerThickness")

            if val is not None:

                self.ui.edit_boundary_layer_2.setText(str(val))

            val = foam_file.get_value("addLayersControls.expansionRatio")

            if val is not None:

                self.ui.edit_boundary_layer_3.setText(str(val))

            val = foam_file.get_value("addLayersControls.minThickness")

            if val is not None:

                self.ui.edit_boundary_layer_4.setText(str(val))

            val = foam_file.get_value("addLayersControls.featureAngle")

            if val is not None:

                self.ui.edit_boundary_layer_5.setText(str(val))

            val = foam_file.get_value("addLayersControls.maxFaceThicknessRatio")

            if val is not None:

                self.ui.edit_boundary_layer_6.setText(str(val))

            self._load_n_surface_layers(snappy_path)

        except Exception:

            traceback.print_exc()

    def _load_n_surface_layers(self, snappy_path: Path):

        try:

            with open(snappy_path, 'r', encoding='utf-8') as f:

                content = f.read()

            pattern = r'layers\s*\{[^}]*"fluid_to_\.\*"\s*\{[^}]*nSurfaceLayers\s+(\d+)'

            match = re.search(pattern, content, re.DOTALL)

            if match:

                val = match.group(1)

                self.ui.edit_boundary_layer_1.setText(val)

        except Exception:

            traceback.print_exc()

    def _update_boundary_layer_settings(self) -> bool:

        try:

            case_path = Path(self.case_data.path) / "2.meshing_MheadBL"

            snappy_path = case_path / "system" / "snappyHexMeshDict"

            if not snappy_path.exists():

                return False

            foam_file = FoamFile(str(snappy_path))

            if not foam_file.load():

                return False

            val = float(self.ui.edit_boundary_layer_2.text() or "0.3")

            foam_file.set_value("addLayersControls.firstLayerThickness", val)

            val = float(self.ui.edit_boundary_layer_3.text() or "1.3")

            foam_file.set_value("addLayersControls.expansionRatio", val)

            val = float(self.ui.edit_boundary_layer_4.text() or "0.1")

            foam_file.set_value("addLayersControls.minThickness", val)

            val = int(self.ui.edit_boundary_layer_5.text() or "360")

            foam_file.set_value("addLayersControls.featureAngle", val)

            val = float(self.ui.edit_boundary_layer_6.text() or "0.5")

            foam_file.set_value("addLayersControls.maxFaceThicknessRatio", val)

            foam_file.save()

            self._update_n_surface_layers(snappy_path)

            return True

        except Exception:

            traceback.print_exc()

            return False

    def _update_n_surface_layers(self, snappy_path: Path):

        try:

            n_surface_layers = int(self.ui.edit_boundary_layer_1.text() or "3")

            with open(snappy_path, 'r', encoding='utf-8') as f:

                content = f.read()

            pattern = r'(layers\s*\{[^}]*"fluid_to_\.\*"\s*\{[^}]*nSurfaceLayers\s+)\d+'

            replacement = rf'\g<1>{n_surface_layers}'

            new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

            with open(snappy_path, 'w', encoding='utf-8') as f:

                f.write(new_content)

        except Exception:

            traceback.print_exc()

