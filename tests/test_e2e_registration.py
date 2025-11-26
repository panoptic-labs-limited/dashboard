"""
End-to-end tests for dashboard registration and rendering.

Tests the complete flow:
1. Register functions
2. Register components
3. Register dashboard
4. Render widgets
5. Execute input data sources
"""

import sys
import pytest
from pathlib import Path

# Add client to path
sys.path.insert(0, str(Path(__file__).parent.parent / "client"))

from viz import Component, L, Dashboard, Select, Slider, MultiSelect, Toggle
from viz.layout import WidgetType
from viz.api.registry import RegistryClient
import plotly.express as px
import pandas as pd


# ==============================================================================
# Test Data Sources
# ==============================================================================

def get_test_regions():
    """Test data source function."""
    return [
        {"value": "north", "label": "North"},
        {"value": "south", "label": "South"},
        {"value": "east", "label": "East"},
        {"value": "west", "label": "West"}
    ]


def get_test_products():
    """Test data source for products."""
    return [
        {"value": "widget", "label": "Widget"},
        {"value": "gadget", "label": "Gadget"},
        {"value": "doohickey", "label": "Doohickey"}
    ]


# ==============================================================================
# Test Components
# ==============================================================================

class TestSalesChart(Component):
    """Test component for sales visualization."""
    __id__ = "test_sales_chart"

    region: str
    product: str = "widget"

    def load(self):
        """Load test sales data."""
        return pd.DataFrame({
            'product': ['Widget', 'Gadget', 'Doohickey'],
            'sales': [100, 150, 75],
            'region': [self.region] * 3
        })

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Filter by product."""
        if self.product != "all":
            data = data[data['product'].str.lower() == self.product]
        return data

    def render(self, data: pd.DataFrame):
        """Create bar chart."""
        fig = px.bar(data, x='product', y='sales', title=f"Sales in {self.region}")
        return fig


class TestMetricsCard(Component):
    """Test component for metrics display."""
    __id__ = "test_metrics_card"

    region: str
    show_change: bool = False

    def load(self):
        """Load test metrics."""
        return {
            'north': {'revenue': 10000, 'change': 15},
            'south': {'revenue': 8500, 'change': -5},
            'east': {'revenue': 12000, 'change': 20},
            'west': {'revenue': 9500, 'change': 10}
        }

    def transform(self, data: dict) -> dict:
        """Extract region data."""
        return data.get(self.region, {'revenue': 0, 'change': 0})

    def render(self, data: dict):
        """Create metrics display."""
        result = {
            'type': 'metric',
            'value': data['revenue'],
            'label': 'Revenue'
        }
        if self.show_change:
            result['change'] = data['change']
        return result


# ==============================================================================
# Test Fixtures
# ==============================================================================

@pytest.fixture
def registry_client():
    """Create a registry client for testing."""
    # Use test credentials
    client = RegistryClient(
        base_url="http://localhost:8000",
        username="testuser",
        password="testpassword123"
    )
    return client


@pytest.fixture
def test_dashboard():
    """Create a test dashboard."""
    dashboard = Dashboard(
        id="test_dashboard",
        title="Test Dashboard"
    )

    with dashboard.page(id="test_page", title="Test Page"):
        with L.section(title="Controls"):
            with L.row():
                with L.column(weight=1):
                    L.input(Select(
                        name="region",
                        label="Region",
                        options=get_test_regions(),
                        default="north"
                    ))

                    L.input(MultiSelect(
                        name="products",
                        label="Products",
                        options=get_test_products(),
                        default=["widget"],
                        max_selections=3
                    ))

                with L.column(weight=1):
                    L.input(Slider(
                        name="threshold",
                        label="Threshold",
                        min_value=0,
                        max_value=100,
                        default=50,
                        show_value=True
                    ))

                    L.input(Toggle(
                        name="show_change",
                        label="Show Change",
                        default=False
                    ))

        with L.section(title="Visualizations"):
            with L.row():
                with L.column(weight=2):
                    L.widget(
                        widget_type=WidgetType.CHART,
                        title="Sales Chart",
                        component_alias="test_sales_chart",
                        params={
                            "region": "region",
                            "product": "products"
                        }
                    )

                with L.column(weight=1):
                    L.widget(
                        widget_type=WidgetType.METRIC,
                        title="Metrics",
                        component_alias="test_metrics_card",
                        params={
                            "region": "region",
                            "show_change": "show_change"
                        }
                    )

    return dashboard


# ==============================================================================
# Tests
# ==============================================================================

@pytest.mark.asyncio
async def test_e2e_registration_flow(registry_client, test_dashboard):
    """Test the complete registration flow."""

    print("\n" + "=" * 60)
    print("Starting E2E Registration Test")
    print("=" * 60)

    # Step 1: Manually register components
    print("\n1. Registering components...")
    try:
        # We need to manually create component schemas since serialize_component
        # expects an instance, but we have classes
        import inspect

        # Register TestSalesChart
        component_schema = {
            "alias": "test_sales_chart",
            "class_name": TestSalesChart.__name__,
            "source_code": inspect.getsource(TestSalesChart),
            "description": TestSalesChart.__doc__.strip() if TestSalesChart.__doc__ else None,
            "parameters": [
                {"name": "region", "type": "str", "required": True},
                {"name": "product", "type": "str", "required": False, "default": "widget"}
            ],
            "metadata": {"name": "TestSalesChart", "version": "1.0.0", "tags": ["test"]},
            "memory_limit_mb": 200,
            "timeout_seconds": 30
        }
        response = registry_client.client.post(
            f"{registry_client.base_url}/components/",
            headers=registry_client._get_headers(),
            json=component_schema
        )
        response.raise_for_status()
        print(f"   ✓ Registered component: test_sales_chart")

        # Register TestMetricsCard
        component_schema = {
            "alias": "test_metrics_card",
            "class_name": TestMetricsCard.__name__,
            "source_code": inspect.getsource(TestMetricsCard),
            "description": TestMetricsCard.__doc__.strip() if TestMetricsCard.__doc__ else None,
            "parameters": [
                {"name": "region", "type": "str", "required": True},
                {"name": "show_change", "type": "bool", "required": False, "default": False}
            ],
            "metadata": {"name": "TestMetricsCard", "version": "1.0.0", "tags": ["test"]},
            "memory_limit_mb": 200,
            "timeout_seconds": 30
        }
        response = registry_client.client.post(
            f"{registry_client.base_url}/components/",
            headers=registry_client._get_headers(),
            json=component_schema
        )
        response.raise_for_status()
        print(f"   ✓ Registered component: test_metrics_card")

    except Exception as e:
        print(f"   ✗ Component registration failed: {e}")
        raise

    # Step 2: Register dashboard with functions
    print("\n2. Registering dashboard with functions...")
    try:
        result = registry_client.register_dashboard_full(test_dashboard)

        print(f"   ✓ Registered {len(result['functions'])} functions")
        print(f"   ✓ Registered dashboard: {result['dashboard']['id']}")

        assert 'dashboard' in result
        assert result['dashboard']['id'] == 'test_dashboard'
        assert len(result['functions']) == 2  # get_test_regions, get_test_products

    except Exception as e:
        print(f"   ✗ Registration failed: {e}")
        raise

    print("\n✓ Registration flow completed successfully")


@pytest.mark.asyncio
async def test_e2e_dashboard_retrieval(registry_client):
    """Test retrieving a registered dashboard."""

    print("\n" + "=" * 60)
    print("Testing Dashboard Retrieval")
    print("=" * 60)

    # Retrieve dashboard
    print("\n1. Fetching dashboard...")
    try:
        response = registry_client.client.get(
            f"{registry_client.base_url}/dashboards/test_dashboard",
            headers=registry_client._get_headers()
        )
        response.raise_for_status()
        dashboard = response.json()

        print(f"   ✓ Retrieved dashboard: {dashboard['id']}")
        print(f"   ✓ Title: {dashboard['title']}")
        print(f"   ✓ Pages: {len(dashboard['children'])}")

        assert dashboard['id'] == 'test_dashboard'
        assert dashboard['title'] == 'Test Dashboard'
        assert len(dashboard['children']) > 0

    except Exception as e:
        print(f"   ✗ Retrieval failed: {e}")
        raise

    print("\n✓ Dashboard retrieval completed successfully")


@pytest.mark.asyncio
async def test_e2e_component_execution(registry_client):
    """Test executing registered components."""

    print("\n" + "=" * 60)
    print("Testing Component Execution")
    print("=" * 60)

    # Test TestSalesChart component
    print("\n1. Executing TestSalesChart component...")
    try:
        response = registry_client.client.post(
            f"{registry_client.base_url}/execute/component/test_sales_chart",
            headers=registry_client._get_headers(),
            json={
                "stage": "load_transform_render",
                "params": {
                    "region": "north",
                    "product": "widget"
                }
            }
        )
        response.raise_for_status()
        result = response.json()

        print(f"   ✓ Status: {result['status']}")
        print(f"   ✓ Execution time: {result['execution_time_ms']}ms")
        print(f"   ✓ Output type: {result['output']['type']}")

        assert result['status'] == 'success'
        assert result['output']['type'] == 'plotly'

    except Exception as e:
        print(f"   ✗ Execution failed: {e}")
        raise

    # Test TestMetricsCard component
    print("\n2. Executing TestMetricsCard component...")
    try:
        response = registry_client.client.post(
            f"{registry_client.base_url}/execute/component/test_metrics_card",
            headers=registry_client._get_headers(),
            json={
                "stage": "load_transform_render",
                "params": {
                    "region": "south",
                    "show_change": True
                }
            }
        )
        response.raise_for_status()
        result = response.json()

        print(f"   ✓ Status: {result['status']}")
        print(f"   ✓ Execution time: {result['execution_time_ms']}ms")
        print(f"   ✓ Output: {result['output']}")

        assert result['status'] == 'success'
        assert 'type' in result['output']

    except Exception as e:
        print(f"   ✗ Execution failed: {e}")
        raise

    print("\n✓ Component execution completed successfully")


@pytest.mark.asyncio
async def test_e2e_function_execution(registry_client):
    """Test executing registered functions (data sources)."""

    print("\n" + "=" * 60)
    print("Testing Function Execution")
    print("=" * 60)

    # Execute get_test_regions function
    print("\n1. Executing get_test_regions function...")
    try:
        response = registry_client.client.post(
            f"{registry_client.base_url}/execute/function/get_test_regions",
            headers=registry_client._get_headers(),
            json={"params": {}}
        )
        response.raise_for_status()
        result = response.json()

        print(f"   ✓ Status: {result['status']}")
        print(f"   ✓ Execution time: {result['execution_time_ms']}ms")
        print(f"   ✓ Result: {result['output']['result']}")

        assert result['status'] == 'success'
        assert isinstance(result['output']['result'], list)
        assert len(result['output']['result']) == 4

    except Exception as e:
        print(f"   ✗ Execution failed: {e}")
        raise

    print("\n✓ Function execution completed successfully")


@pytest.mark.asyncio
async def test_e2e_dashboard_rendering(registry_client):
    """Test rendering entire dashboard."""

    print("\n" + "=" * 60)
    print("Testing Dashboard Rendering")
    print("=" * 60)

    print("\n1. Rendering dashboard with input values...")
    try:
        response = registry_client.client.post(
            f"{registry_client.base_url}/dashboards/test_dashboard/render",
            headers=registry_client._get_headers(),
            json={
                "input_values": {
                    "region": "north",
                    "products": ["widget"],
                    "threshold": 75,
                    "show_change": True
                }
            }
        )
        response.raise_for_status()
        result = response.json()

        print(f"   ✓ Dashboard: {result['dashboard_id']}")
        print(f"   ✓ Widgets rendered: {len(result['widgets'])}")
        print(f"   ✓ Total execution time: {result['total_execution_time_ms']}ms")

        # Check each widget
        for widget in result['widgets']:
            print(f"   ✓ Widget '{widget['widget_id']}': {widget['status']}")
            assert widget['status'] == 'success'

        assert result['dashboard_id'] == 'test_dashboard'
        assert len(result['widgets']) == 2  # Chart and Metrics

    except Exception as e:
        print(f"   ✗ Rendering failed: {e}")
        raise

    print("\n✓ Dashboard rendering completed successfully")


if __name__ == "__main__":
    """Run tests with pytest."""
    pytest.main([__file__, "-v", "-s"])
