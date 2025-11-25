"""Text-based inputs (text input, textarea, search)."""

from typing import Literal

from pydantic import Field, BaseModel

from .base import Input


# ==============================================================================
# Config Models
# ==============================================================================

class TextInputConfig(BaseModel):
    """Configuration for TextInput."""
    default: str | None = None
    min_length: int | None = None
    max_length: int | None = None
    pattern: str | None = None


class TextAreaConfig(BaseModel):
    """Configuration for TextArea."""
    default: str | None = None
    min_length: int | None = None
    max_length: int | None = None
    rows: int = 3


class SearchInputConfig(BaseModel):
    """Configuration for SearchInput."""
    default: str | None = None
    min_length: int | None = None


# ==============================================================================
# Input Classes
# ==============================================================================

class TextInput(TextInputConfig, Input[TextInputConfig]):
    """Single-line text input."""

    __config_class__ = TextInputConfig
    input_type: Literal["text_input"] = "text_input"

    # Display options (config fields inherited from TextInputConfig)
    input_type_html: Literal["text", "email", "url", "tel"] = Field(
        "text",
        description="HTML input type"
    )
    autocomplete: bool = Field(True, description="Enable autocomplete")


class TextArea(TextAreaConfig, Input[TextAreaConfig]):
    """Multi-line text area."""

    __config_class__ = TextAreaConfig
    input_type: Literal["textarea"] = "textarea"

    # Display options (config fields inherited from TextAreaConfig)
    resize: Literal["none", "vertical", "horizontal", "both"] = Field(
        "vertical",
        description="Resize behavior"
    )


class SearchInput(SearchInputConfig, Input[SearchInputConfig]):
    """Search input with debounce."""

    __config_class__ = SearchInputConfig
    input_type: Literal["search_input"] = "search_input"

    # Display options (config fields inherited from SearchInputConfig)
    clear_button: bool = Field(True, description="Show clear button")
    debounce_ms: int = Field(
        300,
        description="Debounce delay in milliseconds",
        ge=0
    )
