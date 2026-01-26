"""
Main Window - Application Main Window Controller

This module manages the main application window, layout,
and component lifecycle.
"""

import shutil
from pathlib import Path

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from nextlib.widgets.dock import DockWidget
from nextlib.execute.exec_widget import ExecWidget
from nextlib.vtk import PreprocessWidget, PostprocessWidget
from nextlib.graph.pyqtgraph.residual_plot_widget import ResidualPlotWidget
from nextlib.utils.window import center_on_screen
from nextlib.utils.file import copy_files
from nextlib.dialogbox.dialogbox import DirDialogBox

from common.app_data import app_data
from common.case_data import case_data
from common.app_context import AppContext
from view.main.menu_handler import MenuHandler
from view.main.center_widget import CenterWidget


class MainWindow(QMainWindow):
    """
    Main application window.

    Manages the UI layout, components, and case lifecycle.
    """

    def __init__(self, case_path: str = ""):
        """
        Initialize main window.

        Args:
            case_path: Path to case directory
        """
        super().__init__()

        # Store paths and data
        self.case_path = case_path
        self.app_data = app_data
        self.case_data = case_data

        # Service registry
        self.context = AppContext()

        # Components (will be initialized in _setup_components)
        self.exec_widget = None
        self.vtk_pre = None
        self.vtk_post = None
        self.residual_graph = None
        self.dock_manager = None
        self.center_widget = None
        self.menu_handler = None

        # Setup UI
        self._setup_menu()
        self._setup_components()
        self._setup_dock()
        self._setup_window()

    def _setup_menu(self) -> None:
        """Setup menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        self.action_new = QAction("&New", self)
        self.action_new.setShortcut("Ctrl+N")
        file_menu.addAction(self.action_new)

        self.action_open = QAction("&Open...", self)
        self.action_open.setShortcut("Ctrl+O")
        file_menu.addAction(self.action_open)

        self.action_save = QAction("&Save", self)
        self.action_save.setShortcut("Ctrl+S")
        file_menu.addAction(self.action_save)

        self.action_save_as = QAction("Save &As...", self)
        self.action_save_as.setShortcut("Ctrl+Shift+S")
        file_menu.addAction(self.action_save_as)

        file_menu.addSeparator()

        self.action_exit = QAction("E&xit", self)
        self.action_exit.setShortcut("Alt+F4")
        file_menu.addAction(self.action_exit)

        # Run menu
        run_menu = menubar.addMenu("&Run")

        self.action_run = QAction("&Run", self)
        self.action_run.setShortcut("F5")
        run_menu.addAction(self.action_run)

        self.action_stop = QAction("&Stop", self)
        run_menu.addAction(self.action_stop)

        # View menu
        view_menu = menubar.addMenu("&View")

        self.action_view_mesh = QAction("&Mesh", self)
        view_menu.addAction(self.action_view_mesh)

        self.action_view_post = QAction("&Post", self)
        view_menu.addAction(self.action_view_post)

        self.action_view_residuals = QAction("&Residuals", self)
        view_menu.addAction(self.action_view_residuals)

        self.action_view_log = QAction("&Log", self)
        view_menu.addAction(self.action_view_log)

        # Tools menu
        tools_menu = menubar.addMenu("&Tools")

        self.action_file_explorer = QAction("Open &File Explorer", self)
        tools_menu.addAction(self.action_file_explorer)

        self.action_terminal = QAction("Open &Terminal", self)
        tools_menu.addAction(self.action_terminal)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        self.action_about = QAction("&About", self)
        help_menu.addAction(self.action_about)

        # Create menu handler and connect signals
        self.menu_handler = MenuHandler(self)
        self.menu_handler.connect_actions()

    def _setup_components(self) -> None:
        """Setup main components (VTK, Exec, Graph)."""
        # Execution widget (log output)
        self.exec_widget = ExecWidget(self)
        self.context.register("exec", self.exec_widget)

        # Connect to statusbar
        self.exec_widget.connect_to_statusbar(self.statusBar())

        # VTK widgets for pre/post visualization
        self.vtk_pre = PreprocessWidget(self)
        self.vtk_post = PostprocessWidget(self)
        self.context.register("vtk_pre", self.vtk_pre)
        self.context.register("vtk_post", self.vtk_post)

        # Customize vtk_pre toolbar
        self._setup_vtk_pre_toolbar()

        # Residual plot widget
        self.residual_graph = ResidualPlotWidget(self)
        self.context.register("residual_graph", self.residual_graph)

    def _setup_vtk_pre_toolbar(self) -> None:
        """Customize vtk_pre toolbar - hide OpenFOAM button, add probe tool."""
        # Hide "Load OpenFOAM" action
        for action in self.vtk_pre.toolbar.actions():
            if action.text() == "Load OpenFOAM":
                action.setVisible(False)
                break

        # Add point probe tool
        self.vtk_pre.add_tool("point_probe")

        # Hide point_probe button in toolbar
        for action in self.vtk_pre.toolbar.actions():
            if action.text() == "Point Probe":
                action.setVisible(False)
                break

        # Get point_probe tool and connect signals
        probe_tool = self.vtk_pre._optional_tools.get("point_probe")
        if probe_tool:
            probe_tool.center_moved.connect(self._on_probe_position_changed)
            probe_tool.visibility_changed.connect(self._on_probe_visibility_changed)

    def _on_probe_position_changed(self, x: float, y: float, z: float) -> None:
        """Handle probe position change - sync to geometry panel."""
        # Get geometry panel from center widget
        geom_panel = self.center_widget.panel_views.get("geometry")
        if geom_panel:
            geom_panel.ui.edit_input_position_x.setText(f"{x:.4f}")
            geom_panel.ui.edit_input_position_y.setText(f"{y:.4f}")
            geom_panel.ui.edit_input_position_z.setText(f"{z:.4f}")

    def _on_probe_visibility_changed(self, visible: bool) -> None:
        """Handle probe visibility change - restore saved position when shown."""
        if not visible:
            return

        # Load saved position from case_data
        x, y, z = self.case_data.point_probe_position

        # Only restore if position is not at origin (0,0,0)
        if x != 0.0 or y != 0.0 or z != 0.0:
            probe_tool = self.vtk_pre._optional_tools.get("point_probe")
            if probe_tool:
                probe_tool.set_center(x, y, z)

    def _setup_dock(self) -> None:
        """Setup dock widget layout."""
        # Create central widget container for dock manager
        self._central_container = QWidget()
        self._central_container.setLayout(QVBoxLayout())
        self._central_container.layout().setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self._central_container)

        # Create ui object for DockWidget compatibility
        class _UI:
            pass
        self.ui = _UI()
        self.ui.centralwidget = self._central_container

        # Create dock manager
        self.dock_manager = DockWidget(self)
        self.context.register("dock", self.dock_manager)

        # Create center widget with navigation tree and panels
        self.center_widget = CenterWidget(self, self.context)

        # Add widgets to dock
        self.dock_manager.add_center_dock(self.center_widget)
        self.dock_manager.add_side_dock(self.exec_widget, "Log", area="bottom")
        self.dock_manager.add_side_dock(self.vtk_pre, "Mesh", is_tab=True)
        self.dock_manager.add_side_dock(self.vtk_post, "Post", is_tab=True)
        self.dock_manager.add_side_dock(self.residual_graph, "Residuals", is_tab=True)

        # Show Mesh tab by default
        self.dock_manager.change_dock_tab(2)

    def _setup_window(self) -> None:
        """Setup window properties."""
        # Set window title (will be updated after case is loaded)
        self.setWindowTitle(self.app_data.title)

        # Set window size
        self.setMinimumSize(650, 450)
        self.resize(1300, 900)

        # Center on screen
        center_on_screen(self)

        # Setup statusbar
        self.statusBar().showMessage("Ready", 3000)

    def _update_window_title(self) -> None:
        """Update window title with current case path."""
        if self.case_path:
            title = f"{self.app_data.title} [{self.case_path}]"
        else:
            title = self.app_data.title
        self.setWindowTitle(title)

    def initialize(self) -> None:
        """
        Initialize the main window and load case.

        This is called after construction to load the case
        and setup all components.
        """

        # Initialize components
        self.exec_widget.set_defaults()

        # Load or create case
        if self.case_path:
            self._load_case(self.case_path)
        # If no case_path, window opens without a case loaded

        # Update window title with case path
        self._update_window_title()

        # Load geometry data after case is loaded
        geom_panel = self.center_widget.panel_views.get("geometry")
        if geom_panel:
            geom_panel.load_data()

        # Load mesh generation data after case is loaded
        mesh_panel = self.center_widget.panel_views.get("mesh")
        if mesh_panel:
            mesh_panel.load_data()

        # Start with Geometry tab visible - hide mesh, show geometry
        self.center_widget._show_geometry_objects()

        # Update status
        self.statusBar().showMessage("Ready", 3000)

    def _load_case(self, case_path: str) -> None:
        """
        Load a case from the given path.

        Args:
            case_path: Path to case directory
        """
        path = Path(case_path)

        # Check if case exists
        if not path.exists():
            self._create_case_from_template(case_path)

        # Set case data path
        self.case_data.set_path(str(path.resolve()))

        # Try to load existing case data
        self.case_data.load()

        # Set working path for exec widget
        self.exec_widget.set_working_path(str(path.resolve()))


    def _create_case_from_template(self, case_path: str) -> None:
        """
        Create a new case from base template.

        Args:
            case_path: Path where case should be created
        """
        # Get base case template path
        base_case_path = self.app_data.get_config_basecase_path()

        if not base_case_path.exists():
            # Create empty case directory
            Path(case_path).mkdir(parents=True, exist_ok=True)
            return

        # Copy base case to new location
        try:
            copy_files(str(base_case_path), case_path)
        except Exception as e:
            # Create empty directory as fallback
            Path(case_path).mkdir(parents=True, exist_ok=True)

    def open_case(self, path: str = "") -> None:
        """
        Open a case from path.

        Args:
            path: Case path. If empty, shows folder dialog.
        """
        if not path:
            path = DirDialogBox.open_folder(self, "Open Case")

        if not path:
            return

        self.case_path = path
        self._load_case(path)
        self._update_window_title()

    def create_new_case(self, user_select: bool = True) -> None:
        """
        Create a new case.

        Args:
            user_select: If True, show folder dialog for case location
        """
        if user_select:
            path = DirDialogBox.create_folder(self, "Create New Case")
            if not path:
                return
        else:
            # Create temp case
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = str(Path(self.app_data.user_path) / "temp" / f"temp_{timestamp}")

        self.case_path = path
        self._create_case_from_template(path)
        self._load_case(path)
        self._update_window_title()

    def closeEvent(self, event):
        """
        Handle window close event.

        Args:
            event: Close event
        """

        # Check if case is temporary and unsaved
        if self.case_path and "temp" in self.case_path:
            if not self._handle_temp_case_close():
                # User cancelled, don't close
                event.ignore()
                return

        # Cleanup
        self._cleanup()

        # Accept close
        event.accept()

    def _handle_temp_case_close(self) -> bool:
        """
        Handle closing of temporary case.

        Asks user if they want to save the temporary case.

        Returns:
            True if should continue closing, False if cancelled
        """
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
            # Save case to user-selected location
            return self._save_temp_case_as()

        elif reply == QMessageBox.StandardButton.No:
            # Delete temporary case
            self._delete_temp_case()
            return True

        else:  # Cancel
            # Don't close window
            return False

    def _save_temp_case_as(self) -> bool:
        """
        Save temporary case to permanent location.

        Returns:
            True if saved successfully or user cancelled, False to abort close
        """
        # Open directory dialog
        new_path = DirDialogBox.create_folder(self, "Save Case As")

        if not new_path:
            # User cancelled save dialog
            # Ask again what to do
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
            # Copy temp case to new location
            copy_files(self.case_path, new_path)

            # Delete temp case
            self._delete_temp_case()

            return True

        except Exception as e:
            QMessageBox.critical(
                self,
                'Save Error',
                f'Failed to save case:\n{e}'
            )
            return False

    def _delete_temp_case(self) -> None:
        """Delete temporary case directory."""
        if self.case_path and "temp" in self.case_path:
            try:
                shutil.rmtree(self.case_path, ignore_errors=True)
            except Exception:
                pass

    def _cleanup(self) -> None:
        """Cleanup resources before closing."""
        # Save case data (only if not temp)
        if self.case_data.path and "temp" not in self.case_path:
            self.case_data.save()

        # Cleanup exec widget
        if self.exec_widget:
            self.exec_widget.end()

    def __repr__(self) -> str:
        """String representation."""
        return f"MainWindow(case_path='{self.case_path}')"
