"""
Dashboard - top-level configuration for a dashboard application.

Dashboard is not a layout container; it's a configuration object that
holds metadata and a collection of pages.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator, ConfigDict

from viz.layout.page import Page


class Dashboard(BaseModel):
    """
    Top-level dashboard configuration.

    Unlike layout containers (Row, Column, etc.), Dashboard is a configuration
    object that holds metadata and pages. It does not participate in the
    layout tree hierarchy.
    """

    model_config = ConfigDict(
        extra='forbid',
        validate_assignment=True,
    )

    id: str = Field(..., description="Unique dashboard identifier")
    title: str = Field(..., description="Dashboard title")
    description: str | None = Field(None, description="Dashboard description")
    version: str = Field("1.0.0", description="Dashboard version")

    pages: list[Page] = Field(default_factory=list, description="Dashboard pages")

    @field_validator('pages')
    @classmethod
    def validate_has_pages(cls, v: list[Page]) -> list[Page]:
        """Ensure dashboard has at least one page."""
        if not v:
            raise ValueError("Dashboard must have at least one page")
        return v

    def page(self, title: str, description: str | None = None, **kwargs) -> Page:
        """
        Create and add a page to this dashboard.

        Args:
            title: Page title
            description: Optional description
            **kwargs: Additional page fields

        Returns:
            The created Page instance

        Example:
            >>> dashboard = Dashboard(id='my_dashboard', title='My Dashboard')
            >>> with dashboard.page(title='Overview'):
            ...     L.row(...)
        """
        page = Page(title=title, description=description, **kwargs)
        self.pages.append(page)
        return page
