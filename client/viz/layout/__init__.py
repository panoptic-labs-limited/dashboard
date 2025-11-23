"""
Dashboard Layout Framework

Type-safe, hierarchical layout system using Pydantic.
"""

# Base classes
from viz.core.layout import LayoutNode
from .base import Container

# Enums
from .enums import (
    WidgetType,
    InputType,
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

# Builder utilities (moved to top-level viz.builder)
from viz.builder import (
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
