"""
Internal registry client for dashboard registration.

This module is NOT part of the public API - it's only used internally by the CLI.
Users should register dashboards via `streamviz serve` command, not by calling
these functions directly.
"""

from typing import Optional, Dict, Any

import httpx
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from viz.layout.dashboard import Dashboard
from .extractor import ComponentExtractor, serialize_function
from .serializer import serialize_dashboard, serialize_component

console = Console()


class RegistryClient:
    """
    Internal client for registering dashboards with the registry API.

    This class is used internally by the CLI and should not be used directly
    by end users. Registration should happen through `streamviz serve`.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        username: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None
    ):
        """
        Initialize registry client.

        Args:
            base_url: Registry API URL
            username: Username for authentication
            password: Password for authentication
            token: JWT token (if already authenticated)
        """
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.client = httpx.Client(timeout=60.0)

        # Auto-login if credentials provided
        if username and password and not token:
            self.login(username, password)

    def login(self, username: str, password: str) -> str:
        """
        Login and obtain JWT token.

        Args:
            username: Username
            password: Password

        Returns:
            JWT token

        Raises:
            httpx.HTTPStatusError: If login fails
        """
        response = self.client.post(
            f"{self.base_url}/auth/login",
            json={"username": username, "password": password}
        )
        response.raise_for_status()
        data = response.json()
        self.token = data["access_token"]
        return self.token

    def _get_headers(self) -> Dict[str, str]:
        """Get headers with authentication token."""
        if not self.token:
            raise ValueError("Not authenticated. Provide username/password or token.")
        return {"Authorization": f"Bearer {self.token}"}

    def register_dashboard_full(self, dashboard: Dashboard) -> Dict[str, Any]:
        """
        Complete registration flow: functions → components → dashboard.

        This is the main entry point used by the CLI.

        Args:
            dashboard: Dashboard instance to register

        Returns:
            Dictionary with registration results

        Raises:
            httpx.HTTPStatusError: If any registration step fails
        """
        results = {
            "functions": [],
            "components": [],
            "dashboard": None,
            "errors": []
        }

        # Extract components and functions
        extractor = ComponentExtractor(dashboard)
        extractor.extract()

        # Register functions
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:

            # Functions
            functions = extractor.get_functions()
            if functions:
                task = progress.add_task(
                    f"[cyan]Registering {len(functions)} function(s)...",
                    total=len(functions)
                )
                for func, name in functions:
                    try:
                        result = self._register_function(func, name)
                        results["functions"].append({"name": name, "status": "success"})
                        console.print(f"  [green]✓[/green] Function: {name}")
                        progress.advance(task)
                    except Exception as e:
                        results["errors"].append({"type": "function", "name": name, "error": str(e)})
                        console.print(f"  [red]✗[/red] Function: {name} - {e}")
                        progress.advance(task)

            # Components
            components = extractor.get_components()
            if components:
                task = progress.add_task(
                    f"[cyan]Registering {len(components)} component(s)...",
                    total=len(components)
                )
                for component, name in components:
                    try:
                        result = self._register_component(component, name)
                        results["components"].append({"name": name, "status": "success"})
                        console.print(f"  [green]✓[/green] Component: {name}")
                        progress.advance(task)
                    except Exception as e:
                        results["errors"].append({"type": "component", "name": name, "error": str(e)})
                        console.print(f"  [red]✗[/red] Component: {name} - {e}")
                        progress.advance(task)

        # Register dashboard
        try:
            console.print(f"[cyan]Registering dashboard: {dashboard.title}...[/cyan]")
            dashboard_result = self._register_dashboard(dashboard)
            results["dashboard"] = {"id": dashboard.id, "status": "success"}
            console.print(f"[green]✓[/green] Dashboard registered: {dashboard.id}")
            console.print(f"[blue]Dashboard URL:[/blue] {self.base_url}/dashboards/{dashboard.id}")
        except Exception as e:
            results["errors"].append({"type": "dashboard", "id": dashboard.id, "error": str(e)})
            console.print(f"[red]✗[/red] Dashboard registration failed: {e}")

        return results

    def _register_function(self, func: Any, name: str) -> Dict[str, Any]:
        """
        Register a function with the registry (PUT for idempotent update).

        Args:
            func: Function object
            name: Function name

        Returns:
            Registration response
        """
        function_data = serialize_function(func, name)

        response = self.client.put(
            f"{self.base_url}/functions/{name}",
            json=function_data,
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    def _register_component(self, component_class: type, name: str) -> Dict[str, Any]:
        """
        Register a component with the registry (PUT for upsert).

        Args:
            component_class: Component class (Type[Component])
            name: Component name

        Returns:
            Registration response
        """
        component_data = serialize_component(component_class, name)

        # Try PUT first (update existing), fallback to POST (create new)
        response = self.client.put(
            f"{self.base_url}/components/{name}",
            json=component_data,
            headers=self._get_headers()
        )

        if response.status_code == 404:
            # Component doesn't exist, create it
            response = self.client.post(
                f"{self.base_url}/components/",
                json=component_data,
                headers=self._get_headers()
            )

        response.raise_for_status()
        return response.json()

    def _register_dashboard(self, dashboard: Dashboard) -> Dict[str, Any]:
        """
        Register dashboard structure with the registry.

        Args:
            dashboard: Dashboard instance

        Returns:
            Registration response
        """
        # Serialize dashboard structure
        structure = serialize_dashboard(dashboard)

        dashboard_data = {
            "id": dashboard.id,
            "title": dashboard.title,
            "description": dashboard.description,
            "structure": structure
        }

        # Try PUT first (update existing), fallback to POST (create new)
        response = self.client.put(
            f"{self.base_url}/dashboards/{dashboard.id}",
            json=dashboard_data,
            headers=self._get_headers()
        )

        if response.status_code == 404:
            # Dashboard doesn't exist, create it
            response = self.client.post(
                f"{self.base_url}/dashboards/",
                json=dashboard_data,
                headers=self._get_headers()
            )

        response.raise_for_status()
        return response.json()

    def close(self):
        """Close the HTTP client."""
        self.client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
