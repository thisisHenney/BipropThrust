"""
Application Context - Service Registry and Dependency Injection Container

This module provides a simple service locator pattern for managing
application-wide services and components.
"""

from typing import Any, Optional


class AppContext:
    """
    Service registry for managing application-wide services.

    Provides dependency injection functionality to decouple components
    and make them easier to test and maintain.

    Example:
        >>> ctx = AppContext()
        >>> ctx.register("database", db_instance)
        >>> db = ctx.get("database")
    """

    def __init__(self):
        """Initialize the service registry."""
        self._services: dict[str, Any] = {}

    def register(self, name: str, service: Any) -> None:
        """
        Register a service in the context.

        Args:
            name: Service name/identifier
            service: Service instance to register

        Raises:
            ValueError: If service name is already registered
        """
        if name in self._services:
            raise ValueError(f"Service '{name}' is already registered")
        self._services[name] = service

    def get(self, name: str) -> Optional[Any]:
        """
        Retrieve a service from the context.

        Args:
            name: Service name/identifier

        Returns:
            The registered service or None if not found
        """
        return self._services.get(name)

    def has(self, name: str) -> bool:
        """
        Check if a service is registered.

        Args:
            name: Service name/identifier

        Returns:
            True if service exists, False otherwise
        """
        return name in self._services

    def unregister(self, name: str) -> None:
        """
        Unregister a service from the context.

        Args:
            name: Service name/identifier
        """
        if name in self._services:
            del self._services[name]

    def clear(self) -> None:
        """Clear all registered services."""
        self._services.clear()

    def list_services(self) -> list[str]:
        """
        Get list of all registered service names.

        Returns:
            List of service names
        """
        return list(self._services.keys())
