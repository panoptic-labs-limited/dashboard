"""
Container components (Row, Column, Tab, Tabs, Section).

These components can contain children and form the structure of layouts.
"""

from __future__ import annotations

from typing import Union, Literal, Optional

from pydantic import Field

from .base import Container
from .components import Widget
from viz.inputs.base import Input

# Type alias for standard layout children
LayoutChild = Union['Row', 'Column', Widget, Input]


class Row(Container[LayoutChild]):
    """
    Horizontal layout container.

    Children are arranged left-to-right.
    Can contain: Rows, Columns, Widgets, Inputs
    """

    type: Literal["row"] = "row"
    gap: Optional[str] = Field(None, description="Gap between children (CSS)")
    align: Optional[Literal["start", "center", "end", "stretch"]] = None


class Column(Container[LayoutChild]):
    """
    Vertical layout container.

    Children are arranged top-to-bottom.
    Can contain: Rows, Columns, Widgets, Inputs

    Weight controls relative width when placed in a Row.
    E.g., weights [1, 2] → columns take 1/3 and 2/3 of space.
    """

    type: Literal["column"] = "column"
    weight: int = Field(1, description="Relative width weight (like CSS flex-grow)", ge=1)
    gap: Optional[str] = Field(None, description="Gap between children (CSS)")


class Tab(Container[LayoutChild]):
    """
    Individual tab within a Tabs container.

    Can contain: Rows, Columns, Widgets, Inputs
    """

    type: Literal["tab"] = "tab"
    title: str
    icon: Optional[str] = None
    disabled: bool = False


class Tabs(Container['Tab']):
    """
    Tab container holding multiple Tab components.

    Can only contain: Tab objects
    """

    type: Literal["tabs"] = "tabs"
    default_tab: Optional[str] = Field(
        None,
        description="ID of default active tab"
    )


class Section(Container[Union['Row', 'Column', 'Tabs', Widget, Input]]):
    """
    Section for organizing content within a Page.

    Can contain: Rows, Columns, Tabs, Widgets, Inputs
    """

    type: Literal["section"] = "section"
    title: Optional[str] = None
    collapsible: bool = False
    collapsed: bool = False


# Resolve forward references
Row.model_rebuild()
Column.model_rebuild()
Tab.model_rebuild()
Section.model_rebuild()
