"""Comprehensive input components for dashboards."""

# Base classes
from .base import Option, BaseInput

# Sources
from .sources import FunctionSource

# Config models (for type hints and schemas)
from .config import (
    SelectConfig,
    MultiSelectConfig,
    RadioGroupConfig,
    CheckboxConfig,
    CheckboxGroupConfig,
    ToggleConfig,
    TextInputConfig,
    TextAreaConfig,
    SearchInputConfig,
    NumericInputConfig,
    SliderConfig,
    RangeSliderConfig,
    NumericRangeConfig,
    DateConfig,
    DateRangeConfig,
    TimeConfig,
    DateTimeConfig,
    RelativeDateConfig,
)

# Choice-based inputs
from .choice import (
    Select,
    MultiSelect,
    RadioGroup,
    Checkbox,
    CheckboxGroup,
    Toggle,
)

# Text inputs
from .text import (
    TextInput,
    TextArea,
    SearchInput,
)

# Numeric inputs
from .numeric import (
    NumericInput,
    Slider,
    RangeSlider,
    NumericRange,
)

# Date/time inputs
from .date_time import (
    DateInput,
    DateRangeInput,
    TimeInput,
    DateTimeInput,
    RelativeDateInput,
)

__all__ = [
    # Base classes
    "Option",
    "BaseInput",

    # Sources
    "FunctionSource",

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
