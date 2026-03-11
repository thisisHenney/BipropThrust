
from typing import Any, Optional

class AppContext:

    def __init__(self):

        self._services: dict[str, Any] = {}

    def register(self, name: str, service: Any) -> None:

        if name in self._services:

            raise ValueError(f"Service '{name}' is already registered")

        self._services[name] = service

    def get(self, name: str) -> Optional[Any]:

        return self._services.get(name)

    def has(self, name: str) -> bool:

        return name in self._services

    def unregister(self, name: str) -> None:

        if name in self._services:

            del self._services[name]

    def clear(self) -> None:

        self._services.clear()

    def list_services(self) -> list[str]:

        return list(self._services.keys())

