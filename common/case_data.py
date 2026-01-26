"""
Case Data - Simulation Case Management

This module manages simulation case-specific data including geometry,
settings, and metadata.
"""

import json
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from nextlib.base.basecase import BaseCase


@dataclass
class GeometryData:
    """
    Geometry object data.

    Attributes:
        name: Geometry name (stem of filename)
        path: Full path to geometry file (STL)
        is_visible: Whether geometry is visible in viewport
        position: Position offset (x, y, z) in meters
        rotation: Rotation angles (rx, ry, rz) in degrees
        probe_position: Point probe position for locationsInMesh (x, y, z) in meters
    """

    name: str = ""
    path: str = ""
    is_visible: bool = True
    position: tuple[float, float, float] = field(default_factory=lambda: (0.0, 0.0, 0.0))
    rotation: tuple[float, float, float] = field(default_factory=lambda: (0.0, 0.0, 0.0))
    probe_position: tuple[float, float, float] = field(default_factory=lambda: (0.0, 0.0, 0.0))

    def __post_init__(self):
        """Validate geometry data after creation."""
        if self.name and not self.path:
            raise ValueError("Geometry path must be provided with name")

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "GeometryData":
        """Create from dictionary."""
        # Convert position list to tuple if needed
        if "position" in data and isinstance(data["position"], list):
            data["position"] = tuple(data["position"])
        # Convert rotation list to tuple if needed
        if "rotation" in data and isinstance(data["rotation"], list):
            data["rotation"] = tuple(data["rotation"])
        # Convert probe_position list to tuple if needed, or set default if missing
        if "probe_position" in data:
            if isinstance(data["probe_position"], list):
                data["probe_position"] = tuple(data["probe_position"])
        else:
            data["probe_position"] = (0.0, 0.0, 0.0)
        return cls(**data)


@dataclass
class CaseData(BaseCase):
    """
    Simulation case data management.

    Inherits from BaseCase for directory and file management functionality.

    Attributes:
        created_time: ISO format timestamp of case creation
        modified_time: ISO format timestamp of last modification
        objects: Dictionary of geometry objects {name: GeometryData}
        description: Optional case description
        point_probe_position: Point probe position (x, y, z)
    """

    created_time: str = field(
        default_factory=lambda: datetime.now().isoformat(timespec="seconds")
    )
    modified_time: str = field(
        default_factory=lambda: datetime.now().isoformat(timespec="seconds")
    )
    objects: dict[str, GeometryData] = field(default_factory=dict)
    description: str = ""
    point_probe_position: tuple[float, float, float] = field(default_factory=lambda: (0.0, 0.0, 0.0))

    def add_geometry(self, file_path: str) -> str:
        """
        Add a geometry to the case.

        Args:
            file_path: Path to geometry file (STL)

        Returns:
            Name of added geometry

        Raises:
            ValueError: If geometry already exists
            FileNotFoundError: If file doesn't exist
        """
        path = Path(file_path)

        # Validate file exists
        if not path.exists():
            raise FileNotFoundError(f"Geometry file not found: {file_path}")

        # Get geometry name from filename
        name = path.stem

        # Check if already exists
        if name in self.objects:
            raise ValueError(f"Geometry '{name}' already exists in case")

        # Create geometry data
        self.objects[name] = GeometryData(
            name=name, path=str(path.resolve()), is_visible=True
        )

        # Update modification time
        self._update_modified_time()

        return name

    def remove_geometry(self, name: str) -> bool:
        """
        Remove a geometry from the case.

        Args:
            name: Geometry name to remove

        Returns:
            True if removed, False if not found

        Note:
            The 'fluid' geometry cannot be removed (protected).
        """
        # Protect fluid geometry
        if name == "fluid":
            print("Warning: Cannot remove protected geometry 'fluid'")
            return False

        # Check if exists
        if name not in self.objects:
            return False

        # Remove geometry
        del self.objects[name]

        # Update modification time
        self._update_modified_time()

        return True

    def get_geometry(self, name: str) -> Optional[GeometryData]:
        """
        Get geometry data by name.

        Args:
            name: Geometry name

        Returns:
            GeometryData if found, None otherwise
        """
        return self.objects.get(name)

    def list_geometries(self) -> list[str]:
        """
        Get list of all geometry names.

        Returns:
            List of geometry names
        """
        return list(self.objects.keys())

    def set_geometry_visibility(self, name: str, visible: bool) -> bool:
        """
        Set geometry visibility.

        Args:
            name: Geometry name
            visible: Visibility state

        Returns:
            True if updated, False if geometry not found
        """
        if name not in self.objects:
            return False

        self.objects[name].is_visible = visible
        self._update_modified_time()
        return True

    def set_geometry_position(
        self, name: str, x: float, y: float, z: float
    ) -> bool:
        """
        Set geometry position offset.

        Args:
            name: Geometry name
            x: X position offset in meters
            y: Y position offset in meters
            z: Z position offset in meters

        Returns:
            True if updated, False if geometry not found
        """
        if name not in self.objects:
            return False

        self.objects[name].position = (x, y, z)
        self._update_modified_time()
        return True

    def get_geometry_position(self, name: str) -> Optional[tuple[float, float, float]]:
        """
        Get geometry position offset.

        Args:
            name: Geometry name

        Returns:
            Position tuple (x, y, z) or None if not found
        """
        if name not in self.objects:
            return None

        return self.objects[name].position

    def set_geometry_rotation(
        self, name: str, rx: float, ry: float, rz: float
    ) -> bool:
        """
        Set geometry rotation angles.

        Args:
            name: Geometry name
            rx: X rotation angle in degrees
            ry: Y rotation angle in degrees
            rz: Z rotation angle in degrees

        Returns:
            True if updated, False if geometry not found
        """
        if name not in self.objects:
            return False

        self.objects[name].rotation = (rx, ry, rz)
        self._update_modified_time()
        return True

    def get_geometry_rotation(self, name: str) -> Optional[tuple[float, float, float]]:
        """
        Get geometry rotation angles.

        Args:
            name: Geometry name

        Returns:
            Rotation tuple (rx, ry, rz) in degrees or None if not found
        """
        if name not in self.objects:
            return None

        return self.objects[name].rotation

    def set_geometry_probe_position(
        self, name: str, x: float, y: float, z: float
    ) -> bool:
        """
        Set geometry point probe position.

        Args:
            name: Geometry name
            x: X position in meters
            y: Y position in meters
            z: Z position in meters

        Returns:
            True if updated, False if geometry not found
        """
        if name not in self.objects:
            return False

        self.objects[name].probe_position = (x, y, z)
        self._update_modified_time()
        return True

    def get_geometry_probe_position(self, name: str) -> Optional[tuple[float, float, float]]:
        """
        Get geometry point probe position.

        Args:
            name: Geometry name

        Returns:
            Probe position tuple (x, y, z) or None if not found
        """
        if name not in self.objects:
            return None

        # Handle old objects that don't have probe_position yet
        return getattr(self.objects[name], 'probe_position', None)

    def clear_geometries(self, keep_protected: bool = True) -> None:
        """
        Clear all geometries.

        Args:
            keep_protected: If True, keeps 'fluid' geometry
        """
        if keep_protected:
            # Keep only fluid
            self.objects = {
                k: v for k, v in self.objects.items() if k == "fluid"
            }
        else:
            self.objects.clear()

        self._update_modified_time()

    def _update_modified_time(self) -> None:
        """Update the modified timestamp."""
        self.modified_time = datetime.now().isoformat(timespec="seconds")

    def save(self) -> None:
        """
        Save case data to JSON file.

        Saves to: {case_path}/case_data.json
        """
        if not self.path:
            print("Warning: Case path not set, cannot save")
            return

        file_path = Path(self.path) / "case_data.json"

        try:
            # Convert objects dict to serializable format
            data = asdict(self)
            data["objects"] = {
                name: obj.to_dict() if hasattr(obj, "to_dict") else asdict(obj)
                for name, obj in self.objects.items()
            }

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        except Exception as e:
            print(f"Error saving case data: {e}")

    def load(self) -> None:
        """
        Load case data from JSON file.

        Loads from: {case_path}/case_data.json
        """
        if not self.path:
            print("Warning: Case path not set, cannot load")
            return

        file_path = Path(self.path) / "case_data.json"

        if not file_path.exists():
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Update fields
            self.created_time = data.get("created_time", self.created_time)
            self.modified_time = data.get("modified_time", self.modified_time)
            self.description = data.get("description", "")

            # Reconstruct objects
            objects_data = data.get("objects", {})
            self.objects = {
                name: GeometryData.from_dict(obj_data)
                for name, obj_data in objects_data.items()
            }

        except Exception as e:
            print(f"Error loading case data: {e}")

    def get_case_info(self) -> dict:
        """
        Get case information summary.

        Returns:
            Dictionary with case info
        """
        return {
            "path": self.path,
            "created": self.created_time,
            "modified": self.modified_time,
            "description": self.description,
            "geometry_count": len(self.objects),
            "geometries": self.list_geometries(),
        }

    def __repr__(self) -> str:
        """String representation of CaseData."""
        return (
            f"CaseData(path='{self.path}', geometries={len(self.objects)}, "
            f"created='{self.created_time}')"
        )


# Global singleton instance
case_data = CaseData()
case_data.init(file="case_data.json")
