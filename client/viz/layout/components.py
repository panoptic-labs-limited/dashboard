"""
Leaf components (Widgets).

This module re-exports widget classes from viz.widgets for backward compatibility.
New code should import directly from viz.widgets.

Widget Types:
- Frontend-native: LineChartWidget, BarChartWidget, AreaChartWidget, TableWidget, MetricWidget
- Server-rendered: PlotlyWidget

Legacy Widget class is deprecated - use specific widget types instead.
"""

from __future__ import annotations

import warnings
from typing import Literal, Any, Union

from pydantic import Field, model_validator, field_serializer

from viz.core.layout import LeafNode
from .enums import WidgetType

# Re-export widget classes from viz.widgets for backward compatibility
from viz.widgets import (
    Widget,
    LineChartWidget,
    BarChartWidget,
    AreaChartWidget,
    TableWidget,
    MetricWidget,
    PlotlyWidget,
)


class LegacyWidget(LeafNode):
    """
    Legacy widget class - DEPRECATED.

    Use specific widget types instead:
    - LineChartWidget, BarChartWidget, AreaChartWidget for charts
    - TableWidget for data tables
    - MetricWidget for KPIs
    - PlotlyWidget for custom server-rendered visualizations

    This class is kept for backward compatibility only.
    """

    type: Literal["widget"] = "widget"
    widget_type: WidgetType
    title: str | None = None
    description: str | None = None

    # Component reference - either a class or string name
    component: Union[type, str, None] = Field(default=None, repr=False)
    params: dict[str, Any] = Field(default_factory=dict)

    # Widget-specific configuration
    config: dict[str, Any] = Field(default_factory=dict)

    def __init__(self, **data):
        warnings.warn(
            "LegacyWidget is deprecated. Use specific widget types: "
            "LineChartWidget, BarChartWidget, TableWidget, MetricWidget, or PlotlyWidget",
            DeprecationWarning,
            stacklevel=2
        )
        super().__init__(**data)

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
