"""Shared code for Viz distributed dashboarding framework."""

__version__ = "0.1.0"

# Export types
from .types import (
    ExecutionStage,
    SelectorType,
    WidgetType,
    ColumnWidth,
    RenderOutputType,
    LayoutType,
    ComponentAlias,
    DashboardName,
    PageId,
    SelectorName,
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
    # Selector schemas
    SelectorBase,
    SelectorDataSourceFunction,
    DateSelectorSchema,
    DateRangeSelectorSchema,
    DropdownSelectorSchema,
    MultiSelectSelectorSchema,
    TextInputSchema,
    NumericInputSchema,
    SelectorSchema,
    # Layout schemas
    LayoutNodeBase,
    ParameterBinding,
    WidgetSchema,
    SelectorLayoutSchema,
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
    SelectorValueUpdate,
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
    "SelectorType",
    "WidgetType",
    "ColumnWidth",
    "RenderOutputType",
    "LayoutType",
    "ComponentAlias",
    "DashboardName",
    "PageId",
    "SelectorName",
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
    # Selector schemas
    "SelectorBase",
    "SelectorDataSourceFunction",
    "DateSelectorSchema",
    "DateRangeSelectorSchema",
    "DropdownSelectorSchema",
    "MultiSelectSelectorSchema",
    "TextInputSchema",
    "NumericInputSchema",
    "SelectorSchema",
    # Layout schemas
    "LayoutNodeBase",
    "ParameterBinding",
    "WidgetSchema",
    "SelectorLayoutSchema",
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
    "SelectorValueUpdate",
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
