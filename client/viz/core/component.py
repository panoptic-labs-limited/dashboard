"""Base Component class for creating dashboard components."""

from abc import ABC, ABCMeta, abstractmethod
from dataclasses import dataclass, fields as get_dataclass_fields, MISSING
from typing import Any, Dict, Optional
import inspect


class ComponentMeta(ABCMeta):
    """
    Metaclass that automatically applies @dataclass to Component subclasses.

    This allows users to define components with clean field annotations
    without needing to explicitly use @dataclass decorator.
    """
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        # Auto-apply dataclass if the class has field annotations
        # (but not for the base Component class itself)
        if '__annotations__' in namespace and namespace['__annotations__'] and name != 'Component':
            # Apply dataclass with kw_only to make all params keyword-only
            cls = dataclass(kw_only=True)(cls)

        return cls


class Component(ABC, metaclass=ComponentMeta):
    """
    Base class for all dashboard components.

    Users extend this class, define parameters as class fields,
    and implement three methods:
    - load(): Fetch/load data from a source
    - transform(): Process/transform the loaded data
    - render(): Create visualization from transformed data

    The metaclass automatically converts subclasses to dataclasses,
    so you don't need to use @dataclass decorator.

    Example:
        class SalesChart(Component):
            # Parameters as class fields (automatically become constructor params)
            start_date: str
            region: str

            def load(self):
                return db.query(f"SELECT * FROM sales WHERE date >= '{self.start_date}' AND region = '{self.region}'")

            def transform(self, data):
                return aggregate_by_product(data)

            def render(self, data):
                import plotly.express as px
                return px.bar(data, x="product", y="sales")

        # Usage:
        chart = SalesChart(start_date="2024-01-01", region="North")
    """

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
        Extract parameters from the dataclass fields.

        Returns:
            Dict mapping parameter names to their type annotations
        """
        params = {}

        # If this is a dataclass, get fields from it
        if hasattr(cls, '__dataclass_fields__'):
            for field_name, field_obj in cls.__dataclass_fields__.items():
                param_info = {
                    "name": field_name,
                    "required": field_obj.default == MISSING and field_obj.default_factory == MISSING,
                }

                # Get type annotation
                type_str = str(field_obj.type)
                # Clean up the type string
                type_str = type_str.replace("<class '", "").replace("'>", "")
                type_str = type_str.replace("typing.", "")
                param_info["type"] = type_str

                # Get default value
                if field_obj.default != MISSING:
                    param_info["default"] = field_obj.default
                elif field_obj.default_factory != MISSING:
                    param_info["default_factory"] = True

                params[field_name] = param_info
        else:
            # Fallback: extract from class annotations
            annotations = getattr(cls, '__annotations__', {})
            for param_name, param_type in annotations.items():
                type_str = str(param_type)
                type_str = type_str.replace("<class '", "").replace("'>", "")
                type_str = type_str.replace("typing.", "")

                params[param_name] = {
                    "name": param_name,
                    "type": type_str,
                    "required": True,
                }

        return params


class DataSourceComponent(Component):
    """
    Simplified component for selector data sources.

    Only requires implementing load() method.
    Transform and render are no-ops (pass-through).

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

    def render(self, data: Any) -> Any:
        """Pass-through render."""
        return data
