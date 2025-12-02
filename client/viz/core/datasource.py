"""
Data sources for widgets and inputs.

DataSource is the abstract base for all data sources. It identifies WHERE data
comes from, while params (specified at widget/input level) define HOW to query it.

Supported sources:
- TimeseriesSource: Data from Timeseries Service (by name)
- ComponentSource: Data from a Component's load/transform
"""

from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Literal, Union

from pydantic import BaseModel, Field, ConfigDict, computed_field

if TYPE_CHECKING:
    from viz.core.component import Component


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
        # With Component class (local - will be registered)
        ComponentSource(component=SalesLoader)

        # With registered component name (external - already registered)
        ComponentSource(component="sales_loader")

    Serialization:
        - Local component: {"type": "component", "name": "sales_loader", "class_name": "SalesLoader"}
        - External component: {"type": "component", "name": "sales_loader"}
    """

    type: Literal["component"] = "component"

    component: Union[type[Component], str] = Field(
        ...,
        description="Component class or registered component name",
        exclude=True,  # Don't include raw component in serialization
    )

    model_config = ConfigDict(
        extra='forbid',
        arbitrary_types_allowed=True,
    )

    @computed_field
    def name(self) -> str:
        """Component name (derived from component)."""
        if isinstance(self.component, str):
            return self.component
        if not hasattr(self.component, 'name'):
            raise ValueError(
                f"Component class {self.component.__name__} must define 'name' ClassVar"
            )
        return self.component.name

    @computed_field
    def class_name(self) -> str | None:
        """Python class name (only set for local components)."""
        if isinstance(self.component, str):
            return None
        return self.component.__name__
