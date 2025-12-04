"""
Base Widget class for all widget types.

Widgets are leaf nodes in the layout tree that display data visualizations.
Each widget has a data source and optional parameters for querying that source.
"""

from __future__ import annotations

from abc import ABC

from pydantic import Field

from viz.core.datasource import DataSource
from viz.core.layout import ParameterizedNode


class BaseWidget(ParameterizedNode, ABC):
    """
    Abstract base class for all widgets.

    Widgets combine a DataSource (where data comes from) with visualization
    configuration. The `params` field (inherited from ParameterizedNode)
    provides parameters for the data source at the point of use, allowing
    the same DataSource to be reused with different parameters.

    Subclasses define specific visualization types:
    - Frontend-native: LineChartWidget, BarChartWidget, TableWidget, MetricWidget
    - Server-rendered: PlotlyWidget (uses RenderableComponent)

    Example:
        stocks = TimeseriesSource(name="market.stocks")

        # Same source, different params
        LineChartWidget(
            data_source=stocks,
            params={"symbol": "AAPL"},
            x="date",
            y="close"
        )
    """

    title: str | None = Field(None, description="Widget title")
    description: str | None = Field(None, description="Widget description")

    data_source: DataSource = Field(..., description="Data source for this widget")
