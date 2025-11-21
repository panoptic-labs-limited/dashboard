"""
Dashboard Layout Framework

Type-safe, hierarchical layout system using Pydantic.
"""

# Core classes
from .base import (
    # Base classes
    LayoutNode,
    Container,

    # Enums
    WidgetType,
    SelectorType,
    ColumnWidth,

    # Layout components
    Dashboard,
    Page,
    Section,
    Tabs,
    Tab,
    Row,
    Column,
    Widget,
    Selector,

    # Type unions
    LayoutComponent,
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
    "SelectorType",
    "ColumnWidth",

    # Layout components
    "Dashboard",
    "Page",
    "Section",
    "Tabs",
    "Tab",
    "Row",
    "Column",
    "Widget",
    "Selector",

    # Type unions
    "LayoutComponent",

    # Builder
    "LayoutBuilder",
    "L",
]
