"""
Dashboard Layout Framework

Type-safe, hierarchical layout system using Pydantic.
"""

# Base classes
from .base import (
    LayoutNode,
    Container,
)

# Enums
from .enums import (
    WidgetType,
    InputType,
    ColumnWidth,
)

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

# Builder utilities
from .builder import (
    LayoutBuilder,
    L,  # Convenience alias
)

__all__ = [
    # Base classes
    "LayoutNode",
    "Container",

    # Enums
    "WidgetType",
    "InputType",
    "ColumnWidth",

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

    # Builder
    "LayoutBuilder",
    "L",
]
