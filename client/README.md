# Viz Client Library

Python framework for building distributed dashboards with reactive components.

## Features

- Declarative dashboard definitions
- Component-based architecture (load/transform/render)
- Reactive selectors and parameter binding
- Layout system (Dashboard/Page/Section/Row/Column)
- Automatic registration with function registry

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from viz import Dashboard, Page, Section, Row, Column, Widget
from viz import DateSelector, DropdownSelector
from viz import Component

# Define a component
class SalesChart(Component):
    def load(self, start_date: str, region: str):
        # Load data
        return fetch_sales_data(start_date, region)

    def transform(self, data):
        # Transform data
        return aggregate_by_product(data)

    def render(self, data):
        # Return Vega-Lite spec
        return {
            "mark": "bar",
            "encoding": {...},
            "data": {"values": data}
        }

# Create dashboard
dashboard = Dashboard(name="sales", title="Sales Dashboard")

# Add components and selectors
date_selector = DateSelector(name="date", default="2024-01-01")
region_selector = DropdownSelector(
    name="region",
    options=["North", "South", "East", "West"]
)

page = Page(
    title="Overview",
    sections=[
        Section(
            layout=Row([
                Column([date_selector, region_selector]),
                Column([
                    Widget(
                        component=SalesChart(),
                        params={
                            "start_date": date_selector,
                            "region": region_selector
                        }
                    )
                ])
            ])
        )
    ]
)

dashboard.add_page(page)
dashboard.register()  # Registers with function registry
```

## Documentation

See [ARCHITECTURE.md](../ARCHITECTURE.md) for detailed architecture documentation.