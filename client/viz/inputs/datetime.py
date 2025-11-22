"""Date and time inputs."""

from typing import Literal, Optional, Tuple
from pydantic import Field, field_validator

from .base import BaseInput


class DateInput(BaseInput):
    """
    Date picker selector for single date.

    Examples:
        report_date = DateInput(
            name="report_date",
            label="Report Date",
            default="2024-01-01"
        )

        start_date = DateInput(
            name="start_date",
            label="Start Date",
            min_date="2020-01-01",
            max_date="2024-12-31"
        )

        birthdate = DateInput(
            name="birthdate",
            label="Date of Birth",
            max_date="today",
            help_text="Select your date of birth"
        )
    """

    input_type: Literal["date"] = "date"
    default: Optional[str] = Field(None, description="Default date (ISO format: YYYY-MM-DD)")

    # Date constraints
    min_date: Optional[str] = Field(None, description="Minimum selectable date (ISO format or 'today')")
    max_date: Optional[str] = Field(None, description="Maximum selectable date (ISO format or 'today')")

    # Display options
    format: str = Field("YYYY-MM-DD", description="Display format for date")
    first_day_of_week: Literal[0, 1] = Field(0, description="First day of week (0=Sunday, 1=Monday)")

    @field_validator('default', 'min_date', 'max_date')
    @classmethod
    def validate_date_format(cls, v):
        """Validate date is in ISO format or special keyword."""
        if v is None:
            return v
        if v == 'today':
            return v
        # Basic ISO date format validation (YYYY-MM-DD)
        if not isinstance(v, str) or len(v) != 10 or v[4] != '-' or v[7] != '-':
            raise ValueError("Date must be in ISO format (YYYY-MM-DD) or 'today'")
        return v


class DateRangeInput(BaseInput):
    """
    Date range picker for start and end dates.

    Examples:
        date_range = DateRangeInput(
            name="date_range",
            label="Date Range",
            default=("2024-01-01", "2024-12-31")
        )

        quarter = DateRangeInput(
            name="quarter",
            label="Select Quarter",
            default=("2024-01-01", "2024-03-31"),
            min_date="2020-01-01"
        )
    """

    input_type: Literal["date_range"] = "date_range"
    default: Optional[Tuple[str, str]] = Field(
        None,
        description="Default date range (start, end) in ISO format"
    )

    # Date constraints
    min_date: Optional[str] = Field(None, description="Minimum selectable date")
    max_date: Optional[str] = Field(None, description="Maximum selectable date")
    max_days: Optional[int] = Field(None, description="Maximum days in range")

    # Display options
    format: str = Field("YYYY-MM-DD", description="Display format for dates")

    @field_validator('default')
    @classmethod
    def validate_default_is_tuple(cls, v):
        """Ensure default is a tuple of two date strings (or None)."""
        if v is not None:
            if not isinstance(v, tuple) or len(v) != 2:
                raise ValueError("DateRangeInput default must be a tuple of (start_date, end_date)")
            if not all(isinstance(x, str) for x in v):
                raise ValueError("DateRangeInput default values must be strings")
        return v


class TimeInput(BaseInput):
    """
    Time picker selector.

    Examples:
        start_time = TimeInput(
            name="start_time",
            label="Start Time",
            default="09:00"
        )

        appointment = TimeInput(
            name="appointment_time",
            label="Appointment Time",
            default="14:30",
            min_time="09:00",
            max_time="17:00",
            step_minutes=15
        )
    """

    input_type: Literal["time"] = "time"
    default: Optional[str] = Field(None, description="Default time (HH:MM format)")

    # Time constraints
    min_time: Optional[str] = Field(None, description="Minimum selectable time (HH:MM)")
    max_time: Optional[str] = Field(None, description="Maximum selectable time (HH:MM)")
    step_minutes: int = Field(1, description="Step in minutes", ge=1, le=60)

    # Display options
    format_24h: bool = Field(True, description="Use 24-hour format (vs 12-hour AM/PM)")

    @field_validator('default', 'min_time', 'max_time')
    @classmethod
    def validate_time_format(cls, v):
        """Validate time is in HH:MM format."""
        if v is None:
            return v
        if not isinstance(v, str) or len(v) != 5 or v[2] != ':':
            raise ValueError("Time must be in HH:MM format")
        try:
            hours, minutes = v.split(':')
            h, m = int(hours), int(minutes)
            if not (0 <= h <= 23 and 0 <= m <= 59):
                raise ValueError
        except (ValueError, AttributeError):
            raise ValueError("Time must be valid HH:MM (00:00 to 23:59)")
        return v


class DateTimeInput(BaseInput):
    """
    Combined date and time picker selector.

    Examples:
        event_time = DateTimeInput(
            name="event_time",
            label="Event Date & Time",
            default="2024-01-01T14:30"
        )

        scheduled_at = DateTimeInput(
            name="scheduled_at",
            label="Schedule For",
            min_datetime="today",
            help_text="Select date and time for scheduling"
        )
    """

    input_type: Literal["datetime"] = "datetime"
    default: Optional[str] = Field(
        None,
        description="Default datetime (ISO format: YYYY-MM-DDTHH:MM)"
    )

    # DateTime constraints
    min_datetime: Optional[str] = Field(None, description="Minimum selectable datetime")
    max_datetime: Optional[str] = Field(None, description="Maximum selectable datetime")

    # Display options
    format: str = Field("YYYY-MM-DD HH:mm", description="Display format")
    format_24h: bool = Field(True, description="Use 24-hour time format")

    @field_validator('default', 'min_datetime', 'max_datetime')
    @classmethod
    def validate_datetime_format(cls, v):
        """Validate datetime is in ISO format."""
        if v is None:
            return v
        if v == 'today':
            return v
        # Basic ISO datetime format validation (YYYY-MM-DDTHH:MM)
        if not isinstance(v, str) or 'T' not in v:
            raise ValueError("DateTime must be in ISO format (YYYY-MM-DDTHH:MM) or 'today'")
        return v


class RelativeDateInput(BaseInput):
    """
    Input for relative date ranges (last 7 days, this month, etc.).

    Examples:
        time_period = RelativeDateInput(
            name="period",
            label="Time Period",
            options=[
                {"value": "last_7_days", "label": "Last 7 Days"},
                {"value": "last_30_days", "label": "Last 30 Days"},
                {"value": "this_month", "label": "This Month"},
                {"value": "this_quarter", "label": "This Quarter"},
                {"value": "this_year", "label": "This Year"}
            ],
            default="last_7_days"
        )
    """

    input_type: Literal["relative_date"] = "relative_date"
    default: Optional[str] = Field(None, description="Default relative period value")

    # Predefined options for relative dates
    options: list[dict[str, str]] = Field(
        ...,
        description="List of relative date options (value and label)"
    )

    # Option to allow custom range
    allow_custom: bool = Field(False, description="Allow custom date range selection")

    @field_validator('options')
    @classmethod
    def validate_options(cls, v):
        """Ensure options list is valid."""
        if not v or len(v) == 0:
            raise ValueError("RelativeDateInput must have at least one option")
        for opt in v:
            if not isinstance(opt, dict) or 'value' not in opt or 'label' not in opt:
                raise ValueError("Each option must be a dict with 'value' and 'label'")
        return v
