"""Text-based inputs (text input, textarea, search)."""

from typing import Literal, Optional
from pydantic import Field, field_validator

from .base import BaseInput
from .config import TextInputConfig, TextAreaConfig, SearchInputConfig
from .sources import FunctionSource


class TextInput(BaseInput[TextInputConfig]):
    """Single-line text input."""

    __config_class__ = TextInputConfig
    input_type: Literal["text_input"] = "text_input"

    # Config fields
    default: Optional[str] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    pattern: Optional[str] = None


    # Display options
    input_type_html: Literal["text", "email", "url", "tel"] = Field(
        "text",
        description="HTML input type"
    )
    autocomplete: bool = Field(True, description="Enable autocomplete")


class TextArea(BaseInput[TextAreaConfig]):
    """Multi-line text area."""

    __config_class__ = TextAreaConfig
    input_type: Literal["textarea"] = "textarea"

    # Config fields
    default: Optional[str] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    rows: int = 3


    # Display options
    resize: Literal["none", "vertical", "horizontal", "both"] = Field(
        "vertical",
        description="Resize behavior"
    )


class SearchInput(BaseInput[SearchInputConfig]):
    """Search input with debounce."""

    __config_class__ = SearchInputConfig
    input_type: Literal["search_input"] = "search_input"

    # Config fields
    default: Optional[str] = None
    min_length: Optional[int] = None


    # Display options
    clear_button: bool = Field(True, description="Show clear button")
    debounce_ms: int = Field(
        300,
        description="Debounce delay in milliseconds",
        ge=0
    )
