"""Numeric inputs (number input, slider, range)."""

from typing import Literal, Optional, Tuple, Union

from pydantic import Field, BaseModel

from .base import Input


# ==============================================================================
# Config Models
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
# Input Classes
# ==============================================================================

class NumericInput(Input[NumericInputConfig]):
    """Numeric input with constraints."""

    __config_class__ = NumericInputConfig
    input_type: Literal["numeric_input"] = "numeric_input"

    # Config fields
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    step: Optional[Union[int, float]] = None
    default: Optional[Union[int, float]] = None


    # Display options
    prefix: Optional[str] = Field(None, description="Prefix text (e.g., '$')")
    suffix: Optional[str] = Field(None, description="Suffix text (e.g., '%')")


class Slider(Input[SliderConfig]):
    """Visual slider for single value."""

    __config_class__ = SliderConfig
    input_type: Literal["slider"] = "slider"

    # Config fields (min/max required for sliders)
    min_value: Union[int, float] = Field(..., description="Minimum value")
    max_value: Union[int, float] = Field(..., description="Maximum value")
    step: Optional[Union[int, float]] = None
    default: Optional[Union[int, float]] = None


    # Display options
    show_value: bool = Field(True, description="Show current value")
    show_ticks: bool = Field(False, description="Show tick marks")


class RangeSlider(Input[RangeSliderConfig]):
    """Visual slider for range (min/max)."""

    __config_class__ = RangeSliderConfig
    input_type: Literal["range_slider"] = "range_slider"

    # Config fields
    min_value: Union[int, float] = Field(..., description="Minimum value")
    max_value: Union[int, float] = Field(..., description="Maximum value")
    step: Optional[Union[int, float]] = None
    default: Optional[Tuple[Union[int, float], Union[int, float]]] = None


    # Display options
    show_values: bool = Field(True, description="Show current values")


class NumericRange(Input[NumericRangeConfig]):
    """Two numeric inputs for min/max range."""

    __config_class__ = NumericRangeConfig
    input_type: Literal["numeric_range"] = "numeric_range"

    # Config fields
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    step: Optional[Union[int, float]] = None
    default: Optional[Tuple[Union[int, float], Union[int, float]]] = None


    # Display options
    prefix: Optional[str] = Field(None, description="Prefix text")
    suffix: Optional[str] = Field(None, description="Suffix text")
