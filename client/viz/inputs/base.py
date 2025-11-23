"""Base classes for inputs."""

from __future__ import annotations

import uuid
from typing import Optional, TypeVar, Generic, Type, ClassVar

from pydantic import BaseModel, Field, model_validator

from viz.core.layout import LayoutNode
from .sources import FunctionSource

# Generic type variable for config models
TConfig = TypeVar('TConfig', bound=BaseModel)


class Input(LayoutNode, Generic[TConfig]):
    """
    Base class for all input types.

    Generic over TConfig - the configuration model for this input type.
    Each input type has a corresponding config model (e.g., SelectConfig, DateConfig).

    Configuration can be provided via:
    1. Top-level fields (static) - fields like options, default, min_value, etc.
    2. source field (dynamic) - FunctionSource for server-side execution

    Subclasses must:
    - Set __config_class__ to their config model type
    - Declare config fields as top-level properties (for type hints)
    - Set input_type as a Literal for the specific input type

    Extends LayoutNode to integrate inputs directly into the layout tree.
    """

    model_config = {
        'extra': 'forbid',
        'validate_assignment': True,
    }

    # Config class reference (set by subclasses)
    __config_class__: ClassVar[Type[BaseModel]]

    # Override LayoutNode's 'type' field to make it optional with a default
    # Subclasses set input_type which gets synced to type
    type: str = Field("input", description="Discriminator for union types")

    # We override the id default to use "input_" prefix
    id: str = Field(default_factory=lambda: f"input_{uuid.uuid4().hex[:8]}")

    # Core fields
    name: str = Field(..., description="Parameter name (used in component bindings)")
    label: str | None = Field(None, description="Display label")

    # Optional fields
    required: bool = Field(True, description="Whether input is required")
    disabled: bool = Field(False, description="Whether input is disabled")
    help_text: str | None = Field(None, description="Help text or tooltip")
    placeholder: str | None = Field(None, description="Placeholder text")

    # Source for dynamic configuration
    # When None, use top-level fields (static configuration)
    # When FunctionSource, execute function for dynamic configuration
    source: FunctionSource[TConfig | None] = Field(
        None,
        description="Optional FunctionSource for dynamic configuration"
    )

    @model_validator(mode='after')
    def auto_generate_label(self):
        """Auto-generate label from name if not provided."""
        if self.label is None:
            self.label = self.name.replace('_', ' ').title()
        return self

    @model_validator(mode='after')
    def sync_type_field(self):
        """Sync input_type to type field for LayoutNode discriminator."""
        if hasattr(self, 'input_type'):
            # Use object.__setattr__ to bypass validation and avoid recursion
            object.__setattr__(self, 'type', self.input_type)
        return self

    def to_dict(self) -> dict:
        """Serialize to dictionary for API/dashboard structure."""
        return self.model_dump(exclude_none=True)
