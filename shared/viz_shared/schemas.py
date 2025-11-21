"""Pydantic schemas for Viz framework API communication."""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator

from .types import (
    ExecutionStage, SelectorType, LayoutType, RenderOutputType,
    WidgetType, ColumnWidth
)


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
# Selector Schemas
# ============================================================================

class SelectorDataSourceFunction(BaseModel):
    """Function that provides data for a selector."""
    alias: str  # Function alias in registry
    params: Dict[str, Any] = Field(default_factory=dict)


class SelectorBase(BaseModel):
    """Base schema for selectors."""
    name: str = Field(..., description="Parameter name this selector controls")
    label: Optional[str] = None  # Display label (defaults to name)
    selector_type: SelectorType
    default: Optional[Any] = None
    required: bool = True
    description: Optional[str] = None


class DateSelectorSchema(SelectorBase):
    """Date selector configuration."""
    selector_type: SelectorType = SelectorType.DATE
    min_date: Optional[str] = None  # ISO format
    max_date: Optional[str] = None  # ISO format
    data_source: Optional[SelectorDataSourceFunction] = None


class DateRangeSelectorSchema(SelectorBase):
    """Date range selector configuration."""
    selector_type: SelectorType = SelectorType.DATE_RANGE
    min_date: Optional[str] = None
    max_date: Optional[str] = None
    default: Optional[tuple[str, str]] = None


class DropdownSelectorSchema(SelectorBase):
    """Dropdown selector configuration."""
    selector_type: SelectorType = SelectorType.DROPDOWN
    options: Optional[List[Union[str, int, float]]] = None
    data_source: Optional[SelectorDataSourceFunction] = None  # Dynamic options
    allow_custom: bool = False


class MultiSelectSelectorSchema(SelectorBase):
    """Multi-select selector configuration."""
    selector_type: SelectorType = SelectorType.MULTI_SELECT
    options: Optional[List[Union[str, int, float]]] = None
    data_source: Optional[SelectorDataSourceFunction] = None
    max_selections: Optional[int] = None


class TextInputSchema(SelectorBase):
    """Text input selector configuration."""
    selector_type: SelectorType = SelectorType.TEXT_INPUT
    placeholder: Optional[str] = None
    validation_regex: Optional[str] = None
    max_length: Optional[int] = None


class NumericInputSchema(SelectorBase):
    """Numeric input selector configuration."""
    selector_type: SelectorType = SelectorType.NUMERIC_INPUT
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    step: Optional[float] = None
    placeholder: Optional[str] = None


# Union of all selector schemas
SelectorSchema = Union[
    DateSelectorSchema,
    DateRangeSelectorSchema,
    DropdownSelectorSchema,
    MultiSelectSelectorSchema,
    TextInputSchema,
    NumericInputSchema,
]


# ============================================================================
# Layout Schemas
# ============================================================================

class LayoutNodeBase(BaseModel):
    """Base schema for layout nodes."""
    id: str = Field(..., description="Unique ID for this layout node")
    type: LayoutType


class ParameterBinding(BaseModel):
    """Binding between a component parameter and a selector."""
    type: str = "selector"  # Future: could be "constant", "computed", etc.
    selector_name: str  # Name of the selector to bind to


class WidgetSchema(LayoutNodeBase):
    """Widget containing a component instance."""
    type: LayoutType = LayoutType.WIDGET
    widget_type: WidgetType
    component_alias: Optional[str] = None
    params: Dict[str, Union[Any, ParameterBinding]] = Field(default_factory=dict)
    title: Optional[str] = None
    description: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)


class SelectorLayoutSchema(LayoutNodeBase):
    """Selector in the layout."""
    type: LayoutType = LayoutType.SELECTOR
    selector_type: SelectorType
    name: str = Field(..., description="Parameter name")
    label: str
    default: Any = None
    options: Optional[List[Any]] = None
    config: Dict[str, Any] = Field(default_factory=dict)


class ColumnSchema(LayoutNodeBase):
    """Column layout container."""
    type: LayoutType = LayoutType.COLUMN
    width: ColumnWidth = ColumnWidth.FULL
    gap: Optional[str] = Field(None, description="Gap between children (CSS)")
    children: List[Union['RowSchema', 'ColumnSchema', 'WidgetSchema', 'SelectorLayoutSchema']] = Field(default_factory=list)


class RowSchema(LayoutNodeBase):
    """Row layout container."""
    type: LayoutType = LayoutType.ROW
    gap: Optional[str] = Field(None, description="Gap between children (CSS)")
    align: Optional[str] = None  # "start", "center", "end", "stretch"
    children: List[Union['RowSchema', ColumnSchema, WidgetSchema, SelectorLayoutSchema]] = Field(default_factory=list)


class TabSchema(LayoutNodeBase):
    """Individual tab within a Tabs container."""
    type: LayoutType = LayoutType.TAB
    title: str
    icon: Optional[str] = None
    disabled: bool = False
    children: List[Union[RowSchema, ColumnSchema, WidgetSchema, SelectorLayoutSchema]] = Field(default_factory=list)


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
    children: List[Union[RowSchema, ColumnSchema, TabsSchema, WidgetSchema, SelectorLayoutSchema]] = Field(default_factory=list)


class PageSchema(LayoutNodeBase):
    """Page (tab) in a dashboard."""
    type: LayoutType = LayoutType.PAGE
    title: str
    description: Optional[str] = None
    icon: Optional[str] = None
    children: List[Union[SectionSchema, RowSchema, ColumnSchema, TabsSchema, WidgetSchema, SelectorLayoutSchema]] = Field(default_factory=list)


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
    name: str = Field(..., description="Unique dashboard identifier")
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
    id: int
    name: str
    title: str
    description: Optional[str] = None
    structure: DashboardStructure
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SelectorValueUpdate(BaseModel):
    """Update a selector value."""
    selector_name: str
    value: Any


class DashboardRenderRequest(BaseModel):
    """Request to render a dashboard."""
    selector_values: Dict[str, Any] = Field(default_factory=dict)


class WidgetRenderRequest(BaseModel):
    """Request to render a single widget."""
    selector_values: Dict[str, Any] = Field(default_factory=dict)


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
    dashboard_name: str
    selector_values: Dict[str, Any]
    widgets: List[WidgetRenderResult]
    total_execution_time_ms: float


# Enable forward references
ColumnSchema.model_rebuild()
RowSchema.model_rebuild()
TabSchema.model_rebuild()
TabsSchema.model_rebuild()
SectionSchema.model_rebuild()
PageSchema.model_rebuild()
