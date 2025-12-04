"""Common types and enums for Viz framework."""

from enum import Enum
from typing import Literal


class ExecutionStage(str, Enum):
    """Execution stages for components."""
    LOAD = "load"
    LOAD_TRANSFORM = "load_transform"
    LOAD_TRANSFORM_RENDER = "load_transform_render"


class InputType(str, Enum):
    """Types of inputs available."""
    # Text inputs
    TEXT_INPUT = "text_input"
    TEXTAREA = "textarea"
    SEARCH_INPUT = "search_input"

    # Numeric inputs
    NUMERIC_INPUT = "numeric_input"
    SLIDER = "slider"
    RANGE_SLIDER = "range_slider"
    NUMERIC_RANGE = "numeric_range"

    # Choice inputs
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    RADIO = "radio"
    CHECKBOX = "checkbox"
    CHECKBOX_GROUP = "checkbox_group"
    TOGGLE = "toggle"

    # DateTime inputs
    DATE = "date"
    DATE_RANGE = "date_range"
    TIME = "time"
    DATETIME = "datetime"
    RELATIVE_DATE = "relative_date"


class WidgetType(str, Enum):
    """Types of widgets available."""
    CHART = "chart"
    TABLE = "table"
    METRIC = "metric"
    TEXT = "text"
    IMAGE = "image"
    CUSTOM = "custom"


# Column width is now represented as weight (integer), not enum


class RenderOutputType(str, Enum):
    """Types of render outputs."""
    PLOTLY = "plotly"
    VEGA_LITE = "vega_lite"
    ALTAIR = "altair"
    CUSTOM = "custom"


class LayoutType(str, Enum):
    """Types of containers components."""
    DASHBOARD = "dashboard"
    PAGE = "page"
    SECTION = "section"
    TABS = "tabs"
    TAB = "tab"
    ROW = "row"
    COLUMN = "column"
    WIDGET = "widget"
    INPUT = "input"


# Type aliases for common patterns
ComponentAlias = str
DashboardId = str
PageId = str
InputId = str
ParameterName = str
