"""
Post View - Post-processing Visualization Controller

This module manages post-processing visualization of simulation results.
"""

from pathlib import Path

from common.case_data import case_data


class PostView:
    """
    Post-processing view controller.

    Manages loading and displaying simulation results from 5.CHTFCase folder.
    Uses PostprocessWidget (vtk_post) for visualization with:
    - Slice view at Z=0 plane
    - Scalar bar display
    """

    def __init__(self, parent):
        """
        Initialize post view.

        Args:
            parent: Parent widget (CenterWidget)
        """
        self.parent = parent

        # Get VTK post widget from parent (CenterWidget has vtk_post from context)
        self.vtk_post = parent.vtk_post

        # Get case data
        self.case_data = case_data

        # Track if results are loaded
        self._results_loaded = False

        # 케이스 경로 등록 (Refresh 버튼용)
        self._register_case_path()

    def _register_case_path(self):
        """5.CHTFCase 경로를 PostprocessWidget에 등록."""
        if not self.vtk_post or not self.case_data.path:
            return
        chtf_case = Path(self.case_data.path) / "5.CHTFCase"
        self.vtk_post.set_case_path(str(chtf_case))

    def load_results(self) -> bool:
        """
        Load simulation results from 5.CHTFCase folder.

        Configures PostprocessWidget to display:
        - Slice at Z=0 plane
        - Scalar bar

        Returns:
            True if results loaded successfully, False otherwise
        """
        if not self.vtk_post:
            return False

        if not self.case_data.path:
            return False

        # Check if 5.CHTFCase folder exists
        chtf_case = Path(self.case_data.path) / "5.CHTFCase"

        if not chtf_case.exists():
            return False

        # Check for result time folders (numeric folders like 0.001, 0.002, etc.)
        has_results = False
        time_folders = []
        for item in chtf_case.iterdir():
            if item.is_dir():
                try:
                    float(item.name)
                    time_folders.append(item.name)
                    has_results = True
                except ValueError:
                    continue

        if not has_results:
            return False

        # Load OpenFOAM case into vtk_post (직접 케이스 폴더 경로 전달)
        self.vtk_post.load_foam_file(str(chtf_case))

        # Configure slice view (Z=0 plane)
        self._configure_slice()

        # Field selection - commented out, let user select from combo box
        # self._select_temperature_field()
        # self._select_pressure_field()

        # Show scalar bar
        self._show_scalar_bar()

        self._results_loaded = True
        return True

    def _configure_slice(self) -> None:
        """Configure slice view at Z=0 plane."""
        if not self.vtk_post:
            return

        # Enable slice mode
        self.vtk_post.slice_check.setChecked(True)

        # Set axis to Z
        self.vtk_post.axis_combo.setCurrentText("Z")

        # Set position to 0
        self.vtk_post.slice_pos = 0.0
        self.vtk_post._update_slider_position()

    def _select_temperature_field(self) -> None:
        """Select Temperature (T) field for coloring."""
        if not self.vtk_post:
            return

        # Find and select T field
        idx = self.vtk_post.field_combo.findText("T")
        if idx >= 0:
            self.vtk_post.field_combo.setCurrentIndex(idx)

    def _select_pressure_field(self) -> None:
        """Select Pressure (p) field for coloring."""
        if not self.vtk_post:
            return

        # Find and select p field
        idx = self.vtk_post.field_combo.findText("p")
        if idx >= 0:
            self.vtk_post.field_combo.setCurrentIndex(idx)

    def _show_scalar_bar(self) -> None:
        """Show scalar bar for visualization."""
        if not self.vtk_post:
            return

        # Enable scalar bar
        if not self.vtk_post.scalar_bar_visible:
            self.vtk_post._scalar_bar_action.setChecked(True)
            self.vtk_post._on_scalar_bar_toggled(True)

    def is_loaded(self) -> bool:
        """Check if results are currently loaded."""
        return self._results_loaded

    def reload_results(self) -> bool:
        """
        Reload results (force refresh).

        Returns:
            True if results reloaded successfully
        """
        self._results_loaded = False
        return self.load_results()
