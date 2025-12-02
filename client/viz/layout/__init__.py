"""
Dashboard Layout Framework

Type-safe, hierarchical layout system using Pydantic.
"""

# Base classes (re-exported from core for convenience)
from viz.core.layout import Container
# Widgets (from viz.widgets)
from viz.widgets import (
    Widget,
    LineChartWidget,
    BarChartWidget,
    AreaChartWidget,
    TableWidget,
    MetricWidget,
    PlotlyWidget,
)
# Containers
from .containers import (
    Row,
    Column,
    Tab,
    Tabs,
    Section,
)
# Page
from .page import Page

__all__ = [
    # Base classes
    "Container",

    # Widgets
    "Widget",
    "LineChartWidget",
    "BarChartWidget",
    "AreaChartWidget",
    "TableWidget",
    "MetricWidget",
    "PlotlyWidget",

    # Containers
    "Row",
    "Column",
    "Tab",
    "Tabs",
    "Section",

    # Page
    "Page",
]
