
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

    def __init__(self, parent):

        self.parent = parent

        self.ui = self.parent.ui

        self.ctx = self.parent.context

        self.exec_widget = self.ctx.get("exec")

        self.vtk_pre = self.ctx.get("vtk_pre")

        self.vtk_post = self.ctx.get("vtk_post")

        self.residual_graph = self.ctx.get("residual_graph")

        self.app_data = app_data

        self.case_data = case_data

        self._log_watcher = QFileSystemWatcher(self.parent)

        self._log_watcher.fileChanged.connect(self._on_log_file_changed)

        self._log_timer = QTimer(self.parent)

        self._log_timer.timeout.connect(self._check_log_file)

        self._log_check_interval = 2000

        self._graph_update_timer = QTimer(self.parent)

        self._graph_update_timer.setSingleShot(True)

        self._graph_update_timer.timeout.connect(self._do_update_residual_graph)

        self._graph_update_interval = 3000

        self._is_running = False

        self._is_paused = False

        self._log_file_path = None

        self._allclean_commands = []

        self._allrun_commands = []

        self._step_tracker = 0

        self._last_run_completed = False

        self._init_connect()

    def _init_connect(self):

        self.ui.button_edit_hostfile_run.clicked.connect(self._on_edit_hostfile_clicked)

        self.ui.button_run.clicked.connect(self._on_run_clicked)

        self.ui.button_stop.clicked.connect(self._on_stop_clicked)

        self.ui.button_pause.clicked.connect(self._on_pause_clicked)

        self.ui.button_stop.setEnabled(False)

        self.ui.button_pause.setEnabled(False)

        self.ui.checkBox_host_2.toggled.connect(self._on_hostfile_run_toggled)

        self.ui.comboBox_7.currentIndexChanged.connect(self._on_combustion_changed)

        if self.exec_widget:

            self.exec_widget.sig_proc_status.connect(self._on_proc_status_changed)

    def _on_hostfile_run_toggled(self, checked: bool):

        self.app_data.parallel_run_enabled = checked

        self.ui.button_edit_hostfile_run.setEnabled(checked)

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

    def _load_number_of_subdomains(self):

        import os

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

        self.ui.edit_number_of_subdomains_2.setText(str(default_value))

    def _update_decompose_par_dict(self, case_path: Path):

        try:

            n_procs = int(self.ui.edit_number_of_subdomains_2.text())

        except (ValueError, AttributeError):

            return

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

        hosts_path = Path(self.case_data.path) / "5.CHTFCase" / "system" / "hosts"

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

    def _on_combustion_changed(self, index):

        is_on = (index == 0)

        self.ui.comboBox_10.setEnabled(is_on)

    def _on_stop_clicked(self):

        self._is_paused = False

        if self.exec_widget:

            self.exec_widget.stop_process(kill=True)

        self._is_running = False

        self.ui.button_run.setEnabled(True)

        self.ui.button_run.setText("Run Solver")

        self.ui.button_stop.setEnabled(False)

        self.ui.button_pause.setEnabled(False)

        self.ui.button_mesh_generate.setEnabled(True)

        self.ui.button_mesh_stop.setEnabled(False)

        self.ui.button_pause.setText("Pause")

        self.ui.edit_run_status.setText("Stopped")

        self.ui.edit_run_finished.setText(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        self._stop_log_monitoring()

    def _on_pause_clicked(self):

        case_path = Path(self.case_data.path) / "5.CHTFCase"

        if self._is_paused:

            self._set_control_dict_run_params(case_path, stop_at='endTime', start_from='latestTime')

            self._is_paused = False

            if self.exec_widget:

                self.exec_widget._pause_all_proc = False

            self._resume_from_pause(case_path)

        else:

            self._set_control_dict_run_params(case_path, stop_at='writeNow')

            self._is_paused = True

            if self.exec_widget:

                self.exec_widget.stop_process(kill=True)

            self.ui.button_pause.setText("Resume")

    def _set_control_dict_run_params(self, case_path: Path, stop_at: str, start_from: str = None):

        """controlDict의 stopAt / startFrom 값을 변경한다."""

        try:

            file_path = case_path / "system" / "controlDict"

            if not file_path.exists():

                return

            content = file_path.read_text(encoding='utf-8')

            content = re.sub(r'(stopAt\s+)\w+(\s*;)', rf'\g<1>{stop_at}\2', content)

            if start_from:

                content = re.sub(r'(startFrom\s+)\w+(\s*;)', rf'\g<1>{start_from}\2', content)

            file_path.write_text(content, encoding='utf-8')

        except Exception:

            traceback.print_exc()

    def _resume_from_pause(self, case_path: Path):

        """일시정지 후 재개: allrun_commands에서 mpirun(솔버) 단계부터 재실행."""

        mpirun_idx = next(
            (i for i, cmd in enumerate(self._allrun_commands)
             if 'mpirun' in cmd or 'mpiexec' in cmd),
            0
        )

        self._run_simulation_resume(mpirun_idx)

    def _on_proc_status_changed(self, proc_idx: int, cpu_id: int, pid: int, status: str):

        if pid > 0:

            self.ui.edit_run_id.setText(str(pid))

        self.ui.edit_run_status.setText(status)

        if status == 'Starting':

            self._step_tracker += 1

    def _run_simulation(self):

        try:

            case_path = Path(self.case_data.path) / "5.CHTFCase"

            allclean_path = case_path / "Allclean"

            allrun_path = case_path / "Allrun"

            if not allrun_path.exists():

                return

            self._update_decompose_par_dict(case_path)

            n_procs = 4

            try:

                n_procs = int(self.ui.edit_number_of_subdomains_2.text())

            except (ValueError, AttributeError):

                pass

            use_hostfile = self.ui.checkBox_host_2.isChecked()

            application = self._get_application(case_path)

            self._allclean_commands = []

            if allclean_path.exists():

                self._allclean_commands = self._parse_script(allclean_path, n_procs, use_hostfile, application)

            self._allrun_commands = self._parse_script(allrun_path, n_procs, use_hostfile, application)

            commands = self._allclean_commands + self._allrun_commands

            if not commands:

                QMessageBox.warning(
                    None, "Run Solver",
                    "Allclean/Allrun files not found or empty in:\n"
                    f"{case_path}"
                )

                return

            self._step_tracker = 0

            self._last_run_completed = False

            self._set_control_dict_run_params(case_path, stop_at='endTime', start_from='startTime')

            self._execute_commands(case_path, commands)

        except Exception:

            self._restore_ui_after_run()

            self.ui.edit_run_status.setText("Error")

    def _run_simulation_resume(self, allrun_start: int):

        try:

            case_path = Path(self.case_data.path) / "5.CHTFCase"

            commands = self._allrun_commands[allrun_start:]

            if not commands:

                return

            self._update_decompose_par_dict(case_path)

            self._step_tracker = len(self._allclean_commands) + allrun_start

            self._last_run_completed = False

            self._set_control_dict_run_params(case_path, stop_at='endTime', start_from='latestTime')

            self._execute_commands(case_path, commands)

        except Exception:

            self._restore_ui_after_run()

            self.ui.edit_run_status.setText("Error")

    def _execute_commands(self, case_path: Path, commands: list):

        self._log_file_path = case_path / "log.Solver"

        self._solver_numbered_log = None

        self.exec_widget.set_working_path(str(case_path))

        self.exec_widget.set_function_after_finished(self._on_simulation_finished)

        self.exec_widget.set_function_after_error(self._on_simulation_error)

        self.exec_widget.set_function_restore_ui(self._restore_ui_after_run)

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

        log_wrapper = case_path / "log_cmd.sh"

        log_wrapper.write_text(
            '#!/bin/bash\n'
            'set -o pipefail\n'
            'LOG_FILE="$1"\n'
            'shift\n'
            'setsid "$@" 2>&1 | stdbuf -oL tee "$LOG_FILE"\n',
            encoding='utf-8'
        )

        log_wrapper.chmod(0o755)

        self._log_dir = Path(self.case_data.path) / "log" / "RunSolver" / datetime.now().strftime("%Y%m%d_%H%M%S")

        self._log_dir.mkdir(parents=True, exist_ok=True)

        self._is_running = True

        self.ui.button_run.setEnabled(False)

        self.ui.button_run.setText("Running...")

        self.ui.button_stop.setEnabled(True)

        self.ui.button_pause.setEnabled(True)

        self.ui.button_mesh_generate.setEnabled(False)

        self.ui.edit_run_name.setText("Solver")

        self.ui.edit_run_id.setText("-")

        self.ui.edit_run_started.setText(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        self.ui.edit_run_finished.setText("-")

        self.ui.edit_run_status.setText("Running...")

        commands = self._wrap_commands_with_logging(commands)

        if self._solver_numbered_log is None:
            for _cmd_tuple in commands:
                _raw = _cmd_tuple[0] if isinstance(_cmd_tuple, tuple) else _cmd_tuple
                if _raw.startswith("./log_cmd.sh "):
                    parts = _raw.split()
                    if len(parts) >= 2:
                        self._solver_numbered_log = Path(parts[1])
                    break

        if self._solver_numbered_log:

            if self._log_file_path.exists() or self._log_file_path.is_symlink():

                self._log_file_path.unlink()

            self._log_file_path.symlink_to(self._solver_numbered_log)

        self._start_log_monitoring()

        self.exec_widget.run(commands)

    def _get_application(self, case_path: Path) -> str:

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

    def _wrap_commands_with_logging(self, commands: list) -> list:
        case_path = Path(self.case_data.path) / "5.CHTFCase"
        app_name = self._get_application(case_path)

        logged_commands = []

        for i, cmd in enumerate(commands, 1):

            display = self._get_display_cmd(cmd)

            if cmd.startswith("./shell_cmd.sh"):

                logged_commands.append((cmd, display))

            else:

                cmd_name = self._extract_command_name(cmd)

                log_file = self._log_dir / f"{i:02d}_{cmd_name}.log"

                if self._solver_numbered_log is None:
                    is_solver = app_name and app_name in cmd
                    is_mpi = "mpirun" in cmd or "mpiexec" in cmd
                    if is_solver or (is_mpi and not any(
                        util in cmd for util in ("decomposePar", "reconstructPar", "checkMesh")
                    )):
                        self._solver_numbered_log = log_file

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

    def _parse_script(self, script_path: Path, n_procs: int,
                      use_hostfile: bool = False, application: str = "") -> list:

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

            if not line or line.startswith('#'):

                continue

            if any(line.startswith(p) for p in SKIP_PREFIXES):

                continue

            line = re.sub(r'>\s*/dev/null.*', '', line).strip()

            line = re.sub(r'#.*$', '', line).strip()

            if not line:

                continue

            if line.startswith('runApplication '):

                line = line[len('runApplication '):]

                if line.startswith('-s '):

                    parts = line.split(None, 2)

                    if len(parts) >= 3:

                        line = parts[2]

                    else:

                        continue

            if line.startswith('runParallel '):

                app_and_args = line[len('runParallel '):]

                if use_hostfile:

                    line = f"mpirun -np {n_procs} --hostfile system/hosts {app_and_args} -parallel"

                else:

                    line = f"mpirun -np {n_procs} --host localhost --oversubscribe {app_and_args} -parallel"

            line = line.replace('`getNumberOfProcessors`', str(n_procs))

            line = line.replace('$(getNumberOfProcessors)', str(n_procs))

            if application:

                line = line.replace('`getApplication`', application)

                line = line.replace('$(getApplication)', application)

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

    def _load_latest_solver_log(self):

        if not self.case_data.path or not self.residual_graph:

            return

        case_path = Path(self.case_data.path) / "5.CHTFCase"

        solver_log = case_path / "log.Solver"

        need_symlink = (
            not solver_log.exists() and not solver_log.is_symlink()
            or (solver_log.is_symlink() and not solver_log.exists())
            or (solver_log.exists() and not solver_log.is_symlink())
        )

        if need_symlink:

            if solver_log.exists() or solver_log.is_symlink():

                solver_log.unlink()

            self._try_create_solver_log_symlink(solver_log)

        if solver_log.exists():

            self._log_file_path = solver_log

            try:

                self.residual_graph.load_file(str(solver_log), target_vars=['h', 'p', 'rho'])

            except Exception:

                traceback.print_exc()

    def _try_create_solver_log_symlink(self, symlink_path: Path):

        """log/RunSolver 최신 폴더에서 mpirun 솔버 로그를 찾아 log.Solver 심볼릭 링크 생성."""

        log_base = Path(self.case_data.path) / "log" / "RunSolver"

        if not log_base.exists():

            return

        try:

            run_dirs = sorted(
                [d for d in log_base.iterdir() if d.is_dir()],
                key=lambda d: d.name, reverse=True
            )

            for run_dir in run_dirs:

                target = self._find_solver_log_in_dir(run_dir)

                if target and target.exists():

                    symlink_path.symlink_to(target.resolve())

                    return

        except Exception:

            traceback.print_exc()

    def _find_solver_log_in_dir(self, run_dir: Path):

        """디렉터리에서 mpirun 솔버 로그 파일을 찾는다 (*localhost*.log 우선, 없으면 최대 번호)."""

        def num_key(f):

            m = re.match(r'^(\d+)', f.name)

            return int(m.group(1)) if m else 0

        candidates = sorted(run_dir.glob("*localhost*.log"), key=num_key, reverse=True)

        if candidates:

            return candidates[0]

        all_logs = sorted(run_dir.glob("*.log"), key=num_key, reverse=True)

        return all_logs[0] if all_logs else None

    def _detect_resume_state(self):

        """케이스 로드 시 이전 실행이 중단됐는지 감지하여 재개 상태를 설정."""

        if not self.case_data.path:

            return

        case_path = Path(self.case_data.path) / "5.CHTFCase"

        allrun_path = case_path / "Allrun"

        if not allrun_path.exists():

            return

        n_procs = 4

        try:

            n_procs = int(self.ui.edit_number_of_subdomains_2.text())

        except (ValueError, AttributeError):

            pass

        use_hostfile = self.ui.checkBox_host_2.isChecked()

        application = self._get_application(case_path)

        allclean_path = case_path / "Allclean"

        self._allclean_commands = []

        if allclean_path.exists():

            self._allclean_commands = self._parse_script(allclean_path, n_procs, use_hostfile, application)

        self._allrun_commands = self._parse_script(allrun_path, n_procs, use_hostfile, application)

        if not self._allrun_commands:

            return

        solver_log = case_path / "log.Solver"

        if not solver_log.exists():

            return

        try:

            content = solver_log.read_text(encoding='utf-8', errors='ignore')

            last_lines = content[-200:] if len(content) > 200 else content

            if re.search(r'\bEnd\b', last_lines):

                self._last_run_completed = True

                return

        except Exception:

            traceback.print_exc()

            return

        last_step = 0

        log_base = Path(self.case_data.path) / "log" / "RunSolver"

        if log_base.exists():

            try:

                run_dirs = [d for d in log_base.iterdir() if d.is_dir()]

                if run_dirs:

                    latest_dir = max(run_dirs, key=lambda d: d.name)

                    for lf in latest_dir.glob("*.log"):

                        m = re.match(r'^(\d+)_', lf.name)

                        if m:

                            last_step = max(last_step, int(m.group(1)))

            except Exception:

                traceback.print_exc()

        total = len(self._allclean_commands) + len(self._allrun_commands)

        if last_step > 0:

            self._step_tracker = min(last_step, total)

        else:

            self._step_tracker = len(self._allclean_commands) + 1

        self._last_run_completed = False

    def _start_log_monitoring(self):

        self._log_timer.start(self._log_check_interval)

    def _stop_log_monitoring(self):

        self._log_timer.stop()

        self._graph_update_timer.stop()

        if self._log_file_path and str(self._log_file_path) in self._log_watcher.files():

            self._log_watcher.removePath(str(self._log_file_path))

    def _check_log_file(self):

        if not self._log_file_path:

            return

        if self._log_file_path.exists():

            log_path_str = str(self._log_file_path)

            if log_path_str not in self._log_watcher.files():

                self._log_watcher.addPath(log_path_str)

            self._log_timer.stop()

            self._update_residual_graph()

    def _on_log_file_changed(self, path: str):

        self._update_residual_graph()

    def _update_residual_graph(self):

        if not self._graph_update_timer.isActive():

            self._graph_update_timer.start(self._graph_update_interval)

    def _do_update_residual_graph(self):

        if not self._log_file_path or not self._log_file_path.exists():

            return

        if self.residual_graph:

            try:

                self.residual_graph.load_file(str(self._log_file_path), target_vars=['h', 'p', 'rho'])

            except Exception:

                traceback.print_exc()

    def _on_simulation_finished(self):

        if self._is_paused:

            return

        self._is_running = False

        self._last_run_completed = True

        self._stop_log_monitoring()

        self._do_update_residual_graph()

        self.ui.button_run.setEnabled(True)

        self.ui.button_run.setText("Run Solver")

        self.ui.button_stop.setEnabled(False)

        self.ui.button_pause.setEnabled(False)

        self.ui.button_pause.setText("Pause")

        self.ui.button_mesh_generate.setEnabled(True)

        self.ui.edit_run_status.setText("Finished")

        self.ui.edit_run_finished.setText(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def _on_simulation_error(self):

        if self._is_paused:

            return

        self._is_running = False

        self._stop_log_monitoring()

        self.ui.button_run.setEnabled(True)

        self.ui.button_run.setText("Run Solver")

        self.ui.button_stop.setEnabled(False)

        self.ui.button_pause.setEnabled(False)

        self.ui.button_pause.setText("Pause")

        self.ui.button_mesh_generate.setEnabled(True)

        self.ui.edit_run_status.setText("Error")

        self.ui.edit_run_finished.setText(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def _restore_ui_after_run(self):

        if self._is_paused:

            self._is_running = False

            self.ui.button_run.setEnabled(False)

            self.ui.button_stop.setEnabled(True)

            self.ui.button_pause.setEnabled(True)

            self.ui.button_pause.setText("Resume")

            self.ui.button_mesh_generate.setEnabled(False)

            self.ui.edit_run_status.setText("Paused")

            self._stop_log_monitoring()

            return

        self._is_running = False

        self.ui.button_run.setEnabled(True)

        self.ui.button_run.setText("Run Solver")

        self.ui.button_stop.setEnabled(False)

        self.ui.button_pause.setEnabled(False)

        self.ui.button_mesh_generate.setEnabled(True)

        self.ui.edit_run_status.setText("Ready")

        self.ui.edit_run_finished.setText(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        self._stop_log_monitoring()

        self._do_update_residual_graph()

    def _on_run_clicked(self):

        import os

        if self._is_running:

            QMessageBox.warning(
                self.parent,
                "Run Solver",
                "시뮬레이션이 이미 실행 중입니다.\n\n"
                "실행을 중지하려면 Stop 버튼을 누르세요."
            )

            return

        if self.exec_widget and self.exec_widget.is_running():

            QMessageBox.warning(
                self.parent,
                "Run Solver",
                "다른 작업이 이미 실행 중입니다.\n\n"
                "현재 작업이 완료될 때까지 기다리거나 Stop 버튼으로 중지하세요."
            )

            return

        self._clear_error_highlight()

        try:

            n_procs = int(self.ui.edit_number_of_subdomains_2.text())

            use_hostfile = self.ui.checkBox_host_2.isChecked()

            cpu_count = os.cpu_count() or 1

            if not use_hostfile and n_procs > cpu_count:

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

        if (self._step_tracker > 0
                and not self._last_run_completed
                and self._allrun_commands):

            allclean_count = len(self._allclean_commands)

            interrupted_idx = self._step_tracker - 1

            allrun_resume = max(0, interrupted_idx - allclean_count)

            if allrun_resume < len(self._allrun_commands):

                step_name = self._get_display_cmd(self._allrun_commands[allrun_resume])

                total = len(self._allrun_commands)

                msg = QMessageBox(self.parent)

                msg.setWindowTitle("Run Solver")

                msg.setText(
                    f"이전 실행이 중단되었습니다.\n\n"
                    f"중단 단계: {allrun_resume + 1} / {total}  ({step_name})\n\n"
                    f"이 단계부터 이어서 실행하시겠습니까?"
                )

                btn_resume = msg.addButton("이어서 실행", QMessageBox.ButtonRole.YesRole)

                msg.addButton("처음부터 실행", QMessageBox.ButtonRole.NoRole)

                msg.setDefaultButton(btn_resume)

                msg.exec()

                if msg.clickedButton() == btn_resume:

                    self._run_simulation_resume(allrun_resume)

                    return

        self._run_simulation()

    def _update_run_settings(self) -> bool:

        try:

            case_path = Path(self.case_data.path) / "5.CHTFCase" / "constant" / "fluid"

            self._update_turbulence_properties(case_path)

            self._update_surface_film_properties(case_path)

            self._update_combustion_properties(case_path)

            self._update_thermophysical_properties(case_path)

            orig_path = Path(self.case_data.path) / "5.CHTFCase" / "0.orig"

            self._update_fluid_initial_conditions(orig_path / "fluid")

            self._update_solid_initial_conditions(orig_path)

            self._update_spray_mmh_properties(case_path)

            self._update_spray_nto_properties(case_path)

            system_path = Path(self.case_data.path) / "5.CHTFCase" / "system" / "fluid"

            self._update_fv_schemes(system_path)

            self._update_fv_solution(system_path)

            system_root = Path(self.case_data.path) / "5.CHTFCase" / "system"

            self._update_control_dict(system_root)

            return True

        except Exception:

            traceback.print_exc()

            return False

    def _update_turbulence_properties(self, case_path: Path):

        try:

            file_path = case_path / "turbulenceProperties"

            if not file_path.exists():

                return

            foam_file = FoamFile(str(file_path))

            if not foam_file.load():

                return

            ras_model = self.ui.comboBox_2.currentText().strip()

            foam_file.set_value("RAS.RASModel", ras_model)

            foam_file.save()

        except Exception:

            traceback.print_exc()

    def _update_surface_film_properties(self, case_path: Path):

        try:

            file_path = case_path / "surfaceFilmProperties"

            if not file_path.exists():

                return

            foam_file = FoamFile(str(file_path))

            if not foam_file.load():

                return

            is_film_on = (self.ui.comboBox_3.currentIndex() == 0)

            film_model = "thermoSingleLayer" if is_film_on else "none"

            foam_file.set_value("surfaceFilmModel", film_model)

            is_phase_on = (self.ui.comboBox_4.currentIndex() == 0)

            phase_model = "standardPhaseChange" if is_phase_on else "none"

            foam_file.set_value("thermoSingleLayerCoeffs.phaseChangeModel", phase_model)

            foam_file.save()

        except Exception:

            traceback.print_exc()

    def _update_combustion_properties(self, case_path: Path):

        try:

            file_path = case_path / "combustionProperties"

            if not file_path.exists():

                return

            foam_file = FoamFile(str(file_path))

            if not foam_file.load():

                return

            is_combustion_on = (self.ui.comboBox_7.currentIndex() == 0)

            combustion_model = "laminar" if is_combustion_on else "none"

            foam_file.set_value("combustionModel", combustion_model)

            foam_file.save()

        except Exception:

            traceback.print_exc()

    def _update_thermophysical_properties(self, case_path: Path):

        try:

            file_path = case_path / "thermophysicalProperties"

            if not file_path.exists():

                return

            with open(file_path, 'r', encoding='utf-8') as f:

                content = f.read()

            if self.ui.comboBox_10.isEnabled():

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

                    pattern = r'(CHEMKINFile\s+"\<case\>/chemkin/)[\w\.]+(")'

                    replacement = rf'\g<1>{chemkin_file}\2'

                    content = re.sub(pattern, replacement, content)

            thermo_text = self.ui.comboBox_6.currentText().strip()

            if thermo_text == "NASA polynomial":

                thermo_value = "janaf"

            elif thermo_text:

                thermo_value = thermo_text

            else:

                thermo_value = None

            if thermo_value:

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

        self.ui.checkBox_host_2.setChecked(self.app_data.parallel_run_enabled)

        self.ui.button_edit_hostfile_run.setEnabled(self.app_data.parallel_run_enabled)

        self._load_number_of_subdomains()

        self._load_run_settings()

        is_combustion_on = (self.ui.comboBox_7.currentIndex() == 0)

        self.ui.comboBox_10.setEnabled(is_combustion_on)

        self._load_latest_solver_log()

        self._detect_resume_state()

    def _load_run_settings(self):

        try:

            case_path = Path(self.case_data.path) / "5.CHTFCase" / "constant" / "fluid"

            self._load_turbulence_properties(case_path)

            self._load_surface_film_properties(case_path)

            self._load_combustion_properties(case_path)

            self._load_thermophysical_properties(case_path)

            orig_path = Path(self.case_data.path) / "5.CHTFCase" / "0.orig"

            self._load_fluid_initial_conditions(orig_path / "fluid")

            self._load_solid_initial_conditions(orig_path)

            self._load_spray_mmh_properties(case_path)

            self._load_spray_nto_properties(case_path)

            system_path = Path(self.case_data.path) / "5.CHTFCase" / "system" / "fluid"

            self._load_fv_schemes(system_path)

            self._load_fv_solution(system_path)

            system_root = Path(self.case_data.path) / "5.CHTFCase" / "system"

            self._load_control_dict(system_root)

        except Exception:

            traceback.print_exc()

    def _load_turbulence_properties(self, case_path: Path):

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

                for i in range(self.ui.comboBox_2.count()):

                    if self.ui.comboBox_2.itemText(i).strip() == ras_model:

                        self.ui.comboBox_2.setCurrentIndex(i)

                        break

        except Exception:

            traceback.print_exc()

    def _load_surface_film_properties(self, case_path: Path):

        try:

            file_path = case_path / "surfaceFilmProperties"

            if not file_path.exists():

                return

            foam_file = FoamFile(str(file_path))

            if not foam_file.load():

                return

            film_model = foam_file.get_value("surfaceFilmModel")

            if film_model:

                is_on = (str(film_model).strip() == "thermoSingleLayer")

                self.ui.comboBox_3.setCurrentIndex(0 if is_on else 1)

            phase_model = foam_file.get_value("thermoSingleLayerCoeffs.phaseChangeModel")

            if phase_model:

                is_on = (str(phase_model).strip() == "standardPhaseChange")

                self.ui.comboBox_4.setCurrentIndex(0 if is_on else 1)

        except Exception:

            traceback.print_exc()

    def _load_combustion_properties(self, case_path: Path):

        try:

            file_path = case_path / "combustionProperties"

            if not file_path.exists():

                return

            foam_file = FoamFile(str(file_path))

            if not foam_file.load():

                return

            combustion_model = foam_file.get_value("combustionModel")

            if combustion_model:

                is_on = (str(combustion_model).strip() == "laminar")

                self.ui.comboBox_7.setCurrentIndex(0 if is_on else 1)

        except Exception:

            traceback.print_exc()

    def _load_thermophysical_properties(self, case_path: Path):

        try:

            file_path = case_path / "thermophysicalProperties"

            if not file_path.exists():

                return

            with open(file_path, 'r', encoding='utf-8') as f:

                content = f.read()

            pattern = r'CHEMKINFile\s+"\<case\>/chemkin/([\w\.]+)"'

            match = re.search(pattern, content)

            if match:

                chemkin_file = match.group(1)

                if chemkin_file == "chem_ARLRM31N.inp":

                    self.ui.comboBox_10.setCurrentIndex(0)

                elif chemkin_file == "chem_ARLRM31NS.inp":

                    self.ui.comboBox_10.setCurrentIndex(1)

                elif chemkin_file == "chem_Global5S.inp":

                    self.ui.comboBox_10.setCurrentIndex(2)

            thermo_match = re.search(r'thermo\s+(\w+)\s*;', content)

            if thermo_match:

                thermo_value = thermo_match.group(1)

                if thermo_value == "janaf":

                    self._set_combo_text(self.ui.comboBox_6, "NASA polynomial")

                else:

                    found = False

                    for i in range(self.ui.comboBox_6.count()):

                        if self.ui.comboBox_6.itemText(i).strip() == thermo_value:

                            self.ui.comboBox_6.setCurrentIndex(i)

                            found = True

                            break

                    if not found:

                        self.ui.comboBox_6.setCurrentIndex(-1)

        except Exception:

            traceback.print_exc()

    def _update_fluid_initial_conditions(self, fluid_path: Path):

        try:

            if not fluid_path.exists():

                return

            p_file = fluid_path / "p"

            if p_file.exists():

                pressure = float(self.ui.edit_fluid_1.text() or "1")

                if pressure == 1:

                    pressure = 100000

                self._update_internal_field_scalar(p_file, pressure)

            t_file = fluid_path / "T"

            if t_file.exists():

                temperature = float(self.ui.edit_fluid_2.text() or "310")

                self._update_internal_field_scalar(t_file, temperature)

            u_file = fluid_path / "U"

            if u_file.exists():

                vx = float(self.ui.edit_fluid_v_x.text() or "0")

                vy = float(self.ui.edit_fluid_v_y.text() or "0")

                vz = float(self.ui.edit_fluid_v_z.text() or "0")

                self._update_internal_field_vector(u_file, vx, vy, vz)

        except Exception:

            traceback.print_exc()

    def _update_internal_field_scalar(self, file_path: Path, value):

        with open(file_path, 'r', encoding='utf-8') as f:

            content = f.read()

        pattern = r'(internalField\s+uniform\s+)[\d\.eE\+\-]+(\s*;)'

        replacement = rf'\g<1>{value}\2'

        new_content = re.sub(pattern, replacement, content)

        with open(file_path, 'w', encoding='utf-8') as f:

            f.write(new_content)

    def _update_internal_field_vector(self, file_path: Path, x, y, z):

        with open(file_path, 'r', encoding='utf-8') as f:

            content = f.read()

        pattern = r'(internalField\s+uniform\s+\()[\d\.eE\+\-\s]+(\)\s*;)'

        replacement = rf'\g<1>{x} {y} {z}\2'

        new_content = re.sub(pattern, replacement, content)

        with open(file_path, 'w', encoding='utf-8') as f:

            f.write(new_content)

    def _update_solid_initial_conditions(self, orig_path: Path):

        try:

            if not orig_path.exists():

                return

            solid_temp = float(self.ui.edit_solid_1.text() or "300")

            solid_h = self.ui.edit_solid_2.text() or "1000"

            solid_type = self.ui.comboBox_9.currentText()

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

        with open(file_path, 'r', encoding='utf-8') as f:

            content = f.read()

        pattern = r'(internalField\s+uniform\s+)[\d\.eE\+\-]+(\s*;)'

        replacement = rf'\g<1>{temp}\2'

        content = re.sub(pattern, replacement, content)

        h_pattern = rf'({solid_name}\s*\{{[^}}]*h\s+uniform\s+)[\d\.eE\+\-]+(\s*;)'

        h_replacement = rf'\g<1>{h_value}\2'

        content = re.sub(h_pattern, h_replacement, content, flags=re.DOTALL)

        type_pattern = rf'({solid_name}\s*\{{\s*type\s+)\w+(\s*;)'

        type_replacement = rf'\g<1>{bc_type}\2'

        content = re.sub(type_pattern, type_replacement, content)

        with open(file_path, 'w', encoding='utf-8') as f:

            f.write(content)

    def _load_fluid_initial_conditions(self, fluid_path: Path):

        try:

            if not fluid_path.exists():

                return

            p_file = fluid_path / "p"

            if p_file.exists():

                value = self._read_internal_field_scalar(p_file)

                if value is not None:

                    display_value = value

                    if value == 100000:

                        display_value = 1

                    self.ui.edit_fluid_1.setText(str(display_value))

            t_file = fluid_path / "T"

            if t_file.exists():

                value = self._read_internal_field_scalar(t_file)

                if value is not None:

                    self.ui.edit_fluid_2.setText(str(int(value)))

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

        try:

            if not orig_path.exists():

                return

            excluded_folders = {"fluid", "filmRegion"}

            solid_folders = [
                d for d in orig_path.iterdir()
                if d.is_dir() and d.name not in excluded_folders
            ]

            if not solid_folders:

                return

            first_solid = solid_folders[0]

            t_file = first_solid / "T"

            if not t_file.exists():

                return

            with open(t_file, 'r', encoding='utf-8') as f:

                content = f.read()

            temp_pattern = r'internalField\s+uniform\s+([\d\.eE\+\-]+)\s*;'

            temp_match = re.search(temp_pattern, content)

            if temp_match:

                self.ui.edit_solid_1.setText(str(int(float(temp_match.group(1)))))

            solid_name = first_solid.name

            h_pattern = rf'{solid_name}\s*\{{[^}}]*h\s+uniform\s+([\d\.eE\+\-]+)\s*;'

            h_match = re.search(h_pattern, content, re.DOTALL)

            if h_match:

                self.ui.edit_solid_2.setText(h_match.group(1))

            type_pattern = rf'{solid_name}\s*\{{\s*type\s+(\w+)\s*;'

            type_match = re.search(type_pattern, content)

            if type_match:

                bc_type = type_match.group(1)

                for i in range(self.ui.comboBox_9.count()):

                    if self.ui.comboBox_9.itemText(i) == bc_type:

                        self.ui.comboBox_9.setCurrentIndex(i)

                        break

        except Exception:

            traceback.print_exc()

    def _update_spray_mmh_properties(self, case_path: Path):

        try:

            file_path = case_path / "sprayMMHCloudProperties"

            if not file_path.exists():

                return

            with open(file_path, 'r', encoding='utf-8') as f:

                content = f.read()

            mass_total = self.ui.edit_spray_mmh_1.text() or "1.4170e-4"

            duration = self.ui.edit_spray_mmh_2.text() or "1.0e-1"

            umag = self.ui.edit_spray_mmh_3.text() or "34"

            parcels_per_sec = self.ui.edit_spray_mmh_4.text() or "5000000"

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

        try:

            file_path = case_path / "sprayNTOCloudProperties"

            if not file_path.exists():

                return

            with open(file_path, 'r', encoding='utf-8') as f:

                content = f.read()

            mass_total = self.ui.edit_spray_nto_1.text() or "1.4170e-4"

            duration = self.ui.edit_spray_nto_2.text() or "1.0e-1"

            umag = self.ui.edit_spray_nto_3.text() or "34"

            parcels_per_sec = self.ui.edit_spray_nto_4.text() or "5000000"

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

        try:

            file_path = case_path / "sprayMMHCloudProperties"

            if not file_path.exists():

                return

            with open(file_path, 'r', encoding='utf-8') as f:

                content = f.read()

            match = re.search(r'massTotal\s+([\d\.eE\+\-]+)\s*;', content)

            if match:

                self.ui.edit_spray_mmh_1.setText(match.group(1))

            match = re.search(r'duration\s+([\d\.eE\+\-]+)\s*;', content)

            if match:

                self.ui.edit_spray_mmh_2.setText(match.group(1))

            match = re.search(r'UMag\s+([\d\.eE\+\-]+)\s*;', content)

            if match:

                self.ui.edit_spray_mmh_3.setText(match.group(1))

            match = re.search(r'parcelsPerSecond\s+([\d\.eE\+\-]+)\s*;', content)

            if match:

                self.ui.edit_spray_mmh_4.setText(match.group(1))

            match = re.search(r'fixedValueDistribution\s*\{\s*value\s+([\d\.eE\+\-]+)\s*;', content)

            if match:

                value = float(match.group(1))

                display_value = value * 1e6

                self.ui.edit_spray_mmh_5.setText(str(display_value))

            match = re.search(r'position\s+\(\s*([\d\.eE\+\-]+)\s+([\d\.eE\+\-]+)\s+([\d\.eE\+\-]+)\s*\)', content)

            if match:

                self.ui.edit_spray_mmh_6.setText(match.group(1))

                self.ui.edit_spray_mmh_7.setText(match.group(2))

                self.ui.edit_spray_mmh_8.setText(match.group(3))

            match = re.search(r'direction\s+\(\s*([\d\.eE\+\-]+)\s+([\d\.eE\+\-]+)\s+([\d\.eE\+\-]+)\s*\)', content)

            if match:

                self.ui.edit_spray_mmh_9.setText(match.group(1))

                self.ui.edit_spray_mmh_10.setText(match.group(2))

                self.ui.edit_spray_mmh_11.setText(match.group(3))

            match = re.search(r'outerDiameter\s+([\d\.eE\+\-]+)\s*;', content)

            if match:

                self.ui.edit_spray_mmh_12.setText(match.group(1))

            match = re.search(r'innerDiameter\s+([\d\.eE\+\-]+)\s*;', content)

            if match:

                self.ui.edit_spray_mmh_13.setText(match.group(1))

        except Exception:

            traceback.print_exc()

    def _load_spray_nto_properties(self, case_path: Path):

        try:

            file_path = case_path / "sprayNTOCloudProperties"

            if not file_path.exists():

                return

            with open(file_path, 'r', encoding='utf-8') as f:

                content = f.read()

            match = re.search(r'massTotal\s+([\d\.eE\+\-]+)\s*;', content)

            if match:

                self.ui.edit_spray_nto_1.setText(match.group(1))

            match = re.search(r'duration\s+([\d\.eE\+\-]+)\s*;', content)

            if match:

                self.ui.edit_spray_nto_2.setText(match.group(1))

            match = re.search(r'UMag\s+([\d\.eE\+\-]+)\s*;', content)

            if match:

                self.ui.edit_spray_nto_3.setText(match.group(1))

            match = re.search(r'parcelsPerSecond\s+([\d\.eE\+\-]+)\s*;', content)

            if match:

                self.ui.edit_spray_nto_4.setText(match.group(1))

            match = re.search(r'fixedValueDistribution\s*\{\s*value\s+([\d\.eE\+\-]+)\s*;', content)

            if match:

                value = float(match.group(1))

                display_value = value * 1e6

                self.ui.edit_spray_nto_5.setText(str(display_value))

            match = re.search(r'position\s+\(\s*([\d\.eE\+\-]+)\s+([\d\.eE\+\-]+)\s+([\d\.eE\+\-]+)\s*\)', content)

            if match:

                self.ui.edit_spray_nto_6.setText(match.group(1))

                self.ui.edit_spray_nto_7.setText(match.group(2))

                self.ui.edit_spray_nto_8.setText(match.group(3))

            match = re.search(r'direction\s+\(\s*([\d\.eE\+\-]+)\s+([\d\.eE\+\-]+)\s+([\d\.eE\+\-]+)\s*\)', content)

            if match:

                self.ui.edit_spray_nto_9.setText(match.group(1))

                self.ui.edit_spray_nto_10.setText(match.group(2))

                self.ui.edit_spray_nto_11.setText(match.group(3))

            match = re.search(r'outerDiameter\s+([\d\.eE\+\-]+)\s*;', content)

            if match:

                self.ui.edit_spray_nto_12.setText(match.group(1))

            match = re.search(r'innerDiameter\s+([\d\.eE\+\-]+)\s*;', content)

            if match:

                self.ui.edit_spray_nto_13.setText(match.group(1))

        except Exception:

            traceback.print_exc()

    def _update_fv_schemes(self, system_path: Path):

        try:

            file_path = system_path / "fvSchemes"

            if not file_path.exists():

                return

            with open(file_path, 'r', encoding='utf-8') as f:

                content = f.read()

            ddt_scheme = self.ui.combo_numerical_1.currentText().strip()

            if ddt_scheme == "Steady":

                ddt_scheme = "steadyState"

            content = re.sub(
                r'(ddtSchemes\s*\{\s*default\s+)\w+(\s*;)',
                rf'\g<1>{ddt_scheme}\2',
                content
            )

            adv_scheme_v = self.ui.combo_numerical_2.currentText().strip()

            content = re.sub(
                r'(defaultAdvSchemeV\s+)\w+(\s*;)',
                rf'\g<1>{adv_scheme_v}\2',
                content
            )

            adv_scheme = self.ui.combo_numerical_3.currentText().strip()

            content = re.sub(
                r'(defaultAdvScheme\s+)\w+(\s*;)',
                rf'\g<1>{adv_scheme}\2',
                content
            )

            turb_scheme = self.ui.combo_numerical_4.currentText().strip()

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

        try:

            file_path = system_path / "fvSchemes"

            if not file_path.exists():

                return

            with open(file_path, 'r', encoding='utf-8') as f:

                content = f.read()

            match = re.search(r'ddtSchemes\s*\{\s*default\s+(\w+)\s*;', content)

            if match:

                ddt_scheme = match.group(1)

                if ddt_scheme == "steadyState":

                    ddt_scheme = "Steady"

                self._set_combo_text(self.ui.combo_numerical_1, ddt_scheme)

            match = re.search(r'defaultAdvSchemeV\s+(\w+)\s*;', content)

            if match:

                adv_scheme_v = match.group(1)

                self._set_combo_text(self.ui.combo_numerical_2, adv_scheme_v)

            match = re.search(r'defaultAdvScheme\s+(\w+)\s*;', content)

            if match:

                adv_scheme = match.group(1)

                self._set_combo_text(self.ui.combo_numerical_3, adv_scheme)

            match = re.search(r'div\(phi,k\)\s+Gauss\s+(\w+)\s*;', content)

            if match:

                turb_scheme = match.group(1)

                self._set_combo_text(self.ui.combo_numerical_4, turb_scheme)

            match = re.search(r'div\(phi_nei,Yi\)\s+Gauss\s+([\$\w]+)\s*;', content)

            if match:

                yi_scheme = match.group(1)

                if yi_scheme.startswith('$'):

                    var_match = re.search(rf'{yi_scheme[1:]}\s+(\w+)\s*;', content)

                    if var_match:

                        yi_scheme = var_match.group(1)

                self._set_combo_text(self.ui.combo_numerical_5, yi_scheme)

        except Exception:

            traceback.print_exc()

    def _update_fv_solution(self, system_path: Path):

        try:

            file_path = system_path / "fvSolution"

            if not file_path.exists():

                return

            with open(file_path, 'r', encoding='utf-8') as f:

                content = f.read()

            n_correctors = self.ui.edit_numerical_1.text() or "2"

            content = re.sub(
                r'(nCorrectors\s+)[\d]+(\s*;)',
                rf'\g<1>{n_correctors}\2',
                content
            )

            n_outer = self.ui.edit_numerical_2.text() or "1"

            content = re.sub(
                r'(nOuterCorrectors\s+)[\d]+(\s*;)',
                rf'\g<1>{n_outer}\2',
                content
            )

            non_ortho = self.ui.edit_numerical_3.text() or "60"

            content = re.sub(
                r'(nonOrthogonalityThreshold\s+)[\d\.]+(\s*;)',
                rf'\g<1>{non_ortho}\2',
                content
            )

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

        try:

            file_path = system_path / "fvSolution"

            if not file_path.exists():

                return

            with open(file_path, 'r', encoding='utf-8') as f:

                content = f.read()

            match = re.search(r'nCorrectors\s+(\d+)\s*;', content)

            if match:

                self.ui.edit_numerical_1.setText(match.group(1))

            match = re.search(r'nOuterCorrectors\s+(\d+)\s*;', content)

            if match:

                self.ui.edit_numerical_2.setText(match.group(1))

            match = re.search(r'nonOrthogonalityThreshold\s+([\d\.]+)\s*;', content)

            if match:

                self.ui.edit_numerical_3.setText(match.group(1))

            match = re.search(r'fluxScheme\s+(\w+)\s*;', content)

            if match:

                flux_scheme = match.group(1)

                self._set_combo_text(self.ui.combo_numerical_6, flux_scheme)

        except Exception:

            traceback.print_exc()

    def _set_combo_text(self, combo, text: str):

        for i in range(combo.count()):

            if combo.itemText(i).strip() == text:

                combo.setCurrentIndex(i)

                return

        for i in range(combo.count()):

            if text in combo.itemText(i):

                combo.setCurrentIndex(i)

                return

    def _update_control_dict(self, system_path: Path):

        try:

            file_path = system_path / "controlDict"

            if not file_path.exists():

                return

            with open(file_path, 'r', encoding='utf-8') as f:

                content = f.read()

            start_time = self.ui.edit_run_1.text() or "0"

            content = re.sub(
                r'(startTime\s+)[\d\.eE\+\-]+(\s*;)',
                rf'\g<1>{start_time}\2',
                content
            )

            end_time = self.ui.edit_run_2.text() or "0.02"

            content = re.sub(
                r'(endTime\s+)[\d\.eE\+\-]+(\s*;)',
                rf'\g<1>{end_time}\2',
                content
            )

            delta_t = self.ui.edit_run_3.text() or "1e-06"

            content = re.sub(
                r'(deltaT\s+)[\d\.eE\+\-]+(\s*;)',
                rf'\g<1>{delta_t}\2',
                content
            )

            write_interval = self.ui.edit_run_4.text() or "5e-04"

            content = re.sub(
                r'(writeInterval\s+)[\d\.eE\+\-]+(\s*;)',
                rf'\g<1>{write_interval}\2',
                content
            )

            max_co = self.ui.edit_run_5.text() or "0.4"

            content = re.sub(
                r'(maxCo\s+)[\d\.eE\+\-]+(\s*;)',
                rf'\g<1>{max_co}\2',
                content
            )

            if self.ui.groupBox_13.isChecked():

                purge_write = self.ui.edit_run_6.text() or "20"

            else:

                purge_write = "0"

            content = re.sub(
                r'(purgeWrite\s+)[\d]+(\s*;)',
                rf'\g<1>{purge_write}\2',
                content
            )

            write_format = self.ui.combo_run_1.currentText().strip()

            content = re.sub(
                r'(writeFormat\s+)\w+(\s*;)',
                rf'\g<1>{write_format}\2',
                content
            )

            write_precision = self.ui.edit_run_7.text() or "12"

            content = re.sub(
                r'(writePrecision\s+)[\d]+(\s*;)',
                rf'\g<1>{write_precision}\2',
                content
            )

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

        try:

            file_path = system_path / "controlDict"

            if not file_path.exists():

                return

            with open(file_path, 'r', encoding='utf-8') as f:

                content = f.read()

            match = re.search(r'startTime\s+([\d\.eE\+\-]+)\s*;', content)

            if match:

                self.ui.edit_run_1.setText(match.group(1))

            match = re.search(r'endTime\s+([\d\.eE\+\-]+)\s*;', content)

            if match:

                self.ui.edit_run_2.setText(match.group(1))

            match = re.search(r'deltaT\s+([\d\.eE\+\-]+)\s*;', content)

            if match:

                self.ui.edit_run_3.setText(match.group(1))

            match = re.search(r'writeInterval\s+([\d\.eE\+\-]+)\s*;', content)

            if match:

                self.ui.edit_run_4.setText(match.group(1))

            match = re.search(r'maxCo\s+([\d\.eE\+\-]+)\s*;', content)

            if match:

                self.ui.edit_run_5.setText(match.group(1))

            match = re.search(r'purgeWrite\s+(\d+)\s*;', content)

            if match:

                purge_value = int(match.group(1))

                if purge_value > 0:

                    self.ui.groupBox_13.setChecked(True)

                    self.ui.edit_run_6.setText(match.group(1))

                else:

                    self.ui.groupBox_13.setChecked(False)

                    self.ui.edit_run_6.setText("20")

            match = re.search(r'writeFormat\s+(\w+)\s*;', content)

            if match:

                write_format = match.group(1)

                self._set_combo_text(self.ui.combo_run_1, write_format)

            match = re.search(r'writePrecision\s+(\d+)\s*;', content)

            if match:

                self.ui.edit_run_7.setText(match.group(1))

            match = re.search(r'timePrecision\s+(\d+)\s*;', content)

            if match:

                self.ui.edit_run_8.setText(match.group(1))

        except Exception:

            traceback.print_exc()

