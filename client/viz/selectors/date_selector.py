"""Date selector component."""

import uuid
from typing import Optional, Callable
from dataclasses import dataclass, field


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
    id: str = field(default_factory=lambda: f"selector_{uuid.uuid4().hex[:8]}")

    def __post_init__(self):
        """Set label to name if not provided."""
        if self.label is None:
            self.label = self.name.replace("_", " ").title()

    def to_dict(self) -> dict:
        """Serialize to dictionary for dashboard structure."""
        selector_config = {
            "name": self.name,
            "label": self.label,
            "selector_type": "date",
            "default": self.default,
            "required": True
        }

        if self.data_source:
            # If there's a data source function, include reference
            # (the function itself should be registered separately)
            selector_config["data_source"] = {
                "alias": getattr(self.data_source, '_registry_alias', self.data_source.__name__),
                "params": {}
            }

        return {
            "id": self.id,
            "type": "selector",
            "selector": selector_config
        }
