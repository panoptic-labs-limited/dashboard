"""Core components for the Viz client library."""

from .component import Component, DataSourceComponent
from .registry import register_component, auto_register_components
from .layout import LayoutNode

__all__ = [
    "Component",
    "DataSourceComponent",
    "register_component",
    "auto_register_components",
    "LayoutNode",
]
