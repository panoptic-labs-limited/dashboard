"""Viz - Distributed dashboarding framework with reactive components."""

__version__ = "0.1.0"

# Core components
from .core import Component, DataSourceComponent, register_component, auto_register_components
from .api import RegistryClient

# Layout components (to be added)
# from .layout import Dashboard, Page, Section, Row, Column, Widget

# Selectors (to be added)
# from .selectors import DateSelector, DropdownSelector, TextInput, NumericInput

__all__ = [
    "Component",
    "DataSourceComponent",
    "register_component",
    "auto_register_components",
    "RegistryClient",
]
