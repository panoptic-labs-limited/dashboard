"""Date and time inputs."""

from typing import Literal

from pydantic import Field, BaseModel

from .base import BaseInput


# ==============================================================================
# Config Models
# ==============================================================================

class DateConfig(BaseModel):
    """Configuration for DateInput."""
    min_date: str | None = None
    max_date: str | None = None
    default: str | None = None


class DateRangeConfig(BaseModel):
    """Configuration for DateRangeInput."""
    min_date: str | None = None
    max_date: str | None = None
    default: tuple[str, str | None] = None


class TimeConfig(BaseModel):
    """Configuration for TimeInput."""
    min_time: str | None = None
    max_time: str | None = None
    step_minutes: int = 1
    default: str | None = None


class DateTimeConfig(BaseModel):
    """Configuration for DateTimeInput."""
    min_datetime: str | None = None
    max_datetime: str | None = None
    default: str | None = None


class RelativeDateConfig(BaseModel):
    """Configuration for RelativeDateInput."""
    options: list[dict[str, str]]
    default: str | None = None
    allow_custom: bool = False


# ==============================================================================
# Input Classes
# ==============================================================================

class DateInput(DateConfig, BaseInput[DateConfig]):
    """Date picker input."""

    type: Literal["date"] = "date"

    # Display options (config fields inherited from DateConfig)
    format: str = Field("YYYY-MM-DD", description="Display format")
    first_day_of_week: Literal[0, 1] = Field(0, description="0=Sunday, 1=Monday")


class DateRangeInput(DateRangeConfig, BaseInput[DateRangeConfig]):
    """Date range picker."""

    type: Literal["date_range"] = "date_range"

    # Display options (config fields inherited from DateRangeConfig)
    format: str = Field("YYYY-MM-DD", description="Display format")
    max_days: int | None = Field(None, description="Maximum days in range")


class TimeInput(TimeConfig, BaseInput[TimeConfig]):
    """Time picker input."""

    type: Literal["time"] = "time"

    # Display options (config fields inherited from TimeConfig)
    format_24h: bool = Field(True, description="Use 24-hour format")


class DateTimeInput(DateTimeConfig, BaseInput[DateTimeConfig]):
    """Combined date and time picker."""

    type: Literal["datetime"] = "datetime"

    # Display options (config fields inherited from DateTimeConfig)
    format: str = Field("YYYY-MM-DD HH:mm", description="Display format")
    format_24h: bool = Field(True, description="Use 24-hour format")


class RelativeDateInput(RelativeDateConfig, BaseInput[RelativeDateConfig]):
    """Relative date range selector (last 7 days, etc.)."""

    type: Literal["relative_date"] = "relative_date"
