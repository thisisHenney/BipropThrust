
from PySide6.QtWidgets import QMessageBox

from nextlib.program.program import open_file_explorer

from common.app_data import app_data

from common.case_data import case_data

class MenuHandler:

    def __init__(self, main_window):

        self.main_window = main_window

        self.app_data = app_data

        self.case_data = case_data

    def connect_actions(self) -> None:

        mw = self.main_window

        mw.action_new.triggered.connect(self.on_new)

        mw.action_open.triggered.connect(self.on_open)

        mw.action_save.triggered.connect(self.on_save)

        mw.action_save_as.triggered.connect(self.on_save_as)

        mw.action_exit.triggered.connect(self.on_exit)

        mw.action_run.triggered.connect(self.on_run)

        mw.action_stop.triggered.connect(self.on_stop)

        mw.action_view_mesh.triggered.connect(self.on_view_mesh)

        mw.action_view_post.triggered.connect(self.on_view_post)

        mw.action_view_residuals.triggered.connect(self.on_view_residuals)

        mw.action_view_log.triggered.connect(self.on_view_log)

        mw.action_file_explorer.triggered.connect(self.on_file_explorer)

        mw.action_terminal.triggered.connect(self.on_terminal)

        mw.action_about.triggered.connect(self.on_about)

    def on_new(self) -> None:

        self.main_window.create_new_case(user_select=True)

    def on_open(self) -> None:

        self.main_window.open_case()

    def on_save(self) -> None:

        if self.case_data.path:

            self.main_window._on_save_clicked()

        else:

            self.on_save_as()

    def on_save_as(self) -> None:

        self.main_window.save_case_as()

    def on_exit(self) -> None:

        self.main_window.close()

    def on_run(self) -> None:

        self.main_window.statusBar().showMessage("Run - Not implemented yet", 3000)

    def on_stop(self) -> None:

        self.main_window.statusBar().showMessage("Stop - Not implemented yet", 3000)

    def on_view_mesh(self) -> None:

        if self.main_window.dock_manager:

            self.main_window.dock_manager.change_dock_tab(2)

    def on_view_post(self) -> None:

        if self.main_window.dock_manager:

            self.main_window.dock_manager.change_dock_tab(3)

    def on_view_residuals(self) -> None:

        if self.main_window.dock_manager:

            self.main_window.dock_manager.change_dock_tab(0)

    def on_view_log(self) -> None:

        self.main_window.statusBar().showMessage("Log panel is at the bottom", 2000)

    def on_file_explorer(self) -> None:

        if self.case_data.path:

            open_file_explorer(self.main_window, self.case_data.path)

        else:

            self.main_window.statusBar().showMessage("No case loaded", 2000)

    def on_terminal(self) -> None:

        self.main_window.statusBar().showMessage("Terminal - Not implemented yet", 3000)

    def on_about(self) -> None:

        QMessageBox.about(
            self.main_window,
            f"About {self.app_data.name}",
            f"<h2>{self.app_data.title}</h2>"
            f"<p>OpenFOAM Bipropellant Thruster Simulation GUI</p>"
            f"<p>Version: {self.app_data.version}</p>"
            f"<p>Copyright (c) 2025 KARI</p>"
            f"<hr>"
            f"<p><b>Technology Stack:</b></p>"
            f"<ul>"
            f"<li>GUI Framework: PySide6 (Qt 6)</li>"
            f"<li>3D Visualization: VTK</li>"
            f"<li>CFD Framework: OpenFOAM</li>"
            f"</ul>"
        )

