"""API client for communicating with the Viz Function Registry."""

from typing import Optional, Dict, Any, List

import httpx

from viz_shared import (
    ComponentCreate,
    ComponentResponse,
    ComponentUpdate,
    DashboardCreate,
    DashboardResponse,
    DashboardUpdate,
    ComponentMetadata,
    ComponentParameter,
)


class RegistryClient:
    """Client for interacting with the Viz Function Registry API."""

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        username: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None
    ):
        """
        Initialize the registry client.

        Args:
            base_url: Base URL of the registry API
            username: Username for authentication (optional)
            password: Password for authentication (optional)
            token: JWT token for authentication (optional)
        """
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.client = httpx.Client(timeout=30.0)

        # Auto-login if username/password provided
        if username and password and not token:
            self.login(username, password)

    def login(self, username: str, password: str) -> str:
        """
        Login and get JWT token.

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

    def register(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """
        Register a new user.

        Args:
            username: Username
            email: Email address
            password: Password

        Returns:
            User data

        Raises:
            httpx.HTTPStatusError: If registration fails
        """
        response = self.client.post(
            f"{self.base_url}/auth/register",
            json={"username": username, "email": email, "password": password}
        )
        response.raise_for_status()
        return response.json()

    def _get_headers(self) -> Dict[str, str]:
        """Get headers with authentication token."""
        if not self.token:
            raise ValueError("Not authenticated. Call login() first or provide a token.")
        return {"Authorization": f"Bearer {self.token}"}

    # ========================================================================
    # Component Methods
    # ========================================================================

    def create_component(
        self,
        alias: str,
        class_name: str,
        source_code: str,
        description: Optional[str] = None,
        parameters: Optional[List[ComponentParameter]] = None,
        metadata: Optional[ComponentMetadata] = None,
        memory_limit_mb: int = 200,
        timeout_seconds: int = 30
    ) -> ComponentResponse:
        """
        Create a new component.

        Args:
            alias: Unique identifier for the component
            class_name: Name of the component class
            source_code: Complete Python source code
            description: Optional description
            parameters: Optional list of parameter definitions
            metadata: Optional metadata
            memory_limit_mb: Memory limit (default: 200MB)
            timeout_seconds: Timeout (default: 30s)

        Returns:
            Created component

        Raises:
            httpx.HTTPStatusError: If creation fails
        """
        component_data = ComponentCreate(
            alias=alias,
            class_name=class_name,
            source_code=source_code,
            description=description,
            parameters=parameters or [],
            metadata=metadata,
            memory_limit_mb=memory_limit_mb,
            timeout_seconds=timeout_seconds
        )

        response = self.client.post(
            f"{self.base_url}/components/",
            json=component_data.model_dump(),
            headers=self._get_headers()
        )
        response.raise_for_status()
        return ComponentResponse(**response.json())

    def list_components(self) -> List[ComponentResponse]:
        """List all components owned by the current user."""
        response = self.client.get(
            f"{self.base_url}/components/",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return [ComponentResponse(**c) for c in response.json()]

    def get_component(self, alias: str) -> ComponentResponse:
        """Get a component by alias."""
        response = self.client.get(
            f"{self.base_url}/components/{alias}",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return ComponentResponse(**response.json())

    def update_component(self, alias: str, update_data: ComponentUpdate) -> ComponentResponse:
        """Update a component."""
        response = self.client.put(
            f"{self.base_url}/components/{alias}",
            json=update_data.model_dump(exclude_unset=True),
            headers=self._get_headers()
        )
        response.raise_for_status()
        return ComponentResponse(**response.json())

    def delete_component(self, alias: str) -> None:
        """Delete a component."""
        response = self.client.delete(
            f"{self.base_url}/components/{alias}",
            headers=self._get_headers()
        )
        response.raise_for_status()

    # ========================================================================
    # Dashboard Methods
    # ========================================================================

    def create_dashboard(
        self,
        name: str,
        title: str,
        structure: Dict[str, Any],
        description: Optional[str] = None
    ) -> DashboardResponse:
        """
        Create a new dashboard.

        Args:
            name: Unique dashboard identifier
            title: Dashboard title
            structure: Dashboard structure (DashboardStructure dict)
            description: Optional description

        Returns:
            Created dashboard

        Raises:
            httpx.HTTPStatusError: If creation fails
        """
        dashboard_data = DashboardCreate(
            name=name,
            title=title,
            description=description,
            structure=structure
        )

        response = self.client.post(
            f"{self.base_url}/dashboards/",
            json=dashboard_data.model_dump(),
            headers=self._get_headers()
        )
        response.raise_for_status()
        return DashboardResponse(**response.json())

    def list_dashboards(self) -> List[DashboardResponse]:
        """List all dashboards owned by the current user."""
        response = self.client.get(
            f"{self.base_url}/dashboards/",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return [DashboardResponse(**d) for d in response.json()]

    def get_dashboard(self, name: str) -> DashboardResponse:
        """Get a dashboard by name."""
        response = self.client.get(
            f"{self.base_url}/dashboards/{name}",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return DashboardResponse(**response.json())

    def update_dashboard(self, name: str, update_data: DashboardUpdate) -> DashboardResponse:
        """Update a dashboard."""
        response = self.client.put(
            f"{self.base_url}/dashboards/{name}",
            json=update_data.model_dump(exclude_unset=True),
            headers=self._get_headers()
        )
        response.raise_for_status()
        return DashboardResponse(**response.json())

    def delete_dashboard(self, name: str) -> None:
        """Delete a dashboard."""
        response = self.client.delete(
            f"{self.base_url}/dashboards/{name}",
            headers=self._get_headers()
        )
        response.raise_for_status()

    def close(self):
        """Close the HTTP client."""
        self.client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
