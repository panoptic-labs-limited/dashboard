"""Base Component class for creating dashboard components."""

import inspect
from abc import ABC, abstractmethod
from typing import Any, Dict

from pydantic import BaseModel, ConfigDict


class Component(BaseModel, ABC):
    """
    Base class for all dashboard components using Pydantic.

    Users extend this class, define parameters as Pydantic fields,
    and implement three methods:
    - load(): Fetch/load data from a source
    - transform(): Process/transform the loaded data
    - render(): Create visualization from transformed data

    Pydantic provides automatic validation, serialization, and type checking
    for component parameters.

    Example:
        class SalesChart(Component):
            # Parameters as Pydantic fields (automatically validated)
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
