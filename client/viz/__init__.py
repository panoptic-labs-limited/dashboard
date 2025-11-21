"""Viz - Distributed dashboarding framework with reactive components."""

__version__ = "0.1.0"

# Core components
from .core import Component, DataSourceComponent, register_component, auto_register_components
from .api import RegistryClient

# Layout components
from .layout import (
    Dashboard, Page, Section, Row, Column, Widget, Selector,
    Tabs, Tab, LayoutBuilder as L, ColumnWidth, WidgetType, SelectorType
)

# Selectors
from .selectors import DateSelector, DropdownSelector

__all__ = [
    # Core
    "Component",
    "DataSourceComponent",
    "register_component",
    "auto_register_components",
    "RegistryClient",
    # Layout
    "Dashboard",
    "Page",
    "Section",
    "Row",
    "Column",
    "Widget",
    "Selector",
    "Tabs",
    "Tab",
    "L",
    "ColumnWidth",
    "WidgetType",
    "SelectorType",
    # Selectors
    "DateSelector",
    "DropdownSelector",
]
