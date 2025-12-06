"""Base classes for inputs."""

from __future__ import annotations

import uuid
from typing import TypeVar, Generic

from pydantic import BaseModel, Field, model_validator

from viz.core.datasource import DataSource
from viz.core.layout import ParameterizedNode
from viz.core.reference import Referenceable

# Generic type variable for config models
TConfig = TypeVar('TConfig', bound=BaseModel)


class BaseInput(Referenceable, ParameterizedNode, Generic[TConfig]):
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

    Extends ParameterizedNode for params support and Referenceable for ref serialization.
    """

    # Override id to have input-specific prefix
    id: str = Field(default_factory=lambda: f"input_{uuid.uuid4().hex[:8]}")

    # Subclasses override with Literal type (e.g., type: Literal["select"] = "select")
    type: str = Field("input", description="Discriminator for union types")

    # Core fields
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
        """Auto-generate label from id if not provided."""
        if self.label is None:
            # Extract the meaningful part of id (remove prefix like 'input_')
            label_source = self.id
            if '_' in label_source:
                # Skip auto-generated UUIDs (input_abc123) but use semantic ids (region_select)
                parts = label_source.split('_')
                if len(parts) == 2 and len(parts[1]) == 8:
                    # Looks like auto-generated (prefix_uuid), don't auto-label
                    pass
                else:
                    # Semantic id like "region_select" -> "Region Select"
                    self.label = label_source.replace('_', ' ').title()
        return self

    def to_dict(self) -> dict:
        """Serialize to dictionary for API/dashboard structure."""
        return self.model_dump(exclude_none=True)
