# Client Library Refactor Plan: DataSources & Widgets

## Status: ✅ COMPLETED (2024-11-30)

All 8 phases have been implemented successfully. See implementation notes at the bottom.

## Overview

Refactor the client library to introduce a unified `DataSource` concept and typed widget hierarchy, enabling widgets and inputs to be powered by multiple data backends (Timeseries Service, Components, Functions).

## Key Design Decisions

### Naming Convention
- **`name`** - human-defined identifier (timeseries name, component name, input name)
- **`id`** - auto-generated unique identifier (for LayoutNodes, widgets)

### Core Concepts

1. **DataSource** - identifies WHERE data comes from (reusable, no params)
2. **Params** - HOW to query the data source (per-usage, at widget/input level)
3. **Component** - data-only component with `load/transform`
4. **RenderableComponent** - component with `load/transform/render` (produces Plotly JSON)
5. **Widget** - visualization type (frontend-native or server-rendered)

### DataSource + Params Pattern
```python
# Define source once
stocks = TimeseriesSource(name="market.stocks")

# Reuse with different params
chart1 = LineChartWidget(data_source=stocks, params={"symbol": "AAPL"}, ...)
chart2 = LineChartWidget(data_source=stocks, params={"symbol": symbol_input}, ...)
```

---

## Implementation Plan

### Phase 1: Core DataSource Infrastructure

#### 1.1 Create `core/datasource.py`
- [x] `DataSource` - abstract base class
- [x] `TimeseriesSource(DataSource)` - references Timeseries Service by name
- [x] `ComponentSource(DataSource)` - references a Component class or name (non-generic due to Pydantic limitations)
- [x] `FunctionSource(DataSource)` - wraps a callable (migrate from inputs/sources.py)

```python
class DataSource(BaseModel, ABC):
    """Base for all data sources."""
    type: str

class TimeseriesSource(DataSource):
    type: Literal["timeseries"] = "timeseries"
    name: str  # e.g., "market.stocks.aapl"

T = TypeVar('T', bound='Component')

class ComponentSource(DataSource, Generic[T]):
    type: Literal["component"] = "component"
    component: type[T] | str  # Class or registered name

class FunctionSource(DataSource):
    type: Literal["function"] = "function"
    func: Callable[..., Any]
```

#### 1.2 Update `core/component.py`
- [x] Rename `Component` base class (keep `load/transform`, make `render` optional or remove)
- [x] Create `RenderableComponent(Component)` with abstract `render()` method
- [x] Update `DataSourceComponent` if still needed, or deprecate

```python
class Component(BaseModel, ABC):
    """Data-only component: load + transform."""

    @abstractmethod
    def load(self) -> Any: ...

    @abstractmethod
    def transform(self, data: Any) -> Any: ...

class RenderableComponent(Component, ABC):
    """Component that also renders (returns Plotly JSON, etc.)."""

    @abstractmethod
    def render(self, data: Any) -> Any: ...
```

#### 1.3 Update `core/__init__.py`
- [x] Export new classes: `DataSource`, `TimeseriesSource`, `ComponentSource`, `FunctionSource`, `RenderableComponent`

---

### Phase 2: Widget Hierarchy

#### 2.1 Create `widgets/` module structure
```
widgets/
├── __init__.py
├── base.py          # Widget abstract base
├── charts.py        # LineChartWidget, BarChartWidget, AreaChartWidget
├── table.py         # TableWidget
├── metric.py        # MetricWidget
└── plotly.py        # PlotlyWidget (server-rendered)
```

#### 2.2 Create `widgets/base.py`
- [x] `Widget(LeafNode, ABC)` - abstract base for all widgets
- [x] Common fields: `title`, `description`, `data_source`, `params`

```python
class Widget(LeafNode, ABC):
    """Abstract base for all widgets."""
    title: str | None = None
    description: str | None = None
    data_source: DataSource
    params: dict[str, Any] = Field(default_factory=dict)
```

#### 2.3 Create `widgets/charts.py`
- [x] `LineChartWidget` - frontend-native line chart
- [x] `BarChartWidget` - frontend-native bar chart
- [x] `AreaChartWidget` - frontend-native area chart

```python
class LineChartWidget(Widget):
    type: Literal["line_chart"] = "line_chart"
    x: str = "date"
    y: str | list[str] = "value"
    color: str | None = None
    # ... other config

class BarChartWidget(Widget):
    type: Literal["bar_chart"] = "bar_chart"
    x: str
    y: str | list[str]
    color: str | None = None
    orientation: Literal["vertical", "horizontal"] = "vertical"
```

#### 2.4 Create `widgets/table.py`
- [x] `TableWidget` - frontend-native data table

```python
class TableWidget(Widget):
    type: Literal["table"] = "table"
    columns: list[str] | None = None  # None = auto from data
    page_size: int = 10
    sortable: bool = True
```

#### 2.5 Create `widgets/metric.py`
- [x] `MetricWidget` - single KPI/metric display

```python
class MetricWidget(Widget):
    type: Literal["metric"] = "metric"
    value_field: str = "value"
    label: str | None = None
    format: str | None = None  # e.g., "{:.2f}%"
    comparison_field: str | None = None  # for delta display
```

#### 2.6 Create `widgets/plotly.py`
- [x] `PlotlyWidget` - server-rendered via RenderableComponent

```python
class PlotlyWidget(Widget):
    type: Literal["plotly"] = "plotly"
    data_source: ComponentSource[RenderableComponent]
    # No x, y, etc. - component.render() handles everything
```

#### 2.7 Create `widgets/__init__.py`
- [x] Export all widget classes

---

### Phase 3: Update Inputs to Use DataSource

#### 3.1 Update `inputs/base.py`
- [x] Change `source: FunctionSource` to `source: DataSource | None`
- [x] Add `params: dict[str, Any]` field for source params

#### 3.2 Migrate/Remove `inputs/sources.py`
- [x] `FunctionSource` moves to `core/datasource.py`
- [x] Update imports across codebase
- [x] Delete `inputs/sources.py` or keep as re-export for backward compatibility

#### 3.3 Update input classes
- [x] Ensure all inputs work with new `DataSource` pattern

---

### Phase 4: Update Existing Widget Code

#### 4.1 Refactor `layout/components.py`
- [x] Current `Widget` class becomes deprecated or renamed
- [x] Update to use new widget base or remove in favor of `widgets/`

#### 4.2 Update `layout/__init__.py`
- [x] Export new widget classes from `widgets/`
- [x] Deprecation warnings for old `Widget` if keeping

#### 4.3 Update `layout/containers.py`
- [x] Update type hints to accept new widget types

---

### Phase 5: Serialization & API Updates

#### 5.1 Update `api/serializer.py`
- [x] `serialize_widget()` - handle new widget types
- [x] `serialize_data_source()` - new function for DataSource serialization
- [x] Update `serialize_dashboard()` to handle new structure

#### 5.2 Update `api/extractor.py`
- [x] Extract DataSources from widgets and inputs
- [x] Handle TimeseriesSource, ComponentSource, FunctionSource

---

### Phase 6: Rename `alias` to `name`

#### 6.1 Update Component registration
- [x] `register_component(component, name=...)` instead of `alias`
- [x] Update `Component` if it has `__alias__` attribute (now `__component_name__`)

#### 6.2 Update serializers
- [x] Change `alias` fields to `name` in serialization output

#### 6.3 Update API client
- [x] Update `RegistryClient` methods to use `name`

---

### Phase 7: Testing & Documentation

#### 7.1 Test imports
- [x] All new classes importable from `viz`
- [x] No circular import issues

#### 7.2 Test widget creation
- [x] Each widget type with each DataSource type
- [x] Params binding with Inputs

#### 7.3 Test serialization
- [x] Dashboard with mixed widget types serializes correctly

#### 7.4 Update `viz/__init__.py`
- [x] Export new public API:
  - DataSources: `DataSource`, `TimeseriesSource`, `ComponentSource`, `FunctionSource`
  - Components: `Component`, `RenderableComponent`
  - Widgets: `LineChartWidget`, `BarChartWidget`, `TableWidget`, `MetricWidget`, `PlotlyWidget`

---

### Phase 8: Builder Updates

#### 8.1 Update `builder.py`
- [x] Add helper methods for new widget types:
  - `L.line_chart(data_source, x, y, ...)`
  - `L.bar_chart(data_source, x, y, ...)`
  - `L.area_chart(data_source, x, y, ...)`
  - `L.table(data_source, columns, ...)`
  - `L.metric(data_source, value_field, ...)`
  - `L.plotly(data_source)`
- [x] Remove old `L.widget()` method (replaced by typed methods)

---

## File Structure After Refactor

```
client/viz/
├── __init__.py              # Public API exports
├── builder.py               # LayoutBuilder with new widget helpers
├── core/
│   ├── __init__.py
│   ├── component.py         # Component, RenderableComponent
│   ├── context.py           # Builder context stack
│   ├── datasource.py        # DataSource, TimeseriesSource, ComponentSource, FunctionSource [NEW]
│   └── layout.py            # LayoutNode, LeafNode, Container
├── widgets/                 # [NEW]
│   ├── __init__.py
│   ├── base.py              # Widget base class
│   ├── charts.py            # LineChartWidget, BarChartWidget, AreaChartWidget
│   ├── table.py             # TableWidget
│   ├── metric.py            # MetricWidget
│   └── plotly.py            # PlotlyWidget
├── inputs/
│   ├── __init__.py
│   ├── base.py              # Input (updated to use DataSource)
│   ├── choice.py
│   ├── text.py
│   ├── numeric.py
│   └── date_time.py
├── layout/
│   ├── __init__.py
│   ├── containers.py        # Row, Column, Section, Tabs, Tab
│   ├── dashboard.py         # Dashboard, Page
│   └── enums.py             # WidgetType (may deprecate)
└── api/
    ├── __init__.py
    ├── serializer.py        # Updated for new types
    ├── extractor.py         # Updated for new types
    └── registry.py
```

---

## Migration Notes

### Breaking Changes
- `Widget` class replaced by specific widget types
- `alias` renamed to `name` throughout
- `FunctionSource` moved from `inputs/sources.py` to `core/datasource.py`

### Deprecations
- Old `Widget` class (provide migration path)
- `WidgetType` enum (widget type now implicit in class)
- `alias` parameter (use `name`)

### Backward Compatibility
- Keep old imports working with deprecation warnings where possible
- `inputs/sources.py` can re-export from `core/datasource.py`

---

## Implementation Notes

### Completed 2024-11-30

#### Key Changes Made
1. **DataSource classes in `core/datasource.py`**: Implemented non-generic due to Pydantic limitations with Generic types causing recursion errors
2. **Widget hierarchy in `widgets/`**: Created typed widget classes (LineChartWidget, BarChartWidget, AreaChartWidget, TableWidget, MetricWidget, PlotlyWidget)
3. **LegacyWidget for backward compatibility**: Old Widget class renamed to LegacyWidget with deprecation warning
4. **Serialization updated**: `serialize_data_source()`, `serialize_params()`, updated `serialize_widget()` to handle new types
5. **Extractor updated**: Now extracts from `data_source` field in widgets, handles all DataSource types
6. **`inputs/sources.py` deprecated**: Re-exports FunctionSource from `core/datasource.py` with deprecation warning

#### Implementation Decisions
- **ComponentSource without Generic[T]**: Pydantic's handling of Generic types caused recursion errors. Using `Any` type for component field instead.
- **PlotlyWidget takes ComponentSource**: Not typed to RenderableComponent since Generic was removed, but documentation indicates it should be a RenderableComponent
- **`__component_name__` attribute**: Components can define explicit name via `__component_name__` class attribute (replaces `__id__` / `__alias__`)
- **Regex escaping fixed**: Snake_case conversion regex properly escapes backreferences

#### Testing Verified
- All imports work without circular dependencies
- Widget creation with all DataSource types works
- Serialization produces correct JSON structure
- Component/function extraction from dashboard works correctly
- Builder factory methods work with context managers

#### Phase 8 Notes (Builder Updates)
- Added `L.line_chart()`, `L.bar_chart()`, `L.area_chart()`, `L.table()`, `L.metric()`, `L.plotly()` methods
- Removed old `L.widget()` method that used WidgetType enum
- All builder methods integrate with context managers for fluent API
- WidgetType enum kept for backward compatibility but marked as deprecated with warnings
