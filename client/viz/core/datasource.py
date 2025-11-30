"""
Data sources for widgets and inputs.

DataSource is the abstract base for all data sources. It identifies WHERE data
comes from, while params (specified at widget/input level) define HOW to query it.

Supported sources:
- TimeseriesSource: Data from Timeseries Service (by name)
- ComponentSource: Data from a Component's load/transform
- FunctionSource: Data from a simple callable
"""

from __future__ import annotations

from abc import ABC
from typing import Callable, Any, Literal, TYPE_CHECKING

from pydantic import BaseModel, Field, ConfigDict

if TYPE_CHECKING:
    pass


class DataSource(BaseModel, ABC):
    """
    Abstract base for all data sources.

    DataSource identifies where data comes from. Parameters for querying
    the source are specified at the widget/input level, not here.

    This allows the same DataSource to be reused with different parameters:

        stocks = TimeseriesSource(name="market.stocks")

        chart1 = LineChartWidget(data_source=stocks, params={"symbol": "AAPL"})
        chart2 = LineChartWidget(data_source=stocks, params={"symbol": "GOOG"})
    """

    model_config = ConfigDict(
        extra='forbid',
        use_enum_values=True,
    )

    type: str = Field(..., description="Discriminator for source type")


class TimeseriesSource(DataSource):
    """
    Data source from Timeseries Service.

    References a timeseries by its namespaced name (e.g., "market.stocks.aapl").
    The Timeseries Service returns well-structured (date, value) data with metadata.

    Examples:
        # Simple timeseries
        TimeseriesSource(name="market.stocks.aapl")

        # Used with params at widget level
        stocks = TimeseriesSource(name="market.stocks")
        LineChartWidget(data_source=stocks, params={"symbol": symbol_input})
    """

    type: Literal["timeseries"] = "timeseries"
    name: str = Field(..., description="Namespaced timeseries name (e.g., 'market.stocks.aapl')")


class ComponentSource(DataSource):
    """
    Data source from a Component's load/transform pipeline.

    References a Component class or registered component name. The component's
    load() and transform() methods are executed to produce data.

    For RenderableComponent (with render()), use with PlotlyWidget.
    For regular Component (data only), use with frontend-native widgets.

    Examples:
        # With Component class
        ComponentSource(component=SalesLoader)

        # With registered component name
        ComponentSource(component="sales_loader")
    """

    type: Literal["component"] = "component"
    # Component class or registered name
    # Using Any to avoid Pydantic issues with Union[type, str]
    component: Any = Field(
        ...,
        description="Component class or registered component name"
    )

    model_config = ConfigDict(
        extra='forbid',
        arbitrary_types_allowed=True,
    )


class FunctionSource(DataSource):
    """
    Data source from a simple callable function.

    The function is executed server-side to produce data. Useful for
    simple data fetching without needing a full Component class.

    Examples:
        # Simple function
        FunctionSource(func=get_available_regions)
    """

    type: Literal["function"] = "function"
    func: Callable[..., Any] = Field(
        ...,
        description="Callable that returns data"
    )

    model_config = ConfigDict(
        extra='forbid',
        arbitrary_types_allowed=True,
    )
