"""
Page container for dashboard layouts.
"""

from __future__ import annotations

from typing import Literal, Union

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
