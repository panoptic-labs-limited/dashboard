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


class InputType(str, Enum):
    """Supported input types."""
    # Choice-based inputs
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    RADIO = "radio"
    CHECKBOX = "checkbox"
    CHECKBOX_GROUP = "checkbox_group"
    TOGGLE = "toggle"

    # Text inputs
    TEXT_INPUT = "text_input"
    TEXTAREA = "textarea"
    SEARCH_INPUT = "search_input"

    # Numeric inputs
    NUMERIC_INPUT = "numeric_input"
    SLIDER = "slider"
    RANGE_SLIDER = "range_slider"
    NUMERIC_RANGE = "numeric_range"

    # Date/time inputs
    DATE = "date"
    DATE_RANGE = "date_range"
    TIME = "time"
    DATETIME = "datetime"
    RELATIVE_DATE = "relative_date"
