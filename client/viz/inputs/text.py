"""Text-based inputs (text input, textarea, search)."""

from typing import Literal, Optional
from pydantic import Field, field_validator

from .base import BaseInput


class TextInput(BaseInput):
    """
    Single-line text input selector.

    Examples:
        search = TextInput(
            name="search_query",
            label="Search",
            placeholder="Enter search terms..."
        )

        username = TextInput(
            name="username",
            label="Username",
            default="admin",
            max_length=50
        )

        email = TextInput(
            name="email",
            label="Email Address",
            input_type="email",
            required=True
        )
    """

    input_type: Literal["text_input"] = "text_input"
    default: Optional[str] = None

    # Text input options
    input_type: Literal["text", "email", "url", "tel"] = Field(
        "text",
        description="HTML input type for validation"
    )
    min_length: Optional[int] = Field(None, description="Minimum length")
    max_length: Optional[int] = Field(None, description="Maximum length")
    pattern: Optional[str] = Field(None, description="Regex pattern for validation")
    autocomplete: bool = Field(True, description="Enable autocomplete")

    @field_validator('default')
    @classmethod
    def validate_default_is_string(cls, v):
        """Ensure default is a string (or None)."""
        if v is not None and not isinstance(v, str):
            raise ValueError("TextInput default must be a string")
        return v


class TextArea(BaseInput):
    """
    Multi-line text area selector.

    Examples:
        description = TextArea(
            name="description",
            label="Description",
            placeholder="Enter detailed description...",
            rows=5
        )

        notes = TextArea(
            name="notes",
            label="Additional Notes",
            max_length=500,
            help_text="Optional notes (max 500 characters)"
        )
    """

    input_type: Literal["textarea"] = "textarea"
    default: Optional[str] = None

    # Textarea options
    rows: int = Field(3, description="Number of visible text rows", ge=1)
    min_length: Optional[int] = Field(None, description="Minimum length")
    max_length: Optional[int] = Field(None, description="Maximum length")
    resize: Literal["none", "vertical", "horizontal", "both"] = Field(
        "vertical",
        description="Resize behavior"
    )

    @field_validator('default')
    @classmethod
    def validate_default_is_string(cls, v):
        """Ensure default is a string (or None)."""
        if v is not None and not isinstance(v, str):
            raise ValueError("TextArea default must be a string")
        return v


class SearchInput(BaseInput):
    """
    Search input with search icon and clear button.

    Examples:
        search = SearchInput(
            name="search",
            label="Search",
            placeholder="Search products...",
            debounce_ms=300
        )

        filter_text = SearchInput(
            name="filter",
            label="Filter Results",
            clear_button=True
        )
    """

    input_type: Literal["search_input"] = "search_input"
    default: Optional[str] = None

    # Search-specific options
    clear_button: bool = Field(True, description="Show clear button")
    debounce_ms: int = Field(
        300,
        description="Debounce delay in milliseconds for search input",
        ge=0
    )
    min_length: Optional[int] = Field(None, description="Minimum search length")

    @field_validator('default')
    @classmethod
    def validate_default_is_string(cls, v):
        """Ensure default is a string (or None)."""
        if v is not None and not isinstance(v, str):
            raise ValueError("SearchInput default must be a string")
        return v
