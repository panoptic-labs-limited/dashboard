"""Dashboard - top-level container."""

from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class Dashboard:
    """
    Top-level dashboard container.

    Contains multiple pages (tabs) and manages the overall
    dashboard structure and registration.

    Example:
        dashboard = Dashboard(
            name="sales_dashboard",
            title="Sales Analytics",
            description="Monthly sales metrics and trends"
        )
        dashboard.add_page(overview_page)
        dashboard.add_page(details_page)
        dashboard.register(client)
    """
    name: str
    title: str
    description: Optional[str] = None
    pages: List = field(default_factory=list)

    def add_page(self, page) -> None:
        """Add a page to the dashboard."""
        self.pages.append(page)

    def to_dict(self) -> dict:
        """Serialize to dictionary for storage in registry."""
        return {
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "pages": [
                page.to_dict() if hasattr(page, 'to_dict') else page
                for page in self.pages
            ]
        }

    def register(self, client) -> dict:
        """
        Register dashboard with the function registry.

        Args:
            client: RegistryClient instance

        Returns:
            Dashboard registration response from registry (as dict)
        """
        from viz.api.client import RegistryClient

        if not isinstance(client, RegistryClient):
            raise TypeError("client must be a RegistryClient instance")

        # Serialize dashboard structure
        structure = self.to_dict()

        # Register with the registry
        response = client.create_dashboard(
            name=self.name,
            title=self.title,
            description=self.description,
            structure=structure
        )

        # Convert Pydantic model to dict
        return response.model_dump()
