"""Viz - Distributed dashboarding framework with reactive components."""

__version__ = "0.1.0"

# Core components
from .core import Component, DataSourceComponent, register_component, auto_register_components
from .api import RegistryClient

# Layout components
from .layout import (
    Dashboard, Page, Section, Row, Column, Widget, Selector,
    Tabs, Tab, LayoutBuilder as L, ColumnWidth, WidgetType, InputType
)

# Inputs
from .inputs import (
    # Base
    Option,
    BaseInput,
    # Sources
    FunctionSource,
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

__all__ = [
    # Core
    "Component",
    "DataSourceComponent",
    "register_component",
    "auto_register_components",
    "RegistryClient",
    # Layout
    "Dashboard",
    "Page",
    "Section",
    "Row",
    "Column",
    "Widget",
    "Selector",
    "Tabs",
    "Tab",
    "L",
    "ColumnWidth",
    "WidgetType",
    "InputType",
    # Inputs - Base
    "Option",
    "BaseInput",
    # Inputs - Sources
    "FunctionSource",
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
