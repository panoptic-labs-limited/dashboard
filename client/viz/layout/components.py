"""
Leaf components (Widget).

These are terminal nodes in the layout tree that don't contain children.
"""

from __future__ import annotations

from typing import Literal, Any, TYPE_CHECKING

from pydantic import Field

from .base import LeafNode
from .enums import WidgetType

if TYPE_CHECKING:
    from viz.core.component import Component


class Widget(LeafNode):
    """
    Leaf node representing a visualization or content widget.

    Examples: charts, tables, metrics, images
    """

    type: Literal["widget"] = "widget"
    widget_type: WidgetType
    title: str | None = None
    description: str | None = None

    # Component reference (instance, not alias string)
    # Using default=None instead of exclude=True to keep the field accessible
    component: Component | None = Field(default=None, repr=False)
    component_alias: str | None = None  # Will be populated during serialization
    params: dict[str, Any] = Field(default_factory=dict)

    def model_dump(self, **kwargs):
        """Override to exclude component field from serialization."""
        data = super().model_dump(**kwargs)
        data.pop('component', None)
        return data

    # Widget-specific configuration
    config: dict[str, Any] = Field(default_factory=dict)
