/**
 * TypeScript types for Viz dashboard structure.
 * Mirrors the Pydantic schemas from viz_shared.
 */

export type LayoutType = 'page' | 'section' | 'row' | 'column' | 'widget' | 'selector';
export type SelectorType = 'date' | 'date_range' | 'dropdown' | 'multi_select' | 'text_input' | 'numeric_input';
export type RenderOutputType = 'plotly' | 'vega_lite' | 'altair' | 'custom';

// Selector schemas
export interface SelectorDataSourceFunction {
  alias: string;
  params: Record<string, any>;
}

export interface SelectorBase {
  name: string;
  label?: string;
  selector_type: SelectorType;
  default?: any;
  required: boolean;
  description?: string;
}

export interface DateSelectorSchema extends SelectorBase {
  selector_type: 'date';
  min_date?: string;
  max_date?: string;
  data_source?: SelectorDataSourceFunction;
}

export interface DropdownSelectorSchema extends SelectorBase {
  selector_type: 'dropdown';
  options?: Array<string | number | float>;
  data_source?: SelectorDataSourceFunction;
  allow_custom: boolean;
}

export interface MultiSelectSelectorSchema extends SelectorBase {
  selector_type: 'multi_select';
  options?: Array<string | number | float>;
  data_source?: SelectorDataSourceFunction;
  max_selections?: number;
}

export type SelectorSchema = DateSelectorSchema | DropdownSelectorSchema | MultiSelectSelectorSchema;

// Layout node schemas
export interface LayoutNodeBase {
  id: string;
  type: LayoutType;
}

export interface ParameterBinding {
  type: 'selector' | 'literal';
  name?: string;  // For selector bindings
  value?: any;    // For literal bindings
}

export interface WidgetSchema extends LayoutNodeBase {
  type: 'widget';
  component_alias: string;
  params: Record<string, ParameterBinding>;
  title?: string;
  description?: string;
}

export interface SelectorLayoutSchema extends LayoutNodeBase {
  type: 'selector';
  selector: SelectorSchema;
}

export interface ColumnSchema extends LayoutNodeBase {
  type: 'column';
  width?: string;
  children: Array<RowSchema | WidgetSchema | SelectorLayoutSchema>;
}

export interface RowSchema extends LayoutNodeBase {
  type: 'row';
  children: ColumnSchema[];
}

export interface SectionSchema extends LayoutNodeBase {
  type: 'section';
  title?: string;
  collapsible: boolean;
  collapsed: boolean;
  children: Array<RowSchema | ColumnSchema>;
}

export interface PageSchema extends LayoutNodeBase {
  type: 'page';
  title: string;
  description?: string;
  icon?: string;
  sections: SectionSchema[];
}

export interface DashboardStructure {
  name: string;
  title: string;
  description?: string;
  theme?: string;
  pages: PageSchema[];
}

// Dashboard API responses
export interface DashboardResponse {
  id: number;
  name: string;
  title: string;
  description?: string;
  structure: DashboardStructure;
  owner_id: number;
  created_at: string;
  updated_at: string;
}

// Render request/response
export interface DashboardRenderRequest {
  selector_values: Record<string, any>;
}

export interface RenderOutput {
  type: RenderOutputType;
  data: any;
  config?: Record<string, any>;
}

export interface WidgetRenderResult {
  widget_id: string;
  component_alias: string;
  status: 'success' | 'error' | 'timeout';
  output?: RenderOutput | Record<string, any>;
  error_message?: string;
  execution_time_ms?: number;
}

export interface DashboardRenderResponse {
  dashboard_name: string;
  selector_values: Record<string, any>;
  widgets: WidgetRenderResult[];
  total_execution_time_ms: number;
}
