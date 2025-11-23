"""Viz - Distributed dashboarding framework with reactive components."""

__version__ = "0.1.0"

from .api import RegistryClient
# Builder utilities
from .builder import LayoutBuilder, L
# Core components
from .core import Component, DataSourceComponent, register_component, auto_register_components
# Inputs
from .inputs import (
    # Base
    Option,
    Input,
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
# Layout components
from .layout import (
    Dashboard, Page, Section, Row, Column, Widget,
    Tabs, Tab, WidgetType
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
    "Tabs",
    "Tab",
    # Builder
    "LayoutBuilder",
    "L",
    # Enums
    "WidgetType",
    # Inputs - Base
    "Option",
    "Input",
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
