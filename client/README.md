# Viz Client Library

Python framework for building distributed dashboards with reactive components.

## Features

- **Clean Dataclass Pattern**: Define component parameters as class fields - no decorators needed
- **Component-Based Architecture**: Load/transform/render pattern for separation of concerns
- **Server-Side Execution**: All computation runs in isolated processes on the registry
- **Multiple Visualization Formats**: Plotly (primary), Vega-Lite, Altair support
- **Reactive Parameters**: Automatic re-execution when selector values change
- **Automatic Registration**: Components auto-register with the function registry

## Installation

```bash
# Install shared package first
cd ../shared
pip install -e .

# Install client library
cd ../client
pip install -e .
```

## Quick Start

### 1. Define a Component

Components use a clean dataclass pattern - just define parameters as class fields:

```python
from viz import Component
import plotly.express as px

class SalesChart(Component):
    # Parameters as class fields (automatically become constructor params)
    start_date: str
    region: str

    def load(self):
        # Access params via self.param_name
        return fetch_sales_data(self.start_date, self.region)

    def transform(self, data):
        # Process the data
        return aggregate_by_product(data)

    def render(self, data):
        # Return Plotly figure (recommended)
        return px.bar(data, x="product", y="sales")

        # Or return Vega-Lite spec
        # return {
        #     "mark": "bar",
        #     "encoding": {
        #         "x": {"field": "product", "type": "nominal"},
        #         "y": {"field": "sales", "type": "quantitative"}
        #     },
        #     "data": {"values": data}
        # }
```

**Key Design**: The `ComponentMeta` metaclass automatically applies `@dataclass` to your component, so you don't need to use the decorator yourself. All parameters become keyword-only constructor arguments.

### 2. Register the Component

```python
from viz import RegistryClient, register_component

# Connect to registry
client = RegistryClient(
    base_url="http://localhost:8000",
    username="testuser",
    password="testpassword123"
)

# Register your component
register_component(SalesChart, alias="sales_chart", client=client)
```

### 3. Build a Dashboard (Coming Soon)

```python
from viz import Dashboard, Page, Section, Row, Column, Widget
from viz import DateSelector, DropdownSelector

# Create dashboard with layout components (in development)
dashboard = Dashboard(name="sales", title="Sales Dashboard")

# Add selectors
date_selector = DateSelector(name="date", default="2024-01-01")
region_selector = DropdownSelector(
    name="region",
    options=["North", "South", "East", "West"]
)

# Add page with widgets
page = Page(
    title="Overview",
    sections=[
        Section(
            layout=Row([
                Column([date_selector, region_selector]),
                Column([
                    Widget(
                        component=SalesChart(
                            start_date=date_selector,
                            region=region_selector
                        )
                    )
                ])
            ])
        )
    ]
)

dashboard.add_page(page)
dashboard.register()
```

## Component Types

### Standard Component

Full three-stage execution pipeline:

```python
class MyComponent(Component):
    param1: str
    param2: int = 10  # Optional with default

    def load(self):
        """Fetch/load data"""
        return fetch_data(self.param1, self.param2)

    def transform(self, data):
        """Process data"""
        return process(data)

    def render(self, data):
        """Create visualization"""
        import plotly.express as px
        return px.line(data, x="date", y="value")
```

### Data Source Component

Simplified component for selector data sources (only needs `load`):

```python
from viz import DataSourceComponent

class AvailableDates(DataSourceComponent):
    def load(self):
        return ["2024-01-01", "2024-01-02", "2024-01-03"]

# Or with parameters
class RegionOptions(DataSourceComponent):
    country: str

    def load(self):
        return fetch_regions_for_country(self.country)
```

## Visualization Formats

The `render()` method can return:

1. **Plotly Figures** (Recommended - familiar to data analysts)
   ```python
   import plotly.express as px
   return px.bar(df, x="category", y="value")
   ```

2. **Vega-Lite Specs** (Lightweight, declarative)
   ```python
   return {
       "mark": "bar",
       "encoding": {"x": {...}, "y": {...}},
       "data": {"values": data}
   }
   ```

3. **Altair Charts** (Compiles to Vega-Lite)
   ```python
   import altair as alt
   return alt.Chart(df).mark_bar().encode(x="category", y="value")
   ```

All formats are automatically serialized for server-side execution.

## API Client Usage

### Basic Usage

```python
from viz import RegistryClient

# Create client (auto-login if credentials provided)
client = RegistryClient(
    base_url="http://localhost:8000",
    username="myuser",
    password="mypassword"
)

# Create a component
component_data = client.create_component(
    alias="my_component",
    class_name="MyComponent",
    source_code=MyComponent.get_source_code(),
    parameters=MyComponent.get_parameters()
)

# List components
components = client.list_components()

# Get component details
component = client.get_component("my_component")
```

### Context Manager

```python
from viz import RegistryClient

with RegistryClient(base_url="http://localhost:8000") as client:
    client.login("username", "password")
    # Use client...
```

## Helper Functions

### Auto-register Components

```python
from viz import register_component, auto_register_components
from viz import RegistryClient

client = RegistryClient(...)

# Register single component
register_component(SalesChart, alias="sales_chart", client=client)

# Auto-discover and register all components in a module
import my_components
auto_register_components(my_components, client=client)
```

## Current Status

✅ **Complete**:
- Component base class with dataclass pattern
- ComponentMeta metaclass (automatic dataclass conversion)
- DataSourceComponent for simplified data sources
- RegistryClient for API communication
- Component registration helpers

🚧 **In Progress**:
- Layout components (Dashboard, Page, Section, Row, Column)
- Widget wrapper
- Selector components (DateSelector, DropdownSelector, etc.)

## Documentation

See [ARCHITECTURE.md](../ARCHITECTURE.md) for detailed architecture documentation and design decisions.