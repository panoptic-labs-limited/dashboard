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

class NumericInput(NumericInputConfig, Input[NumericInputConfig]):
    """Numeric input with constraints."""

    __config_class__ = NumericInputConfig
    input_type: Literal["numeric_input"] = "numeric_input"

    # Display options (config fields inherited from NumericInputConfig)
    prefix: str | None = Field(None, description="Prefix text (e.g., '$')")
    suffix: str | None = Field(None, description="Suffix text (e.g., '%')")


class Slider(SliderConfig, Input[SliderConfig]):
    """Visual slider for single value."""

    __config_class__ = SliderConfig
    input_type: Literal["slider"] = "slider"

    # Display options (config fields inherited from SliderConfig)
    show_value: bool = Field(True, description="Show current value")
    show_ticks: bool = Field(False, description="Show tick marks")


class RangeSlider(RangeSliderConfig, Input[RangeSliderConfig]):
    """Visual slider for range (min/max)."""

    __config_class__ = RangeSliderConfig
    input_type: Literal["range_slider"] = "range_slider"

    # Display options (config fields inherited from RangeSliderConfig)
    show_values: bool = Field(True, description="Show current values")


class NumericRange(NumericRangeConfig, Input[NumericRangeConfig]):
    """Two numeric inputs for min/max range."""

    __config_class__ = NumericRangeConfig
    input_type: Literal["numeric_range"] = "numeric_range"

    # Display options (config fields inherited from NumericRangeConfig)
    prefix: str | None = Field(None, description="Prefix text")
    suffix: str | None = Field(None, description="Suffix text")
