"""Date and time inputs."""

from typing import Literal, Optional, Tuple, List

from pydantic import Field, BaseModel

from .base import BaseInput


# ==============================================================================
# Config Models
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


# ==============================================================================
# Input Classes
# ==============================================================================

class DateInput(BaseInput[DateConfig]):
    """Date picker input."""

    __config_class__ = DateConfig
    input_type: Literal["date"] = "date"

    # Config fields
    min_date: Optional[str] = None
    max_date: Optional[str] = None
    default: Optional[str] = None


    # Display options
    format: str = Field("YYYY-MM-DD", description="Display format")
    first_day_of_week: Literal[0, 1] = Field(0, description="0=Sunday, 1=Monday")


class DateRangeInput(BaseInput[DateRangeConfig]):
    """Date range picker."""

    __config_class__ = DateRangeConfig
    input_type: Literal["date_range"] = "date_range"

    # Config fields
    min_date: Optional[str] = None
    max_date: Optional[str] = None
    default: Optional[Tuple[str, str]] = None


    # Display options
    format: str = Field("YYYY-MM-DD", description="Display format")
    max_days: Optional[int] = Field(None, description="Maximum days in range")


class TimeInput(BaseInput[TimeConfig]):
    """Time picker input."""

    __config_class__ = TimeConfig
    input_type: Literal["time"] = "time"

    # Config fields
    min_time: Optional[str] = None
    max_time: Optional[str] = None
    step_minutes: int = 1
    default: Optional[str] = None


    # Display options
    format_24h: bool = Field(True, description="Use 24-hour format")


class DateTimeInput(BaseInput[DateTimeConfig]):
    """Combined date and time picker."""

    __config_class__ = DateTimeConfig
    input_type: Literal["datetime"] = "datetime"

    # Config fields
    min_datetime: Optional[str] = None
    max_datetime: Optional[str] = None
    default: Optional[str] = None


    # Display options
    format: str = Field("YYYY-MM-DD HH:mm", description="Display format")
    format_24h: bool = Field(True, description="Use 24-hour format")


class RelativeDateInput(BaseInput[RelativeDateConfig]):
    """Relative date range selector (last 7 days, etc.)."""

    __config_class__ = RelativeDateConfig
    input_type: Literal["relative_date"] = "relative_date"

    # Config fields
    options: list[dict[str, str]] = Field(..., description="Relative date options")
    default: Optional[str] = None
    allow_custom: bool = False

