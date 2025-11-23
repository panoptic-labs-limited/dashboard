"""Choice-based inputs (select, multi-select, radio, checkbox)."""

from typing import Literal, Optional, List, Any

from pydantic import Field, field_validator, BaseModel, model_validator

from .base import BaseInput


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


# ==============================================================================
# Config Models
# ==============================================================================

class SelectConfig(BaseModel):
    """Configuration for Select input."""
    options: List[Option]
    default: Optional[Any] = None


class MultiSelectConfig(BaseModel):
    """Configuration for MultiSelect input."""
    options: List[Option]
    default: Optional[List[Any]] = None
    max_selections: Optional[int] = None


class RadioGroupConfig(BaseModel):
    """Configuration for RadioGroup input."""
    options: List[Option]
    default: Optional[Any] = None


class CheckboxConfig(BaseModel):
    """Configuration for Checkbox input."""
    default: Optional[bool] = None


class CheckboxGroupConfig(BaseModel):
    """Configuration for CheckboxGroup input."""
    options: List[Option]
    default: Optional[List[Any]] = None


class ToggleConfig(BaseModel):
    """Configuration for Toggle input."""
    default: Optional[bool] = None
    on_label: Optional[str] = None
    off_label: Optional[str] = None


# ==============================================================================
# Input Classes
# ==============================================================================

class Select(BaseInput[SelectConfig]):
    """
    Single-selection dropdown/select input.

    Examples:
        # Static options (top-level fields)
        region = Select(
            name="region",
            label="Select Region",
            options=[
                Option(value="north", label="North"),
                Option(value="south", label="South")
            ],
            default="north"
        )

        # Dynamic options (FunctionSource)
        region = Select(
            name="region",
            source=FunctionSource(
                func=get_regions_for_country,
                params={"country": "country"}
            )
        )
    """

    __config_class__ = SelectConfig
    input_type: Literal["select"] = "select"

    # Config fields (from SelectConfig)
    options: Optional[List[Option]] = None
    default: Optional[Any] = None

    # Select-specific display options
    searchable: bool = Field(False, description="Enable search/filter in dropdown")
    clear_button: bool = Field(False, description="Show clear button")

    @field_validator('options', mode='before')
    @classmethod
    def normalize_options(cls, v):
        """Convert list items to Option objects."""
        if v is None:
            return v
        if isinstance(v, list):
            return [
                opt if isinstance(opt, Option) else Option.model_validate(opt)
                for opt in v
            ]
        return v


class MultiSelect(BaseInput[MultiSelectConfig]):
    """
    Multi-selection dropdown input.

    Examples:
        # Static options
        categories = MultiSelect(
            name="categories",
            options=[Option("electronics"), Option("clothing")],
            default=["electronics"]
        )

        # Dynamic
        tags = MultiSelect(
            name="tags",
            source=FunctionSource(func=get_available_tags)
        )
    """

    __config_class__ = MultiSelectConfig
    input_type: Literal["multi_select"] = "multi_select"

    # Config fields
    options: Optional[List[Option]] = None
    default: Optional[List[Any]] = None
    max_selections: Optional[int] = None

    # Display options
    searchable: bool = Field(False, description="Enable search/filter")

    @field_validator('options', mode='before')
    @classmethod
    def normalize_options(cls, v):
        """Convert list items to Option objects."""
        if v is None:
            return v
        if isinstance(v, list):
            return [
                opt if isinstance(opt, Option) else Option.model_validate(opt)
                for opt in v
            ]
        return v

    @field_validator('default')
    @classmethod
    def validate_default_is_list(cls, v):
        """Ensure default is a list (or None)."""
        if v is not None and not isinstance(v, list):
            raise ValueError("MultiSelect default must be a list")
        return v


class RadioGroup(BaseInput[RadioGroupConfig]):
    """
    Radio button group input (single selection).

    Examples:
        view_mode = RadioGroup(
            name="view_mode",
            options=[Option("grid"), Option("list"), Option("table")],
            default="grid"
        )
    """

    __config_class__ = RadioGroupConfig
    input_type: Literal["radio"] = "radio"

    # Config fields
    options: Optional[List[Option]] = None
    default: Optional[Any] = None

    # Display options
    layout: Literal["vertical", "horizontal"] = Field(
        "vertical",
        description="Layout direction for radio buttons"
    )

    @field_validator('options', mode='before')
    @classmethod
    def normalize_options(cls, v):
        """Convert list items to Option objects."""
        if v is None:
            return v
        if isinstance(v, list):
            return [
                opt if isinstance(opt, Option) else Option.model_validate(opt)
                for opt in v
            ]
        return v


class Checkbox(BaseInput[CheckboxConfig]):
    """
    Single boolean checkbox input.

    Examples:
        show_legend = Checkbox(
            name="show_legend",
            label="Show Legend",
            default=True
        )
    """

    __config_class__ = CheckboxConfig
    input_type: Literal["checkbox"] = "checkbox"

    # Config fields
    default: Optional[bool] = None

    @field_validator('default')
    @classmethod
    def validate_default_is_bool(cls, v):
        """Ensure default is boolean (or None)."""
        if v is not None and not isinstance(v, bool):
            raise ValueError("Checkbox default must be a boolean")
        return v


class CheckboxGroup(BaseInput[CheckboxGroupConfig]):
    """
    Group of checkboxes for multiple selections.

    Examples:
        features = CheckboxGroup(
            name="features",
            options=[
                Option(value="analytics", label="Analytics Dashboard"),
                Option(value="reports", label="Custom Reports")
            ],
            default=["analytics"]
        )
    """

    __config_class__ = CheckboxGroupConfig
    input_type: Literal["checkbox_group"] = "checkbox_group"

    # Config fields
    options: Optional[List[Option]] = None
    default: Optional[List[Any]] = None

    # Display options
    layout: Literal["vertical", "horizontal", "grid"] = Field(
        "vertical",
        description="Layout direction for checkboxes"
    )
    columns: Optional[int] = Field(None, description="Number of columns for grid layout")

    @field_validator('options', mode='before')
    @classmethod
    def normalize_options(cls, v):
        """Convert list items to Option objects."""
        if v is None:
            return v
        if isinstance(v, list):
            return [
                opt if isinstance(opt, Option) else Option.model_validate(opt)
                for opt in v
            ]
        return v

    @field_validator('default')
    @classmethod
    def validate_default_is_list(cls, v):
        """Ensure default is a list (or None)."""
        if v is not None and not isinstance(v, list):
            raise ValueError("CheckboxGroup default must be a list")
        return v


class Toggle(BaseInput[ToggleConfig]):
    """
    Visual toggle switch for boolean values.

    Examples:
        dark_mode = Toggle(
            name="dark_mode",
            label="Dark Mode",
            default=False,
            on_label="On",
            off_label="Off"
        )
    """

    __config_class__ = ToggleConfig
    input_type: Literal["toggle"] = "toggle"

    # Config fields
    default: Optional[bool] = None
    on_label: Optional[str] = None
    off_label: Optional[str] = None

    @field_validator('default')
    @classmethod
    def validate_default_is_bool(cls, v):
        """Ensure default is boolean (or None)."""
        if v is not None and not isinstance(v, bool):
            raise ValueError("Toggle default must be a boolean")
        return v
