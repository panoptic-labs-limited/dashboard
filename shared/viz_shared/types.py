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
    DATE = "date"
    DATE_RANGE = "date_range"
    DROPDOWN = "dropdown"
    MULTI_SELECT = "multi_select"
    TEXT_INPUT = "text_input"
    NUMERIC_INPUT = "numeric_input"
    SLIDER = "slider"
    RANGE_SLIDER = "range_slider"


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
