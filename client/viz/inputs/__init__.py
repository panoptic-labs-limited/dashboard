"""Comprehensive input components for dashboards."""

# Base classes
from .base import BaseInput
# Choice-based inputs and configs
from .choice import (
    # Config models
    Option,
    SelectConfig,
    MultiSelectConfig,
    RadioGroupConfig,
    CheckboxConfig,
    CheckboxGroupConfig,
    ToggleConfig,
    # Input classes
    Select,
    MultiSelect,
    RadioGroup,
    Checkbox,
    CheckboxGroup,
    Toggle,
)
# Date/time inputs and configs
from .date_time import (
    # Config models
    DateConfig,
    DateRangeConfig,
    TimeConfig,
    DateTimeConfig,
    RelativeDateConfig,
    # Input classes
    DateInput,
    DateRangeInput,
    TimeInput,
    DateTimeInput,
    RelativeDateInput,
)
# Numeric inputs and configs
from .numeric import (
    # Config models
    NumericInputConfig,
    SliderConfig,
    RangeSliderConfig,
    NumericRangeConfig,
    # Input classes
    NumericInput,
    Slider,
    RangeSlider,
    NumericRange,
)
# Text inputs and configs
from .text import (
    # Config models
    TextInputConfig,
    TextAreaConfig,
    SearchInputConfig,
    # Input classes
    TextInput,
    TextArea,
    SearchInput,
)

__all__ = [
    # Base classes
    "Option",
    "BaseInput",

    # Config models
    "SelectConfig",
    "MultiSelectConfig",
    "RadioGroupConfig",
    "CheckboxConfig",
    "CheckboxGroupConfig",
    "ToggleConfig",
    "TextInputConfig",
    "TextAreaConfig",
    "SearchInputConfig",
    "NumericInputConfig",
    "SliderConfig",
    "RangeSliderConfig",
    "NumericRangeConfig",
    "DateConfig",
    "DateRangeConfig",
    "TimeConfig",
    "DateTimeConfig",
    "RelativeDateConfig",

    # Choice inputs
    "Select",
    "MultiSelect",
    "RadioGroup",
    "Checkbox",
    "CheckboxGroup",
    "Toggle",

    # Text inputs
    "TextInput",
    "TextArea",
    "SearchInput",

    # Numeric inputs
    "NumericInput",
    "Slider",
    "RangeSlider",
    "NumericRange",

    # Date/time inputs
    "DateInput",
    "DateRangeInput",
    "TimeInput",
    "DateTimeInput",
    "RelativeDateInput",
]
