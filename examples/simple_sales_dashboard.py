"""
Simple Sales Dashboard Example

Demonstrates:
- Component definition with dataclass pattern
- Dashboard structure with layout components
- Selector binding to component parameters
- Registration with the function registry
"""

from viz import (
    Component,
    Dashboard, Page, Section, Row, Column, Widget,
    DateSelector, DropdownSelector,
    RegistryClient, register_component
)
import plotly.express as px


# Define a simple component
class SalesChart(Component):
    """Sales bar chart component."""

    # Parameters as class fields
    region: str
    date: str = "2024-01-01"

    def load(self):
        """Load mock sales data."""
        # Mock data - in real scenario this would query a database
        return [
            {"product": "Widget A", "sales": 1000, "region": self.region, "date": self.date},
            {"product": "Widget B", "sales": 1500, "region": self.region, "date": self.date},
            {"product": "Widget C", "sales": 800, "region": self.region, "date": self.date},
            {"product": "Widget D", "sales": 1200, "region": self.region, "date": self.date},
        ]

    def transform(self, data):
        """No transformation needed for this simple example."""
        return data

    def render(self, data):
        """Render as Plotly bar chart."""
        import pandas as pd
        df = pd.DataFrame(data)

        fig = px.bar(
            df,
            x="product",
            y="sales",
            title=f"Sales by Product - {self.region} ({self.date})",
            labels={"product": "Product", "sales": "Sales ($)"}
        )

        return fig


class SalesMetrics(Component):
    """Sales metrics summary component."""

    region: str
    date: str = "2024-01-01"

    def load(self):
        """Load mock metrics."""
        return {
            "total_sales": 4500,
            "num_products": 4,
            "avg_sale": 1125,
            "region": self.region,
            "date": self.date
        }

    def transform(self, data):
        """Calculate additional metrics."""
        data["sales_per_product"] = data["total_sales"] / data["num_products"]
        return data

    def render(self, data):
        """Render as simple table/metric display."""
        # Return a simple dict structure (could be rendered as metrics cards in UI)
        return {
            "type": "metrics",
            "data": {
                "Total Sales": f"${data['total_sales']:,}",
                "Number of Products": data['num_products'],
                "Average Sale": f"${data['avg_sale']:,}",
                "Region": data['region'],
                "Date": data['date']
            }
        }


def main():
    """Create and register the sales dashboard."""

    # Connect to registry
    print("Connecting to registry...")
    client = RegistryClient(
        base_url="http://localhost:8000",
        username="testuser",
        password="testpassword123"
    )
    print("✓ Connected to registry")

    # Register components
    print("\nRegistering components...")
    register_component(SalesChart, alias="sales_chart", client=client)
    print("✓ Registered SalesChart component")

    register_component(SalesMetrics, alias="sales_metrics", client=client)
    print("✓ Registered SalesMetrics component")

    # Create selectors
    print("\nCreating selectors...")
    date_selector = DateSelector(
        name="report_date",
        label="Report Date",
        default="2024-01-01"
    )

    region_selector = DropdownSelector(
        name="region",
        label="Region",
        options=["North", "South", "East", "West"],
        default="North"
    )
    print("✓ Created selectors")

    # Create dashboard structure
    print("\nBuilding dashboard structure...")
    dashboard = Dashboard(
        name="sales_dashboard",
        title="Sales Analytics Dashboard",
        description="Simple sales dashboard demonstrating Viz framework"
    )

    # Create page with layout
    overview_page = Page(
        title="Overview",
        description="Sales overview and metrics",
        sections=[
            Section(
                title="Controls",
                layout=Row([
                    Column(
                        width="1/2",
                        children=[date_selector]
                    ),
                    Column(
                        width="1/2",
                        children=[region_selector]
                    )
                ])
            ),
            Section(
                title="Metrics",
                layout=Row([
                    Column(
                        width="1/1",
                        children=[
                            Widget(
                                component=SalesMetrics(
                                    region=region_selector,
                                    date=date_selector
                                ),
                                title="Sales Summary"
                            )
                        ]
                    )
                ])
            ),
            Section(
                title="Sales Chart",
                layout=Row([
                    Column(
                        width="1/1",
                        children=[
                            Widget(
                                component=SalesChart(
                                    region=region_selector,
                                    date=date_selector
                                ),
                                title="Sales by Product"
                            )
                        ]
                    )
                ])
            )
        ]
    )

    dashboard.add_page(overview_page)
    print("✓ Built dashboard structure")

    # Register dashboard
    print("\nRegistering dashboard...")
    result = dashboard.register(client)
    print(f"✓ Dashboard registered successfully!")
    print(f"  ID: {result.get('id')}")
    print(f"  Name: {result.get('name')}")
    print(f"  Title: {result.get('title')}")

    print("\n" + "="*60)
    print("SUCCESS! Dashboard created and registered.")
    print("="*60)
    print(f"\nDashboard '{dashboard.name}' is ready!")
    print(f"API Base: http://localhost:8000")
    print(f"\nNext steps:")
    print(f"- View dashboard: GET /dashboards/{dashboard.name}")
    print(f"- Execute component: POST /dashboard/{dashboard.name}/component/{{widget_id}}/render")


if __name__ == "__main__":
    main()
