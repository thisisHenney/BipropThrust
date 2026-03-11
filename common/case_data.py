
import json

from dataclasses import dataclass, asdict, field

from datetime import datetime

from pathlib import Path

from typing import Optional

from nextlib.base.basecase import BaseCase

@dataclass

class GeometryData:

    name: str = ""

    path: str = ""

    is_visible: bool = True

    position: tuple[float, float, float] = field(default_factory=lambda: (0.0, 0.0, 0.0))

    rotation: tuple[float, float, float] = field(default_factory=lambda: (0.0, 0.0, 0.0))

    probe_position: tuple[float, float, float] = field(default_factory=lambda: (0.0, 0.0, 0.0))

    def __post_init__(self):

        if self.name and not self.path and self.name != "fluid":

            raise ValueError("Geometry path must be provided with name")

    def to_dict(self) -> dict:

        return asdict(self)

    @classmethod

    def from_dict(cls, data: dict) -> "GeometryData":

        if "position" in data and isinstance(data["position"], list):

            data["position"] = tuple(data["position"])

        if "rotation" in data and isinstance(data["rotation"], list):

            data["rotation"] = tuple(data["rotation"])

        if "probe_position" in data:

            if isinstance(data["probe_position"], list):

                data["probe_position"] = tuple(data["probe_position"])

        else:

            data["probe_position"] = (0.0, 0.0, 0.0)

        return cls(**data)

@dataclass

class CaseData(BaseCase):

    created_time: str = field(
        default_factory=lambda: datetime.now().isoformat(timespec="seconds")
    )

    modified_time: str = field(
        default_factory=lambda: datetime.now().isoformat(timespec="seconds")
    )

    objects: dict[str, GeometryData] = field(default_factory=dict)

    description: str = ""

    point_probe_position: tuple[float, float, float] = field(default_factory=lambda: (0.0, 0.0, 0.0))

    def __post_init__(self):

        super().__post_init__()

    def add_geometry(self, file_path: str) -> str:

        path = Path(file_path)

        if not path.exists():

            raise FileNotFoundError(f"Geometry file not found: {file_path}")

        name = path.stem

        if name in self.objects:

            self.objects[name].path = str(path.resolve())

            self._update_modified_time()

            return name

        self.objects[name] = GeometryData(
            name=name, path=str(path.resolve()), is_visible=True
        )

        self._update_modified_time()

        return name

    def remove_geometry(self, name: str) -> bool:

        if name == "fluid":

            print("Warning: Cannot remove protected geometry 'fluid'")

            return False

        if name not in self.objects:

            return False

        del self.objects[name]

        self._update_modified_time()

        return True

    def get_geometry(self, name: str) -> Optional[GeometryData]:

        return self.objects.get(name)

    def list_geometries(self) -> list[str]:

        return list(self.objects.keys())

    def set_geometry_visibility(self, name: str, visible: bool) -> bool:

        if name not in self.objects:

            return False

        self.objects[name].is_visible = visible

        self._update_modified_time()

        return True

    def set_geometry_position(
        self, name: str, x: float, y: float, z: float
    ) -> bool:

        if name not in self.objects:

            return False

        self.objects[name].position = (x, y, z)

        self._update_modified_time()

        return True

    def get_geometry_position(self, name: str) -> Optional[tuple[float, float, float]]:

        if name not in self.objects:

            return None

        return self.objects[name].position

    def set_geometry_rotation(
        self, name: str, rx: float, ry: float, rz: float
    ) -> bool:

        if name not in self.objects:

            return False

        self.objects[name].rotation = (rx, ry, rz)

        self._update_modified_time()

        return True

    def get_geometry_rotation(self, name: str) -> Optional[tuple[float, float, float]]:

        if name not in self.objects:

            return None

        return self.objects[name].rotation

    def set_geometry_probe_position(
        self, name: str, x: float, y: float, z: float
    ) -> bool:

        if name not in self.objects:

            return False

        self.objects[name].probe_position = (x, y, z)

        self._update_modified_time()

        return True

    def get_geometry_probe_position(self, name: str) -> Optional[tuple[float, float, float]]:

        if name not in self.objects:

            return None

        return getattr(self.objects[name], 'probe_position', None)

    def clear_geometries(self, keep_protected: bool = True) -> None:

        if keep_protected:

            self.objects = {
                k: v for k, v in self.objects.items() if k == "fluid"
            }

        else:

            self.objects.clear()

        self._update_modified_time()

    def _update_modified_time(self) -> None:

        self.modified_time = datetime.now().isoformat(timespec="seconds")

    def save(self) -> None:

        if not self.path:

            print("Warning: Case path not set, cannot save")

            return

        file_path = Path(self.path) / "case_data.json"

        try:

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

        if not self.path:

            print("Warning: Case path not set, cannot load")

            return

        file_path = Path(self.path) / "case_data.json"

        if not file_path.exists():

            return

        try:

            with open(file_path, "r", encoding="utf-8") as f:

                data = json.load(f)

            self.created_time = data.get("created_time", self.created_time)

            self.modified_time = data.get("modified_time", self.modified_time)

            self.description = data.get("description", "")

            objects_data = data.get("objects", {})

            self.objects = {
                name: GeometryData.from_dict(obj_data)
                for name, obj_data in objects_data.items()
            }

        except Exception as e:

            print(f"Error loading case data: {e}")

    def get_case_info(self) -> dict:

        return {
            "path": self.path,
            "created": self.created_time,
            "modified": self.modified_time,
            "description": self.description,
            "geometry_count": len(self.objects),
            "geometries": self.list_geometries(),
        }

    def __repr__(self) -> str:

        return (
            f"CaseData(path='{self.path}', geometries={len(self.objects)}, "
            f"created='{self.created_time}')"
        )

case_data = CaseData()

case_data.init(file="case_data.json")

