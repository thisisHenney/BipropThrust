
import sys
import signal
import traceback
from pathlib import Path
from datetime import datetime

# Add nextlib to path
sys.path.insert(0, '/home/test/lib')

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt


def _global_excepthook(exc_type, exc_value, exc_tb):
    if issubclass(exc_type, KeyboardInterrupt):
        return
    print("\n" + "=" * 60)
    print("[UNHANDLED EXCEPTION]")
    traceback.print_exception(exc_type, exc_value, exc_tb)
    print("=" * 60 + "\n")


sys.excepthook = _global_excepthook


def _sigint_handler(sig, frame):
    app = QApplication.instance()
    if app:
        app.quit()


signal.signal(signal.SIGINT, _sigint_handler)

from nextlib.utils.single_instance import SingleInstance

from common.app_data import app_data
from view.main.main_window import MainWindow
from view.style.theme import apply_theme


def qt_message_handler(_msg_type, _context, message):
    # Filter out the device pixel ratio warning
    if "cached device pixel ratio" in message.lower():
        return
    # Other messages are silently ignored


class BipropThrustApp:

    def __init__(self, case_path: str = ""):
        self.app = None
        
        self.main_window = None
        self.case_path = case_path
        self._setup_application()

    def _setup_application(self) -> None:
        # Install custom message handler to filter warnings
        from PySide6.QtCore import qInstallMessageHandler
        qInstallMessageHandler(qt_message_handler)

        # Enable high DPI scaling
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )

        # Create Qt application
        self.app = QApplication(sys.argv)

        # Set application metadata
        self.app.setApplicationName(app_data.name)
        self.app.setApplicationVersion(app_data.version)
        self.app.setOrganizationName("NEXTfoam")

        # Apply professional dark theme
        apply_theme(self.app)

        # Prevent duplicate instances
        self._single_instance = SingleInstance(f"com.nextfoam.{app_data.name}")
        if not self._single_instance.try_lock():
            QMessageBox.critical(
                None, app_data.name,
                f"{app_data.name} is already running.\n\nOnly one instance can run at a time."
            )
            sys.exit(1)

    def _get_or_create_case_path(self) -> str:
        if self.case_path:
            # Validate provided case path
            path = Path(self.case_path)
            if path.exists() and path.is_dir():
                return str(path.resolve())
            # If path doesn't exist, fall through to create temp case

        # Create temporary case
        temp_case_path = self._create_temp_case()
        return temp_case_path

    def _create_temp_case(self) -> str:
        # Create temp directory with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_name = f"temp_{timestamp}"

        # Temp cases stored in user_path/temp/
        temp_base = Path(app_data.user_path) / "temp"
        temp_base.mkdir(parents=True, exist_ok=True)

        temp_case = temp_base / temp_name
        temp_case.mkdir(exist_ok=True)

        # Copy basecase template to temp case
        self._copy_basecase_to(temp_case)

        return str(temp_case)

    def _copy_basecase_to(self, target_path: Path) -> None:
        import shutil

        # Get basecase path (config/basecase in project root)
        project_root = Path(__file__).parent
        basecase_path = project_root / "config" / "basecase"

        if not basecase_path.exists():
            return

        try:
            # Copy all contents from basecase to target
            # Use copytree with dirs_exist_ok to merge directories
            for item in basecase_path.iterdir():
                src = basecase_path / item.name
                dst = target_path / item.name

                if src.is_dir():
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)

        except Exception:
            traceback.print_exc()

    def start(self) -> None:
        try:
            # Get or create case path
            case_path = self._get_or_create_case_path()

            # Create main window
            self.main_window = MainWindow(case_path)

            # Initialize and show
            self.main_window.initialize()
            self.main_window.show()

        except Exception as e:
            import traceback옴
            traceback.print_exc()
            sys.exit(1)

    def run(self) -> int:
        return self.app.exec()

    def cleanup_old_temp_cases(self) -> None:
        import shutil

        temp_base = Path(app_data.user_path) / "temp"
        if not temp_base.exists():
            return

        try:
            for temp_dir in temp_base.iterdir():
                if not temp_dir.is_dir() or not temp_dir.name.startswith("temp_"):
                    continue
                shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            traceback.print_exc()


def main():
    case_path = ""
    if len(sys.argv) > 1:
        case_path = sys.argv[1]

    app = BipropThrustApp(case_path)

    # Clean up leftover temp cases from crashed/previous sessions
    app.cleanup_old_temp_cases()

    app.start()

    exit_code = app.run()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
