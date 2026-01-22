"""
Menu Handler - Menu Action Handler

This module handles all menu actions for the main window.
"""

from PySide6.QtWidgets import QMessageBox

from nextlib.program.program import open_file_explorer

from common.app_data import app_data
from common.case_data import case_data


class MenuHandler:
    """
    Handles menu actions for the main window.

    Connects menu actions to their respective handlers.
    """

    def __init__(self, main_window):
        """
        Initialize menu handler.

        Args:
            main_window: MainWindow instance
        """
        self.main_window = main_window
        self.app_data = app_data
        self.case_data = case_data

    def connect_actions(self) -> None:
        """Connect all menu actions to their handlers."""
        mw = self.main_window

        # File menu
        mw.action_new.triggered.connect(self.on_new)
        mw.action_open.triggered.connect(self.on_open)
        mw.action_save.triggered.connect(self.on_save)
        mw.action_save_as.triggered.connect(self.on_save_as)
        mw.action_exit.triggered.connect(self.on_exit)

        # Run menu
        mw.action_run.triggered.connect(self.on_run)
        mw.action_stop.triggered.connect(self.on_stop)

        # View menu
        mw.action_view_mesh.triggered.connect(self.on_view_mesh)
        mw.action_view_post.triggered.connect(self.on_view_post)
        mw.action_view_residuals.triggered.connect(self.on_view_residuals)
        mw.action_view_log.triggered.connect(self.on_view_log)

        # Tools menu
        mw.action_file_explorer.triggered.connect(self.on_file_explorer)
        mw.action_terminal.triggered.connect(self.on_terminal)

        # Help menu
        mw.action_about.triggered.connect(self.on_about)

    # ========== File Menu ==========

    def on_new(self) -> None:
        """Handle New action."""
        print("Menu: New")
        self.main_window.create_new_case(user_select=True)

    def on_open(self) -> None:
        """Handle Open action."""
        print("Menu: Open")
        self.main_window.open_case()

    def on_save(self) -> None:
        """Handle Save action."""
        print("Menu: Save")
        if self.case_data.path:
            self.case_data.save()
            self.main_window.statusBar().showMessage("Case saved", 3000)
        else:
            self.on_save_as()

    def on_save_as(self) -> None:
        """Handle Save As action."""
        print("Menu: Save As")
        # TODO: Implement save as functionality
        self.main_window.statusBar().showMessage("Save As - Not implemented yet", 3000)

    def on_exit(self) -> None:
        """Handle Exit action."""
        print("Menu: Exit")
        self.main_window.close()

    # ========== Run Menu ==========

    def on_run(self) -> None:
        """Handle Run action."""
        print("Menu: Run")
        # TODO: Implement run simulation
        self.main_window.statusBar().showMessage("Run - Not implemented yet", 3000)

    def on_stop(self) -> None:
        """Handle Stop action."""
        print("Menu: Stop")
        # TODO: Implement stop simulation
        self.main_window.statusBar().showMessage("Stop - Not implemented yet", 3000)

    # ========== View Menu ==========

    def on_view_mesh(self) -> None:
        """Handle View Mesh action."""
        print("Menu: View Mesh")
        if self.main_window.dock_manager:
            self.main_window.dock_manager.change_dock_tab(2)

    def on_view_post(self) -> None:
        """Handle View Post action."""
        print("Menu: View Post")
        if self.main_window.dock_manager:
            self.main_window.dock_manager.change_dock_tab(3)

    def on_view_residuals(self) -> None:
        """Handle View Residuals action."""
        print("Menu: View Residuals")
        if self.main_window.dock_manager:
            self.main_window.dock_manager.change_dock_tab(0)

    def on_view_log(self) -> None:
        """Handle View Log action."""
        print("Menu: View Log")
        # Log is in bottom dock, always visible
        self.main_window.statusBar().showMessage("Log panel is at the bottom", 2000)

    # ========== Tools Menu ==========

    def on_file_explorer(self) -> None:
        """Handle Open File Explorer action."""
        print("Menu: File Explorer")
        if self.case_data.path:
            open_file_explorer(self.main_window, self.case_data.path)
        else:
            self.main_window.statusBar().showMessage("No case loaded", 2000)

    def on_terminal(self) -> None:
        """Handle Open Terminal action."""
        print("Menu: Terminal")
        # TODO: Implement terminal opening
        self.main_window.statusBar().showMessage("Terminal - Not implemented yet", 3000)

    # ========== Help Menu ==========

    def on_about(self) -> None:
        """Handle About action."""
        print("Menu: About")
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
