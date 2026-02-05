"""
Application Data - Global Application Configuration and Settings

This module manages application-wide configuration, paths, and settings.
"""

import json
import platform
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Optional

from nextlib.utils.file import make_dir


@dataclass
class AppData:
    """
    Global application configuration and path management.

    Attributes:
        name: Application name
        version: Application version
        title: Application title (auto-generated from name and version)
        app_path: Application installation directory
        config_path: Configuration templates directory
        help_path: Help documentation directory
        res_path: Resources directory (icons, images, etc.)
        user_path: User-specific data directory (platform-dependent)
    """

    # Application identity
    name: str = "BipropThrust"
    version: str = "v1.00"

    # Paths (initialized in __post_init__)
    app_path: str = field(default="", init=False)
    config_path: str = field(default="", init=False)
    help_path: str = field(default="", init=False)
    res_path: str = field(default="", init=False)
    user_path: str = field(default="", init=False)

    # Window geometry (saved/restored across sessions)
    window_geometry: dict = field(default_factory=dict, init=False)

    # Platform-specific user paths
    _user_path_win: str = field(default="", init=False, repr=False)
    _user_path_linux: str = field(default="", init=False, repr=False)

    def __post_init__(self):
        """Initialize paths after dataclass creation."""
        # Set application base path (parent of common/)
        self.app_path = str(Path(__file__).resolve().parents[1])

        # Set sub-paths
        self.config_path = str(Path(self.app_path) / "config")
        self.help_path = str(Path(self.app_path) / "help")
        self.res_path = str(Path(self.app_path) / "res")

        # Set platform-specific user paths
        self._user_path_win = str(
            Path.home() / "AppData" / "Local" / "NEXTfoam" / self.name / self.version
        )
        self._user_path_linux = str(
            Path.home() / ".local" / "NEXTfoam" / self.name / self.version
        )

    @property
    def title(self) -> str:
        """Get application title."""
        return f"{self.name}-{self.version}"

    def init(self) -> None:
        """
        Initialize application data.

        Sets up user path based on platform and ensures
        all required directories exist.
        """
        self._resolve_user_path()
        self._ensure_dirs()

    def _resolve_user_path(self) -> None:
        """Set user_path based on current platform."""
        system = platform.system()
        if system == "Windows":
            self.user_path = self._user_path_win
        elif system == "Linux":
            self.user_path = self._user_path_linux
        else:
            # Fallback for other platforms (macOS, etc.)
            self.user_path = str(Path.home() / ".NEXTfoam" / self.name / self.version)

    def _ensure_dirs(self) -> None:
        """Ensure all required directories exist."""
        # Create user directory
        make_dir(self.user_path, exist_ok=True)

        # Verify critical paths exist
        for path_name in ["app_path", "config_path", "res_path"]:
            path = getattr(self, path_name)
            if not Path(path).exists():
                print(f"Warning: {path_name} does not exist: {path}")

    def save(self) -> None:
        """
        Save application data to JSON file.

        Saves to: {user_path}/app_data.json
        """
        file_path = Path(self.user_path) / "app_data.json"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                # Exclude private fields from serialization
                data = {k: v for k, v in asdict(self).items() if not k.startswith("_")}
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving app data: {e}")

    def load(self) -> None:
        """
        Load application data from JSON file.

        Loads from: {user_path}/app_data.json
        Only updates non-path fields to preserve correct paths.
        """
        file_path = Path(self.user_path) / "app_data.json"
        if not file_path.exists():
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Only update safe fields (not paths)
            safe_fields = {
                "name", "version",
                "window_geometry",
            }
            for k, v in data.items():
                if k in safe_fields:
                    setattr(self, k, v)
        except Exception as e:
            print(f"Error loading app data: {e}")

    def get_config_basecase_path(self) -> Path:
        """
        Get the base case template path.

        Returns:
            Path to config/basecase directory
        """
        return Path(self.config_path) / "basecase"

    def get_icon_path(self, icon_name: str) -> Optional[Path]:
        """
        Get path to an icon file.

        Args:
            icon_name: Icon filename (e.g., "app_icon.png")

        Returns:
            Path to icon file or None if not found
        """
        icon_path = Path(self.res_path) / "icons" / icon_name
        return icon_path if icon_path.exists() else None

    def __repr__(self) -> str:
        """String representation of AppData."""
        return (
            f"AppData(name='{self.name}', version='{self.version}', "
            f"app_path='{self.app_path}', user_path='{self.user_path}')"
        )


# Global singleton instance
app_data = AppData()
app_data.init()
