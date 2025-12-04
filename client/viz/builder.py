"""
Fluent builder API for creating layouts.

Provides convenient factory methods and fluent interface
for building dashboard layouts.
"""

from typing import Any

from viz.core.context import current_context, add_to_context
from viz.core.datasource import DataSource, ComponentSource
from viz.containers.containers import Row, Column, Tab, Tabs, Section
from viz.containers.page import Page
from viz.widgets import (
    LineChartWidget,
    BarChartWidget,
    AreaChartWidget,
    TableWidget,
    MetricWidget,
    PlotlyWidget,
)


class LayoutBuilder:
    """Fluent builder for creating layouts."""

    # Delegate to core/context module for context management
    # These are kept for backward compatibility but now just wrap the core functions
    @classmethod
    def _current_context(cls):
        """Get the current context container."""
        return current_context()

    @classmethod
    def _push_context(cls, container):
        """Push a container onto the context stack."""
        from viz.core.context import push_context
        push_context(container)

    @classmethod
    def _pop_context(cls):
        """Pop a container from the context stack."""
        from viz.core.context import pop_context
        return pop_context()

    @classmethod
    def _add_to_context(cls, child):
        """Add a child to the current context container if one exists."""
        add_to_context(child)

    @classmethod
    def page(cls, title: str, description: str | None = None, **kwargs) -> Page:
        """
        Create a new page.

        Args:
            title: Page title
            description: Optional description
            **kwargs: Additional fields (icon, etc.)

        Returns:
            Page instance

        Note:
            If called within a context manager, automatically adds to parent.
        """
        page = Page(title=title, description=description, **kwargs)
        cls._add_to_context(page)
        return page

    @classmethod
    def section(
            cls,
            title: str | None = None,
            collapsible: bool = False,
            **kwargs
    ) -> Section:
        """
        Create a new section.

        Args:
            title: Optional section title
            collapsible: Whether section can be collapsed
            **kwargs: Additional fields

        Returns:
            Section instance

        Note:
            If called within a context manager, automatically adds to parent.
        """
        section = Section(title=title, collapsible=collapsible, **kwargs)
        cls._add_to_context(section)
        return section

    @classmethod
    def tabs(cls, default_tab: str | None = None, **kwargs) -> Tabs:
        """
        Create a tabs container.

        Args:
            default_tab: ID of default active tab
            **kwargs: Additional fields

        Returns:
            Tabs instance

        Note:
            If called within a context manager, automatically adds to parent.
        """
        tabs = Tabs(default_tab=default_tab, **kwargs)
        cls._add_to_context(tabs)
        return tabs

    @classmethod
    def tab(cls, title: str, icon: str | None = None, **kwargs) -> Tab:
        """
        Create a tab.

        Args:
            title: Tab title
            icon: Optional icon name
            **kwargs: Additional fields (disabled, etc.)

        Returns:
            Tab instance

        Note:
            If called within a context manager, automatically adds to parent.
        """
        tab = Tab(title=title, icon=icon, **kwargs)
        cls._add_to_context(tab)
        return tab

    @classmethod
    def row(cls, gap: str | None = None, **kwargs) -> Row:
        """
        Create a row.

        Args:
            gap: Gap between children (CSS value)
            **kwargs: Additional fields (align, etc.)

        Returns:
            Row instance

        Example:
            >>> row = LayoutBuilder.row(gap="20px", align="center")

        Note:
            If called within a context manager, automatically adds to parent.
        """
        row = Row(gap=gap, **kwargs)
        cls._add_to_context(row)
        return row

    @classmethod
    def column(
            cls,
            weight: int = 1,
            gap: str | None = None,
            **kwargs
    ) -> Column:
        """
        Create a column.

        Args:
            weight: Column weight for relative width (like CSS flex-grow)
            gap: Gap between children (CSS value)
            **kwargs: Additional fields

        Returns:
            Column instance

        Example:
            >>> col = LayoutBuilder.column(weight=2)

        Note:
            If called within a context manager, automatically adds to parent.
        """
        column = Column(weight=weight, gap=gap, **kwargs)
        cls._add_to_context(column)
        return column

    @classmethod
    def columns(cls, *weights: int) -> tuple[Column, ...]:
        """
        Create a row with columns of specified weights.

        Returns a tuple of Column instances that can be unpacked and used
        with context managers. The containing Row is automatically added
        to the current context.

        Args:
            *weights: Integer weights for each column (like CSS flex-grow).
                     E.g., columns(1, 2) creates two columns with 1/3 and 2/3 width.

        Returns:
            Tuple of Column instances

        Examples:
            # Create two equal columns
            col1, col2 = L.columns(1, 1)
            with col1:
                L.widget(...)
            with col2:
                L.widget(...)

            # Create three columns: 1/4, 1/2, 1/4
            left, center, right = L.columns(1, 2, 1)

        Note:
            The Row is automatically added to the current context (if any).
        """
        if not weights:
            raise ValueError("Must specify at least one weight")
        if any(w < 1 for w in weights):
            raise ValueError("Weights must be >= 1")

        # Create columns with weights and add to row
        cols = tuple(Column(weight=w) for w in weights)

        # Create row and add to current context
        row = Row(children=cols)
        cls._add_to_context(row)

        return cols

    @classmethod
    def input(cls, input_instance):
        """
        Add an input to the current containers context.

        Args:
            input_instance: An input instance (Select, DateInput, etc.)

        Returns:
            The input instance (for convenience)

        Example:
            >>> from viz import Select
            >>> region = L.input(Select(
            ...     name="region",
            ...     options=["North", "South"]
            ... ))

        Note:
            The input is automatically added to the current context (if any).
            Returns the input instance so you can store it in a variable.
        """
        cls._add_to_context(input_instance)
        return input_instance

    # -------------------------------------------------------------------------
    # Widget Factory Methods
    # -------------------------------------------------------------------------

    @classmethod
    def line_chart(
            cls,
            data_source: DataSource,
            title: str | None = None,
            x: str = "date",
            y: str | list[str] = "value",
            params: dict[str, Any] | None = None,
            **kwargs
    ) -> LineChartWidget:
        """
        Create a line chart widget.

        Args:
            data_source: DataSource for the chart data
            title: Optional widget title
            x: Column name for x-axis
            y: Column name(s) for y-axis
            params: Parameters for the data source (can include Input refs)
            **kwargs: Additional fields (description, color, series, etc.)

        Returns:
            LineChartWidget instance

        Example:
            >>> stocks = TimeseriesSource(name="market.stocks")
            >>> chart = L.line_chart(
            ...     data_source=stocks,
            ...     title="Stock Price",
            ...     x="date",
            ...     y="close",
            ...     params={"symbol": symbol_input}
            ... )
        """
        widget = LineChartWidget(
            data_source=data_source,
            title=title,
            x=x,
            y=y,
            params=params or {},
            **kwargs
        )
        cls._add_to_context(widget)
        return widget

    @classmethod
    def bar_chart(
            cls,
            data_source: DataSource,
            title: str | None = None,
            x: str = "category",
            y: str | list[str] = "value",
            params: dict[str, Any] | None = None,
            **kwargs
    ) -> BarChartWidget:
        """
        Create a bar chart widget.

        Args:
            data_source: DataSource for the chart data
            title: Optional widget title
            x: Column name for x-axis (categories)
            y: Column name(s) for y-axis (values)
            params: Parameters for the data source
            **kwargs: Additional fields (orientation, color, etc.)

        Returns:
            BarChartWidget instance
        """
        widget = BarChartWidget(
            data_source=data_source,
            title=title,
            x=x,
            y=y,
            params=params or {},
            **kwargs
        )
        cls._add_to_context(widget)
        return widget

    @classmethod
    def area_chart(
            cls,
            data_source: DataSource,
            title: str | None = None,
            x: str = "date",
            y: str | list[str] = "value",
            params: dict[str, Any] | None = None,
            **kwargs
    ) -> AreaChartWidget:
        """
        Create an area chart widget.

        Args:
            data_source: DataSource for the chart data
            title: Optional widget title
            x: Column name for x-axis
            y: Column name(s) for y-axis
            params: Parameters for the data source
            **kwargs: Additional fields (stacked, color, etc.)

        Returns:
            AreaChartWidget instance
        """
        widget = AreaChartWidget(
            data_source=data_source,
            title=title,
            x=x,
            y=y,
            params=params or {},
            **kwargs
        )
        cls._add_to_context(widget)
        return widget

    @classmethod
    def table(
            cls,
            data_source: DataSource,
            title: str | None = None,
            columns: list[str] | None = None,
            params: dict[str, Any] | None = None,
            **kwargs
    ) -> TableWidget:
        """
        Create a table widget.

        Args:
            data_source: DataSource for the table data
            title: Optional widget title
            columns: Column names to display (None = auto from data)
            params: Parameters for the data source
            **kwargs: Additional fields (page_size, sortable, filterable, etc.)

        Returns:
            TableWidget instance

        Example:
            >>> data = ComponentSource(component=SalesData)
            >>> table = L.table(
            ...     data_source=data,
            ...     title="Sales Data",
            ...     columns=["date", "product", "revenue"],
            ...     page_size=20
            ... )
        """
        widget = TableWidget(
            data_source=data_source,
            title=title,
            columns=columns,
            params=params or {},
            **kwargs
        )
        cls._add_to_context(widget)
        return widget

    @classmethod
    def metric(
            cls,
            data_source: DataSource,
            title: str | None = None,
            value_field: str = "value",
            params: dict[str, Any] | None = None,
            **kwargs
    ) -> MetricWidget:
        """
        Create a metric/KPI widget.

        Args:
            data_source: DataSource for the metric data
            title: Optional widget title
            value_field: Field name containing the metric value
            params: Parameters for the data source
            **kwargs: Additional fields (format, comparison_value, etc.)

        Returns:
            MetricWidget instance

        Example:
            >>> revenue = TimeseriesSource(name="metrics.revenue")
            >>> kpi = L.metric(
            ...     data_source=revenue,
            ...     title="Total Revenue",
            ...     value_field="total",
            ...     format="${value:,.0f}"
            ... )
        """
        widget = MetricWidget(
            data_source=data_source,
            title=title,
            value_field=value_field,
            params=params or {},
            **kwargs
        )
        cls._add_to_context(widget)
        return widget

    @classmethod
    def plotly(
            cls,
            data_source: ComponentSource,
            title: str | None = None,
            params: dict[str, Any] | None = None,
            **kwargs
    ) -> PlotlyWidget:
        """
        Create a server-rendered Plotly widget.

        Uses a RenderableComponent that implements load(), transform(), and render()
        to produce a Plotly figure on the server.

        Args:
            data_source: ComponentSource with a RenderableComponent
            title: Optional widget title
            params: Parameters for the component
            **kwargs: Additional fields (description, etc.)

        Returns:
            PlotlyWidget instance

        Example:
            >>> class SalesChart(RenderableComponent):
            ...     region: str
            ...
            ...     def load(self):
            ...         return db.query(...)
            ...
            ...     def transform(self, data):
            ...         return aggregate(data)
            ...
            ...     def render(self, data):
            ...         import plotly.express as px
            ...         return px.bar(data, x="product", y="sales")
            ...
            >>> chart = L.plotly(
            ...     data_source=ComponentSource(component=SalesChart),
            ...     title="Sales by Product",
            ...     params={"region": region_input}
            ... )
        """
        widget = PlotlyWidget(
            data_source=data_source,
            title=title,
            params=params or {},
            **kwargs
        )
        cls._add_to_context(widget)
        return widget


# Convenience alias
L = LayoutBuilder
