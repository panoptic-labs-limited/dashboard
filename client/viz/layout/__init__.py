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
# Legacy widget (deprecated)
from .components import LegacyWidget
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
