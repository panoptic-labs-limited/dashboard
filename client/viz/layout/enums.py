"""
Enums for layout system.

DEPRECATED: This module is deprecated. Widget types are now implicit in the
widget class (LineChartWidget, TableWidget, etc.). Import widgets from viz.widgets.
"""

import warnings
from enum import Enum


class WidgetType(str, Enum):
    """
    DEPRECATED: Widget types are now implicit in widget classes.

    Use typed widget classes instead:
    - LineChartWidget, BarChartWidget, AreaChartWidget for charts
    - TableWidget for data tables
    - MetricWidget for KPIs
    - PlotlyWidget for custom server-rendered visualizations
    """
    CHART = "chart"
    TABLE = "table"
    METRIC = "metric"
    TEXT = "text"
    IMAGE = "image"
    CUSTOM = "custom"

    def __init__(self, *args, **kwargs):  # noqa: ARG002
        warnings.warn(
            "WidgetType is deprecated. Use typed widget classes instead: "
            "LineChartWidget, TableWidget, MetricWidget, PlotlyWidget",
            DeprecationWarning,
            stacklevel=3
        )
