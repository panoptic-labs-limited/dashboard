"""Config models for inputs.

Each input type has a corresponding config model that defines
the data structure for that input's configuration.
"""

from typing import Any, List, Optional, Tuple
from pydantic import BaseModel

from .base import Option


# ==============================================================================
# Choice Input Configs
# ==============================================================================

class SelectConfig(BaseModel):
    """Configuration for Select input."""
    options: List[Option]
    default: Optional[Any] = None


class MultiSelectConfig(BaseModel):
    """Configuration for MultiSelect input."""
    options: List[Option]
    default: Optional[List[Any]] = None
    max_selections: Optional[int] = None


class RadioGroupConfig(BaseModel):
    """Configuration for RadioGroup input."""
    options: List[Option]
    default: Optional[Any] = None


class CheckboxConfig(BaseModel):
    """Configuration for Checkbox input."""
    default: Optional[bool] = None


class CheckboxGroupConfig(BaseModel):
    """Configuration for CheckboxGroup input."""
    options: List[Option]
    default: Optional[List[Any]] = None


class ToggleConfig(BaseModel):
    """Configuration for Toggle input."""
    default: Optional[bool] = None
    on_label: Optional[str] = None
    off_label: Optional[str] = None


# ==============================================================================
# Text Input Configs
# ==============================================================================

class TextInputConfig(BaseModel):
    """Configuration for TextInput."""
    default: Optional[str] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    pattern: Optional[str] = None


class TextAreaConfig(BaseModel):
    """Configuration for TextArea."""
    default: Optional[str] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    rows: int = 3


class SearchInputConfig(BaseModel):
    """Configuration for SearchInput."""
    default: Optional[str] = None
    min_length: Optional[int] = None


# ==============================================================================
# Numeric Input Configs
# ==============================================================================

class NumericInputConfig(BaseModel):
    """Configuration for NumericInput."""
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    step: Optional[float] = None
    default: Optional[float] = None


class SliderConfig(BaseModel):
    """Configuration for Slider."""
    min_value: float
    max_value: float
    step: Optional[float] = None
    default: Optional[float] = None


class RangeSliderConfig(BaseModel):
    """Configuration for RangeSlider."""
    min_value: float
    max_value: float
    step: Optional[float] = None
    default: Optional[Tuple[float, float]] = None


class NumericRangeConfig(BaseModel):
    """Configuration for NumericRange."""
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    step: Optional[float] = None
    default: Optional[Tuple[float, float]] = None


# ==============================================================================
# Date/Time Input Configs
# ==============================================================================

class DateConfig(BaseModel):
    """Configuration for DateInput."""
    min_date: Optional[str] = None
    max_date: Optional[str] = None
    default: Optional[str] = None


class DateRangeConfig(BaseModel):
    """Configuration for DateRangeInput."""
    min_date: Optional[str] = None
    max_date: Optional[str] = None
    default: Optional[Tuple[str, str]] = None


class TimeConfig(BaseModel):
    """Configuration for TimeInput."""
    min_time: Optional[str] = None
    max_time: Optional[str] = None
    step_minutes: int = 1
    default: Optional[str] = None


class DateTimeConfig(BaseModel):
    """Configuration for DateTimeInput."""
    min_datetime: Optional[str] = None
    max_datetime: Optional[str] = None
    default: Optional[str] = None


class RelativeDateConfig(BaseModel):
    """Configuration for RelativeDateInput."""
    options: List[dict[str, str]]
    default: Optional[str] = None
    allow_custom: bool = False
