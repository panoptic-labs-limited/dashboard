"""Component registration utilities."""

from typing import Type, Optional

from viz.api.client import RegistryClient
from viz.core.component import Component
from viz_shared import ComponentMetadata, ComponentParameter


def register_component(
    component_class: Type[Component],
    alias: str,
    client: RegistryClient,
    description: Optional[str] = None,
    metadata: Optional[ComponentMetadata] = None,
    memory_limit_mb: int = 200,
    timeout_seconds: int = 30
):
    """
    Register a component class with the function registry.

    Args:
        component_class: The Component subclass to register
        alias: Unique identifier for this component
        client: RegistryClient instance
        description: Optional description
        metadata: Optional metadata (author, version, tags)
        memory_limit_mb: Memory limit for execution (default: 200MB)
        timeout_seconds: Timeout for execution (default: 30s)

    Returns:
        ComponentResponse from the registry

    Example:
        from viz import Component, RegistryClient, register_component

        class SalesChart(Component):
            def load(self, date: str):
                return fetch_sales(date)

            def transform(self, data):
                return process(data)

            def render(self, data):
                import plotly.express as px
                return px.bar(data, x="product", y="sales")

        client = RegistryClient(username="user", password="pass")
        register_component(SalesChart, "sales_chart", client)
    """
    # Get source code
    source_code = component_class.get_source_code()

    # Get class name
    class_name = component_class.get_class_name()

    # Extract parameters
    params_dict = component_class.get_parameters()
    parameters = [
        ComponentParameter(
            name=name,
            type=info["type"],
            required=info["required"],
            default=info.get("default"),
            description=None
        )
        for name, info in params_dict.items()
    ]

    # Register with the registry
    result = client.create_component(
        alias=alias,
        class_name=class_name,
        source_code=source_code,
        description=description or component_class.__doc__,
        parameters=parameters,
        metadata=metadata,
        memory_limit_mb=memory_limit_mb,
        timeout_seconds=timeout_seconds
    )

    # Store the registry alias on the class for later reference
    component_class._registry_alias = alias

    return result


def auto_register_components(
    components: dict,
    client: RegistryClient,
    **kwargs
):
    """
    Register multiple components at once.

    Args:
        components: Dict mapping alias → Component class
        client: RegistryClient instance
        **kwargs: Additional arguments passed to register_component

    Returns:
        Dict mapping alias → ComponentResponse

    Example:
        components = {
            "sales_chart": SalesChart,
            "revenue_chart": RevenueChart,
            "user_stats": UserStats,
        }

        client = RegistryClient(username="user", password="pass")
        results = auto_register_components(components, client)
    """
    results = {}
    for alias, component_class in components.items():
        try:
            result = register_component(
                component_class,
                alias,
                client,
                **kwargs
            )
            results[alias] = result
            print(f"✓ Registered: {alias}")
        except Exception as e:
            print(f"✗ Failed to register {alias}: {e}")
            results[alias] = None

    return results
