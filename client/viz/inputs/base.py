"""Base classes for inputs."""

from __future__ import annotations
from typing import Any, Optional, Union, List, Callable
from pydantic import BaseModel, Field, field_validator, model_validator
import uuid


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


class BaseInput(BaseModel):
    """
    Base class for all input types.

    Provides common fields and behavior for all inputs.
    """

    model_config = {
        'extra': 'forbid',
        'validate_assignment': True,
    }

    # Core fields
    name: str = Field(..., description="Parameter name (used in component bindings)")
    label: Optional[str] = Field(None, description="Display label")

    # Optional fields
    id: str = Field(default_factory=lambda: f"input_{uuid.uuid4().hex[:8]}")
    required: bool = Field(True, description="Whether input is required")
    disabled: bool = Field(False, description="Whether input is disabled")
    help_text: Optional[str] = Field(None, description="Help text or tooltip")
    placeholder: Optional[str] = Field(None, description="Placeholder text")

    # Default value (type depends on selector)
    default: Optional[Any] = Field(None, description="Default value")

    @model_validator(mode='after')
    def auto_generate_label(self):
        """Auto-generate label from name if not provided."""
        if self.label is None:
            self.label = self.name.replace('_', ' ').title()
        return self

    def to_dict(self) -> dict:
        """Serialize to dictionary for API/dashboard structure."""
        return self.model_dump(exclude_none=True)


class ChoiceInput(BaseInput):
    """
    Base class for inputs with options (select, multi-select, radio, etc.).

    Supports:
    - Static options: List of values/dicts/Options
    - Dynamic options: Callable that returns options (executed server-side)
    - Parameters: For dynamic options, maps param names to input names or static values
    """

    options: Union[
        List[Union[Option, dict[str, Any], Any]],
        Callable[..., List[Union[Option, dict[str, Any], Any]]]
    ] = Field(..., description="Static list or callable returning options")

    params: dict[str, Any] = Field(
        default_factory=dict,
        description="Parameters for dynamic options (param_name -> input_name or static value)"
    )

    @field_validator('options', mode='before')
    @classmethod
    def normalize_options(cls, v):
        """
        Normalize options: convert list items to Options, preserve callables.

        Callables are preserved as-is (not evaluated) for server-side execution.
        """
        # Callable = reference to component, don't evaluate!
        if callable(v):
            return v

        # Static list - convert each item to Option
        if isinstance(v, list):
            return [
                opt if isinstance(opt, Option) else Option.model_validate(opt)
                for opt in v
            ]

        raise ValueError("options must be a list or callable")

    def has_dynamic_options(self) -> bool:
        """Check if this input uses dynamic options."""
        return callable(self.options)

    def to_dict(self) -> dict:
        """Serialize for API/UI, handling static vs dynamic options."""
        data = super().to_dict()

        if self.has_dynamic_options():
            # Serialize callable reference
            # The callable will be registered separately and replaced with alias
            data['options'] = {
                'type': 'data_source',
                'callable': self.options,  # Will be replaced during registration
            }
            if self.params:
                data['params'] = self.params
        else:
            # Serialize static options
            data['options'] = [opt.model_dump() for opt in self.options]

        return data
