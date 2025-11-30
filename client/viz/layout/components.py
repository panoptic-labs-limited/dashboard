"""
Leaf components (Widget).

These are terminal nodes in the layout tree that don't contain children.
"""

from __future__ import annotations

from typing import Literal, Any, Union, TYPE_CHECKING

from pydantic import Field, model_validator, field_serializer

from viz.core.layout import LeafNode
from .enums import WidgetType

if TYPE_CHECKING:
    pass


class Widget(LeafNode):
    """
    Leaf node representing a visualization or content widget.

    Examples: charts, tables, metrics, images
    """

    type: Literal["widget"] = "widget"
    widget_type: WidgetType
    title: str | None = None
    description: str | None = None

    # Component reference - either a class or string alias
    # Type[Component] for local components (will be auto-registered)
    # str for pre-registered components (referenced by alias)
    # Note: Using Union[type, str, None] to avoid forward reference issues with Type[Component]
    component: Union[type, str, None] = Field(default=None, repr=False)
    params: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode='after')
    def validate_component(self):
        """Ensure component is provided."""
        if self.component is None:
            raise ValueError("Widget must have a component")
        return self

    @field_serializer('component')
    def serialize_component(self, component: Union[type, str, None], _info):
        """Exclude component from serialization - it's handled separately by the serializer."""
        return None

    # Widget-specific configuration
    config: dict[str, Any] = Field(default_factory=dict)
