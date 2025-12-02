"""Viz - Distributed dashboarding framework with reactive components."""

__version__ = "0.1.0"

# API utilities (serializer/extractor)
from .api import serialize_dashboard, serialize_component, serialize_input, ComponentExtractor
# Builder utilities
from .builder import LayoutBuilder, L
# Core components and data sources
from .core import (
    Component,
    RenderableComponent,
    DataSourceComponent,
    DataSource,
    TimeseriesSource,
    ComponentSource,
    FunctionSource,
)
# Inputs
from .inputs import (
    # Base
    Option,
    Input,
    # Config models
    SelectConfig,
    DateConfig,
    NumericInputConfig,
    # Choice inputs
    Select,
    MultiSelect,
    RadioGroup,
    Checkbox,
    CheckboxGroup,
    Toggle,
    # Text inputs
    TextInput,
    TextArea,
    SearchInput,
    # Numeric inputs
    NumericInput,
    Slider,
    RangeSlider,
    NumericRange,
    # Date/time inputs
    DateInput,
    DateRangeInput,
    TimeInput,
    DateTimeInput,
    RelativeDateInput,
)
# Layout components
from .layout import (
    Dashboard, Page, Section, Row, Column,
    Tabs, Tab,
    # Widget base class
    Widget,
)
# Widget types (new)
from .widgets import (
    LineChartWidget,
    BarChartWidget,
    AreaChartWidget,
    TableWidget,
    MetricWidget,
    PlotlyWidget,
)

__all__ = [
    # Core - Components
    "Component",
    "RenderableComponent",
    "DataSourceComponent",
    # Core - Data Sources
    "DataSource",
    "TimeseriesSource",
    "ComponentSource",
    "FunctionSource",
    # API utilities
    "serialize_dashboard",
    "serialize_component",
    "serialize_input",
    "ComponentExtractor",
    # Layout
    "Dashboard",
    "Page",
    "Section",
    "Row",
    "Column",
    "Tabs",
    "Tab",
    # Widgets (new typed widgets)
    "Widget",
    "LineChartWidget",
    "BarChartWidget",
    "AreaChartWidget",
    "TableWidget",
    "MetricWidget",
    "PlotlyWidget",
    # Builder
    "LayoutBuilder",
    "L",
    # Inputs - Base
    "Option",
    "Input",
    # Inputs - Config (commonly used)
    "SelectConfig",
    "DateConfig",
    "NumericInputConfig",
    # Inputs - Choice
    "Select",
    "MultiSelect",
    "RadioGroup",
    "Checkbox",
    "CheckboxGroup",
    "Toggle",
    # Inputs - Text
    "TextInput",
    "TextArea",
    "SearchInput",
    # Inputs - Numeric
    "NumericInput",
    "Slider",
    "RangeSlider",
    "NumericRange",
    # Inputs - Date/Time
    "DateInput",
    "DateRangeInput",
    "TimeInput",
    "DateTimeInput",
    "RelativeDateInput",
]
