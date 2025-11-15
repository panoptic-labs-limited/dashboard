"""Date selector component."""

from typing import Optional, Callable
from dataclasses import dataclass


@dataclass
class DateSelector:
    """
    Date picker selector for dashboards.

    Provides a single date selection input that can be bound
    to component parameters.

    Example:
        date_selector = DateSelector(
            name="report_date",
            label="Report Date",
            default="2024-01-01"
        )

        # Bind to component
        chart = SalesChart(start_date=date_selector)
    """
    name: str
    label: Optional[str] = None
    default: Optional[str] = None
    data_source: Optional[Callable] = None

    def __post_init__(self):
        """Set label to name if not provided."""
        if self.label is None:
            self.label = self.name.replace("_", " ").title()

    def to_dict(self) -> dict:
        """Serialize to dictionary for dashboard structure."""
        result = {
            "type": "selector",
            "selector_type": "date",
            "name": self.name,
            "label": self.label,
            "default": self.default
        }

        if self.data_source:
            # If there's a data source function, include reference
            # (the function itself should be registered separately)
            result["data_source"] = getattr(
                self.data_source,
                '_registry_alias',
                self.data_source.__name__
            )

        return result
