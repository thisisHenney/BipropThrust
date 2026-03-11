
import json

import platform

from dataclasses import dataclass, asdict, field

from pathlib import Path

from typing import Optional

from nextlib.utils.file import make_dir

@dataclass

class AppData:

    name: str = "BipropThrust"

    version: str = "v1.00"

    app_path: str = field(default="", init=False)

    config_path: str = field(default="", init=False)

    help_path: str = field(default="", init=False)

    res_path: str = field(default="", init=False)

    user_path: str = field(default="", init=False)

    window_geometry: dict = field(default_factory=dict, init=False)

    parallel_mesh_enabled: bool = field(default=True, init=False)

    parallel_run_enabled: bool = field(default=True, init=False)

    recent_cases: list = field(default_factory=list, init=False)

    _user_path_win: str = field(default="", init=False, repr=False)

    _user_path_linux: str = field(default="", init=False, repr=False)

    def __post_init__(self):

        self.app_path = str(Path(__file__).resolve().parents[1])

        self.config_path = str(Path(self.app_path) / "config")

        self.help_path = str(Path(self.app_path) / "help")

        self.res_path = str(Path(self.app_path) / "res")

        self._user_path_win = str(
            Path.home() / "AppData" / "Local" / "NEXTfoam" / self.name / self.version
        )

        self._user_path_linux = str(
            Path.home() / ".local" / "share" / "NEXTfoam" / self.name / self.version
        )

    @property

    def title(self) -> str:

        return f"{self.name}-{self.version}"

    def init(self) -> None:

        self._resolve_user_path()

        self._ensure_dirs()

    def _resolve_user_path(self) -> None:

        system = platform.system()

        if system == "Windows":

            self.user_path = self._user_path_win

        elif system == "Linux":

            self.user_path = self._user_path_linux

        else:

            self.user_path = str(Path.home() / ".NEXTfoam" / self.name / self.version)

    def _ensure_dirs(self) -> None:

        make_dir(self.user_path, exist_ok=True)

        for path_name in ["app_path", "config_path", "res_path"]:

            path = getattr(self, path_name)

            if not Path(path).exists():

                print(f"Warning: {path_name} does not exist: {path}")

    def add_recent_case(self, path: str, max_count: int = 10) -> None:

        """최근 케이스 목록 맨 앞에 추가 (중복 제거, 최대 max_count개 유지)"""

        path = str(Path(path).resolve())

        if path in self.recent_cases:

            self.recent_cases.remove(path)

        self.recent_cases.insert(0, path)

        self.recent_cases = self.recent_cases[:max_count]

        self.save()

    def save(self) -> None:

        file_path = Path(self.user_path) / "app_data.json"

        try:

            with open(file_path, "w", encoding="utf-8") as f:

                data = {k: v for k, v in asdict(self).items() if not k.startswith("_")}

                json.dump(data, f, ensure_ascii=False, indent=4)

        except Exception as e:

            print(f"Error saving app data: {e}")

    def load(self) -> None:

        file_path = Path(self.user_path) / "app_data.json"

        if not file_path.exists():

            return

        try:

            with open(file_path, "r", encoding="utf-8") as f:

                data = json.load(f)

            safe_fields = {
                "name", "version",
                "window_geometry",
                "parallel_mesh_enabled", "parallel_run_enabled",
                "recent_cases",
            }

            for k, v in data.items():

                if k in safe_fields:

                    setattr(self, k, v)

        except Exception as e:

            print(f"Error loading app data: {e}")

    def get_config_basecase_path(self) -> Path:

        return Path(self.config_path) / "basecase"

    def get_icon_path(self, icon_name: str) -> Optional[Path]:

        icon_path = Path(self.res_path) / "icons" / icon_name

        return icon_path if icon_path.exists() else None

    def __repr__(self) -> str:

        return (
            f"AppData(name='{self.name}', version='{self.version}', "
            f"app_path='{self.app_path}', user_path='{self.user_path}')"
        )

app_data = AppData()

app_data.init()

