"""
Dashboard Layout Framework

Type-safe, hierarchical layout system using Pydantic.
"""

# Base classes
from .base import Container
# Components (leaf nodes)
from .components import (
    Widget,
    Selector,
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
# Enums
from .enums import (
    WidgetType,
    InputType,
)

__all__ = [
    # Base classes
    "Container",

    # Enums
    "WidgetType",
    "InputType",

    # Components
    "Widget",
    "Selector",

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
