"""
Enums for layout system.

Provides type-safe enum values for widgets, selectors, and column widths.
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


class SelectorType(str, Enum):
    """Supported selector types."""
    DROPDOWN = "dropdown"
    MULTI_SELECT = "multi_select"
    DATE = "date"
    DATE_RANGE = "date_range"
    SLIDER = "slider"
    TEXT_INPUT = "text_input"
    CHECKBOX = "checkbox"
    NUMERIC_INPUT = "numeric_input"


class ColumnWidth(str, Enum):
    """Standard column widths."""
    FULL = "1/1"
    HALF = "1/2"
    THIRD = "1/3"
    TWO_THIRDS = "2/3"
    QUARTER = "1/4"
    THREE_QUARTERS = "3/4"
    SIXTH = "1/6"
    FIVE_SIXTHS = "5/6"
