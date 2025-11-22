"""Numeric inputs (number input, slider, range)."""

from typing import Literal, Optional, Tuple, Union
from pydantic import Field, field_validator, model_validator

from .base import BaseInput


class NumericInput(BaseInput):
    """
    Numeric input selector with optional constraints.

    Examples:
        quantity = NumericInput(
            name="quantity",
            label="Quantity",
            default=1,
            min_value=1,
            max_value=100,
            step=1
        )

        price = NumericInput(
            name="price",
            label="Price",
            default=0.0,
            min_value=0.0,
            step=0.01,
            prefix="$"
        )

        threshold = NumericInput(
            name="threshold",
            label="Threshold",
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            help_text="Value between 0 and 1"
        )
    """

    input_type: Literal["numeric_input"] = "numeric_input"
    default: Optional[Union[int, float]] = None

    # Numeric constraints
    min_value: Optional[Union[int, float]] = Field(None, description="Minimum value")
    max_value: Optional[Union[int, float]] = Field(None, description="Maximum value")
    step: Optional[Union[int, float]] = Field(None, description="Step increment")

    # Display options
    prefix: Optional[str] = Field(None, description="Prefix text (e.g., '$', '#')")
    suffix: Optional[str] = Field(None, description="Suffix text (e.g., '%', 'kg')")

    @field_validator('default')
    @classmethod
    def validate_default_is_numeric(cls, v):
        """Ensure default is numeric (or None)."""
        if v is not None and not isinstance(v, (int, float)):
            raise ValueError("NumericInput default must be a number")
        return v

    @model_validator(mode='after')
    def validate_constraints(self):
        """Validate min/max constraints and default value."""
        if self.min_value is not None and self.max_value is not None:
            if self.min_value > self.max_value:
                raise ValueError("min_value must be less than or equal to max_value")

        if self.default is not None:
            if self.min_value is not None and self.default < self.min_value:
                raise ValueError(f"default ({self.default}) must be >= min_value ({self.min_value})")
            if self.max_value is not None and self.default > self.max_value:
                raise ValueError(f"default ({self.default}) must be <= max_value ({self.max_value})")

        return self


class Slider(BaseInput):
    """
    Visual slider selector for single numeric value.

    Examples:
        volume = Slider(
            name="volume",
            label="Volume",
            default=50,
            min_value=0,
            max_value=100,
            step=5
        )

        confidence = Slider(
            name="confidence",
            label="Confidence Threshold",
            default=0.5,
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            show_value=True
        )
    """

    input_type: Literal["slider"] = "slider"
    default: Optional[Union[int, float]] = None

    # Required for sliders
    min_value: Union[int, float] = Field(..., description="Minimum value")
    max_value: Union[int, float] = Field(..., description="Maximum value")
    step: Optional[Union[int, float]] = Field(None, description="Step increment")

    # Display options
    show_value: bool = Field(True, description="Show current value")
    show_ticks: bool = Field(False, description="Show tick marks")
    marks: Optional[dict[Union[int, float], str]] = Field(
        None,
        description="Custom marks at specific values"
    )

    @field_validator('default')
    @classmethod
    def validate_default_is_numeric(cls, v):
        """Ensure default is numeric (or None)."""
        if v is not None and not isinstance(v, (int, float)):
            raise ValueError("Slider default must be a number")
        return v

    @model_validator(mode='after')
    def validate_constraints(self):
        """Validate min/max constraints and default value."""
        if self.min_value > self.max_value:
            raise ValueError("min_value must be less than or equal to max_value")

        if self.default is not None:
            if self.default < self.min_value:
                raise ValueError(f"default ({self.default}) must be >= min_value ({self.min_value})")
            if self.default > self.max_value:
                raise ValueError(f"default ({self.default}) must be <= max_value ({self.max_value})")

        return self


class RangeSlider(BaseInput):
    """
    Visual slider for selecting a numeric range (min and max).

    Examples:
        price_range = RangeSlider(
            name="price_range",
            label="Price Range",
            default=(100, 500),
            min_value=0,
            max_value=1000,
            step=10,
            prefix="$"
        )

        date_range_years = RangeSlider(
            name="year_range",
            label="Year Range",
            default=(2020, 2024),
            min_value=2000,
            max_value=2024,
            step=1
        )
    """

    input_type: Literal["range_slider"] = "range_slider"
    default: Optional[Tuple[Union[int, float], Union[int, float]]] = None

    # Required for range sliders
    min_value: Union[int, float] = Field(..., description="Minimum value")
    max_value: Union[int, float] = Field(..., description="Maximum value")
    step: Optional[Union[int, float]] = Field(None, description="Step increment")

    # Display options
    show_values: bool = Field(True, description="Show current range values")
    prefix: Optional[str] = Field(None, description="Prefix for values")
    suffix: Optional[str] = Field(None, description="Suffix for values")

    @field_validator('default')
    @classmethod
    def validate_default_is_tuple(cls, v):
        """Ensure default is a tuple of two numbers (or None)."""
        if v is not None:
            if not isinstance(v, tuple) or len(v) != 2:
                raise ValueError("RangeSlider default must be a tuple of (min, max)")
            if not all(isinstance(x, (int, float)) for x in v):
                raise ValueError("RangeSlider default values must be numbers")
        return v

    @model_validator(mode='after')
    def validate_constraints(self):
        """Validate min/max constraints and default range."""
        if self.min_value > self.max_value:
            raise ValueError("min_value must be less than or equal to max_value")

        if self.default is not None:
            range_min, range_max = self.default
            if range_min > range_max:
                raise ValueError(f"default range min ({range_min}) must be <= max ({range_max})")
            if range_min < self.min_value:
                raise ValueError(f"default range min ({range_min}) must be >= min_value ({self.min_value})")
            if range_max > self.max_value:
                raise ValueError(f"default range max ({range_max}) must be <= max_value ({self.max_value})")

        return self


class NumericRange(BaseInput):
    """
    Two numeric inputs for min/max range selection.

    Examples:
        age_range = NumericRange(
            name="age_range",
            label="Age Range",
            default=(18, 65),
            min_value=0,
            max_value=120
        )

        salary_range = NumericRange(
            name="salary",
            label="Salary Range",
            default=(50000, 150000),
            min_value=0,
            step=1000,
            prefix="$"
        )
    """

    input_type: Literal["numeric_range"] = "numeric_range"
    default: Optional[Tuple[Union[int, float], Union[int, float]]] = None

    # Numeric constraints
    min_value: Optional[Union[int, float]] = Field(None, description="Minimum value")
    max_value: Optional[Union[int, float]] = Field(None, description="Maximum value")
    step: Optional[Union[int, float]] = Field(None, description="Step increment")

    # Display options
    prefix: Optional[str] = Field(None, description="Prefix text")
    suffix: Optional[str] = Field(None, description="Suffix text")

    @field_validator('default')
    @classmethod
    def validate_default_is_tuple(cls, v):
        """Ensure default is a tuple of two numbers (or None)."""
        if v is not None:
            if not isinstance(v, tuple) or len(v) != 2:
                raise ValueError("NumericRange default must be a tuple of (min, max)")
            if not all(isinstance(x, (int, float)) for x in v):
                raise ValueError("NumericRange default values must be numbers")
        return v

    @model_validator(mode='after')
    def validate_constraints(self):
        """Validate constraints and default range."""
        if self.min_value is not None and self.max_value is not None:
            if self.min_value > self.max_value:
                raise ValueError("min_value must be less than or equal to max_value")

        if self.default is not None:
            range_min, range_max = self.default
            if range_min > range_max:
                raise ValueError(f"default range min ({range_min}) must be <= max ({range_max})")
            if self.min_value is not None and range_min < self.min_value:
                raise ValueError(f"default range min ({range_min}) must be >= min_value ({self.min_value})")
            if self.max_value is not None and range_max > self.max_value:
                raise ValueError(f"default range max ({range_max}) must be <= max_value ({self.max_value})")

        return self
