"""Pydantic schemas for Viz framework API communication."""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator, EmailStr

from app.types import (
    ExecutionStage, InputType, LayoutType, RenderOutputType,
    WidgetType
)


# ============================================================================
# Auth Schemas
# ============================================================================

class UserCreate(BaseModel):
    """Schema for creating a new user."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Schema for login request."""
    username: str
    password: str


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for decoded JWT token data."""
    username: Optional[str] = None


# ============================================================================
# Function Schemas
# ============================================================================

class FunctionCreate(BaseModel):
    """Schema for creating a new function."""
    alias: str = Field(..., description="Unique identifier for the function")
    code: str = Field(..., description="Python function code")
    description: Optional[str] = None
    memory_limit_mb: int = Field(default=200, ge=1, le=2048)
    timeout_seconds: int = Field(default=30, ge=1, le=300)


class FunctionUpdate(BaseModel):
    """Schema for updating a function."""
    code: Optional[str] = None
    description: Optional[str] = None
    memory_limit_mb: Optional[int] = Field(None, ge=1, le=2048)
    timeout_seconds: Optional[int] = Field(None, ge=1, le=300)


class FunctionResponse(BaseModel):
    """Schema for function response."""
    id: int
    alias: str
    code: str
    description: Optional[str] = None
    owner_id: int
    memory_limit_mb: int
    timeout_seconds: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExecutionRequest(BaseModel):
    """Request to execute a function."""
    params: Dict[str, Any] = Field(default_factory=dict)


class ExecutionResponse(BaseModel):
    """Response from function execution."""
    id: int
    function_id: int
    status: str  # "success", "error", "timeout"
    input_params: Optional[Dict[str, Any]] = None
    output: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    execution_time_ms: Optional[float] = None
    memory_used_mb: Optional[float] = None
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# Component Schemas
# ============================================================================

class ComponentMetadata(BaseModel):
    """Metadata for a component."""
    name: str
    description: Optional[str] = None
    author: Optional[str] = None
    version: str = "1.0.0"
    tags: List[str] = Field(default_factory=list)


class ComponentParameter(BaseModel):
    """Parameter definition for a component."""
    name: str
    type: str  # "str", "int", "float", "bool", "date", etc.
    required: bool = True
    default: Optional[Any] = None
    description: Optional[str] = None


class ComponentCreate(BaseModel):
    """Schema for creating a new component."""
    alias: str = Field(..., description="Unique identifier for the component")
    class_name: str = Field(..., description="Name of the component class")
    source_code: str = Field(..., description="Complete Python source code")
    description: Optional[str] = None
    parameters: List[ComponentParameter] = Field(default_factory=list)
    metadata: Optional[ComponentMetadata] = None

    # Resource limits
    memory_limit_mb: int = Field(default=200, ge=1, le=2048)
    timeout_seconds: int = Field(default=30, ge=1, le=300)


class ComponentUpdate(BaseModel):
    """Schema for updating a component."""
    source_code: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[List[ComponentParameter]] = None
    metadata: Optional[ComponentMetadata] = None
    memory_limit_mb: Optional[int] = Field(None, ge=1, le=2048)
    timeout_seconds: Optional[int] = Field(None, ge=1, le=300)


class ComponentResponse(BaseModel):
    """Schema for component response."""
    id: int
    alias: str
    class_name: str
    source_code: str
    description: Optional[str] = None
    parameters: List[ComponentParameter]
    metadata: Optional[ComponentMetadata] = Field(None, validation_alias="component_metadata")
    owner_id: int
    memory_limit_mb: int
    timeout_seconds: int
    created_at: datetime
    updated_at: datetime

    @field_validator('metadata', mode='before')
    @classmethod
    def validate_metadata(cls, v):
        """Convert empty dict to None for metadata field."""
        if v == {} or v is None:
            return None
        return v

    class Config:
        from_attributes = True
        populate_by_name = True  # Allow populating by field name or alias


# ============================================================================
# Execution Schemas
# ============================================================================

class ComponentExecutionRequest(BaseModel):
    """Request to execute a component."""
    stage: ExecutionStage = ExecutionStage.LOAD_TRANSFORM_RENDER
    params: Dict[str, Any] = Field(default_factory=dict)


class RenderOutput(BaseModel):
    """Render output from a component."""
    type: RenderOutputType
    data: Union[Dict[str, Any], str]  # JSON data or serialized Plotly figure
    config: Optional[Dict[str, Any]] = None


class ComponentExecutionResponse(BaseModel):
    """Response from component execution."""
    id: int
    component_id: int
    status: str  # "success", "error", "timeout"
    stage: ExecutionStage
    output: Optional[Union[Dict[str, Any], RenderOutput]] = None
    error_message: Optional[str] = None
    execution_time_ms: Optional[float] = None
    memory_used_mb: Optional[float] = None
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# Input Schemas
# ============================================================================

class Option(BaseModel):
    """Represents a selectable option."""
    value: Any = Field(..., description="The actual option value")
    label: str = Field(..., description="Display label for the option")
    selected: bool = Field(False, description="Pre-selected state")
    disabled: bool = Field(False, description="Disabled state")
    icon: Optional[str] = Field(None, description="Optional icon identifier")
    group: Optional[str] = Field(None, description="Group name for grouped options")


class InputDataSource(BaseModel):
    """Function or API source that provides data for an input."""
    type: str = Field("function", description="Source type: 'function' or 'api'")
    alias: Optional[str] = Field(None, description="Function alias in registry")
    params: Dict[str, Any] = Field(default_factory=dict, description="Parameters for the source")


class InputBase(BaseModel):
    """Base schema for inputs."""
    type: str = Field("input", description="Node type")
    id: str = Field(..., description="Unique identifier for this input")
    input_type: InputType
    label: Optional[str] = None
    description: Optional[str] = None
    default: Optional[Any] = None
    required: bool = True
    source: Optional[InputDataSource] = None
    visible: bool = True
    disabled: bool = False


# ==============================================================================
# Text Input Schemas
# ==============================================================================

class TextInputSchema(InputBase):
    """Single-line text input."""
    input_type: InputType = InputType.TEXT_INPUT
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    pattern: Optional[str] = None
    input_type_html: str = Field("text", description="HTML input type: text, email, url, tel")
    autocomplete: bool = True
    placeholder: Optional[str] = None


class TextAreaSchema(InputBase):
    """Multi-line text area."""
    input_type: InputType = InputType.TEXTAREA
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    rows: int = 3
    resize: str = Field("vertical", description="Resize behavior: none, vertical, horizontal, both")
    placeholder: Optional[str] = None


class SearchInputSchema(InputBase):
    """Search input with debounce."""
    input_type: InputType = InputType.SEARCH_INPUT
    min_length: Optional[int] = None
    clear_button: bool = True
    debounce_ms: int = Field(300, ge=0, description="Debounce delay in milliseconds")
    placeholder: Optional[str] = None


# ==============================================================================
# Numeric Input Schemas
# ==============================================================================

class NumericInputSchema(InputBase):
    """Numeric input with constraints."""
    input_type: InputType = InputType.NUMERIC_INPUT
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    step: Optional[float] = None
    prefix: Optional[str] = Field(None, description="Prefix text (e.g., '$')")
    suffix: Optional[str] = Field(None, description="Suffix text (e.g., '%')")
    placeholder: Optional[str] = None


class SliderSchema(InputBase):
    """Visual slider for single value."""
    input_type: InputType = InputType.SLIDER
    min_value: float
    max_value: float
    step: Optional[float] = None
    show_value: bool = True
    show_ticks: bool = False


class RangeSliderSchema(InputBase):
    """Visual slider for range (min/max)."""
    input_type: InputType = InputType.RANGE_SLIDER
    min_value: float
    max_value: float
    step: Optional[float] = None
    default: Optional[tuple[float, Optional[float]]] = None
    show_values: bool = True


class NumericRangeSchema(InputBase):
    """Two numeric inputs for min/max range."""
    input_type: InputType = InputType.NUMERIC_RANGE
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    step: Optional[float] = None
    default: Optional[tuple[float, Optional[float]]] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None


# ==============================================================================
# Choice Input Schemas
# ==============================================================================

class SelectSchema(InputBase):
    """Single-selection dropdown/select input."""
    input_type: InputType = InputType.SELECT
    options: Optional[List[Option]] = None
    searchable: bool = False
    clear_button: bool = False


class MultiSelectSchema(InputBase):
    """Multi-selection dropdown input."""
    input_type: InputType = InputType.MULTI_SELECT
    options: Optional[List[Option]] = None
    default: Optional[List[Any]] = None
    max_selections: Optional[int] = None
    searchable: bool = False


class RadioGroupSchema(InputBase):
    """Radio button group input (single selection)."""
    input_type: InputType = InputType.RADIO
    options: Optional[List[Option]] = None
    layout: str = Field("vertical", description="Layout direction: vertical, horizontal")


class CheckboxSchema(InputBase):
    """Single boolean checkbox input."""
    input_type: InputType = InputType.CHECKBOX
    default: Optional[bool] = None


class CheckboxGroupSchema(InputBase):
    """Group of checkboxes for multiple selections."""
    input_type: InputType = InputType.CHECKBOX_GROUP
    options: Optional[List[Option]] = None
    default: Optional[List[Any]] = None
    layout: str = Field("vertical", description="Layout: vertical, horizontal, grid")
    columns: Optional[int] = Field(None, description="Number of columns for grid containers")


class ToggleSchema(InputBase):
    """Visual toggle switch for boolean values."""
    input_type: InputType = InputType.TOGGLE
    default: Optional[bool] = None
    on_label: Optional[str] = None
    off_label: Optional[str] = None


# ==============================================================================
# DateTime Input Schemas
# ==============================================================================

class DateInputSchema(InputBase):
    """Date picker input."""
    input_type: InputType = InputType.DATE
    min_date: Optional[str] = None
    max_date: Optional[str] = None
    format: str = Field("YYYY-MM-DD", description="Display format")
    first_day_of_week: int = Field(0, description="0=Sunday, 1=Monday")


class DateRangeInputSchema(InputBase):
    """Date range picker."""
    input_type: InputType = InputType.DATE_RANGE
    min_date: Optional[str] = None
    max_date: Optional[str] = None
    default: Optional[tuple[str, Optional[str]]] = None
    format: str = Field("YYYY-MM-DD", description="Display format")
    max_days: Optional[int] = Field(None, description="Maximum days in range")


class TimeInputSchema(InputBase):
    """Time picker input."""
    input_type: InputType = InputType.TIME
    min_time: Optional[str] = None
    max_time: Optional[str] = None
    step_minutes: int = 1
    format_24h: bool = True


class DateTimeInputSchema(InputBase):
    """Combined date and time picker."""
    input_type: InputType = InputType.DATETIME
    min_datetime: Optional[str] = None
    max_datetime: Optional[str] = None
    format: str = Field("YYYY-MM-DD HH:mm", description="Display format")
    format_24h: bool = True


class RelativeDateInputSchema(InputBase):
    """Relative date range selector (last 7 days, etc.)."""
    input_type: InputType = InputType.RELATIVE_DATE
    options: List[Dict[str, str]]
    allow_custom: bool = False


# ==============================================================================
# Union of all input schemas
# ==============================================================================

InputSchema = Union[
    # Text inputs
    TextInputSchema,
    TextAreaSchema,
    SearchInputSchema,
    # Numeric inputs
    NumericInputSchema,
    SliderSchema,
    RangeSliderSchema,
    NumericRangeSchema,
    # Choice inputs
    SelectSchema,
    MultiSelectSchema,
    RadioGroupSchema,
    CheckboxSchema,
    CheckboxGroupSchema,
    ToggleSchema,
    # DateTime inputs
    DateInputSchema,
    DateRangeInputSchema,
    TimeInputSchema,
    DateTimeInputSchema,
    RelativeDateInputSchema,
]


# ============================================================================
# Layout Schemas
# ============================================================================

class LayoutNodeBase(BaseModel):
    """Base schema for containers nodes."""
    id: str = Field(..., description="Unique ID for this containers node")
    type: LayoutType


class ParameterBinding(BaseModel):
    """Binding between a component parameter and an input."""
    type: str = "input"  # Future: could be "constant", "computed", etc.
    input_id: str  # ID of the input to bind to


class WidgetSchema(LayoutNodeBase):
    """Widget containing a component instance."""
    type: LayoutType = LayoutType.WIDGET
    widget_type: WidgetType
    component_alias: Optional[str] = None
    params: Dict[str, Union[Any, ParameterBinding]] = Field(default_factory=dict)
    title: Optional[str] = None
    description: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)


class ColumnSchema(LayoutNodeBase):
    """Column containers container."""
    type: LayoutType = LayoutType.COLUMN
    weight: int = Field(1, description="Relative width weight (like CSS flex-grow)", ge=1)
    gap: Optional[str] = Field(None, description="Gap between children (CSS)")
    children: List[Union['RowSchema', 'ColumnSchema', 'WidgetSchema', InputSchema]] = Field(default_factory=list)


class RowSchema(LayoutNodeBase):
    """Row containers container."""
    type: LayoutType = LayoutType.ROW
    gap: Optional[str] = Field(None, description="Gap between children (CSS)")
    align: Optional[str] = None  # "start", "center", "end", "stretch"
    children: List[Union['RowSchema', ColumnSchema, WidgetSchema, InputSchema]] = Field(default_factory=list)


class TabSchema(LayoutNodeBase):
    """Individual tab within a Tabs container."""
    type: LayoutType = LayoutType.TAB
    title: str
    icon: Optional[str] = None
    disabled: bool = False
    children: List[Union[RowSchema, ColumnSchema, WidgetSchema, InputSchema]] = Field(default_factory=list)


class TabsSchema(LayoutNodeBase):
    """Tabs container holding multiple Tab components."""
    type: LayoutType = LayoutType.TABS
    default_tab: Optional[str] = Field(None, description="ID of default active tab")
    children: List[TabSchema] = Field(default_factory=list)


class SectionSchema(LayoutNodeBase):
    """Section containing rows and columns."""
    type: LayoutType = LayoutType.SECTION
    title: Optional[str] = None
    collapsible: bool = False
    collapsed: bool = False
    children: List[Union[RowSchema, ColumnSchema, TabsSchema, WidgetSchema, InputSchema]] = Field(default_factory=list)


class PageSchema(LayoutNodeBase):
    """Page (tab) in a dashboard."""
    type: LayoutType = LayoutType.PAGE
    title: str
    description: Optional[str] = None
    icon: Optional[str] = None
    children: List[Union[SectionSchema, RowSchema, ColumnSchema, TabsSchema, WidgetSchema, InputSchema]] = Field(default_factory=list)


class DashboardStructure(BaseModel):
    """Complete dashboard structure."""
    id: str = Field(..., description="Unique ID for dashboard")
    type: LayoutType = LayoutType.DASHBOARD
    title: str
    description: Optional[str] = None
    version: str = "1.0.0"
    children: List[PageSchema] = Field(default_factory=list)


# ============================================================================
# Dashboard API Schemas
# ============================================================================

class DashboardCreate(BaseModel):
    """Schema for creating a dashboard."""
    id: str = Field(..., description="Unique dashboard identifier")
    title: str
    description: Optional[str] = None
    structure: DashboardStructure


class DashboardUpdate(BaseModel):
    """Schema for updating a dashboard."""
    title: Optional[str] = None
    description: Optional[str] = None
    structure: Optional[DashboardStructure] = None


class DashboardResponse(BaseModel):
    """Schema for dashboard response."""
    db_id: int = Field(..., alias="id", description="Database ID")
    id: str = Field(..., alias="dashboard_id", description="Dashboard identifier")
    title: str
    description: Optional[str] = None
    structure: DashboardStructure
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


class InputValueUpdate(BaseModel):
    """Update an input value."""
    input_id: str
    value: Any


class DashboardRenderRequest(BaseModel):
    """Request to render a dashboard."""
    input_values: Dict[str, Any] = Field(default_factory=dict)


class WidgetRenderRequest(BaseModel):
    """Request to render a single widget."""
    input_values: Dict[str, Any] = Field(default_factory=dict)


class WidgetRenderResult(BaseModel):
    """Result of rendering a single widget."""
    widget_id: str
    component_alias: str
    status: str
    output: Optional[Union[Dict[str, Any], RenderOutput]] = None
    error_message: Optional[str] = None
    execution_time_ms: Optional[float] = None


class DashboardRenderResponse(BaseModel):
    """Response from rendering a dashboard."""
    dashboard_id: str
    input_values: Dict[str, Any]
    widgets: List[WidgetRenderResult]
    total_execution_time_ms: float


# Enable forward references
ColumnSchema.model_rebuild()
RowSchema.model_rebuild()
TabSchema.model_rebuild()
TabsSchema.model_rebuild()
SectionSchema.model_rebuild()
PageSchema.model_rebuild()
