/**
 * TypeScript types matching the Viz framework API schemas.
 *
 * These types correspond to the Pydantic schemas defined in registry/app/schemas.py
 * and registry/app/types.py
 */

// ============================================================================
// Enums (matching app/types.py)
// ============================================================================

export type InputType =
  // Text inputs
  | 'text_input'
  | 'textarea'
  | 'search_input'
  // Numeric inputs
  | 'numeric_input'
  | 'slider'
  | 'range_slider'
  | 'numeric_range'
  // Choice inputs
  | 'select'
  | 'multi_select'
  | 'radio'
  | 'checkbox'
  | 'checkbox_group'
  | 'toggle'
  // DateTime inputs
  | 'date'
  | 'date_range'
  | 'time'
  | 'datetime'
  | 'relative_date';

export type WidgetType = 'chart' | 'table' | 'metric' | 'text' | 'image' | 'custom';

export type LayoutType =
  | 'dashboard'
  | 'page'
  | 'section'
  | 'tabs'
  | 'tab'
  | 'row'
  | 'column'
  | 'widget'
  | 'input';

// Column width is now represented as weight (integer), not enum fraction

export type RenderOutputType = 'plotly' | 'vega_lite' | 'altair' | 'custom';

// ============================================================================
// Input Schemas (matching app/schemas.py InputSchema types)
// ============================================================================

export interface Option {
  value: any;
  label: string;
  selected?: boolean;
  disabled?: boolean;
  icon?: string | null;
  group?: string | null;
}

export interface InputDataSource {
  type: 'function' | 'api';
  alias?: string | null;
  params?: Record<string, any>;
}

export interface InputBase {
  type: 'input';
  id: string;
  input_type: InputType;
  label?: string | null;
  description?: string | null;
  default?: any;
  required: boolean;
  source?: InputDataSource | null;
  visible?: boolean;
  disabled?: boolean;
}

// Text Inputs
export interface TextInputSchema extends InputBase {
  input_type: 'text_input';
  min_length?: number | null;
  max_length?: number | null;
  pattern?: string | null;
  input_type_html?: string;
  autocomplete?: boolean;
  placeholder?: string | null;
}

export interface TextAreaSchema extends InputBase {
  input_type: 'textarea';
  min_length?: number | null;
  max_length?: number | null;
  rows?: number;
  resize?: 'none' | 'vertical' | 'horizontal' | 'both';
  placeholder?: string | null;
}

export interface SearchInputSchema extends InputBase {
  input_type: 'search_input';
  min_length?: number | null;
  clear_button?: boolean;
  debounce_ms?: number;
  placeholder?: string | null;
}

// Numeric Inputs
export interface NumericInputSchema extends InputBase {
  input_type: 'numeric_input';
  min_value?: number | null;
  max_value?: number | null;
  step?: number | null;
  prefix?: string | null;
  suffix?: string | null;
  placeholder?: string | null;
}

export interface SliderSchema extends InputBase {
  input_type: 'slider';
  min_value: number;
  max_value: number;
  step?: number | null;
  show_value?: boolean;
  show_ticks?: boolean;
}

export interface RangeSliderSchema extends InputBase {
  input_type: 'range_slider';
  min_value: number;
  max_value: number;
  step?: number | null;
  default?: [number, number | null] | null;
  show_values?: boolean;
}

export interface NumericRangeSchema extends InputBase {
  input_type: 'numeric_range';
  min_value?: number | null;
  max_value?: number | null;
  step?: number | null;
  default?: [number, number | null] | null;
  prefix?: string | null;
  suffix?: string | null;
}

// Choice Inputs
export interface SelectSchema extends InputBase {
  input_type: 'select';
  options?: Option[] | null;
  searchable?: boolean;
  clear_button?: boolean;
}

export interface MultiSelectSchema extends InputBase {
  input_type: 'multi_select';
  options?: Option[] | null;
  default?: any[] | null;
  max_selections?: number | null;
  searchable?: boolean;
}

export interface RadioGroupSchema extends InputBase {
  input_type: 'radio';
  options?: Option[] | null;
  layout?: 'vertical' | 'horizontal';
}

export interface CheckboxSchema extends InputBase {
  input_type: 'checkbox';
  default?: boolean | null;
}

export interface CheckboxGroupSchema extends InputBase {
  input_type: 'checkbox_group';
  options?: Option[] | null;
  default?: any[] | null;
  layout?: 'vertical' | 'horizontal' | 'grid';
  columns?: number | null;
}

export interface ToggleSchema extends InputBase {
  input_type: 'toggle';
  default?: boolean | null;
  on_label?: string | null;
  off_label?: string | null;
}

// DateTime Inputs
export interface DateInputSchema extends InputBase {
  input_type: 'date';
  min_date?: string | null;
  max_date?: string | null;
  format?: string;
  first_day_of_week?: number;
}

export interface DateRangeInputSchema extends InputBase {
  input_type: 'date_range';
  min_date?: string | null;
  max_date?: string | null;
  default?: [string, string | null] | null;
  format?: string;
  max_days?: number | null;
}

export interface TimeInputSchema extends InputBase {
  input_type: 'time';
  min_time?: string | null;
  max_time?: string | null;
  step_minutes?: number;
  format_24h?: boolean;
}

export interface DateTimeInputSchema extends InputBase {
  input_type: 'datetime';
  min_datetime?: string | null;
  max_datetime?: string | null;
  format?: string;
  format_24h?: boolean;
}

export interface RelativeDateInputSchema extends InputBase {
  input_type: 'relative_date';
  options: Array<{ [key: string]: string }>;
  allow_custom?: boolean;
}

// Union of all input schemas
export type InputSchema =
  | TextInputSchema
  | TextAreaSchema
  | SearchInputSchema
  | NumericInputSchema
  | SliderSchema
  | RangeSliderSchema
  | NumericRangeSchema
  | SelectSchema
  | MultiSelectSchema
  | RadioGroupSchema
  | CheckboxSchema
  | CheckboxGroupSchema
  | ToggleSchema
  | DateInputSchema
  | DateRangeInputSchema
  | TimeInputSchema
  | DateTimeInputSchema
  | RelativeDateInputSchema;

// ============================================================================
// Layout Schemas (matching app/schemas.py containers types)
// ============================================================================

export interface LayoutNodeBase {
  id: string;
  type: LayoutType;
}

export interface ParameterBinding {
  type: 'input';
  input_id: string;
}

export interface WidgetSchema extends LayoutNodeBase {
  type: 'widget';
  widget_type: WidgetType;
  component_alias?: string | null;
  params?: Record<string, any | ParameterBinding>;
  title?: string | null;
  description?: string | null;
  config?: Record<string, any>;
}

export interface ColumnSchema extends LayoutNodeBase {
  type: 'column';
  weight?: number;
  gap?: string | null;
  children: Array<RowSchema | ColumnSchema | WidgetSchema>;
}

export interface RowSchema extends LayoutNodeBase {
  type: 'row';
  gap?: string | null;
  align?: 'start' | 'center' | 'end' | 'stretch' | null;
  children: Array<RowSchema | ColumnSchema | WidgetSchema>;
}

export interface TabSchema extends LayoutNodeBase {
  type: 'tab';
  title: string;
  icon?: string | null;
  disabled?: boolean;
  children: Array<RowSchema | ColumnSchema | WidgetSchema>;
}

export interface TabsSchema extends LayoutNodeBase {
  type: 'tabs';
  default_tab?: string | null;
  children: TabSchema[];
}

export interface SectionSchema extends LayoutNodeBase {
  type: 'section';
  title?: string | null;
  collapsible?: boolean;
  collapsed?: boolean;
  children: Array<RowSchema | ColumnSchema | TabsSchema | WidgetSchema>;
}

export interface PageSchema extends LayoutNodeBase {
  type: 'page';
  title: string;
  description?: string | null;
  icon?: string | null;
  children: Array<SectionSchema | RowSchema | ColumnSchema | TabsSchema | WidgetSchema>;
}

export interface DashboardStructure {
  id: string;
  type: 'dashboard';
  title: string;
  description?: string | null;
  version?: string;
  children: PageSchema[];
}

// ============================================================================
// Dashboard API Types
// ============================================================================

export interface DashboardResponse {
  db_id: number;
  id: string;
  title: string;
  description?: string | null;
  structure: DashboardStructure;
  owner_id: number;
  created_at: string;
  updated_at: string;
}

export interface RenderOutput {
  type: RenderOutputType;
  data: Record<string, any> | string;
  config?: Record<string, any> | null;
}

export interface WidgetRenderResult {
  widget_id: string;
  component_alias: string;
  status: 'success' | 'error' | 'timeout';
  output?: Record<string, any> | RenderOutput | null;
  error_message?: string | null;
  execution_time_ms?: number | null;
}

export interface DashboardRenderResponse {
  dashboard_id: string;
  input_values: Record<string, any>;
  widgets: WidgetRenderResult[];
  total_execution_time_ms: number;
}

// ============================================================================
// Legacy Layout Types (for backward compatibility - can be removed later)
// ============================================================================

export interface InputLayoutSchema extends LayoutNodeBase {
  type: 'input';
  input: InputSchema;
}

// Helper type for any containers node
export type LayoutNode =
  | DashboardStructure
  | PageSchema
  | SectionSchema
  | RowSchema
  | ColumnSchema
  | TabsSchema
  | TabSchema
  | WidgetSchema
  | InputLayoutSchema;
