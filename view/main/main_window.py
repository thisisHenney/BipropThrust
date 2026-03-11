
import shutil

import traceback

from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QMessageBox,
    QGroupBox, QPushButton, QCheckBox, QComboBox, QProgressBar,
    QToolButton, QTextEdit, QInputDialog, QFileDialog
)

from PySide6.QtCore import Qt

from PySide6.QtGui import QAction

from view.style.theme import toggle_theme, get_current_mode, get_colors

from nextlib.widgets.dock import DockWidget

from nextlib.execute.exec_widget import ExecWidget

from nextlib.vtk import PreprocessWidget, PostprocessWidget

from nextlib.graph.pyqtgraph.residual_plot_widget import ResidualPlotWidget

from nextlib.utils.window import center_on_screen, save_window_geometry, restore_window_geometry

from nextlib.utils.file import copy_files

from nextlib.dialogbox.dialogbox import DirDialogBox

from common.app_data import app_data

from common.case_data import case_data

from common.app_context import AppContext

from view.main.menu_handler import MenuHandler

from view.main.center_widget import CenterWidget

class MainWindow(QMainWindow):

    def __init__(self, case_path: str = ""):

        super().__init__()

        self.case_path = case_path

        self.app_data = app_data

        self.case_data = case_data

        self.context = AppContext()

        self.exec_widget = None

        self.vtk_pre = None

        self.vtk_post = None

        self.residual_graph = None

        self.dock_manager = None

        self.center_widget = None

        self.menu_handler = None

        self._setup_menu()

        self._setup_components()

        self._setup_dock()

        self._setup_window()

    def _setup_menu(self) -> None:

        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")

        self.action_new = QAction("&New", self)

        self.action_new.setShortcut("Ctrl+N")

        file_menu.addAction(self.action_new)

        self.action_open = QAction("&Open...", self)

        self.action_open.setShortcut("Ctrl+O")

        file_menu.addAction(self.action_open)

        self.menu_recent = file_menu.addMenu("Open &Recent")

        self._update_recent_menu()

        self.action_save = QAction("&Save", self)

        self.action_save.setShortcut("Ctrl+S")

        self.action_save.triggered.connect(self._on_save_clicked)

        file_menu.addAction(self.action_save)

        self.action_save_as = QAction("Save &As...", self)

        self.action_save_as.setShortcut("Ctrl+Shift+S")

        file_menu.addAction(self.action_save_as)

        file_menu.addSeparator()

        self.action_exit = QAction("E&xit", self)

        self.action_exit.setShortcut("Alt+F4")

        file_menu.addAction(self.action_exit)

        run_menu = menubar.addMenu("&Run")

        self.action_run = QAction("&Run", self)

        self.action_run.setShortcut("F5")

        run_menu.addAction(self.action_run)

        self.action_stop = QAction("&Stop", self)

        run_menu.addAction(self.action_stop)

        view_menu = menubar.addMenu("&View")

        self.action_view_mesh = QAction("&Mesh", self)

        self.action_view_mesh.setCheckable(True)

        self.action_view_mesh.setChecked(True)

        self.action_view_mesh.triggered.connect(lambda checked: self._on_view_dock_toggled(2, checked))

        view_menu.addAction(self.action_view_mesh)

        self.action_view_post = QAction("&Post", self)

        self.action_view_post.setCheckable(True)

        self.action_view_post.setChecked(True)

        self.action_view_post.triggered.connect(lambda checked: self._on_view_dock_toggled(3, checked))

        view_menu.addAction(self.action_view_post)

        self.action_view_residuals = QAction("&Residuals", self)

        self.action_view_residuals.setCheckable(True)

        self.action_view_residuals.setChecked(True)

        self.action_view_residuals.triggered.connect(lambda checked: self._on_view_dock_toggled(4, checked))

        view_menu.addAction(self.action_view_residuals)

        self.action_view_log = QAction("&Log", self)

        self.action_view_log.setCheckable(True)

        self.action_view_log.setChecked(True)

        self.action_view_log.triggered.connect(lambda checked: self._on_view_dock_toggled(1, checked))

        view_menu.addAction(self.action_view_log)

        self._dock_view_actions = {
            1: self.action_view_log,
            2: self.action_view_mesh,
            3: self.action_view_post,
            4: self.action_view_residuals,
        }

        tools_menu = menubar.addMenu("&Tools")

        self.action_file_explorer = QAction("Open &File Explorer", self)

        tools_menu.addAction(self.action_file_explorer)

        self.action_terminal = QAction("Open &Terminal", self)

        tools_menu.addAction(self.action_terminal)

        help_menu = menubar.addMenu("&Help")

        self.action_about = QAction("&About", self)

        help_menu.addAction(self.action_about)

        menubar.setCornerWidget(self._create_theme_toggle(), Qt.Corner.TopRightCorner)

        self.menu_handler = MenuHandler(self)

        self.menu_handler.connect_actions()

    def _setup_components(self) -> None:

        self.exec_widget = ExecWidget(self)

        self.context.register("exec", self.exec_widget)

        if self.exec_widget.styleSheet():

            self.exec_widget.setStyleSheet("")

        for w in self.exec_widget.findChildren(QWidget):

            if w.styleSheet():

                w.setStyleSheet("")

        self.exec_widget.connect_to_statusbar(self.statusBar())

        self.vtk_pre = PreprocessWidget(self)

        self.vtk_post = PostprocessWidget(self)

        self.context.register("vtk_pre", self.vtk_pre)

        self.context.register("vtk_post", self.vtk_post)

        self._setup_vtk_pre_toolbar()

        self.residual_graph = ResidualPlotWidget(self)

        self.residual_graph.refresh_requested.connect(self._on_residual_refresh)

        self.context.register("residual_graph", self.residual_graph)

    def _setup_vtk_pre_toolbar(self) -> None:

        for action in self.vtk_pre.toolbar.actions():

            if action.text() == "Load OpenFOAM":

                action.setVisible(False)

                break

        self.vtk_pre.add_tool("point_probe")

        for action in self.vtk_pre.toolbar.actions():

            if action.text() == "Point Probe":

                action.setVisible(False)

                break

        probe_tool = self.vtk_pre._optional_tools.get("point_probe")

        if probe_tool:

            probe_tool.center_moved.connect(self._on_probe_position_changed)

            probe_tool.visibility_changed.connect(self._on_probe_visibility_changed)

    def _on_save_clicked(self) -> None:

        mesh_panel = self.center_widget.panel_views.get("mesh")

        if mesh_panel:

            mesh_panel._update_snappyhex_dict()

            mesh_panel._update_castellation_settings()

            mesh_panel._update_snap_settings()

            mesh_panel._update_boundary_layer_settings()

        run_panel = self.center_widget.panel_views.get("run")

        if run_panel:

            run_panel._update_run_settings()

        self.case_data.save()

        self.statusBar().showMessage("Saved", 2000)

    def _on_residual_refresh(self) -> None:

        self.center_widget._load_residual_log()

    def _create_theme_toggle(self) -> QToolButton:

        self._theme_btn = QToolButton()

        self._theme_btn.setText("\u25D0")

        self._theme_btn.setToolTip("Switch to dark theme")

        self._theme_btn.setStyleSheet(
            "QToolButton { padding: 2px 8px; margin: 2px 4px; font-size: 14px; }"
        )

        self._theme_btn.clicked.connect(self._on_theme_toggle)

        return self._theme_btn

    def _on_theme_toggle(self) -> None:

        import pyqtgraph as pg

        from PySide6.QtWidgets import QApplication

        new_mode = toggle_theme(QApplication.instance())

        c = get_colors()

        if new_mode == "dark":

            self._theme_btn.setToolTip("Switch to light theme")

        else:

            self._theme_btn.setToolTip("Switch to dark theme")

        if self.vtk_pre:

            r = self.vtk_pre.renderer

            r.SetBackground(*c["vtk_bg1"])

            r.SetBackground2(*c["vtk_bg2"])

            self.vtk_pre.vtk_widget.GetRenderWindow().Render()

        if self.vtk_post:

            r = self.vtk_post.renderer

            r.SetBackground(*c["vtk_post_bg1"])

            r.SetBackground2(*c["vtk_post_bg2"])

            self.vtk_post.vtk_widget.GetRenderWindow().Render()

        if self.residual_graph:

            self.residual_graph.plot_widget.setBackground(c["graph_bg"])

            axis_pen = pg.mkPen(color=c["graph_axis"])

            for axis_name in ('bottom', 'left'):

                axis = self.residual_graph.plot_widget.getAxis(axis_name)

                axis.setPen(axis_pen)

                axis.setTextPen(axis_pen)

            self.residual_graph.plot_widget.setLabel('bottom', 'Time', color=c["graph_axis"])

            self.residual_graph.plot_widget.setLabel('left', 'Residual', color=c["graph_axis"])

    def _on_probe_position_changed(self, x: float, y: float, z: float) -> None:

        geom_panel = self.center_widget.panel_views.get("geometry")

        if geom_panel:

            geom_panel.ui.edit_input_position_x.setText(f"{x:.4f}")

            geom_panel.ui.edit_input_position_y.setText(f"{y:.4f}")

            geom_panel.ui.edit_input_position_z.setText(f"{z:.4f}")

    def _on_probe_visibility_changed(self, visible: bool) -> None:

        if not visible:

            return

        x, y, z = self.case_data.point_probe_position

        if x != 0.0 or y != 0.0 or z != 0.0:

            probe_tool = self.vtk_pre._optional_tools.get("point_probe")

            if probe_tool:

                probe_tool.set_center(x, y, z)

    def _on_view_dock_toggled(self, dock_num: int, checked: bool) -> None:

        if not self.dock_manager:

            return

        if checked:

            self.dock_manager.show_dock(dock_num)

        else:

            self.dock_manager.hide_dock(dock_num)

    def _on_dock_visibility_changed(self, dock_num: int, visible: bool) -> None:

        action = self._dock_view_actions.get(dock_num)

        if action:

            action.blockSignals(True)

            action.setChecked(visible)

            action.blockSignals(False)

    def _setup_dock(self) -> None:

        self._central_container = QWidget()

        self._central_container.setLayout(QVBoxLayout())

        self._central_container.layout().setContentsMargins(0, 0, 0, 0)

        self.setCentralWidget(self._central_container)

        class _UI:

            pass

        self.ui = _UI()

        self.ui.centralwidget = self._central_container

        dock_layout_file = str(Path(self.app_data.user_path) / "dock_layout.dat")

        self.dock_manager = DockWidget(self, layout_file=dock_layout_file)

        self.context.register("dock", self.dock_manager)

        self.dock_manager.visibility_changed.connect(self._on_dock_visibility_changed)

        self.center_widget = CenterWidget(self, self.context)

        self.dock_manager.add_center_dock(self.center_widget)

        self.dock_manager.add_side_dock(self.exec_widget, "Log", area="bottom")

        self.dock_manager.add_side_dock(self.vtk_pre, "Mesh", is_tab=True)

        self.dock_manager.add_side_dock(self.vtk_post, "Post", is_tab=True)

        self.dock_manager.add_side_dock(self.residual_graph, "Residuals", is_tab=True)

        self.dock_manager.change_dock_tab(2)

    def _setup_window(self) -> None:

        self.setWindowTitle(self.app_data.title)

        self.setMinimumSize(650, 450)

        self.app_data.load()

        self._update_recent_menu()

        restore_window_geometry(self, self.app_data.window_geometry)

        self.dock_manager.restore_layout()

        self._sync_view_menu_states()

        self.statusBar().showMessage("Ready", 3000)

    def _sync_view_menu_states(self) -> None:

        for dock_num, action in self._dock_view_actions.items():

            dock_info = self.dock_manager.docks.get(dock_num)

            if dock_info:

                action.setChecked(dock_info.show_state)

    def _update_window_title(self) -> None:

        if self.case_path:

            title = f"{self.app_data.title} [{self.case_path}]"

        else:

            title = self.app_data.title

        self.setWindowTitle(title)

    def initialize(self) -> None:

        self.exec_widget.set_defaults()

        if self.case_path:

            self._load_case(self.case_path)

        self._update_window_title()

        geom_panel = self.center_widget.panel_views.get("geometry")

        if geom_panel:

            geom_panel.load_data()

        mesh_panel = self.center_widget.panel_views.get("mesh")

        if mesh_panel:

            mesh_panel.load_data()

        run_panel = self.center_widget.panel_views.get("run")

        if run_panel:

            run_panel.load_data()

        self.center_widget._load_residual_log()

        post_panel = self.center_widget.panel_views.get("post")

        if post_panel:

            post_panel.load_results()

        self.center_widget.select_default_tab()

        self.statusBar().showMessage("Ready", 3000)

    def _load_case(self, case_path: str) -> None:

        path = Path(case_path)

        if not path.exists():

            self._create_case_from_template(case_path)

        self.case_data.set_path(str(path.resolve()))

        self.case_data.load()

        self.exec_widget.set_working_path(str(path.resolve()))

    def _create_case_from_template(self, case_path: str) -> None:

        base_case_path = self.app_data.get_config_basecase_path()

        if not base_case_path.exists():

            Path(case_path).mkdir(parents=True, exist_ok=True)

            return

        try:

            copy_files(str(base_case_path), case_path)

        except Exception as e:

            Path(case_path).mkdir(parents=True, exist_ok=True)

    def open_case(self, path: str = "") -> None:

        if not path:

            path = DirDialogBox.open_folder(self, "Open Case")

        if not path:

            return

        self._delete_temp_case()

        self._reset_all_state()

        self.case_path = path

        self._load_case(path)

        self._reload_panels()

        self._update_window_title()

        self.app_data.add_recent_case(path)

        self._update_recent_menu()

    def create_new_case(self, user_select: bool = True) -> None:

        if user_select:

            path = DirDialogBox.create_folder(self, "Create New Case")

            if not path:

                return

        else:

            from datetime import datetime

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            path = str(Path(self.app_data.user_path) / "temp" / f"temp_{timestamp}")

        self._delete_temp_case()

        self._reset_all_state()

        self.case_path = path

        self._create_case_from_template(path)

        self._load_case(path)

        self._reload_panels()

        self._update_window_title()

    def _update_recent_menu(self) -> None:

        """최근 케이스 서브메뉴를 app_data.recent_cases로 갱신"""

        self.menu_recent.clear()

        recent = self.app_data.recent_cases

        if not recent:

            action = self.menu_recent.addAction("(없음)")

            action.setEnabled(False)

            return

        for i, path in enumerate(recent):

            exists = Path(path).exists()

            display = path if len(path) <= 55 else f"...{path[-52:]}"

            action = self.menu_recent.addAction(f"&{i + 1}. {display}" if i < 9 else f"{i + 1}. {display}")

            action.setEnabled(exists)

            if exists:

                action.triggered.connect(lambda checked=False, p=path: self.open_case(p))

            else:

                action.setToolTip("경로가 존재하지 않습니다")

        self.menu_recent.addSeparator()

        clear_action = self.menu_recent.addAction("목록 지우기")

        clear_action.triggered.connect(self._clear_recent_cases)

    def _clear_recent_cases(self) -> None:

        self.app_data.recent_cases.clear()

        self.app_data.save()

        self._update_recent_menu()

    def _reset_all_state(self) -> None:

        if self.exec_widget and self.exec_widget.is_running():

            self.exec_widget.stop_process(kill=True)

        if self.vtk_pre:

            for obj in list(self.vtk_pre.obj_manager.get_all()):

                self.vtk_pre.obj_manager.remove(obj.id)

            mesh_panel = self.center_widget.panel_views.get("mesh")

            if mesh_panel:

                mesh_panel._clear_existing_mesh()

            self.vtk_pre.vtk_widget.GetRenderWindow().Render()

        if self.vtk_post:

            self.vtk_post._cancel_loading()

            self.vtk_post.renderer.RemoveAllViewProps()

            self.vtk_post.reader = None

            if hasattr(self.vtk_post, 'foam_reader'):

                self.vtk_post.foam_reader = None

            self.vtk_post.field_combo.blockSignals(True)

            self.vtk_post.field_combo.clear()

            self.vtk_post.field_combo.blockSignals(False)

            self.vtk_post.vtk_widget.GetRenderWindow().Render()

        post_panel = self.center_widget.panel_views.get("post")

        if post_panel:

            post_panel._results_loaded = False

        if self.exec_widget:

            self.exec_widget._log_view.clear()

            self.exec_widget._output_view.clear()

            self.exec_widget._log_msg = ''

            self.exec_widget._all_msgs = []

            self.exec_widget._output_buffer = {}

        if self.residual_graph:

            self.residual_graph.plot_widget.clear()

        run_panel = self.center_widget.panel_views.get("run")

        if run_panel:

            run_panel.ui.edit_run_status.setText("Ready")

            run_panel.ui.edit_run_started.setText("-")

            run_panel.ui.edit_run_finished.setText("-")

    def _reload_panels(self) -> None:

        for key in ("geometry", "mesh", "run"):

            panel = self.center_widget.panel_views.get(key)

            if panel:

                panel.load_data()

        post_panel = self.center_widget.panel_views.get("post")

        if post_panel:

            post_panel.load_results()

        self.center_widget.select_default_tab()

        self.exec_widget.add_log_ready()

    def closeEvent(self, event):

        if self.case_path and "temp" in self.case_path:

            if not self._handle_temp_case_close():

                event.ignore()

                return

        self._cleanup()

        if self.case_path and "temp" in self.case_path:

            self._delete_temp_case()

        event.accept()

    def _handle_temp_case_close(self) -> bool:

        reply = QMessageBox.question(
            self,
            'Save Temporary Case?',
            'This is a temporary case that will be deleted.\n\n'
            'Do you want to save it to a permanent location?',
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No |
            QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Yes
        )

        if reply == QMessageBox.StandardButton.Yes:

            return self._save_temp_case_as()

        elif reply == QMessageBox.StandardButton.No:

            return True

        else:

            return False

    def _pick_save_path(self, title: str = "Save Case As") -> str | None:

        """부모 폴더 선택 → 케이스 이름 입력 → 새 폴더 경로 반환 (폴더 자동 생성)."""

        parent_dir = QFileDialog.getExistingDirectory(
            self, f"{title} - 저장할 위치 선택",
            str(Path.home()),
            QFileDialog.Option.ShowDirsOnly
        )

        if not parent_dir:

            return None

        default_name = Path(self.case_path).name if self.case_path else "NewCase"

        name, ok = QInputDialog.getText(
            self, title, "케이스 폴더 이름:", text=default_name
        )

        if not ok or not name.strip():

            return None

        name = name.strip()

        new_path = str(Path(parent_dir) / name)

        if Path(new_path).exists():

            reply = QMessageBox.question(
                self, title,
                f"'{name}' 폴더가 이미 존재합니다.\n덮어쓰시겠습니까?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply != QMessageBox.StandardButton.Yes:

                return None

        Path(new_path).mkdir(parents=True, exist_ok=True)

        return new_path

    def _save_temp_case_as(self) -> bool:

        new_path = self._pick_save_path("Save Case As")

        if not new_path:

            reply = QMessageBox.question(
                self,
                'Save Cancelled',
                'Save was cancelled.\n\n'
                'Do you want to close without saving? (Case will be deleted)',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:

                self._delete_temp_case()

                return True

            else:

                return False

        try:

            copy_files(self.case_path, new_path)

            old_temp = self.case_path

            self.case_path = new_path

            self.case_data.set_path(new_path)

            shutil.rmtree(old_temp, ignore_errors=True)

            self._update_window_title()

            return True

        except Exception as e:

            QMessageBox.critical(
                self,
                'Save Error',
                f'Failed to save case:\n{e}'
            )

            return False

    def save_case_as(self) -> bool:

        new_path = self._pick_save_path("Save Case As")

        if not new_path:

            return False

        try:

            copy_files(self.case_path, new_path)

            is_temp = "temp" in self.case_path

            old_path = self.case_path

            self.case_path = new_path

            self.case_data.set_path(new_path)

            if is_temp:

                shutil.rmtree(old_path, ignore_errors=True)

            self._update_window_title()

            self.statusBar().showMessage(f"Saved to {new_path}", 3000)

            return True

        except Exception as e:

            QMessageBox.critical(self, 'Save Error', f'Failed to save case:\n{e}')

            return False

    def _delete_temp_case(self) -> None:

        if self.case_path and "temp" in self.case_path:

            try:

                shutil.rmtree(self.case_path, ignore_errors=True)

            except Exception:

                traceback.print_exc()

    def _cleanup(self) -> None:

        self.dock_manager.save_layout()

        self.app_data.window_geometry = save_window_geometry(self)

        self.app_data.save()

        if self.case_data.path and "temp" not in self.case_path:

            self.case_data.save()

        if self.exec_widget:

            self.exec_widget.end()

    def __repr__(self) -> str:

        return f"MainWindow(case_path='{self.case_path}')"

