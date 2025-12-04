"""
Page container for dashboard layouts.
"""

from __future__ import annotations

from typing import Literal, Union

from viz.core.layout import BaseContainer
from viz.inputs.base import BaseInput
from viz.widgets import BaseWidget
from .containers import Section, Row, Column, Tabs


class Page(BaseContainer[Union[Section, Row, Column, Tabs, BaseWidget, BaseInput]]):
    """
    Page container representing a dashboard page/view.

    Can contain: Sections, Rows, Columns, Tabs, Widgets, Inputs
    """

    type: Literal["page"] = "page"
    title: str
    description: str | None = None
    icon: str | None = None
