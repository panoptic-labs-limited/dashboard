"""
Enums for layout system.

Provides type-safe enum values for widgets.
"""

from enum import Enum


class WidgetType(str, Enum):
    """Supported widget types."""
    CHART = "chart"
    TABLE = "table"
    METRIC = "metric"
    TEXT = "text"
    IMAGE = "image"
    CUSTOM = "custom"
