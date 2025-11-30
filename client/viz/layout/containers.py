"""
Container components (Row, Column, Tab, Tabs, Section).

These components can contain children and form the structure of layouts.
"""

from __future__ import annotations

from typing import Literal
from typing import Union

from pydantic import Field

from viz.core.layout import Container, LeafNode

# Type alias for standard layout children
LayoutChild = Union['Row', 'Column', LeafNode]


class Row(Container[LayoutChild]):
    """
    Horizontal layout container.

    Children are arranged left-to-right.
    Can contain: Rows, Columns, Widgets, Inputs
    """

    type: Literal["row"] = "row"
    gap: str | None = Field(None, description="Gap between children (CSS)")
    align: Literal["start", "center", "end", "stretch"] | None = None


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
    gap: str | None = Field(None, description="Gap between children (CSS)")


class Tab(Container[LayoutChild]):
    """
    Individual tab within a Tabs container.

    Can contain: Rows, Columns, Widgets, Inputs
    """

    type: Literal["tab"] = "tab"
    title: str
    icon: str | None = None
    disabled: bool = False


class Tabs(Container[Tab]):
    """
    Tab container holding multiple Tab components.

    Can only contain: Tab objects
    """

    type: Literal["tabs"] = "tabs"
    default_tab: str | None = Field(
        None,
        description="ID of default active tab"
    )


class Section(Container[Union[Row, Column, Tabs, LeafNode]]):
    """
    Section for organizing content within a Page.

    Can contain: Rows, Columns, Tabs, Widgets, Inputs
    """

    type: Literal["section"] = "section"
    title: str | None = None
    collapsible: bool = False
    collapsed: bool = False
