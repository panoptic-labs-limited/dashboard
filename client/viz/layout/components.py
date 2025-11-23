"""
Leaf components (Widget).

These are terminal nodes in the layout tree that don't contain children.
"""

from __future__ import annotations

from typing import Literal, Any

from pydantic import Field

from .base import LeafNode
from .enums import WidgetType


class Widget(LeafNode):
    """
    Leaf node representing a visualization or content widget.

    Examples: charts, tables, metrics, images
    """

    type: Literal["widget"] = "widget"
    widget_type: WidgetType
    title: str | None = None
    description: str | None = None

    # Component reference
    component_alias: str | None = None
    params: dict[str, Any] = Field(default_factory=dict)

    # Widget-specific configuration
    config: dict[str, Any] = Field(default_factory=dict)
