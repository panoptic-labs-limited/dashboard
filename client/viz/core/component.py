"""Base Component class for creating dashboard components."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import inspect


class Component(ABC):
    """
    Base class for all dashboard components.

    Users extend this class and implement three methods:
    - load(): Fetch/load data from a source
    - transform(): Process/transform the loaded data
    - render(): Create visualization from transformed data

    Example:
        class SalesChart(Component):
            def load(self, start_date: str, region: str):
                return db.query("SELECT * FROM sales WHERE ...")

            def transform(self, data):
                return aggregate_by_product(data)

            def render(self, data):
                import plotly.express as px
                return px.bar(data, x="product", y="sales")
    """

    @abstractmethod
    def load(self, **params) -> Any:
        """
        Load/fetch data from a source.

        This method should:
        - Fetch data from databases, APIs, files, etc.
        - Return raw data in any format (dict, DataFrame, list, etc.)
        - Be stateless and repeatable

        Args:
            **params: Parameters passed from selectors or dashboard config

        Returns:
            Raw data in any format
        """
        pass

    @abstractmethod
    def transform(self, data: Any, **params) -> Any:
        """
        Transform/process the loaded data.

        This method should:
        - Clean, filter, aggregate, or reshape data
        - Prepare data for visualization
        - Return processed data

        Args:
            data: Output from load() method
            **params: Parameters passed from selectors or dashboard config

        Returns:
            Processed data ready for rendering
        """
        pass

    @abstractmethod
    def render(self, data: Any, **params) -> Any:
        """
        Render the final visualization.

        This method should return one of:
        - Plotly Figure (recommended): px.bar(...) or go.Figure(...)
        - Altair Chart: alt.Chart(...).mark_bar()
        - Vega-Lite spec: {"mark": "bar", ...}
        - Custom dict: {"type": "custom", "data": ...}

        Args:
            data: Output from transform() method
            **params: Parameters passed from selectors or dashboard config

        Returns:
            Visualization object or spec
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
        Extract parameters from the load() method signature.

        Returns:
            Dict mapping parameter names to their type annotations
        """
        load_signature = inspect.signature(cls.load)
        params = {}

        for param_name, param in load_signature.parameters.items():
            if param_name in ['self', 'cls']:
                continue

            param_info = {
                "name": param_name,
                "required": param.default == inspect.Parameter.empty,
            }

            # Get type annotation
            if param.annotation != inspect.Parameter.empty:
                # Convert type to string
                type_str = str(param.annotation)
                # Clean up the type string
                type_str = type_str.replace("<class '", "").replace("'>", "")
                type_str = type_str.replace("typing.", "")
                param_info["type"] = type_str
            else:
                param_info["type"] = "Any"

            # Get default value
            if param.default != inspect.Parameter.empty:
                param_info["default"] = param.default

            params[param_name] = param_info

        return params


class DataSourceComponent(Component):
    """
    Simplified component for selector data sources.

    Only requires implementing load() method.
    Transform and render are no-ops.

    Example:
        class AvailableDates(DataSourceComponent):
            def load(self):
                return ["2024-01-01", "2024-01-02", "2024-01-03"]
    """

    def transform(self, data: Any, **params) -> Any:
        """Pass-through transform."""
        return data

    def render(self, data: Any, **params) -> Any:
        """Pass-through render."""
        return data
