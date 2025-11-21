"""
Simple Sales Dashboard Example

Demonstrates:
- Component definition with dataclass pattern
- Dashboard structure with new Pydantic layout system
- Fluent builder API with LayoutBuilder (L)
- Type-safe layout construction with enums
- Registration with the function registry
"""

from viz import (
    Component,
    L,  # LayoutBuilder fluent API
    WidgetType, SelectorType, ColumnWidth,
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
        # Mock data - varies by region to demonstrate reactivity
        # In real scenario this would query a database
        region_multipliers = {
            "North": 1.0,
            "South": 1.3,
            "East": 0.8,
            "West": 1.1
        }
        multiplier = region_multipliers.get(self.region, 1.0)

        return [
            {"product": "Widget A", "sales": int(1000 * multiplier), "region": self.region, "date": self.date},
            {"product": "Widget B", "sales": int(1500 * multiplier), "region": self.region, "date": self.date},
            {"product": "Widget C", "sales": int(800 * multiplier), "region": self.region, "date": self.date},
            {"product": "Widget D", "sales": int(1200 * multiplier), "region": self.region, "date": self.date},
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
        # Vary totals by region
        region_multipliers = {
            "North": 1.0,
            "South": 1.3,
            "East": 0.8,
            "West": 1.1
        }
        multiplier = region_multipliers.get(self.region, 1.0)
        total = int(4500 * multiplier)

        return {
            "total_sales": total,
            "num_products": 4,
            "avg_sale": int(total / 4),
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

    # Create dashboard structure using fluent builder API
    print("\nBuilding dashboard structure...")
    dashboard = (
        L.dashboard(
            title="Sales Analytics Dashboard",
            description="Simple sales dashboard demonstrating new Viz Pydantic layout system"
        )
        .add(
            L.page(
                title="Overview",
                description="Sales overview and metrics"
            )
            .add(
                # Controls Section
                L.section(title="Controls")
                .add(
                    L.row(gap="16px")
                    .add(
                        L.column(width=ColumnWidth.HALF)
                        .add(
                            L.selector(
                                selector_type=SelectorType.DATE,
                                name="date",
                                label="Report Date",
                                default="2024-01-01"
                            )
                        )
                    )
                    .add(
                        L.column(width=ColumnWidth.HALF)
                        .add(
                            L.selector(
                                selector_type=SelectorType.DROPDOWN,
                                name="region",
                                label="Region",
                                options=["North", "South", "East", "West"],
                                default="North"
                            )
                        )
                    )
                )
            )
            .add(
                # Metrics Section
                L.section(title="Metrics")
                .add(
                    L.row()
                    .add(
                        L.column(width=ColumnWidth.FULL)
                        .add(
                            L.widget(
                                widget_type=WidgetType.METRIC,
                                title="Sales Summary",
                                component_alias="sales_metrics",
                                params={
                                    "region": "region",  # Binds to region selector
                                    "date": "date"       # Binds to date selector
                                }
                            )
                        )
                    )
                )
            )
            .add(
                # Sales Chart Section
                L.section(title="Sales Chart")
                .add(
                    L.row()
                    .add(
                        L.column(width=ColumnWidth.FULL)
                        .add(
                            L.widget(
                                widget_type=WidgetType.CHART,
                                title="Sales by Product",
                                component_alias="sales_chart",
                                params={
                                    "region": "region",  # Binds to region selector
                                    "date": "date"       # Binds to date selector
                                }
                            )
                        )
                    )
                )
            )
        )
    )
    print("✓ Built dashboard structure")

    # Display dashboard structure
    print("\nDashboard structure created:")
    print(f"  Title: {dashboard.title}")
    print(f"  Pages: {len(dashboard.children)}")
    print(f"  Dashboard ID: {dashboard.id}")

    # Serialize to JSON for inspection
    dashboard_json = dashboard.model_dump_json(indent=2)
    print(f"\nDashboard JSON structure preview (first 500 chars):")
    print(dashboard_json[:500] + "...")

    print("\n" + "="*60)
    print("SUCCESS! Dashboard structure created with new Pydantic system.")
    print("="*60)
    print(f"\nDashboard '{dashboard.title}' is ready!")
    print(f"\nNew features demonstrated:")
    print(f"- ✓ Fluent builder API with L (LayoutBuilder)")
    print(f"- ✓ Type-safe enums (WidgetType, SelectorType, ColumnWidth)")
    print(f"- ✓ Component binding via aliases and params")
    print(f"- ✓ Pydantic validation and JSON serialization")

    # Note: Registration with backend would need to be updated
    # to work with the new schema structure
    print("\nNote: Backend integration for .register() needs updating")
    print("to work with new DashboardStructure schema.")


if __name__ == "__main__":
    main()
