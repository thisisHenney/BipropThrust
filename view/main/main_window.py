"""
Main Window - Application Main Window Controller

This module manages the main application window, layout,
and component lifecycle.
"""

import shutil
from pathlib import Path

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QMessageBox
from PySide6.QtCore import Qt

from nextlib.utils.window import center_on_screen
from nextlib.utils.file import copy_files
from nextlib.dialogbox.dialogbox import DirDialogBox

from common.app_data import app_data
from common.case_data import case_data
from common.app_context import AppContext


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

        # Setup UI
        self._setup_ui()
        self._setup_window()

    def _setup_ui(self) -> None:
        """Setup basic UI components."""
        # Create central widget with simple layout for now
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Add a simple label
        label = QLabel(f"{self.app_data.title}\n\nInitializing...")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 16pt; color: #666;")
        layout.addWidget(label)

        self.setCentralWidget(central_widget)

    def _setup_window(self) -> None:
        """Setup window properties."""
        # Set window title (will be updated after case is loaded)
        self.setWindowTitle(self.app_data.title)

        # Set window size
        self.setMinimumSize(650, 450)
        self.resize(1300, 900)

        # Center on screen
        center_on_screen(self)

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
        print(f"Initializing main window with case: {self.case_path}")

        # Load or create case
        if self.case_path:
            self._load_case(self.case_path)
        else:
            print("Warning: No case path provided")

        # Update window title with case path
        self._update_window_title()

        # Update status
        if hasattr(self, 'statusBar'):
            self.statusBar().showMessage('Ready', 3000)

    def _load_case(self, case_path: str) -> None:
        """
        Load a case from the given path.

        Args:
            case_path: Path to case directory
        """
        path = Path(case_path)

        # Check if case exists
        if not path.exists():
            print(f"Case path does not exist, creating: {case_path}")
            self._create_case_from_template(case_path)

        # Set case data path
        self.case_data.set_path(str(path.resolve()))

        # Try to load existing case data
        self.case_data.load()

        print(f"Case loaded: {self.case_data.path}")

    def _create_case_from_template(self, case_path: str) -> None:
        """
        Create a new case from base template.

        Args:
            case_path: Path where case should be created
        """
        # Get base case template path
        base_case_path = self.app_data.get_config_basecase_path()

        if not base_case_path.exists():
            print(f"Warning: Base case template not found: {base_case_path}")
            # Create empty case directory
            Path(case_path).mkdir(parents=True, exist_ok=True)
            return

        # Copy base case to new location
        print(f"Copying base case from {base_case_path} to {case_path}")
        try:
            copy_files(str(base_case_path), case_path)
            print("Base case copied successfully")
        except Exception as e:
            print(f"Error copying base case: {e}")
            # Create empty directory as fallback
            Path(case_path).mkdir(parents=True, exist_ok=True)

    def closeEvent(self, event):
        """
        Handle window close event.

        Args:
            event: Close event
        """
        print("Closing main window...")

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
            print(f"Saving case to: {new_path}")
            copy_files(self.case_path, new_path)

            # Delete temp case
            self._delete_temp_case()

            print(f"Case saved successfully to: {new_path}")
            return True

        except Exception as e:
            print(f"Error saving case: {e}")
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
                print(f"Temporary case deleted: {self.case_path}")
            except Exception as e:
                print(f"Error deleting temp case: {e}")

    def _cleanup(self) -> None:
        """Cleanup resources before closing."""
        # Save case data (only if not temp or already saved)
        if self.case_data.path and "temp" not in self.case_path:
            self.case_data.save()
            print("Case data saved")

        # TODO: Cleanup other resources (VTK, exec, etc.)

    def __repr__(self) -> str:
        """String representation."""
        return f"MainWindow(case_path='{self.case_path}')"
