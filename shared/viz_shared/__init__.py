"""Shared code for Viz distributed dashboarding framework."""

__version__ = "0.1.0"

# Export types
from .types import (
    ExecutionStage,
    InputType,
    WidgetType,
    ColumnWidth,
    RenderOutputType,
    LayoutType,
    ComponentAlias,
    DashboardId,
    PageId,
    InputId,
    ParameterName,
)

# Export schemas
from .schemas import (
    # Component schemas
    ComponentMetadata,
    ComponentParameter,
    ComponentCreate,
    ComponentUpdate,
    ComponentResponse,
    # Execution schemas
    ComponentExecutionRequest,
    RenderOutput,
    ComponentExecutionResponse,
    # Input schemas
    Option,
    InputDataSource,
    InputBase,
    InputSchema,
    # Text input schemas
    TextInputSchema,
    TextAreaSchema,
    SearchInputSchema,
    # Numeric input schemas
    NumericInputSchema,
    SliderSchema,
    RangeSliderSchema,
    NumericRangeSchema,
    # Choice input schemas
    SelectSchema,
    MultiSelectSchema,
    RadioGroupSchema,
    CheckboxSchema,
    CheckboxGroupSchema,
    ToggleSchema,
    # DateTime input schemas
    DateInputSchema,
    DateRangeInputSchema,
    TimeInputSchema,
    DateTimeInputSchema,
    RelativeDateInputSchema,
    # Layout schemas
    LayoutNodeBase,
    ParameterBinding,
    WidgetSchema,
    ColumnSchema,
    RowSchema,
    TabSchema,
    TabsSchema,
    SectionSchema,
    PageSchema,
    DashboardStructure,
    # Dashboard API schemas
    DashboardCreate,
    DashboardUpdate,
    DashboardResponse,
    InputValueUpdate,
    DashboardRenderRequest,
    WidgetRenderRequest,
    WidgetRenderResult,
    DashboardRenderResponse,
)

# Export utilities
from .utils import (
    serialize_render_output,
    validate_component_source,
    extract_component_parameters,
    generate_unique_id,
)

__all__ = [
    # Types
    "ExecutionStage",
    "InputType",
    "WidgetType",
    "ColumnWidth",
    "RenderOutputType",
    "LayoutType",
    "ComponentAlias",
    "DashboardId",
    "PageId",
    "InputId",
    "ParameterName",
    # Component schemas
    "ComponentMetadata",
    "ComponentParameter",
    "ComponentCreate",
    "ComponentUpdate",
    "ComponentResponse",
    # Execution schemas
    "ComponentExecutionRequest",
    "RenderOutput",
    "ComponentExecutionResponse",
    # Input schemas
    "Option",
    "InputDataSource",
    "InputBase",
    "InputSchema",
    # Text input schemas
    "TextInputSchema",
    "TextAreaSchema",
    "SearchInputSchema",
    # Numeric input schemas
    "NumericInputSchema",
    "SliderSchema",
    "RangeSliderSchema",
    "NumericRangeSchema",
    # Choice input schemas
    "SelectSchema",
    "MultiSelectSchema",
    "RadioGroupSchema",
    "CheckboxSchema",
    "CheckboxGroupSchema",
    "ToggleSchema",
    # DateTime input schemas
    "DateInputSchema",
    "DateRangeInputSchema",
    "TimeInputSchema",
    "DateTimeInputSchema",
    "RelativeDateInputSchema",
    # Layout schemas
    "LayoutNodeBase",
    "ParameterBinding",
    "WidgetSchema",
    "ColumnSchema",
    "RowSchema",
    "TabSchema",
    "TabsSchema",
    "SectionSchema",
    "PageSchema",
    "DashboardStructure",
    # Dashboard API schemas
    "DashboardCreate",
    "DashboardUpdate",
    "DashboardResponse",
    "InputValueUpdate",
    "DashboardRenderRequest",
    "WidgetRenderRequest",
    "WidgetRenderResult",
    "DashboardRenderResponse",
    # Utilities
    "serialize_render_output",
    "validate_component_source",
    "extract_component_parameters",
    "generate_unique_id",
]
