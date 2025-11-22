"""Base classes for inputs."""

from __future__ import annotations
from typing import Any, Optional, TypeVar, Generic, Type, ClassVar, Union
from pydantic import BaseModel, Field, model_validator
import uuid

from .sources import FunctionSource
class Option(BaseModel):
    """
    Represents a selectable option.

    Can be constructed from:
    - Simple value: "north"
    - Dict: {"value": "north", "label": "North Region"}
    - Dict with selected: {"value": "north", "label": "North", "selected": True}
    - Explicit: Option(value="north", label="North Region")

    Future fields: disabled, icon, group for advanced UI features.
    """

    value: Any = Field(..., description="The actual option value")
    label: str = Field(..., description="Display label for the option")
    selected: bool = Field(False, description="Pre-selected state")
    disabled: bool = Field(False, description="Disabled state")
    icon: Optional[str] = Field(None, description="Optional icon identifier")
    group: Optional[str] = Field(None, description="Group name for grouped options")

    @model_validator(mode='before')
    @classmethod
    def normalize_input(cls, data):
        """
        Normalize various input formats to dict.

        Handles:
        - dict with value/label
        - simple value → {value: x, label: str(x)}
        """
        if isinstance(data, dict):
            # If label not provided, use value as label
            if 'label' not in data and 'value' in data:
                data['label'] = str(data['value'])
            return data

        # Simple value - use as both value and label
        return {'value': data, 'label': str(data)}


# Generic type variable for config models
TConfig = TypeVar('TConfig', bound=BaseModel)


class BaseInput(BaseModel, Generic[TConfig]):
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
    """

    model_config = {
        'extra': 'forbid',
        'validate_assignment': True,
    }

    # Config class reference (set by subclasses)
    __config_class__: ClassVar[Type[BaseModel]]

    # Core fields
    name: str = Field(..., description="Parameter name (used in component bindings)")
    label: Optional[str] = Field(None, description="Display label")

    # Optional fields
    id: str = Field(default_factory=lambda: f"input_{uuid.uuid4().hex[:8]}")
    required: bool = Field(True, description="Whether input is required")
    disabled: bool = Field(False, description="Whether input is disabled")
    help_text: Optional[str] = Field(None, description="Help text or tooltip")
    placeholder: Optional[str] = Field(None, description="Placeholder text")

    # Source for dynamic configuration
    # When None, use top-level fields (static configuration)
    # When FunctionSource, execute function for dynamic configuration
    source: Optional[FunctionSource[TConfig]] = Field(
        None,
        description="Optional FunctionSource for dynamic configuration"
    )

    @model_validator(mode='after')
    def auto_generate_label(self):
        """Auto-generate label from name if not provided."""
        if self.label is None:
            self.label = self.name.replace('_', ' ').title()
        return self

    def to_dict(self) -> dict:
        """Serialize to dictionary for API/dashboard structure."""
        return self.model_dump(exclude_none=True)
