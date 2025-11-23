"""Numeric inputs (number input, slider, range)."""

from typing import Literal

from pydantic import Field, BaseModel

from .base import Input


# ==============================================================================
# Config Models
# ==============================================================================

class NumericInputConfig(BaseModel):
    """Configuration for NumericInput."""
    min_value: float | None = None
    max_value: float | None = None
    step: float | None = None
    default: float | None = None


class SliderConfig(BaseModel):
    """Configuration for Slider."""
    min_value: float
    max_value: float
    step: float | None = None
    default: float | None = None


class RangeSliderConfig(BaseModel):
    """Configuration for RangeSlider."""
    min_value: float
    max_value: float
    step: float | None = None
    default: tuple[float, float | None] = None


class NumericRangeConfig(BaseModel):
    """Configuration for NumericRange."""
    min_value: float | None = None
    max_value: float | None = None
    step: float | None = None
    default: tuple[float, float | None] = None


# ==============================================================================
# Input Classes
# ==============================================================================

class NumericInput(Input[NumericInputConfig]):
    """Numeric input with constraints."""

    __config_class__ = NumericInputConfig
    input_type: Literal["numeric_input"] = "numeric_input"

    # Config fields
    min_value: int | float | None = None
    max_value: int | float | None = None
    step: int | float | None = None
    default: int | float | None = None


    # Display options
    prefix: str | None = Field(None, description="Prefix text (e.g., '$')")
    suffix: str | None = Field(None, description="Suffix text (e.g., '%')")


class Slider(Input[SliderConfig]):
    """Visual slider for single value."""

    __config_class__ = SliderConfig
    input_type: Literal["slider"] = "slider"

    # Config fields (min/max required for sliders)
    min_value: int | float = Field(..., description="Minimum value")
    max_value: int | float = Field(..., description="Maximum value")
    step: int | float | None = None
    default: int | float | None = None


    # Display options
    show_value: bool = Field(True, description="Show current value")
    show_ticks: bool = Field(False, description="Show tick marks")


class RangeSlider(Input[RangeSliderConfig]):
    """Visual slider for range (min/max)."""

    __config_class__ = RangeSliderConfig
    input_type: Literal["range_slider"] = "range_slider"

    # Config fields
    min_value: int | float = Field(..., description="Minimum value")
    max_value: int | float = Field(..., description="Maximum value")
    step: int | float | None = None
    default: tuple[int | float, int | float] | None = None


    # Display options
    show_values: bool = Field(True, description="Show current values")


class NumericRange(Input[NumericRangeConfig]):
    """Two numeric inputs for min/max range."""

    __config_class__ = NumericRangeConfig
    input_type: Literal["numeric_range"] = "numeric_range"

    # Config fields
    min_value: int | float | None = None
    max_value: int | float | None = None
    step: int | float | None = None
    default: tuple[int | float, int | float] | None = None


    # Display options
    prefix: str | None = Field(None, description="Prefix text")
    suffix: str | None = Field(None, description="Suffix text")
