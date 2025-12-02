"""
Component classes for data loading and rendering.

Components are the primary way to define data pipelines:
- Component: Base class with load() and transform() for data-only components
- RenderableComponent: Extends Component with render() for server-side visualization
- @component: Decorator to convert a function into a DataSourceComponent
"""

import inspect
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, cast, get_type_hints

from pydantic import BaseModel, ConfigDict, Field


class Component(BaseModel, ABC):
    """
    Base class for data-only components.

    Components define a data pipeline with:
    - load(): Fetch data from databases, APIs, files, etc.
    - transform(): Process/reshape data for consumption

    Use Component when the frontend will handle rendering (frontend-native widgets).
    For server-side rendering, use RenderableComponent instead.

    Example:
        class SalesLoader(Component):
            region: str
            start_date: str

            def load(self):
                return db.query(f"SELECT * FROM sales WHERE region = '{self.region}'")

            def transform(self, data):
                return aggregate_by_month(data)

        # Use with frontend-native widget
        LineChartWidget(
            data_source=ComponentSource(component=SalesLoader),
            params={"region": "North", "start_date": "2024-01-01"},
            x="month",
            y="revenue"
        )
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,  # Allow non-Pydantic types in methods
        extra='forbid',  # Prevent extra fields
    )

    @abstractmethod
    def load(self) -> Any:
        """
        Load/fetch data from a source.

        This method should:
        - Fetch data from databases, APIs, files, etc.
        - Access parameters via self.param_name
        - Return raw data in any format (dict, DataFrame, list, etc.)
        - Be stateless and repeatable

        Returns:
            Raw data in any format
        """
        pass

    @abstractmethod
    def transform(self, data: Any) -> Any:
        """
        Transform/process the loaded data.

        This method should:
        - Clean, filter, aggregate, or reshape data
        - Prepare data for visualization
        - Return processed data

        Args:
            data: Output from load() method

        Returns:
            Processed data ready for rendering
        """
        pass

    @classmethod
    def get_source_code(cls) -> str:
        """Get the source code of this component class."""
        return inspect.getsource(cls)

    @classmethod
    def get_class_name(cls) -> str:
        """Get the name of this component class."""
        return cls.__name__

    @classmethod
    def get_parameters(cls) -> Dict[str, Any]:
        """
        Extract parameters from the Pydantic model fields.

        Returns:
            Dict mapping parameter names to their type annotations and metadata
        """
        params = {}

        # Get fields from Pydantic model
        for field_name, field_info in cls.model_fields.items():
            param_info = {
                "name": field_name,
                "required": field_info.is_required(),
            }

            # Get type annotation
            type_str = str(field_info.annotation)
            # Clean up the type string
            type_str = type_str.replace("<class '", "").replace("'>", "")
            type_str = type_str.replace("typing.", "")
            param_info["type"] = type_str

            # Get default value if present
            if not field_info.is_required():
                # Pydantic stores defaults in field_info.default
                if field_info.default is not None:
                    param_info["default"] = field_info.default
                elif field_info.default_factory is not None:
                    param_info["default_factory"] = True

            params[field_name] = param_info

        return params


class RenderableComponent(Component, ABC):
    """
    Component with server-side rendering capability.

    Extends Component with a render() method that produces visualization output
    (typically Plotly JSON). Use with PlotlyWidget for full server-side control.

    Example:
        class SalesChart(RenderableComponent):
            region: str

            def load(self):
                return db.query(f"SELECT * FROM sales WHERE region = '{self.region}'")

            def transform(self, data):
                return aggregate_by_product(data)

            def render(self, data):
                import plotly.express as px
                return px.bar(data, x="product", y="sales")

        # Use with PlotlyWidget
        PlotlyWidget(
            data_source=ComponentSource(component=SalesChart),
            params={"region": region_input}
        )
    """

    @abstractmethod
    def render(self, data: Any) -> Any:
        """
        Render the final visualization.

        This method should return one of:
        - Plotly Figure (recommended): px.bar(...) or go.Figure(...)
        - Altair Chart: alt.Chart(...).mark_bar()
        - Vega-Lite spec: {"mark": "bar", ...}
        - Custom dict: {"type": "custom", "data": ...}

        Args:
            data: Output from transform() method

        Returns:
            Visualization object or spec
        """
        pass


class DataSourceComponent(Component):
    """
    Simplified component for data sources.

    Only requires implementing load() method.
    Transform is a pass-through by default.

    Useful for simple data fetching without transformation logic.

    Example:
        class AvailableDates(DataSourceComponent):
            def load(self):
                return ["2024-01-01", "2024-01-02", "2024-01-03"]

        # Or with parameters:
        class RegionOptions(DataSourceComponent):
            country: str

            def load(self):
                return fetch_regions(self.country)
    """

    def transform(self, data: Any) -> Any:
        """Pass-through transform."""
        return data


def component(func: Callable[..., Any]) -> type["DataSourceComponent"]:
    """
    Decorator to convert a function into a DataSourceComponent class.

    The function's parameters become fields on the generated component class,
    and the function body becomes the load() method.

    Args:
        func: Function to wrap as a component

    Returns:
        A DataSourceComponent subclass

    Examples:
        # Simple function with no parameters
        @component
        def get_available_dates():
            return ["2024-01-01", "2024-01-02", "2024-01-03"]

        # Function with parameters
        @component
        def get_regions(country: str):
            return fetch_regions(country)

        # Function with default parameters
        @component
        def get_products(category: str = "all", limit: int = 100):
            return fetch_products(category, limit)

        # Use with ComponentSource
        Select(
            name="region",
            source=ComponentSource(component=get_regions),
            params={"country": country_input}
        )
    """
    # Get function signature
    sig = inspect.signature(func)
    func_name = func.__name__
    func_module = getattr(func, '__module__', __name__)

    # Try to get type hints, fall back to Any for untyped params
    try:
        hints = get_type_hints(func)
    except Exception:  # noqa: BLE001
        hints = {}

    # Build field definitions for Pydantic model
    annotations: Dict[str, Any] = {}
    field_defaults: Dict[str, Any] = {}

    for name, param in sig.parameters.items():
        # Get type annotation (default to Any)
        param_type = hints.get(name, Any)
        annotations[name] = param_type

        # Handle default values
        if param.default is not inspect.Parameter.empty:
            field_defaults[name] = param.default
        # If no default, field is required (Pydantic handles this automatically)

    # Capture func and sig in closure for load_method
    _func = func
    _param_names = list(sig.parameters.keys())

    # Create the load method that calls the original function with self's fields
    def load_method(self: "DataSourceComponent") -> Any:
        # Build kwargs from instance fields
        kwargs = {p: getattr(self, p) for p in _param_names}
        return _func(**kwargs)

    # Build class dict
    class_dict: Dict[str, Any] = {
        '__module__': func_module,
        '__component_name__': func_name,
        '__doc__': func.__doc__,
        '_source_func': func,  # Keep reference to original function
        '__annotations__': annotations,
        'load': load_method,
    }

    # Add field defaults
    for field_name, default_value in field_defaults.items():
        class_dict[field_name] = default_value

    # Create the class dynamically
    component_class = cast(
        type[DataSourceComponent],
        type(func_name, (DataSourceComponent,), class_dict)
    )

    # Rebuild the model to pick up annotations properly
    component_class.model_rebuild()

    return component_class
