"""
Leaf components (Widget and Selector).

These are terminal nodes in the layout tree that don't contain children.
"""

from __future__ import annotations
from typing import Literal, Optional, List, Any
from pydantic import Field

from .base import LayoutNode
from .enums import WidgetType, SelectorType


class Widget(LayoutNode):
    """
    Leaf node representing a visualization or content widget.

    Examples: charts, tables, metrics, images
    """

    type: Literal["widget"] = "widget"
    widget_type: WidgetType
    title: Optional[str] = None
    description: Optional[str] = None

    # Component reference
    component_alias: Optional[str] = None
    params: dict[str, Any] = Field(default_factory=dict)

    # Widget-specific configuration
    config: dict[str, Any] = Field(default_factory=dict)


class Selector(LayoutNode):
    """
    Leaf node for user input components.

    Examples: dropdowns, date pickers, sliders
    """

    type: Literal["selector"] = "selector"
    selector_type: SelectorType
    name: str = Field(..., description="Parameter name")
    label: str
    default: Any = None
    options: Optional[List[Any]] = None

    # Selector-specific configuration
    config: dict[str, Any] = Field(default_factory=dict)
