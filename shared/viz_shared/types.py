"""Common types and enums for Viz framework."""

from enum import Enum
from typing import Literal


class ExecutionStage(str, Enum):
    """Execution stages for components."""
    LOAD = "load"
    LOAD_TRANSFORM = "load_transform"
    LOAD_TRANSFORM_RENDER = "load_transform_render"


class SelectorType(str, Enum):
    """Types of selectors available."""
    DROPDOWN = "dropdown"
    MULTI_SELECT = "multi_select"
    DATE = "date"
    DATE_RANGE = "date_range"
    SLIDER = "slider"
    TEXT_INPUT = "text_input"
    CHECKBOX = "checkbox"
    NUMERIC_INPUT = "numeric_input"


class WidgetType(str, Enum):
    """Types of widgets available."""
    CHART = "chart"
    TABLE = "table"
    METRIC = "metric"
    TEXT = "text"
    IMAGE = "image"
    CUSTOM = "custom"


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


class RenderOutputType(str, Enum):
    """Types of render outputs."""
    PLOTLY = "plotly"
    VEGA_LITE = "vega_lite"
    ALTAIR = "altair"
    CUSTOM = "custom"


class LayoutType(str, Enum):
    """Types of layout components."""
    DASHBOARD = "dashboard"
    PAGE = "page"
    SECTION = "section"
    TABS = "tabs"
    TAB = "tab"
    ROW = "row"
    COLUMN = "column"
    WIDGET = "widget"
    SELECTOR = "selector"


# Type aliases for common patterns
ComponentAlias = str
DashboardName = str
PageId = str
SelectorName = str
ParameterName = str
