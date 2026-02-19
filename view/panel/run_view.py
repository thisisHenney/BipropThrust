"""
Run View - Handles simulation run logic

This view connects to UI widgets defined in center_form_ui.py
and implements OpenFOAM simulation execution functionality.
"""

import re
import sys
import subprocess
import traceback
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QFileSystemWatcher, QTimer
from PySide6.QtWidgets import QMessageBox

from nextlib.openfoam.PyFoamCase.foamfile import FoamFile

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
        self.residual_graph = self.ctx.get("residual_graph")

        # Get data instances
        self.app_data = app_data
        self.case_data = case_data

        # File watcher for log.solver
        self._log_watcher = QFileSystemWatcher(self.parent)
        self._log_watcher.fileChanged.connect(self._on_log_file_changed)

        # Timer for periodic log check (fallback for file watcher issues)
        self._log_timer = QTimer(self.parent)
        self._log_timer.timeout.connect(self._check_log_file)
        self._log_check_interval = 2000  # 2 seconds

        # Simulation state
        self._is_running = False
        self._log_file_path = None

        # Connect signals
        self._init_connect()

    def _init_connect(self):
        """Initialize signal connections."""
        self.ui.button_edit_hostfile_run.clicked.connect(self._on_edit_hostfile_clicked)
        self.ui.button_run.clicked.connect(self._on_run_clicked)
        self.ui.button_stop.clicked.connect(self._on_stop_clicked)
        self.ui.button_pause.clicked.connect(self._on_pause_clicked)

        # Disable Stop/Pause buttons initially (enable when running)
        self.ui.button_stop.setEnabled(False)
        self.ui.button_pause.setEnabled(False)

        self.ui.checkBox_host_2.toggled.connect(self._on_hostfile_run_toggled)

        # Connect comboBox_7 to enable/disable comboBox_10
        self.ui.comboBox_7.currentIndexChanged.connect(self._on_combustion_changed)

        # Connect exec_widget signals for process status
        if self.exec_widget:
            self.exec_widget.sig_proc_status.connect(self._on_proc_status_changed)

    def _on_hostfile_run_toggled(self, checked: bool):
        """Save hostfile checkbox state to app_data and enable/disable Edit button."""
        self.app_data.parallel_run_enabled = checked
        self.ui.button_edit_hostfile_run.setEnabled(checked)

    def _highlight_error_widget(self, widget):
        """
        Highlight widget with red border and scroll to it.

        Args:
            widget: QWidget to highlight (typically QLineEdit)
        """
        from PySide6.QtWidgets import QScrollArea

        # Save original stylesheet and widget reference for later restoration
        if not hasattr(self, '_error_highlighted_widget'):
            self._error_highlighted_widget = None
            self._error_original_style = ""

        # Save state
        self._error_highlighted_widget = widget
        self._error_original_style = widget.styleSheet()

        # Apply red border style
        widget.setStyleSheet("border: 2px solid #ff4444; border-radius: 3px;")

        # Find parent scroll area and scroll to widget
        parent = widget.parent()
        while parent is not None:
            if isinstance(parent, QScrollArea):
                parent.ensureWidgetVisible(widget, 50, 50)
                break
            parent = parent.parent()

        # Set focus to the widget and select all text
        widget.setFocus()
        widget.selectAll()

    def _clear_error_highlight(self):
        """Clear error highlighting from previously highlighted widget."""
        if hasattr(self, '_error_highlighted_widget') and self._error_highlighted_widget:
            # Clear inline style and force update
            self._error_highlighted_widget.setStyleSheet("")
            self._error_highlighted_widget.style().unpolish(self._error_highlighted_widget)
            self._error_highlighted_widget.style().polish(self._error_highlighted_widget)
            self._error_highlighted_widget.update()
            self._error_highlighted_widget = None
            self._error_original_style = ""

    def _load_number_of_subdomains(self):
        """Load numberOfSubdomains from 5.CHTFCase/system/decomposeParDict."""
        import os

        # Default value: CPU count / 2
        cpu_count = os.cpu_count() or 4
        default_value = max(1, cpu_count // 2)

        decompose_dict_path = Path(self.case_data.path) / "5.CHTFCase" / "system" / "decomposeParDict"

        if decompose_dict_path.exists():
            try:
                content = decompose_dict_path.read_text()
                match = re.search(r'numberOfSubdomains\s+(\d+)', content)
                if match:
                    self.ui.edit_number_of_subdomains_2.setText(match.group(1))
                    return
            except Exception:
                traceback.print_exc()

        # Set default value if file doesn't exist or couldn't read
        self.ui.edit_number_of_subdomains_2.setText(str(default_value))

    def _update_decompose_par_dict(self, case_path: Path):
        """Update numberOfSubdomains in all decomposeParDict files (main + regions)."""
        try:
            n_procs = int(self.ui.edit_number_of_subdomains_2.text())
        except (ValueError, AttributeError):
            return

        # Find all decomposeParDict files (system/ and system/*/decomposeParDict)
        system_path = case_path / "system"
        if not system_path.exists():
            return

        for dict_path in system_path.rglob("decomposeParDict"):
            try:
                content = dict_path.read_text()
                new_content = re.sub(
                    r'(numberOfSubdomains\s+)\d+',
                    rf'\g<1>{n_procs}',
                    content
                )
                dict_path.write_text(new_content)
            except Exception:
                traceback.print_exc()

    def _on_edit_hostfile_clicked(self):
        """Handle Edit host file button click - open hosts file in text editor."""
        # Path to hosts file in 5.CHTFCase/system/
        hosts_path = Path(self.case_data.path) / "5.CHTFCase" / "system" / "hosts"

        if not hosts_path.exists():
            # Create empty hosts file if it doesn't exist
            hosts_path.parent.mkdir(parents=True, exist_ok=True)
            hosts_path.touch()

        # Open with appropriate text editor based on platform
        try:
            if sys.platform == "win32":
                subprocess.Popen(["notepad", str(hosts_path)])
            else:
                subprocess.Popen(["gedit", str(hosts_path)])
        except Exception:
            traceback.print_exc()

    def _on_combustion_changed(self, index):
        """Handle combustion comboBox_7 change - enable/disable comboBox_10."""
        is_on = (index == 0)
        self.ui.comboBox_10.setEnabled(is_on)

    def _on_stop_clicked(self):
        """Handle Stop button click - stop the running simulation."""
        if self.exec_widget:
            self.exec_widget.stop_process()

        self._is_running = False
        self.ui.button_run.setEnabled(True)
        self.ui.button_run.setText("Run Solver")
        self.ui.button_stop.setEnabled(False)
        self.ui.button_pause.setEnabled(False)
        self.ui.button_mesh_generate.setEnabled(True)  # Re-enable Mesh Generate
        self.ui.button_mesh_stop.setEnabled(False)  # Disable Mesh Stop
        self.ui.edit_run_status.setText("Stopped")
        self.ui.edit_run_finished.setText(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self._stop_log_monitoring()

    def _on_pause_clicked(self):
        """Handle Pause button click - pause/resume the running simulation."""
        if self.exec_widget:
            self.exec_widget.pause_process()

    def _on_proc_status_changed(self, proc_idx: int, cpu_id: int, pid: int, status: str):
        """Handle process status change from exec_widget.

        Args:
            proc_idx: Process index
            cpu_id: CPU ID assigned to process
            pid: Process ID
            status: Status string (e.g., 'Starting', 'Running', 'Waiting')
        """
        # Update process ID display
        if pid > 0:
            self.ui.edit_run_id.setText(str(pid))

        # Update status display
        self.ui.edit_run_status.setText(status)

    def _run_simulation(self):
        """Execute the Allclean/Allrun scripts in 5.CHTFCase folder."""
        try:
            case_path = Path(self.case_data.path) / "5.CHTFCase"
            allclean_path = case_path / "Allclean"
            allrun_path = case_path / "Allrun"

            if not allrun_path.exists():
                return

            # Update decomposeParDict with UI value
            self._update_decompose_par_dict(case_path)

            # Set log file path
            self._log_file_path = case_path / "log.solver"

            # Remove old log file if exists
            if self._log_file_path.exists():
                self._log_file_path.unlink()

            # Set working directory for exec_widget
            self.exec_widget.set_working_path(str(case_path))

            # Register callbacks
            self.exec_widget.set_function_after_finished(self._on_simulation_finished)
            self.exec_widget.set_function_after_error(self._on_simulation_error)
            self.exec_widget.set_function_restore_ui(self._restore_ui_after_run)

            # Create shell wrappers
            shell_wrapper = case_path / "shell_cmd.sh"
            shell_wrapper.write_text('#!/bin/bash\neval "$@"\n', encoding='utf-8')
            shell_wrapper.chmod(0o755)

            of_wrapper = case_path / "of_cmd.sh"
            of_wrapper.write_text(
                '#!/bin/bash\n'
                'source /usr/lib/openfoam/openfoam2212/etc/bashrc\n'
                '. ${WM_PROJECT_DIR}/bin/tools/RunFunctions\n'
                '. ${WM_PROJECT_DIR}/bin/tools/CleanFunctions\n'
                '"$@"\n',
                encoding='utf-8'
            )
            of_wrapper.chmod(0o755)

            # Get parameters
            n_procs = 4
            try:
                n_procs = int(self.ui.edit_number_of_subdomains_2.text())
            except (ValueError, AttributeError):
                pass

            use_hostfile = self.ui.checkBox_host_2.isChecked()
            application = self._get_application(case_path)

            # Parse Allclean/Allrun scripts to build command list
            commands = []
            if allclean_path.exists():
                commands.extend(self._parse_script(allclean_path, n_procs, use_hostfile, application))
            if allrun_path.exists():
                commands.extend(self._parse_script(allrun_path, n_procs, use_hostfile, application))

            if not commands:
                QMessageBox.warning(
                    None, "Run Solver",
                    "Allclean/Allrun files not found or empty in:\n"
                    f"{case_path}"
                )
                return

            # Start simulation
            self._is_running = True
            self.ui.button_run.setEnabled(False)
            self.ui.button_run.setText("Running...")
            self.ui.button_stop.setEnabled(True)
            self.ui.button_pause.setEnabled(True)
            self.ui.button_mesh_generate.setEnabled(False)

            # Update process info display
            self.ui.edit_run_name.setText("Solver")
            self.ui.edit_run_id.setText("-")
            self.ui.edit_run_started.setText(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.ui.edit_run_finished.setText("-")
            self.ui.edit_run_status.setText("Running...")

            # Start log monitoring
            self._start_log_monitoring()

            # Execute commands
            self.exec_widget.run(commands)

        except Exception:
            self._restore_ui_after_run()
            self.ui.edit_run_status.setText("Error")

    def _get_application(self, case_path: Path) -> str:
        """Read application name from controlDict."""
        try:
            control_dict = case_path / "system" / "controlDict"
            if control_dict.exists():
                foam_file = FoamFile(str(control_dict))
                if foam_file.load():
                    app = foam_file.get_value("application")
                    if app:
                        return str(app)
        except Exception:
            traceback.print_exc()
        return "chtMultiRegionFoam"

    def _parse_script(self, script_path: Path, n_procs: int,
                      use_hostfile: bool = False, application: str = "") -> list:
        """Parse Allclean/Allrun script into individual wrapped commands.

        Args:
            script_path: Path to Allclean or Allrun file
            n_procs: Number of parallel processors
            use_hostfile: True to use --hostfile, False for --host localhost
            application: Application name from controlDict

        Returns:
            List of commands wrapped with shell_cmd.sh or of_cmd.sh
        """
        SKIP_PREFIXES = (
            '#!',
            'cd "${0%/*}"',
            '. ${WM_PROJECT_DIR',
        )
        SHELL_CMDS = {'rm', 'cp', 'mkdir', 'mv', 'ls', 'find', 'echo', 'sed'}

        commands = []
        try:
            lines = script_path.read_text(encoding='utf-8').splitlines()
        except Exception:
            return commands

        for raw_line in lines:
            line = raw_line.strip()

            # Skip empty/comment lines
            if not line or line.startswith('#'):
                continue

            # Skip boilerplate
            if any(line.startswith(p) for p in SKIP_PREFIXES):
                continue

            # Remove inline redirection/comments
            line = re.sub(r'>\s*/dev/null.*', '', line).strip()
            line = re.sub(r'#.*$', '', line).strip()
            if not line:
                continue

            # Strip runApplication prefix (handle -s suffix flag)
            if line.startswith('runApplication '):
                line = line[len('runApplication '):]
                # Handle -s suffix flag: runApplication -s suffix command args
                if line.startswith('-s '):
                    parts = line.split(None, 2)  # ['-s', 'suffix', 'command args...']
                    if len(parts) >= 3:
                        line = parts[2]
                    else:
                        continue

            # Convert runParallel to mpirun
            if line.startswith('runParallel '):
                app_and_args = line[len('runParallel '):]
                if use_hostfile:
                    line = f"mpirun -np {n_procs} --hostfile system/hosts {app_and_args} -parallel"
                else:
                    line = f"mpirun -np {n_procs} --host localhost --oversubscribe {app_and_args} -parallel"

            # Substitute getNumberOfProcessors
            line = line.replace('`getNumberOfProcessors`', str(n_procs))
            line = line.replace('$(getNumberOfProcessors)', str(n_procs))

            # Substitute getApplication
            if application:
                line = line.replace('`getApplication`', application)
                line = line.replace('$(getApplication)', application)

            # Handle mpirun hostfile options
            if 'mpirun' in line:
                if use_hostfile:
                    if '--host localhost' in line:
                        line = line.replace('--host localhost --oversubscribe', '--hostfile system/hosts')
                else:
                    if '--hostfile system/hosts' in line:
                        line = line.replace('--hostfile system/hosts', '--host localhost --oversubscribe')

            # Classify: shell command vs OpenFOAM command
            first_word = line.split()[0]
            if first_word in SHELL_CMDS:
                commands.append(f"./shell_cmd.sh {line}")
            else:
                commands.append(f"./of_cmd.sh {line}")

        return commands

    def _start_log_monitoring(self):
        """Start monitoring log.solver file for residuals."""
        self._log_timer.start(self._log_check_interval)

    def _stop_log_monitoring(self):
        """Stop monitoring log.solver file."""
        self._log_timer.stop()

        # Remove file from watcher
        if self._log_file_path and str(self._log_file_path) in self._log_watcher.files():
            self._log_watcher.removePath(str(self._log_file_path))

    def _check_log_file(self):
        """Periodically check if log.solver exists and update graph."""
        if not self._log_file_path:
            return

        if self._log_file_path.exists():
            # Add to file watcher if not already watching
            log_path_str = str(self._log_file_path)
            if log_path_str not in self._log_watcher.files():
                self._log_watcher.addPath(log_path_str)

            # Update residual graph
            self._update_residual_graph()

    def _on_log_file_changed(self, path: str):
        """Handle log file changes."""
        self._update_residual_graph()

    def _update_residual_graph(self):
        """Update residual graph with latest log data."""
        if not self._log_file_path or not self._log_file_path.exists():
            return

        if self.residual_graph:
            try:
                self.residual_graph.load_file(str(self._log_file_path))
            except Exception:
                traceback.print_exc()

    def _on_simulation_finished(self):
        """Handle simulation completion."""
        self._is_running = False
        self._stop_log_monitoring()
        self._update_residual_graph()
        self.ui.button_run.setEnabled(True)
        self.ui.button_run.setText("Run Solver")
        self.ui.button_stop.setEnabled(False)
        self.ui.button_pause.setEnabled(False)
        self.ui.button_mesh_generate.setEnabled(True)  # Re-enable Mesh Generate
        self.ui.edit_run_status.setText("Finished")
        self.ui.edit_run_finished.setText(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def _on_simulation_error(self):
        """Handle simulation error."""
        self._is_running = False
        self._stop_log_monitoring()
        self.ui.button_run.setEnabled(True)
        self.ui.button_run.setText("Run Solver")
        self.ui.button_stop.setEnabled(False)
        self.ui.button_pause.setEnabled(False)
        self.ui.button_mesh_generate.setEnabled(True)  # Re-enable Mesh Generate
        self.ui.edit_run_status.setText("Error")
        self.ui.edit_run_finished.setText(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def _restore_ui_after_run(self):
        """Restore UI after simulation ends."""
        self._is_running = False
        self.ui.button_run.setEnabled(True)
        self.ui.button_run.setText("Run Solver")
        self.ui.button_stop.setEnabled(False)
        self.ui.button_pause.setEnabled(False)
        self.ui.button_mesh_generate.setEnabled(True)  # Re-enable Mesh Generate

        # Update status to show completion
        self.ui.edit_run_status.setText("Ready")
        self.ui.edit_run_finished.setText(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        self._stop_log_monitoring()
        self._update_residual_graph()

    def _on_run_clicked(self):
        """Handle Run button click - update settings and start simulation."""
        import os

        if self._is_running:
            return

        # Clear any previous error highlighting first
        self._clear_error_highlight()

        # Validate CPU count
        try:
            n_procs = int(self.ui.edit_number_of_subdomains_2.text())
            cpu_count = os.cpu_count() or 1
            if n_procs > cpu_count:
                self._highlight_error_widget(self.ui.edit_number_of_subdomains_2)
                QMessageBox.critical(
                    self.parent,
                    "Error",
                    f"Number of Subdomains ({n_procs}) exceeds available CPU count ({cpu_count}).\n\n"
                    f"Please reduce the value to {cpu_count} or less."
                )
                return
        except (ValueError, AttributeError):
            pass

        if not self._update_run_settings():
            return

        self._run_simulation()

    def _update_run_settings(self) -> bool:
        """Update all run-related settings to OpenFOAM files."""
        try:
            case_path = Path(self.case_data.path) / "5.CHTFCase" / "constant" / "fluid"

            # Update turbulenceProperties
            self._update_turbulence_properties(case_path)

            # Update surfaceFilmProperties
            self._update_surface_film_properties(case_path)

            # Update combustionProperties
            self._update_combustion_properties(case_path)

            # Update thermophysicalProperties (CHEMKINFile)
            self._update_thermophysical_properties(case_path)

            # Update fluid initial conditions (p, T, U)
            orig_path = Path(self.case_data.path) / "5.CHTFCase" / "0.orig"
            self._update_fluid_initial_conditions(orig_path / "fluid")

            # Update solid initial conditions (T files in non-fluid folders)
            self._update_solid_initial_conditions(orig_path)

            # Update spray cloud properties
            self._update_spray_mmh_properties(case_path)
            self._update_spray_nto_properties(case_path)

            # Update numerical schemes (fvSchemes and fvSolution)
            system_path = Path(self.case_data.path) / "5.CHTFCase" / "system" / "fluid"
            self._update_fv_schemes(system_path)
            self._update_fv_solution(system_path)

            # Update controlDict (in system folder, not fluid)
            system_root = Path(self.case_data.path) / "5.CHTFCase" / "system"
            self._update_control_dict(system_root)

            return True

        except Exception:
            traceback.print_exc()
            return False

    def _update_turbulence_properties(self, case_path: Path):
        """Update turbulenceProperties with RAS.RASModel from comboBox_2."""
        try:
            file_path = case_path / "turbulenceProperties"
            if not file_path.exists():
                return

            foam_file = FoamFile(str(file_path))
            if not foam_file.load():
                return

            # Get selected RAS model from comboBox_2
            ras_model = self.ui.comboBox_2.currentText().strip()
            foam_file.set_value("RAS.RASModel", ras_model)
            foam_file.save()

        except Exception:
            traceback.print_exc()
    def _update_surface_film_properties(self, case_path: Path):
        """Update surfaceFilmProperties with surfaceFilmModel and phaseChangeModel."""
        try:
            file_path = case_path / "surfaceFilmProperties"
            if not file_path.exists():
                return

            foam_file = FoamFile(str(file_path))
            if not foam_file.load():
                return

            # comboBox_3: surfaceFilmModel (On=thermoSingleLayer, Off=none)
            is_film_on = (self.ui.comboBox_3.currentIndex() == 0)
            film_model = "thermoSingleLayer" if is_film_on else "none"
            foam_file.set_value("surfaceFilmModel", film_model)

            # comboBox_4: phaseChangeModel (On=standardPhaseChange, Off=none)
            is_phase_on = (self.ui.comboBox_4.currentIndex() == 0)
            phase_model = "standardPhaseChange" if is_phase_on else "none"
            foam_file.set_value("thermoSingleLayerCoeffs.phaseChangeModel", phase_model)

            foam_file.save()

        except Exception:
            traceback.print_exc()
    def _update_combustion_properties(self, case_path: Path):
        """Update combustionProperties with combustionModel from comboBox_7."""
        try:
            file_path = case_path / "combustionProperties"
            if not file_path.exists():
                return

            foam_file = FoamFile(str(file_path))
            if not foam_file.load():
                return

            # comboBox_7: combustionModel (On=laminar, Off=none)
            is_combustion_on = (self.ui.comboBox_7.currentIndex() == 0)
            combustion_model = "laminar" if is_combustion_on else "none"
            foam_file.set_value("combustionModel", combustion_model)
            foam_file.save()

        except Exception:
            traceback.print_exc()
    def _update_thermophysical_properties(self, case_path: Path):
        """Update thermophysicalProperties CHEMKINFile and thermo type."""
        try:
            file_path = case_path / "thermophysicalProperties"
            if not file_path.exists():
                return

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Update CHEMKINFile only if combustion is on (comboBox_10 is enabled)
            if self.ui.comboBox_10.isEnabled():
                # Map comboBox_10 selection to CHEMKIN file
                selection = self.ui.comboBox_10.currentText()
                if selection == "31Reaction":
                    chemkin_file = "chem_ARLRM31N.inp"
                elif selection == "31Reaction+global":
                    chemkin_file = "chem_ARLRM31NS.inp"
                elif selection == "51Reaction":
                    chemkin_file = "chem_Global5S.inp"
                else:
                    chemkin_file = None

                if chemkin_file:
                    # Pattern to match CHEMKINFile line
                    pattern = r'(CHEMKINFile\s+"\<case\>/chemkin/)[\w\.]+(")'
                    replacement = rf'\g<1>{chemkin_file}\2'
                    content = re.sub(pattern, replacement, content)

            # Update thermoType.thermo from comboBox_6
            thermo_text = self.ui.comboBox_6.currentText().strip()
            if thermo_text == "NASA polynomial":
                thermo_value = "janaf"
            elif thermo_text:
                thermo_value = thermo_text
            else:
                thermo_value = None

            if thermo_value:
                # Pattern to match thermo value in thermoType block
                content = re.sub(
                    r'(thermo\s+)\w+(\s*;)',
                    rf'\g<1>{thermo_value}\2',
                    content
                )

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

        except Exception:
            traceback.print_exc()
    def load_data(self):
        """Load run settings and parameters."""

        # Restore hostfile checkbox from app_data and sync Edit button
        self.ui.checkBox_host_2.setChecked(self.app_data.parallel_run_enabled)
        self.ui.button_edit_hostfile_run.setEnabled(self.app_data.parallel_run_enabled)

        # Load numberOfSubdomains from decomposeParDict
        self._load_number_of_subdomains()

        # Load settings from OpenFOAM files
        self._load_run_settings()

        # Sync comboBox_10 enabled state with comboBox_7
        is_combustion_on = (self.ui.comboBox_7.currentIndex() == 0)
        self.ui.comboBox_10.setEnabled(is_combustion_on)

    def _load_run_settings(self):
        """Load run settings from OpenFOAM files to UI."""
        try:
            case_path = Path(self.case_data.path) / "5.CHTFCase" / "constant" / "fluid"

            # Load turbulenceProperties
            self._load_turbulence_properties(case_path)

            # Load surfaceFilmProperties
            self._load_surface_film_properties(case_path)

            # Load combustionProperties
            self._load_combustion_properties(case_path)

            # Load thermophysicalProperties
            self._load_thermophysical_properties(case_path)

            # Load fluid initial conditions (p, T, U)
            orig_path = Path(self.case_data.path) / "5.CHTFCase" / "0.orig"
            self._load_fluid_initial_conditions(orig_path / "fluid")

            # Load solid initial conditions (T files)
            self._load_solid_initial_conditions(orig_path)

            # Load spray cloud properties
            self._load_spray_mmh_properties(case_path)
            self._load_spray_nto_properties(case_path)

            # Load numerical schemes (fvSchemes and fvSolution)
            system_path = Path(self.case_data.path) / "5.CHTFCase" / "system" / "fluid"
            self._load_fv_schemes(system_path)
            self._load_fv_solution(system_path)

            # Load controlDict (in system folder, not fluid)
            system_root = Path(self.case_data.path) / "5.CHTFCase" / "system"
            self._load_control_dict(system_root)

        except Exception:
            traceback.print_exc()
    def _load_turbulence_properties(self, case_path: Path):
        """Load RAS.RASModel from turbulenceProperties to comboBox_2."""
        try:
            file_path = case_path / "turbulenceProperties"
            if not file_path.exists():
                return

            foam_file = FoamFile(str(file_path))
            if not foam_file.load():
                return

            ras_model = foam_file.get_value("RAS.RASModel")
            if ras_model:
                ras_model = str(ras_model).strip()
                # Find matching item in comboBox_2
                for i in range(self.ui.comboBox_2.count()):
                    if self.ui.comboBox_2.itemText(i).strip() == ras_model:
                        self.ui.comboBox_2.setCurrentIndex(i)
                        break

        except Exception:
            traceback.print_exc()
    def _load_surface_film_properties(self, case_path: Path):
        """Load surfaceFilmModel and phaseChangeModel from surfaceFilmProperties."""
        try:
            file_path = case_path / "surfaceFilmProperties"
            if not file_path.exists():
                return

            foam_file = FoamFile(str(file_path))
            if not foam_file.load():
                return

            # surfaceFilmModel -> comboBox_3
            film_model = foam_file.get_value("surfaceFilmModel")
            if film_model:
                # On (thermoSingleLayer) = index 0, Off (none) = index 1
                is_on = (str(film_model).strip() == "thermoSingleLayer")
                self.ui.comboBox_3.setCurrentIndex(0 if is_on else 1)

            # phaseChangeModel -> comboBox_4
            phase_model = foam_file.get_value("thermoSingleLayerCoeffs.phaseChangeModel")
            if phase_model:
                is_on = (str(phase_model).strip() == "standardPhaseChange")
                self.ui.comboBox_4.setCurrentIndex(0 if is_on else 1)

        except Exception:
            traceback.print_exc()
    def _load_combustion_properties(self, case_path: Path):
        """Load combustionModel from combustionProperties to comboBox_7."""
        try:
            file_path = case_path / "combustionProperties"
            if not file_path.exists():
                return

            foam_file = FoamFile(str(file_path))
            if not foam_file.load():
                return

            combustion_model = foam_file.get_value("combustionModel")
            if combustion_model:
                # On (laminar) = index 0, Off (none) = index 1
                is_on = (str(combustion_model).strip() == "laminar")
                self.ui.comboBox_7.setCurrentIndex(0 if is_on else 1)

        except Exception:
            traceback.print_exc()
    def _load_thermophysical_properties(self, case_path: Path):
        """Load CHEMKINFile and thermo type from thermophysicalProperties."""
        try:
            file_path = case_path / "thermophysicalProperties"
            if not file_path.exists():
                return

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract CHEMKIN file name
            pattern = r'CHEMKINFile\s+"\<case\>/chemkin/([\w\.]+)"'
            match = re.search(pattern, content)

            if match:
                chemkin_file = match.group(1)
                # Map to comboBox_10 index
                if chemkin_file == "chem_ARLRM31N.inp":
                    self.ui.comboBox_10.setCurrentIndex(0)  # 31Reaction
                elif chemkin_file == "chem_ARLRM31NS.inp":
                    self.ui.comboBox_10.setCurrentIndex(1)  # 31Reaction+global
                elif chemkin_file == "chem_Global5S.inp":
                    self.ui.comboBox_10.setCurrentIndex(2)  # 51Reaction

            # Extract thermoType.thermo value
            thermo_match = re.search(r'thermo\s+(\w+)\s*;', content)
            if thermo_match:
                thermo_value = thermo_match.group(1)
                # Map file value to UI text
                if thermo_value == "janaf":
                    self._set_combo_text(self.ui.comboBox_6, "NASA polynomial")
                else:
                    # If not janaf, clear the combobox or try to find match
                    found = False
                    for i in range(self.ui.comboBox_6.count()):
                        if self.ui.comboBox_6.itemText(i).strip() == thermo_value:
                            self.ui.comboBox_6.setCurrentIndex(i)
                            found = True
                            break
                    if not found:
                        self.ui.comboBox_6.setCurrentIndex(-1)  # Clear/empty

        except Exception:
            traceback.print_exc()
    def _update_fluid_initial_conditions(self, fluid_path: Path):
        """Update fluid initial conditions (p, T, U files)."""
        try:
            if not fluid_path.exists():
                return

            # Update p file - pressure
            p_file = fluid_path / "p"
            if p_file.exists():
                pressure = float(self.ui.edit_fluid_1.text() or "1")
                # If value is 1, multiply by 100000
                if pressure == 1:
                    pressure = 100000
                self._update_internal_field_scalar(p_file, pressure)

            # Update T file - temperature
            t_file = fluid_path / "T"
            if t_file.exists():
                temperature = float(self.ui.edit_fluid_2.text() or "310")
                self._update_internal_field_scalar(t_file, temperature)

            # Update U file - velocity
            u_file = fluid_path / "U"
            if u_file.exists():
                vx = float(self.ui.edit_fluid_v_x.text() or "0")
                vy = float(self.ui.edit_fluid_v_y.text() or "0")
                vz = float(self.ui.edit_fluid_v_z.text() or "0")
                self._update_internal_field_vector(u_file, vx, vy, vz)

        except Exception:
            traceback.print_exc()
    def _update_internal_field_scalar(self, file_path: Path, value):
        """Update internalField uniform scalar value using regex."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Pattern: internalField uniform NUMBER;
        pattern = r'(internalField\s+uniform\s+)[\d\.eE\+\-]+(\s*;)'
        replacement = rf'\g<1>{value}\2'
        new_content = re.sub(pattern, replacement, content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

    def _update_internal_field_vector(self, file_path: Path, x, y, z):
        """Update internalField uniform vector value using regex."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Pattern: internalField uniform (x y z);
        pattern = r'(internalField\s+uniform\s+\()[\d\.eE\+\-\s]+(\)\s*;)'
        replacement = rf'\g<1>{x} {y} {z}\2'
        new_content = re.sub(pattern, replacement, content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

    def _update_solid_initial_conditions(self, orig_path: Path):
        """Update solid initial conditions (T files in all non-fluid folders)."""
        try:
            if not orig_path.exists():
                return

            # Get UI values
            solid_temp = float(self.ui.edit_solid_1.text() or "300")
            solid_h = self.ui.edit_solid_2.text() or "1000"
            solid_type = self.ui.comboBox_9.currentText()

            # Find all solid folders (exclude fluid and filmRegion)
            excluded_folders = {"fluid", "filmRegion"}
            solid_folders = [
                d for d in orig_path.iterdir()
                if d.is_dir() and d.name not in excluded_folders
            ]

            for solid_folder in solid_folders:
                t_file = solid_folder / "T"
                if t_file.exists():
                    self._update_solid_t_file(t_file, solid_folder.name, solid_temp, solid_h, solid_type)

        except Exception:
            traceback.print_exc()
    def _update_solid_t_file(self, file_path: Path, solid_name: str, temp: float, h_value: str, bc_type: str):
        """Update solid T file with temperature, h value, and boundary type."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update internalField uniform temperature
        pattern = r'(internalField\s+uniform\s+)[\d\.eE\+\-]+(\s*;)'
        replacement = rf'\g<1>{temp}\2'
        content = re.sub(pattern, replacement, content)

        # Update boundaryField.solid_name.h uniform value
        # Pattern: solid_name { ... h uniform VALUE; ... }
        h_pattern = rf'({solid_name}\s*\{{[^}}]*h\s+uniform\s+)[\d\.eE\+\-]+(\s*;)'
        h_replacement = rf'\g<1>{h_value}\2'
        content = re.sub(h_pattern, h_replacement, content, flags=re.DOTALL)

        # Update boundaryField.solid_name.type value
        type_pattern = rf'({solid_name}\s*\{{\s*type\s+)\w+(\s*;)'
        type_replacement = rf'\g<1>{bc_type}\2'
        content = re.sub(type_pattern, type_replacement, content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _load_fluid_initial_conditions(self, fluid_path: Path):
        """Load fluid initial conditions (p, T, U files) to UI."""
        try:
            if not fluid_path.exists():
                return

            # Load p file - pressure
            p_file = fluid_path / "p"
            if p_file.exists():
                value = self._read_internal_field_scalar(p_file)
                if value is not None:
                    # Convert to display value (if >= 100000, show as value/100000 if it equals 1)
                    display_value = value
                    if value == 100000:
                        display_value = 1
                    self.ui.edit_fluid_1.setText(str(display_value))

            # Load T file - temperature
            t_file = fluid_path / "T"
            if t_file.exists():
                value = self._read_internal_field_scalar(t_file)
                if value is not None:
                    self.ui.edit_fluid_2.setText(str(int(value)))

            # Load U file - velocity
            u_file = fluid_path / "U"
            if u_file.exists():
                vx, vy, vz = self._read_internal_field_vector(u_file)
                if vx is not None:
                    self.ui.edit_fluid_v_x.setText(str(vx))
                    self.ui.edit_fluid_v_y.setText(str(vy))
                    self.ui.edit_fluid_v_z.setText(str(vz))

        except Exception:
            traceback.print_exc()
    def _read_internal_field_scalar(self, file_path: Path):
        """Read internalField uniform scalar value."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            pattern = r'internalField\s+uniform\s+([\d\.eE\+\-]+)\s*;'
            match = re.search(pattern, content)
            if match:
                return float(match.group(1))
        except Exception:
            traceback.print_exc()
        return None

    def _read_internal_field_vector(self, file_path: Path):
        """Read internalField uniform vector value."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            pattern = r'internalField\s+uniform\s+\(\s*([\d\.eE\+\-]+)\s+([\d\.eE\+\-]+)\s+([\d\.eE\+\-]+)\s*\)\s*;'
            match = re.search(pattern, content)
            if match:
                return float(match.group(1)), float(match.group(2)), float(match.group(3))
        except Exception:
            traceback.print_exc()
        return None, None, None

    def _load_solid_initial_conditions(self, orig_path: Path):
        """Load solid initial conditions from first solid folder's T file."""
        try:
            if not orig_path.exists():
                return

            # Find first solid folder (exclude fluid and filmRegion)
            excluded_folders = {"fluid", "filmRegion"}
            solid_folders = [
                d for d in orig_path.iterdir()
                if d.is_dir() and d.name not in excluded_folders
            ]

            if not solid_folders:
                return

            # Use first solid folder as reference
            first_solid = solid_folders[0]
            t_file = first_solid / "T"

            if not t_file.exists():
                return

            with open(t_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Load internalField temperature
            temp_pattern = r'internalField\s+uniform\s+([\d\.eE\+\-]+)\s*;'
            temp_match = re.search(temp_pattern, content)
            if temp_match:
                self.ui.edit_solid_1.setText(str(int(float(temp_match.group(1)))))

            # Load h uniform value from boundaryField.solid_name section
            solid_name = first_solid.name
            h_pattern = rf'{solid_name}\s*\{{[^}}]*h\s+uniform\s+([\d\.eE\+\-]+)\s*;'
            h_match = re.search(h_pattern, content, re.DOTALL)
            if h_match:
                self.ui.edit_solid_2.setText(h_match.group(1))

            # Load type from boundaryField.solid_name section
            type_pattern = rf'{solid_name}\s*\{{\s*type\s+(\w+)\s*;'
            type_match = re.search(type_pattern, content)
            if type_match:
                bc_type = type_match.group(1)
                # Find matching item in comboBox_9
                for i in range(self.ui.comboBox_9.count()):
                    if self.ui.comboBox_9.itemText(i) == bc_type:
                        self.ui.comboBox_9.setCurrentIndex(i)
                        break

        except Exception:
            traceback.print_exc()
    def _update_spray_mmh_properties(self, case_path: Path):
        """Update sprayMMHCloudProperties with spray settings from UI."""
        try:
            file_path = case_path / "sprayMMHCloudProperties"
            if not file_path.exists():
                return

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Get UI values
            mass_total = self.ui.edit_spray_mmh_1.text() or "1.4170e-4"
            duration = self.ui.edit_spray_mmh_2.text() or "1.0e-1"
            umag = self.ui.edit_spray_mmh_3.text() or "34"
            parcels_per_sec = self.ui.edit_spray_mmh_4.text() or "5000000"

            # Size distribution value: multiply by 1e-6
            size_value = float(self.ui.edit_spray_mmh_5.text() or "26.5")
            size_value_converted = f"{size_value}e-6"

            pos_x = self.ui.edit_spray_mmh_6.text() or "0.0001"
            pos_y = self.ui.edit_spray_mmh_7.text() or "0.0"
            pos_z = self.ui.edit_spray_mmh_8.text() or "0.0"

            dir_x = self.ui.edit_spray_mmh_9.text() or "1"
            dir_y = self.ui.edit_spray_mmh_10.text() or "0"
            dir_z = self.ui.edit_spray_mmh_11.text() or "0"

            outer_dia = self.ui.edit_spray_mmh_12.text() or "5.8e-4"
            inner_dia = self.ui.edit_spray_mmh_13.text() or "0"

            # Update values using regex
            content = re.sub(r'(massTotal\s+)[\d\.eE\+\-]+(\s*;)', rf'\g<1>{mass_total}\2', content)
            content = re.sub(r'(duration\s+)[\d\.eE\+\-]+(\s*;)', rf'\g<1>{duration}\2', content)
            content = re.sub(r'(UMag\s+)[\d\.eE\+\-]+(\s*;)', rf'\g<1>{umag}\2', content)
            content = re.sub(r'(parcelsPerSecond\s+)[\d\.eE\+\-]+(\s*;)', rf'\g<1>{parcels_per_sec}\2', content)
            content = re.sub(r'(fixedValueDistribution\s*\{\s*value\s+)[\d\.eE\+\-]+(\s*;)', rf'\g<1>{size_value_converted}\2', content)
            content = re.sub(r'(position\s+\()[^\)]+(\)\s*;)', rf'\g<1>{pos_x} {pos_y} {pos_z}\2', content)
            content = re.sub(r'(direction\s+\()[^\)]+(\)\s*;)', rf'\g<1>{dir_x} {dir_y} {dir_z}\2', content)
            content = re.sub(r'(outerDiameter\s+)[\d\.eE\+\-]+(\s*;)', rf'\g<1>{outer_dia}\2', content)
            content = re.sub(r'(innerDiameter\s+)[\d\.eE\+\-]+(\s*;)', rf'\g<1>{inner_dia}\2', content)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

        except Exception:
            traceback.print_exc()
    def _update_spray_nto_properties(self, case_path: Path):
        """Update sprayNTOCloudProperties with spray settings from UI."""
        try:
            file_path = case_path / "sprayNTOCloudProperties"
            if not file_path.exists():
                return

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Get UI values
            mass_total = self.ui.edit_spray_nto_1.text() or "1.4170e-4"
            duration = self.ui.edit_spray_nto_2.text() or "1.0e-1"
            umag = self.ui.edit_spray_nto_3.text() or "34"
            parcels_per_sec = self.ui.edit_spray_nto_4.text() or "5000000"

            # Size distribution value: multiply by 1e-6
            size_value = float(self.ui.edit_spray_nto_5.text() or "26.5")
            size_value_converted = f"{size_value}e-6"

            pos_x = self.ui.edit_spray_nto_6.text() or "0.0001"
            pos_y = self.ui.edit_spray_nto_7.text() or "0.0"
            pos_z = self.ui.edit_spray_nto_8.text() or "0.0"

            dir_x = self.ui.edit_spray_nto_9.text() or "1"
            dir_y = self.ui.edit_spray_nto_10.text() or "0"
            dir_z = self.ui.edit_spray_nto_11.text() or "0"

            outer_dia = self.ui.edit_spray_nto_12.text() or "5.8e-4"
            inner_dia = self.ui.edit_spray_nto_13.text() or "0"

            # Update values using regex
            content = re.sub(r'(massTotal\s+)[\d\.eE\+\-]+(\s*;)', rf'\g<1>{mass_total}\2', content)
            content = re.sub(r'(duration\s+)[\d\.eE\+\-]+(\s*;)', rf'\g<1>{duration}\2', content)
            content = re.sub(r'(UMag\s+)[\d\.eE\+\-]+(\s*;)', rf'\g<1>{umag}\2', content)
            content = re.sub(r'(parcelsPerSecond\s+)[\d\.eE\+\-]+(\s*;)', rf'\g<1>{parcels_per_sec}\2', content)
            content = re.sub(r'(fixedValueDistribution\s*\{\s*value\s+)[\d\.eE\+\-]+(\s*;)', rf'\g<1>{size_value_converted}\2', content)
            content = re.sub(r'(position\s+\()[^\)]+(\)\s*;)', rf'\g<1>{pos_x} {pos_y} {pos_z}\2', content)
            content = re.sub(r'(direction\s+\()[^\)]+(\)\s*;)', rf'\g<1>{dir_x} {dir_y} {dir_z}\2', content)
            content = re.sub(r'(outerDiameter\s+)[\d\.eE\+\-]+(\s*;)', rf'\g<1>{outer_dia}\2', content)
            content = re.sub(r'(innerDiameter\s+)[\d\.eE\+\-]+(\s*;)', rf'\g<1>{inner_dia}\2', content)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

        except Exception:
            traceback.print_exc()
    def _load_spray_mmh_properties(self, case_path: Path):
        """Load sprayMMHCloudProperties settings to UI."""
        try:
            file_path = case_path / "sprayMMHCloudProperties"
            if not file_path.exists():
                return

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Load massTotal
            match = re.search(r'massTotal\s+([\d\.eE\+\-]+)\s*;', content)
            if match:
                self.ui.edit_spray_mmh_1.setText(match.group(1))

            # Load duration
            match = re.search(r'duration\s+([\d\.eE\+\-]+)\s*;', content)
            if match:
                self.ui.edit_spray_mmh_2.setText(match.group(1))

            # Load UMag
            match = re.search(r'UMag\s+([\d\.eE\+\-]+)\s*;', content)
            if match:
                self.ui.edit_spray_mmh_3.setText(match.group(1))

            # Load parcelsPerSecond
            match = re.search(r'parcelsPerSecond\s+([\d\.eE\+\-]+)\s*;', content)
            if match:
                self.ui.edit_spray_mmh_4.setText(match.group(1))

            # Load sizeDistribution value (convert from scientific notation)
            match = re.search(r'fixedValueDistribution\s*\{\s*value\s+([\d\.eE\+\-]+)\s*;', content)
            if match:
                value = float(match.group(1))
                # Convert from e-6 to display value
                display_value = value * 1e6
                self.ui.edit_spray_mmh_5.setText(str(display_value))

            # Load position
            match = re.search(r'position\s+\(\s*([\d\.eE\+\-]+)\s+([\d\.eE\+\-]+)\s+([\d\.eE\+\-]+)\s*\)', content)
            if match:
                self.ui.edit_spray_mmh_6.setText(match.group(1))
                self.ui.edit_spray_mmh_7.setText(match.group(2))
                self.ui.edit_spray_mmh_8.setText(match.group(3))

            # Load direction
            match = re.search(r'direction\s+\(\s*([\d\.eE\+\-]+)\s+([\d\.eE\+\-]+)\s+([\d\.eE\+\-]+)\s*\)', content)
            if match:
                self.ui.edit_spray_mmh_9.setText(match.group(1))
                self.ui.edit_spray_mmh_10.setText(match.group(2))
                self.ui.edit_spray_mmh_11.setText(match.group(3))

            # Load outerDiameter
            match = re.search(r'outerDiameter\s+([\d\.eE\+\-]+)\s*;', content)
            if match:
                self.ui.edit_spray_mmh_12.setText(match.group(1))

            # Load innerDiameter
            match = re.search(r'innerDiameter\s+([\d\.eE\+\-]+)\s*;', content)
            if match:
                self.ui.edit_spray_mmh_13.setText(match.group(1))

        except Exception:
            traceback.print_exc()
    def _load_spray_nto_properties(self, case_path: Path):
        """Load sprayNTOCloudProperties settings to UI."""
        try:
            file_path = case_path / "sprayNTOCloudProperties"
            if not file_path.exists():
                return

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Load massTotal
            match = re.search(r'massTotal\s+([\d\.eE\+\-]+)\s*;', content)
            if match:
                self.ui.edit_spray_nto_1.setText(match.group(1))

            # Load duration
            match = re.search(r'duration\s+([\d\.eE\+\-]+)\s*;', content)
            if match:
                self.ui.edit_spray_nto_2.setText(match.group(1))

            # Load UMag
            match = re.search(r'UMag\s+([\d\.eE\+\-]+)\s*;', content)
            if match:
                self.ui.edit_spray_nto_3.setText(match.group(1))

            # Load parcelsPerSecond
            match = re.search(r'parcelsPerSecond\s+([\d\.eE\+\-]+)\s*;', content)
            if match:
                self.ui.edit_spray_nto_4.setText(match.group(1))

            # Load sizeDistribution value (convert from scientific notation)
            match = re.search(r'fixedValueDistribution\s*\{\s*value\s+([\d\.eE\+\-]+)\s*;', content)
            if match:
                value = float(match.group(1))
                # Convert from e-6 to display value
                display_value = value * 1e6
                self.ui.edit_spray_nto_5.setText(str(display_value))

            # Load position
            match = re.search(r'position\s+\(\s*([\d\.eE\+\-]+)\s+([\d\.eE\+\-]+)\s+([\d\.eE\+\-]+)\s*\)', content)
            if match:
                self.ui.edit_spray_nto_6.setText(match.group(1))
                self.ui.edit_spray_nto_7.setText(match.group(2))
                self.ui.edit_spray_nto_8.setText(match.group(3))

            # Load direction
            match = re.search(r'direction\s+\(\s*([\d\.eE\+\-]+)\s+([\d\.eE\+\-]+)\s+([\d\.eE\+\-]+)\s*\)', content)
            if match:
                self.ui.edit_spray_nto_9.setText(match.group(1))
                self.ui.edit_spray_nto_10.setText(match.group(2))
                self.ui.edit_spray_nto_11.setText(match.group(3))

            # Load outerDiameter
            match = re.search(r'outerDiameter\s+([\d\.eE\+\-]+)\s*;', content)
            if match:
                self.ui.edit_spray_nto_12.setText(match.group(1))

            # Load innerDiameter
            match = re.search(r'innerDiameter\s+([\d\.eE\+\-]+)\s*;', content)
            if match:
                self.ui.edit_spray_nto_13.setText(match.group(1))

        except Exception:
            traceback.print_exc()
    def _update_fv_schemes(self, system_path: Path):
        """Update fvSchemes with numerical scheme settings from UI."""
        try:
            file_path = system_path / "fvSchemes"
            if not file_path.exists():
                return

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # combo_numerical_1 → ddtSchemes.default
            ddt_scheme = self.ui.combo_numerical_1.currentText().strip()
            # Map UI text to file value
            if ddt_scheme == "Steady":
                ddt_scheme = "steadyState"
            content = re.sub(
                r'(ddtSchemes\s*\{\s*default\s+)\w+(\s*;)',
                rf'\g<1>{ddt_scheme}\2',
                content
            )

            # combo_numerical_2 → defaultAdvSchemeV (for U)
            adv_scheme_v = self.ui.combo_numerical_2.currentText().strip()
            content = re.sub(
                r'(defaultAdvSchemeV\s+)\w+(\s*;)',
                rf'\g<1>{adv_scheme_v}\2',
                content
            )

            # combo_numerical_3 → defaultAdvScheme (for h, K, etc.)
            adv_scheme = self.ui.combo_numerical_3.currentText().strip()
            content = re.sub(
                r'(defaultAdvScheme\s+)\w+(\s*;)',
                rf'\g<1>{adv_scheme}\2',
                content
            )

            # combo_numerical_4 → div(phi,k/omega/epsilon) turbulence schemes
            turb_scheme = self.ui.combo_numerical_4.currentText().strip()
            # Update k, omega, epsilon lines
            content = re.sub(
                r'(div\(phi,k\)\s+Gauss\s+)\w+(\s*;)',
                rf'\g<1>{turb_scheme}\2',
                content
            )
            content = re.sub(
                r'(div\(phi,omega\)\s+Gauss\s+)\w+(\s*;)',
                rf'\g<1>{turb_scheme}\2',
                content
            )
            content = re.sub(
                r'(div\(phi,epsilon\)\s+Gauss\s+)\w+(\s*;)',
                rf'\g<1>{turb_scheme}\2',
                content
            )

            # combo_numerical_5 → div(phi_nei/own,Yi) - replace $defaultAdvScheme in Yi lines
            yi_scheme = self.ui.combo_numerical_5.currentText().strip()
            content = re.sub(
                r'(div\(phi_nei,Yi\)\s+Gauss\s+)[\$\w]+(\s*;)',
                rf'\g<1>{yi_scheme}\2',
                content
            )
            content = re.sub(
                r'(div\(phi_own,Yi\)\s+Gauss\s+)[\$\w]+(\s*;)',
                rf'\g<1>{yi_scheme}\2',
                content
            )

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

        except Exception:
            traceback.print_exc()
    def _load_fv_schemes(self, system_path: Path):
        """Load fvSchemes settings to UI."""
        try:
            file_path = system_path / "fvSchemes"
            if not file_path.exists():
                return

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Load ddtSchemes.default → combo_numerical_1
            match = re.search(r'ddtSchemes\s*\{\s*default\s+(\w+)\s*;', content)
            if match:
                ddt_scheme = match.group(1)
                # Map file value to UI text
                if ddt_scheme == "steadyState":
                    ddt_scheme = "Steady"
                self._set_combo_text(self.ui.combo_numerical_1, ddt_scheme)

            # Load defaultAdvSchemeV → combo_numerical_2
            match = re.search(r'defaultAdvSchemeV\s+(\w+)\s*;', content)
            if match:
                adv_scheme_v = match.group(1)
                self._set_combo_text(self.ui.combo_numerical_2, adv_scheme_v)

            # Load defaultAdvScheme → combo_numerical_3
            match = re.search(r'defaultAdvScheme\s+(\w+)\s*;', content)
            if match:
                adv_scheme = match.group(1)
                self._set_combo_text(self.ui.combo_numerical_3, adv_scheme)

            # Load turbulence scheme from div(phi,k) → combo_numerical_4
            match = re.search(r'div\(phi,k\)\s+Gauss\s+(\w+)\s*;', content)
            if match:
                turb_scheme = match.group(1)
                self._set_combo_text(self.ui.combo_numerical_4, turb_scheme)

            # Load Yi scheme from div(phi_nei,Yi) → combo_numerical_5
            match = re.search(r'div\(phi_nei,Yi\)\s+Gauss\s+([\$\w]+)\s*;', content)
            if match:
                yi_scheme = match.group(1)
                # If it's a variable reference ($defaultAdvScheme), load defaultAdvScheme value
                if yi_scheme.startswith('$'):
                    var_match = re.search(rf'{yi_scheme[1:]}\s+(\w+)\s*;', content)
                    if var_match:
                        yi_scheme = var_match.group(1)
                self._set_combo_text(self.ui.combo_numerical_5, yi_scheme)

        except Exception:
            traceback.print_exc()
    def _update_fv_solution(self, system_path: Path):
        """Update fvSolution with PIMPLE settings from UI."""
        try:
            file_path = system_path / "fvSolution"
            if not file_path.exists():
                return

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # edit_numerical_1 → PIMPLE.nCorrectors
            n_correctors = self.ui.edit_numerical_1.text() or "2"
            content = re.sub(
                r'(nCorrectors\s+)[\d]+(\s*;)',
                rf'\g<1>{n_correctors}\2',
                content
            )

            # edit_numerical_2 → PIMPLE.nOuterCorrectors
            n_outer = self.ui.edit_numerical_2.text() or "1"
            content = re.sub(
                r'(nOuterCorrectors\s+)[\d]+(\s*;)',
                rf'\g<1>{n_outer}\2',
                content
            )

            # edit_numerical_3 → PIMPLE.nonOrthogonalityThreshold
            non_ortho = self.ui.edit_numerical_3.text() or "60"
            content = re.sub(
                r'(nonOrthogonalityThreshold\s+)[\d\.]+(\s*;)',
                rf'\g<1>{non_ortho}\2',
                content
            )

            # combo_numerical_6 → PIMPLE.fluxScheme
            flux_scheme = self.ui.combo_numerical_6.currentText().strip()
            content = re.sub(
                r'(fluxScheme\s+)\w+(\s*;)',
                rf'\g<1>{flux_scheme}\2',
                content
            )

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

        except Exception:
            traceback.print_exc()
    def _load_fv_solution(self, system_path: Path):
        """Load fvSolution settings to UI."""
        try:
            file_path = system_path / "fvSolution"
            if not file_path.exists():
                return

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Load nCorrectors → edit_numerical_1
            match = re.search(r'nCorrectors\s+(\d+)\s*;', content)
            if match:
                self.ui.edit_numerical_1.setText(match.group(1))

            # Load nOuterCorrectors → edit_numerical_2
            match = re.search(r'nOuterCorrectors\s+(\d+)\s*;', content)
            if match:
                self.ui.edit_numerical_2.setText(match.group(1))

            # Load nonOrthogonalityThreshold → edit_numerical_3
            match = re.search(r'nonOrthogonalityThreshold\s+([\d\.]+)\s*;', content)
            if match:
                self.ui.edit_numerical_3.setText(match.group(1))

            # Load fluxScheme → combo_numerical_6
            match = re.search(r'fluxScheme\s+(\w+)\s*;', content)
            if match:
                flux_scheme = match.group(1)
                self._set_combo_text(self.ui.combo_numerical_6, flux_scheme)

        except Exception:
            traceback.print_exc()
    def _set_combo_text(self, combo, text: str):
        """Set combobox to item matching the given text."""
        for i in range(combo.count()):
            if combo.itemText(i).strip() == text:
                combo.setCurrentIndex(i)
                return
        # If not found, try to find partial match
        for i in range(combo.count()):
            if text in combo.itemText(i):
                combo.setCurrentIndex(i)
                return

    def _update_control_dict(self, system_path: Path):
        """Update controlDict with run settings from UI."""
        try:
            file_path = system_path / "controlDict"
            if not file_path.exists():
                return

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # edit_run_1 → startTime
            start_time = self.ui.edit_run_1.text() or "0"
            content = re.sub(
                r'(startTime\s+)[\d\.eE\+\-]+(\s*;)',
                rf'\g<1>{start_time}\2',
                content
            )

            # edit_run_2 → endTime
            end_time = self.ui.edit_run_2.text() or "0.02"
            content = re.sub(
                r'(endTime\s+)[\d\.eE\+\-]+(\s*;)',
                rf'\g<1>{end_time}\2',
                content
            )

            # edit_run_3 → deltaT
            delta_t = self.ui.edit_run_3.text() or "1e-06"
            content = re.sub(
                r'(deltaT\s+)[\d\.eE\+\-]+(\s*;)',
                rf'\g<1>{delta_t}\2',
                content
            )

            # edit_run_4 → writeInterval
            write_interval = self.ui.edit_run_4.text() or "5e-04"
            content = re.sub(
                r'(writeInterval\s+)[\d\.eE\+\-]+(\s*;)',
                rf'\g<1>{write_interval}\2',
                content
            )

            # edit_run_5 → maxCo
            max_co = self.ui.edit_run_5.text() or "0.4"
            content = re.sub(
                r'(maxCo\s+)[\d\.eE\+\-]+(\s*;)',
                rf'\g<1>{max_co}\2',
                content
            )

            # edit_run_6 → purgeWrite (0 if groupBox_13 unchecked, else value)
            if self.ui.groupBox_13.isChecked():
                purge_write = self.ui.edit_run_6.text() or "20"
            else:
                purge_write = "0"
            content = re.sub(
                r'(purgeWrite\s+)[\d]+(\s*;)',
                rf'\g<1>{purge_write}\2',
                content
            )

            # combo_run_1 → writeFormat
            write_format = self.ui.combo_run_1.currentText().strip()
            content = re.sub(
                r'(writeFormat\s+)\w+(\s*;)',
                rf'\g<1>{write_format}\2',
                content
            )

            # edit_run_7 → writePrecision
            write_precision = self.ui.edit_run_7.text() or "12"
            content = re.sub(
                r'(writePrecision\s+)[\d]+(\s*;)',
                rf'\g<1>{write_precision}\2',
                content
            )

            # edit_run_8 → timePrecision
            time_precision = self.ui.edit_run_8.text() or "12"
            content = re.sub(
                r'(timePrecision\s+)[\d]+(\s*;)',
                rf'\g<1>{time_precision}\2',
                content
            )

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

        except Exception:
            traceback.print_exc()

    def _load_control_dict(self, system_path: Path):
        """Load controlDict settings to UI."""
        try:
            file_path = system_path / "controlDict"
            if not file_path.exists():
                return

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Load startTime → edit_run_1
            match = re.search(r'startTime\s+([\d\.eE\+\-]+)\s*;', content)
            if match:
                self.ui.edit_run_1.setText(match.group(1))

            # Load endTime → edit_run_2
            match = re.search(r'endTime\s+([\d\.eE\+\-]+)\s*;', content)
            if match:
                self.ui.edit_run_2.setText(match.group(1))

            # Load deltaT → edit_run_3
            match = re.search(r'deltaT\s+([\d\.eE\+\-]+)\s*;', content)
            if match:
                self.ui.edit_run_3.setText(match.group(1))

            # Load writeInterval → edit_run_4
            match = re.search(r'writeInterval\s+([\d\.eE\+\-]+)\s*;', content)
            if match:
                self.ui.edit_run_4.setText(match.group(1))

            # Load maxCo → edit_run_5
            match = re.search(r'maxCo\s+([\d\.eE\+\-]+)\s*;', content)
            if match:
                self.ui.edit_run_5.setText(match.group(1))

            # Load purgeWrite → edit_run_6 and groupBox_13 checkbox
            match = re.search(r'purgeWrite\s+(\d+)\s*;', content)
            if match:
                purge_value = int(match.group(1))
                if purge_value > 0:
                    self.ui.groupBox_13.setChecked(True)
                    self.ui.edit_run_6.setText(match.group(1))
                else:
                    self.ui.groupBox_13.setChecked(False)
                    self.ui.edit_run_6.setText("20")  # Default value when disabled

            # Load writeFormat → combo_run_1
            match = re.search(r'writeFormat\s+(\w+)\s*;', content)
            if match:
                write_format = match.group(1)
                self._set_combo_text(self.ui.combo_run_1, write_format)

            # Load writePrecision → edit_run_7
            match = re.search(r'writePrecision\s+(\d+)\s*;', content)
            if match:
                self.ui.edit_run_7.setText(match.group(1))

            # Load timePrecision → edit_run_8
            match = re.search(r'timePrecision\s+(\d+)\s*;', content)
            if match:
                self.ui.edit_run_8.setText(match.group(1))

        except Exception:
            traceback.print_exc()
