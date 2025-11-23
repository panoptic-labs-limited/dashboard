"""Core components for the Viz client library."""

from .component import Component, DataSourceComponent
from .layout import LayoutNode
from .registry import register_component, auto_register_components

__all__ = [
    "Component",
    "DataSourceComponent",
    "register_component",
    "auto_register_components",
    "LayoutNode",
]
