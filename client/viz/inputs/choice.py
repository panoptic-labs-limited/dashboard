"""Choice-based inputs (select, multi-select, radio, checkbox)."""

from typing import Literal, Optional, List, Any
from pydantic import Field, field_validator

from .base import ChoiceInput, BaseInput


class Select(ChoiceInput):
    """
    Single-selection dropdown/select input.

    Examples:
        # Static options
        region = Select(
            name="region",
            label="Select Region",
            options=["North", "South", "East", "West"],
            default="North"
        )

        # With custom labels
        status = Select(
            name="status",
            options=[
                {"value": "active", "label": "Active"},
                {"value": "inactive", "label": "Inactive"}
            ],
            default="active"
        )

        # Dynamic options
        def get_regions_for_country(country: str):
            return [...regions...]

        region = Select(
            name="region",
            options=get_regions_for_country,
            params={"country": "country"}
        )
    """

    input_type: Literal["select"] = "select"
    default: Optional[Any] = None  # Single value

    # Select-specific options
    searchable: bool = Field(False, description="Enable search/filter in dropdown")
    clear_button: bool = Field(False, description="Show clear button")


class MultiSelect(ChoiceInput):
    """
    Multi-selection dropdown input.

    Examples:
        # Static options
        categories = MultiSelect(
            name="categories",
            label="Select Categories",
            options=["Electronics", "Clothing", "Food"],
            default=["Electronics"]
        )

        # With pre-selected options
        tags = MultiSelect(
            name="tags",
            options=[
                {"value": "python", "label": "Python", "selected": True},
                {"value": "javascript", "label": "JavaScript"},
                {"value": "rust", "label": "Rust", "selected": True}
            ]
        )
    """

    input_type: Literal["multi_select"] = "multi_select"
    default: Optional[List[Any]] = None  # List of values

    # Multi-select specific options
    max_selections: Optional[int] = Field(None, description="Maximum number of selections allowed")
    searchable: bool = Field(False, description="Enable search/filter")

    @field_validator('default')
    @classmethod
    def validate_default_is_list(cls, v):
        """Ensure default is a list (or None)."""
        if v is not None and not isinstance(v, list):
            raise ValueError("MultiSelect default must be a list")
        return v


class RadioGroup(ChoiceInput):
    """
    Radio button group input (single selection).

    Examples:
        view_mode = RadioGroup(
            name="view_mode",
            label="View Mode",
            options=["Grid", "List", "Table"],
            default="Grid"
        )

        priority = RadioGroup(
            name="priority",
            options=[
                {"value": "high", "label": "High Priority", "icon": "🔴"},
                {"value": "medium", "label": "Medium Priority", "icon": "🟡"},
                {"value": "low", "label": "Low Priority", "icon": "🟢"}
            ]
        )
    """

    input_type: Literal["radio"] = "radio"
    default: Optional[Any] = None  # Single value

    # Radio-specific options
    layout: Literal["vertical", "horizontal"] = Field(
        "vertical",
        description="Layout direction for radio buttons"
    )


class Checkbox(BaseInput):
    """
    Single boolean checkbox input.

    Examples:
        show_legend = Checkbox(
            name="show_legend",
            label="Show Legend",
            default=True
        )

        include_archived = Checkbox(
            name="include_archived",
            label="Include Archived Items",
            default=False,
            help_text="Check to include archived items in results"
        )
    """

    input_type: Literal["checkbox"] = "checkbox"
    default: Optional[bool] = Field(None, description="Default checked state")

    @field_validator('default')
    @classmethod
    def validate_default_is_bool(cls, v):
        """Ensure default is boolean (or None)."""
        if v is not None and not isinstance(v, bool):
            raise ValueError("Checkbox default must be a boolean")
        return v


class CheckboxGroup(ChoiceInput):
    """
    Group of checkboxes for multiple selections.

    Similar to MultiSelect but renders as individual checkboxes.

    Examples:
        features = CheckboxGroup(
            name="features",
            label="Enabled Features",
            options=[
                {"value": "analytics", "label": "Analytics Dashboard"},
                {"value": "reports", "label": "Custom Reports"},
                {"value": "exports", "label": "Data Exports"}
            ],
            default=["analytics", "reports"]
        )
    """

    input_type: Literal["checkbox_group"] = "checkbox_group"
    default: Optional[List[Any]] = None  # List of values

    # Layout options
    layout: Literal["vertical", "horizontal", "grid"] = Field(
        "vertical",
        description="Layout direction for checkboxes"
    )
    columns: Optional[int] = Field(None, description="Number of columns for grid layout")

    @field_validator('default')
    @classmethod
    def validate_default_is_list(cls, v):
        """Ensure default is a list (or None)."""
        if v is not None and not isinstance(v, list):
            raise ValueError("CheckboxGroup default must be a list")
        return v


class Toggle(BaseInput):
    """
    Visual toggle switch for boolean values.

    Similar to Checkbox but with switch UI.

    Examples:
        dark_mode = Toggle(
            name="dark_mode",
            label="Dark Mode",
            default=False
        )

        auto_refresh = Toggle(
            name="auto_refresh",
            label="Auto Refresh",
            default=True,
            help_text="Automatically refresh data every 30 seconds"
        )
    """

    input_type: Literal["toggle"] = "toggle"
    default: Optional[bool] = Field(None, description="Default toggle state")

    # Toggle-specific options
    on_label: Optional[str] = Field(None, description="Label for ON state")
    off_label: Optional[str] = Field(None, description="Label for OFF state")

    @field_validator('default')
    @classmethod
    def validate_default_is_bool(cls, v):
        """Ensure default is boolean (or None)."""
        if v is not None and not isinstance(v, bool):
            raise ValueError("Toggle default must be a boolean")
        return v
