"""
Metric widget for displaying single KPI values.

Frontend-native rendering of key performance indicators with optional
comparison and formatting.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from .base import Widget


class MetricWidget(Widget):
    """
    Frontend-native metric/KPI display.

    Shows a single value prominently, optionally with comparison to
    previous period or target.

    Example:
        MetricWidget(
            title="Monthly Revenue",
            data_source=ComponentSource(component=RevenueLoader),
            params={"month": month_input},
            value_field="revenue",
            format="${:,.0f}",
            comparison_field="previous_revenue",
            comparison_label="vs last month"
        )
    """

    type: Literal["metric"] = "metric"

    value_field: str = Field("value", description="Field containing the metric value")
    label: str | None = Field(None, description="Label below the value")

    # Formatting
    format: str | None = Field(
        None,
        description="Python format string (e.g., '{:,.2f}', '${:,.0f}', '{:.1%}')"
    )
    prefix: str | None = Field(None, description="Prefix before value (e.g., '$')")
    suffix: str | None = Field(None, description="Suffix after value (e.g., '%')")

    # Comparison/delta
    comparison_field: str | None = Field(
        None,
        description="Field for comparison value (shows delta)"
    )
    comparison_label: str | None = Field(
        None,
        description="Label for comparison (e.g., 'vs last month')"
    )
    comparison_mode: Literal["absolute", "percentage"] = Field(
        "percentage",
        description="How to display the comparison"
    )

    # Styling
    size: Literal["small", "medium", "large"] = Field(
        "medium",
        description="Display size"
    )
