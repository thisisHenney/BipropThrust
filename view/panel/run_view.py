"""
Run View - Handles simulation run logic

This view connects to UI widgets defined in center_form_ui.py
and implements OpenFOAM simulation execution functionality.
"""

import sys
import subprocess
from pathlib import Path

from common.app_data import app_data
from common.case_data import case_data


class RunView:
    """
    Run view.

    Manages simulation execution and monitoring.
    """

    def __init__(self, parent):
        """
        Initialize run view.

        Args:
            parent: CenterWidget instance (contains ui and context)
        """
        self.parent = parent
        self.ui = self.parent.ui
        self.ctx = self.parent.context

        # Get services from context
        self.exec_widget = self.ctx.get("exec")
        self.vtk_pre = self.ctx.get("vtk_pre")
        self.vtk_post = self.ctx.get("vtk_post")

        # Get data instances
        self.app_data = app_data
        self.case_data = case_data

        # Connect signals
        self._init_connect()

    def _init_connect(self):
        """Initialize signal connections."""
        self.ui.button_edit_hostfile_run.clicked.connect(self._on_edit_hostfile_clicked)
        # TODO: Add other button connections (Run, Stop, etc.)

    def _on_edit_hostfile_clicked(self):
        """Handle Edit host file button click - open hosts file in text editor."""
        # Path to hosts file in 5.CHTFCase/system/
        hosts_path = Path(self.case_data.path) / "5.CHTFCase" / "system" / "hosts"

        if not hosts_path.exists():
            print(f"Hosts file not found: {hosts_path}")
            # Create empty hosts file if it doesn't exist
            hosts_path.parent.mkdir(parents=True, exist_ok=True)
            hosts_path.touch()
            print(f"Created hosts file: {hosts_path}")

        # Open with appropriate text editor based on platform
        try:
            if sys.platform == "win32":
                # Windows - use notepad
                subprocess.Popen(["notepad", str(hosts_path)])
                print(f"Opening hosts file with notepad: {hosts_path}")
            else:
                # Linux - use gedit
                subprocess.Popen(["gedit", str(hosts_path)])
                print(f"Opening hosts file with gedit: {hosts_path}")
        except Exception as e:
            print(f"Error opening hosts file: {e}")
            import traceback
            traceback.print_exc()

    def load_data(self):
        """Load run settings and parameters."""
        print("[DEBUG] RunView.load_data() called")
        # TODO: Load run settings from controlDict, etc.
