"""Base classes for inputs."""

from __future__ import annotations

from typing import TypeVar, Generic

from pydantic import BaseModel, Field, model_validator

from viz.core.datasource import DataSource
from viz.core.layout import ParameterizedNode
from viz.core.reference import NamedReference

# Generic type variable for config models
TConfig = TypeVar('TConfig', bound=BaseModel)


class Input(NamedReference, ParameterizedNode, Generic[TConfig]):
    """
    Base class for all input types.

    Generic over TConfig - the configuration model for this input type.
    Each input type has a corresponding config model (e.g., SelectConfig, DateConfig).

    Configuration can be provided via:
    1. Top-level fields (static) - fields like options, default, min_value, etc.
    2. source + params (dynamic) - DataSource for server-side data fetching

    The source/params pattern mirrors widgets:
    - source: WHERE to get data (TimeseriesSource, ComponentSource)
    - params: HOW to query the source (can reference other Inputs for cascading)

    Subclasses must:
    - Set type as a Literal for the specific input type (e.g., type: Literal["select"] = "select")
    - Declare config fields as top-level properties

    Extends ParameterizedNode for params support and NamedReference for ref serialization.
    """

    model_config = {
        'extra': 'forbid',
        'validate_assignment': True,
    }

    # Subclasses override with Literal type (e.g., type: Literal["select"] = "select")
    type: str = Field("input", description="Discriminator for union types")

    # Core fields (name is inherited from NamedReference)
    label: str | None = Field(None, description="Display label")

    # Optional fields
    required: bool = Field(True, description="Whether input is required")
    disabled: bool = Field(False, description="Whether input is disabled")
    help_text: str | None = Field(None, description="Help text or tooltip")
    placeholder: str | None = Field(None, description="Placeholder text")

    # Dynamic data source (optional)
    # When None, use top-level fields (static configuration)
    # When set, execute source with params for dynamic configuration
    source: DataSource | None = Field(
        None,
        description="Optional DataSource for dynamic options/configuration"
    )
    # params is inherited from ParameterizedNode

    @model_validator(mode='after')
    def auto_generate_label(self):
        """Auto-generate label from name if not provided."""
        if self.label is None:
            self.label = self.name.replace('_', ' ').title()
        return self

    def to_dict(self) -> dict:
        """Serialize to dictionary for API/dashboard structure."""
        return self.model_dump(exclude_none=True)
