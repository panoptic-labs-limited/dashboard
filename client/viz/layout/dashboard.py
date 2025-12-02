"""
Top-level dashboard components (Page and Dashboard).

These are the main entry points for building dashboards.
"""

from __future__ import annotations

from typing import Literal, Union

from pydantic import field_validator

from viz.core.layout import Container
from viz.inputs.base import Input
from viz.widgets import Widget
from .containers import Section, Row, Column, Tabs


class Page(Container[Union[Section, Row, Column, Tabs, Widget, Input]]):
    """
    Page container representing a dashboard page/view.

    Can contain: Sections, Rows, Columns, Tabs, Widgets, Inputs
    """

    type: Literal["page"] = "page"
    title: str
    description: str | None = None
    icon: str | None = None


class Dashboard(Container[Page]):
    """
    Top-level dashboard container.

    Can only contain: Page objects
    """

    type: Literal["dashboard"] = "dashboard"
    title: str
    description: str | None = None
    version: str = "1.0.0"

    @field_validator('children')
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
            >>> dashboard = Dashboard(title='My Dashboard')
            >>> with dashboard.page(title='Overview'):
            ...     L.widget(...)
        """
        page = Page(title=title, description=description, **kwargs)
        self.add(page)
        return page
