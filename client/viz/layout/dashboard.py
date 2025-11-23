"""
Top-level dashboard components (Page and Dashboard).

These are the main entry points for building dashboards.
"""

from __future__ import annotations

from typing import Union, Literal, Optional, List

from pydantic import Field, field_validator

from .base import Container
from .components import Widget, Selector
from .containers import Section, Row, Column, Tabs


class Page(Container):
    """
    Page container representing a dashboard page/view.

    Can contain: Sections, Rows, Columns, Tabs, Widgets, Selectors
    """

    type: Literal["page"] = "page"
    children: list[Union[Section, Row, Column, Tabs, Widget, Selector]] = Field(default_factory=list)
    title: str
    description: Optional[str] = None
    icon: Optional[str] = None


class Dashboard(Container):
    """
    Top-level dashboard container.

    Can only contain: Page objects
    """

    type: Literal["dashboard"] = "dashboard"
    children: list[Page] = Field(default_factory=list)
    title: str
    description: Optional[str] = None
    version: str = "1.0.0"

    @field_validator('children')
    @classmethod
    def validate_has_pages(cls, v: List[Page]) -> List[Page]:
        """Ensure dashboard has at least one page."""
        if not v:
            raise ValueError("Dashboard must have at least one page")
        return v

    def page(self, title: str, description: Optional[str] = None, **kwargs) -> Page:
        """
        Create and add a page to this dashboard.

        Args:
            title: Page title
            description: Optional description
            **kwargs: Additional page fields

        Returns:
            The created Page instance

        Example:
            >>> dashboard = Dashboard(title='My Dashboard')
            >>> with dashboard.page(title='Overview'):
            ...     L.widget(...)
        """
        page = Page(title=title, description=description, **kwargs)
        self.add(page)
        return page


# Resolve forward references
Page.model_rebuild()
