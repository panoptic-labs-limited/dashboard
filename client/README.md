# Viz Client Library

Python framework for building distributed dashboards with reactive components and typed widgets.

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from viz import (
    # Components
    RenderableComponent, ComponentSource,
    # Layout
    Dashboard, Page, Section, Row, Column,
    # Builder
    L,
    # Inputs
    Select, Slider,
)


# 1. Define a RenderableComponent for server-side visualizations
class SalesChart(RenderableComponent):
    region: str
    year: int = 2024

    def load(self):
        return fetch_sales_data(self.region, self.year)

    def transform(self, data):
        return aggregate_by_product(data)

    def render(self, data):
        import plotly.express as px
        return px.bar(data, x="product", y="sales")


# 2. Build the dashboard
dashboard = Dashboard(id="sales", title="Sales Dashboard")

with dashboard.page(title="Overview"):
    with L.section(title="Filters"):
        region = L.input(
            Select(
                name="region",
                options=[("north", "North"), ("south", "South")]
            )
        )
        year = L.input(
            Slider(
                name="year",
                min_value=2020,
                max_value=2024,
                default=2024
            )
        )

    with L.row():
        with L.column(weight=2):
            L.plotly(
                data_source=ComponentSource(component=SalesChart),
                title="Sales by Product",
                params={"region": region, "year": year}
            )
```

## Core Concepts

### Data Sources

Data sources define WHERE data comes from. They are reusable and can be shared across widgets.

```python
from viz import TimeseriesSource, ComponentSource, FunctionSource

# Timeseries Service (by name)
stocks = TimeseriesSource(name="market.stocks")

# Component class
sales_data = ComponentSource(component=SalesLoader)


# Simple function
def get_options():
    return ["A", "B", "C"]


options_source = FunctionSource(func=get_options)
```

### Components

Components define data pipelines with `load()` and `transform()` methods.

| Class                 | Purpose                      | Methods                             |
|-----------------------|------------------------------|-------------------------------------|
| `Component`           | Data-only (frontend renders) | `load()`, `transform()`             |
| `RenderableComponent` | Server-side rendering        | `load()`, `transform()`, `render()` |
| `DataSourceComponent` | Simple data fetching         | `load()` only                       |

```python
from viz import Component, RenderableComponent


# Data-only component (for frontend-native widgets)
class StockData(Component):
    symbol: str

    def load(self):
        return fetch_stock_prices(self.symbol)

    def transform(self, data):
        return data.tail(30)  # Last 30 days


# Server-rendered component (for PlotlyWidget)
class StockChart(RenderableComponent):
    symbol: str

    def load(self):
        return fetch_stock_prices(self.symbol)

    def transform(self, data):
        return data.tail(30)

    def render(self, data):
        import plotly.express as px
        return px.line(data, x="date", y="close")
```

### Widgets

Widgets display data visualizations. Each widget type has specific configuration options.

| Widget            | Type            | Use Case                |
|-------------------|-----------------|-------------------------|
| `LineChartWidget` | Frontend-native | Time series, trends     |
| `BarChartWidget`  | Frontend-native | Comparisons, categories |
| `AreaChartWidget` | Frontend-native | Cumulative data         |
| `TableWidget`     | Frontend-native | Data tables             |
| `MetricWidget`    | Frontend-native | KPIs, single values     |
| `PlotlyWidget`    | Server-rendered | Custom visualizations   |

```python
from viz import (
    LineChartWidget, BarChartWidget, TableWidget,
    MetricWidget, PlotlyWidget,
    TimeseriesSource, ComponentSource
)

# Frontend-native widgets (data processed on frontend)
LineChartWidget(
    data_source=TimeseriesSource(name="stocks"),
    title="Stock Prices",
    x="date",
    y="close",
    params={"symbol": "AAPL"}
)

TableWidget(
    data_source=ComponentSource(component=SalesData),
    title="Sales Table",
    columns=["date", "product", "revenue"],
    page_size=20
)

# Server-rendered widget (Plotly figure generated on server)
PlotlyWidget(
    data_source=ComponentSource(component=SalesChart),
    title="Custom Chart",
    params={"region": region_input}
)
```

### Inputs

Inputs allow user interaction and can be bound to widget parameters.

**Choice Inputs:**

- `Select` - Single selection dropdown
- `MultiSelect` - Multiple selection
- `RadioGroup` - Radio buttons
- `Checkbox` - Single checkbox
- `CheckboxGroup` - Multiple checkboxes
- `Toggle` - Boolean toggle switch

**Text Inputs:**

- `TextInput` - Single line text
- `TextArea` - Multi-line text
- `SearchInput` - Search with autocomplete

**Numeric Inputs:**

- `NumericInput` - Number input
- `Slider` - Single value slider
- `RangeSlider` - Min/max range slider
- `NumericRange` - Two number inputs

**Date/Time Inputs:**

- `DateInput` - Single date
- `DateRangeInput` - Date range
- `TimeInput` - Time picker
- `DateTimeInput` - Date and time
- `RelativeDateInput` - Relative dates (last 7 days, etc.)

```python
from viz import Select, Slider, DateRangeInput, FunctionSource

# Static options
region = Select(
    name="region",
    label="Region",
    options=[("north", "North"), ("south", "South")]
)


# Dynamic options from function
def get_products():
    return [{"value": p.id, "label": p.name} for p in fetch_products()]


product = Select(
    name="product",
    source=FunctionSource(func=get_products)
)

# Numeric slider
year = Slider(
    name="year",
    min_value=2020,
    max_value=2024,
    default=2024,
    show_value=True
)

# Date range
dates = DateRangeInput(
    name="date_range",
    default_start="2024-01-01",
    default_end="2024-12-31"
)
```

### Layout Builder

The `LayoutBuilder` (aliased as `L`) provides a fluent API for building layouts with context managers.

```python
from viz import L, Dashboard, TimeseriesSource

stocks = TimeseriesSource(name="market.stocks")

dashboard = Dashboard(id="my_dashboard", title="My Dashboard")

with dashboard.page(title="Overview", icon="📊"):
    # Section with inputs
    with L.section(title="Filters"):
        symbol = L.input(Select(name="symbol", options=["AAPL", "GOOG"]))

    # Row with multiple columns
    with L.row():
        with L.column(weight=2):
            L.line_chart(
                data_source=stocks,
                title="Price",
                x="date",
                y="close",
                params={"symbol": symbol}
            )
        with L.column(weight=1):
            L.metric(
                data_source=stocks,
                title="Latest Price",
                value_field="close",
                params={"symbol": symbol}
            )

    # Tabs
    with L.tabs():
        with L.tab(title="Chart"):
            L.area_chart(data_source=stocks, x="date", y="volume")
        with L.tab(title="Data"):
            L.table(data_source=stocks, columns=["date", "open", "close"])
```

**Builder Methods:**

| Method                   | Creates                   |
|--------------------------|---------------------------|
| `L.page(title, ...)`     | Page                      |
| `L.section(title, ...)`  | Section                   |
| `L.row(gap, ...)`        | Row container             |
| `L.column(weight, ...)`  | Column container          |
| `L.columns(w1, w2, ...)` | Row with weighted columns |
| `L.tabs(...)`            | Tabs container            |
| `L.tab(title, ...)`      | Tab                       |
| `L.input(input_obj)`     | Add input to layout       |
| `L.line_chart(...)`      | LineChartWidget           |
| `L.bar_chart(...)`       | BarChartWidget            |
| `L.area_chart(...)`      | AreaChartWidget           |
| `L.table(...)`           | TableWidget               |
| `L.metric(...)`          | MetricWidget              |
| `L.plotly(...)`          | PlotlyWidget              |

## File Structure

```
client/viz/
├── __init__.py              # Public API exports
├── builder.py               # LayoutBuilder (L) with widget helpers
├── core/
│   ├── __init__.py
│   ├── component.py         # Component, RenderableComponent, DataSourceComponent
│   ├── context.py           # Builder context stack
│   ├── datasource.py        # DataSource, TimeseriesSource, ComponentSource, FunctionSource
│   └── layout.py            # LayoutNode, LeafNode, Container
├── widgets/
│   ├── __init__.py
│   ├── base.py              # Widget base class
│   ├── charts.py            # LineChartWidget, BarChartWidget, AreaChartWidget
│   ├── table.py             # TableWidget
│   ├── metric.py            # MetricWidget
│   └── plotly.py            # PlotlyWidget
├── inputs/
│   ├── __init__.py
│   ├── base.py              # Input base class
│   ├── choice.py            # Select, MultiSelect, RadioGroup, etc.
│   ├── text.py              # TextInput, TextArea, SearchInput
│   ├── numeric.py           # NumericInput, Slider, RangeSlider
│   └── date_time.py         # DateInput, DateRangeInput, etc.
├── layout/
│   ├── __init__.py
│   ├── containers.py        # Row, Column, Section, Tabs, Tab
│   ├── dashboard.py         # Dashboard, Page
│   └── enums.py             # WidgetType (deprecated)
└── api/
    ├── __init__.py
    ├── serializer.py        # Dashboard/widget serialization
    ├── extractor.py         # Component/function extraction
    └── registry.py          # Registry client
```

## Serialization & Registration

The API module handles serialization for the registry service.

```python
from viz.api import (
    serialize_dashboard,
    serialize_component,
    ComponentExtractor,
)

# Extract components and functions from dashboard
extractor = ComponentExtractor(dashboard)
extractor.extract()

components = extractor.get_components()  # [(class, name), ...]
functions = extractor.get_functions()  # [(func, name), ...]

# Serialize dashboard structure
dashboard_json = serialize_dashboard(dashboard)
```

## Naming Conventions

- **`name`** - Human-defined identifier (component name, timeseries name, input name)
- **`id`** - Auto-generated unique identifier (for widgets, containers)
- **`__component_name__`** - Class attribute to set explicit component name

```python
class MyComponent(RenderableComponent):
    __component_name__ = "my_custom_name"  # Explicit name
    # ...

# Without __component_name__, name is derived from class name:
# MyComponent -> my_component (snake_case)
```

## Example

See `examples/plotly_datasets_dashboard.py` for a complete example using Plotly built-in datasets.

```bash
# Run the example
python examples/plotly_datasets_dashboard.py
```

## Migration from Old API

If you were using the old API, here are the key changes:

| Old                                                     | New                                                          |
|---------------------------------------------------------|--------------------------------------------------------------|
| `Component` with `render()`                             | `RenderableComponent`                                        |
| `L.widget(widget_type=WidgetType.CHART, component=...)` | `L.plotly(data_source=ComponentSource(component=...))`       |
| `WidgetType.CHART`                                      | Use typed widgets: `LineChartWidget`, `BarChartWidget`, etc. |
| `component=MyClass`                                     | `data_source=ComponentSource(component=MyClass)`             |
| `__id__ = "name"`                                       | `__component_name__ = "name"`                                |
| `alias` parameter                                       | `name` parameter                                             |

## Development

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Type checking
mypy viz/
```
