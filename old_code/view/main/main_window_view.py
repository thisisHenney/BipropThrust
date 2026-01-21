from pathlib import Path
from PySide6.QtWidgets import QMainWindow
from nextlib.widgets.dock import DockWidget
from nextlib.execute.exec_widget import ExecWidget
from nextlib.vtk.vtk_widget import VtkWidget
from nextlib.vtk.vtk_manager import vtk_manager
from nextlib.graph.pyqtgraph.residual_plot_widget import ResidualPlotWidget
from nextlib.utils.window import center_on_screen
from nextlib.utils.file import get_temp_dir, copy_files
from nextlib.dialogbox.dialogbox import DirDialogBox
from nextlib.openfoam.foamcase.foamcase import FoamCase
from view.main.main_window_ui import Ui_MainWindow
from view.main.center_widget_view import CenterWidget
from view.main.menu.main_menu import MainMenu
from common.app_data import app_data
from common.case_data import case_data
from common.app_context import AppContext



class MainWindow(QMainWindow):
    def __init__(self, open_path = ""):
        super().__init__()

        self.open_path = open_path
        self.app_data = app_data
        self.case_data = case_data
        self.foam_data = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.main_menu = MainMenu(self)
        self.main_menu.init()

        self.statusbar = self.ui.statusbar
        self.statusbar.showMessage('Hello', 5000)

        self.context = AppContext()

        self.exec = ExecWidget(self)
        self.context.register("exec", self.exec)
        self.exec.connect_to_statusbar(self.statusbar)

        self.vtk1 = VtkWidget(self, registry=vtk_manager)
        self.vtk2 = VtkWidget(self, registry=vtk_manager)
        self.context.register("vtk1", self.vtk1)
        self.context.register("vtk2", self.vtk2)

        vtk_manager.register("pre", self.vtk1)
        vtk_manager.register("post", self.vtk2)

        self.graph = ResidualPlotWidget(self)

        self.dock_manager = DockWidget(self)
        self.context.register("dock", self.dock_manager)

        self.center = CenterWidget(self, self.context)
        self.center.init()

        self.dock_manager.add_center_dock(self.center)
        self.dock_manager.add_side_dock(self.exec, "Log", area="bottom")
        self.dock_manager.add_side_dock(self.vtk1, "Mesh", is_tab=True)         # 2
        self.dock_manager.add_side_dock(self.vtk2, "Post", is_tab=True)         # 3
        self.dock_manager.add_side_dock(self.graph, "Residuals", is_tab=True)   # 0, 1
        self.dock_manager.change_dock_tab(2)

        self.setWindowTitle(f'{self.app_data.title}')
        self.setMinimumSize(650, 450)
        self.resize(1300, 900)

        center_on_screen(self)

        self.closeEvent = self.close_window

    def set_defaults(self):
        self.exec.set_defaults()
        self.vtk1.set_defaults()
        self.vtk2.set_defaults()

        if self.open_path:
            self.open_case(self.open_path)
        else:
            self.create_case()

    def close_window(self, e):
        self.end()
        e.accept()

    def end(self):
        self.exec.end()
        self.vtk1.end()
        self.vtk2.end()

    def create_case(self, user_select_path=False):
        if user_select_path:
            new_path = DirDialogBox.create_folder(self, "Create case")
        else:
            new_path = get_temp_dir(self.app_data.user_path, "TempCase")

        self.case_data.set_path(rf'{new_path}')
        self.case_data.save()

        src_path = Path(self.app_data.config_path) / "basecase"
        copy_files(src_path, new_path)

        self._load_case()

    def open_case(self, path=''):
        if not path:
            path = DirDialogBox.open_folder(self, "Load case")

        self.case_data.set_path(rf'{path}')
        self.case_data.load()

        self._load_case()

    def _load_case(self):
        path = self.case_data.path
        self.setWindowTitle(f"{self.app_data.title} - [{self.case_data.path}]")

        self.exec.set_working_path(path)

        self.foam_data = FoamCase(self.case_data.path)
        # print(self.case_data.path)
        # print(self.foam_data.keys())

        # log_path = Path(Path(path) / "log.solver" )
        # self.graph.load_file(str(log_path))
