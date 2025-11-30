"""
Dashboard Layout Framework

Type-safe, hierarchical layout system using Pydantic.
"""

# Base classes (re-exported from core for convenience)
from viz.core.layout import Container
# Components (leaf nodes)
from .components import Widget
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
# Enums
from .enums import WidgetType

__all__ = [
    # Base classes
    "Container",

    # Enums
    "WidgetType",

    # Components
    "Widget",

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
