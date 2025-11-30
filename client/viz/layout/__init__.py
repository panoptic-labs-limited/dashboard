"""
Dashboard Layout Framework

Type-safe, hierarchical layout system using Pydantic.
"""

# Base classes (re-exported from core for convenience)
from viz.core.layout import Container
# Widgets (re-exported from viz.widgets)
from .components import (
    Widget,
    LineChartWidget,
    BarChartWidget,
    AreaChartWidget,
    TableWidget,
    MetricWidget,
    PlotlyWidget,
    LegacyWidget,
)
# Containers
from .containers import (
    Row,
    Column,
    Tab,
    Tabs,
    Section,
)
# Dashboard and Page
from .dashboard import (
    Page,
    Dashboard,
)
# Enums (WidgetType is deprecated but kept for backward compatibility)
from .enums import WidgetType

__all__ = [
    # Base classes
    "Container",

    # Enums (deprecated)
    "WidgetType",

    # Widgets
    "Widget",
    "LineChartWidget",
    "BarChartWidget",
    "AreaChartWidget",
    "TableWidget",
    "MetricWidget",
    "PlotlyWidget",
    "LegacyWidget",

    # Containers
    "Row",
    "Column",
    "Tab",
    "Tabs",
    "Section",

    # Dashboard
    "Page",
    "Dashboard",
]
