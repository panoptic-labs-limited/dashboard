"""
Chart widgets for frontend-native rendering.

These widgets send data to the frontend which handles the actual rendering.
Configuration specifies how to map data fields to chart axes and styling.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from .base import BaseWidget


class LineChartWidget(BaseWidget):
    """
    Frontend-native line chart.

    Renders time series or continuous data as connected lines.

    Example:
        LineChartWidget(
            title="Stock Price",
            data_source=TimeseriesSource(name="market.stocks"),
            params={"symbol": symbol_input},
            x="date",
            y="close",
            color="symbol"
        )
    """

    type: Literal["line_chart"] = "line_chart"

    x: str = Field("date", description="Field for x-axis (typically date/time)")
    y: str | list[str] = Field("value", description="Field(s) for y-axis")
    color: str | None = Field(None, description="Field for color grouping (multiple lines)")

    # Styling options
    line_shape: Literal["linear", "spline", "step"] = Field(
        "linear",
        description="Line interpolation shape"
    )
    show_points: bool = Field(False, description="Show data points on line")


class BarChartWidget(BaseWidget):
    """
    Frontend-native bar chart.

    Renders categorical data as bars.

    Example:
        BarChartWidget(
            title="Sales by Region",
            data_source=ComponentSource(component=SalesLoader),
            params={"year": year_input},
            x="region",
            y="revenue",
            orientation="vertical"
        )
    """

    type: Literal["bar_chart"] = "bar_chart"

    x: str = Field(..., description="Field for x-axis (category)")
    y: str | list[str] = Field(..., description="Field(s) for y-axis (value)")
    color: str | None = Field(None, description="Field for color grouping (stacked/grouped)")

    orientation: Literal["vertical", "horizontal"] = Field(
        "vertical",
        description="Bar orientation"
    )
    bar_mode: Literal["group", "stack", "relative"] = Field(
        "group",
        description="How to display multiple series"
    )


class AreaChartWidget(BaseWidget):
    """
    Frontend-native area chart.

    Renders data as filled areas, useful for showing cumulative values or
    composition over time.

    Example:
        AreaChartWidget(
            title="Revenue by Product",
            data_source=TimeseriesSource(name="finance.revenue"),
            x="date",
            y="amount",
            color="product",
            stacked=True
        )
    """

    type: Literal["area_chart"] = "area_chart"

    x: str = Field("date", description="Field for x-axis")
    y: str | list[str] = Field("value", description="Field(s) for y-axis")
    color: str | None = Field(None, description="Field for color grouping")

    stacked: bool = Field(False, description="Stack areas on top of each other")
    line_shape: Literal["linear", "spline", "step"] = Field(
        "linear",
        description="Line interpolation shape"
    )
