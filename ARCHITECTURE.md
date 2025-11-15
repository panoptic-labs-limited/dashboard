# Distributed Dashboarding Framework - Architecture

## Overview

A distributed dashboarding framework similar to Streamlit but with distributed compute capabilities. Users write dashboard definitions in Python, components execute server-side with strong isolation, and results are rendered in a web UI.

## Architecture Decisions

Based on requirements:
- **Execution Model**: Server-side (all stages in function registry)
- **Render Output**: JSON/dict with chart spec (e.g., Vega-Lite)
- **Data Flow**: Reactive parameters (automatic re-execution)
- **State Model**: Stateless (functional)

## System Architecture

```
┌─────────────────────────────────────────────────┐
│          Client Library (Python)                 │
│  User writes dashboard definition               │
│  ├── Components (load/transform/render)         │
│  ├── Layout (Dashboard/Page/Section/Row/Column) │
│  └── Selectors (Date/Dropdown/Input)            │
└─────────────────────────────────────────────────┘
                    │
                    │ Serializes to JSON spec
                    │ Registers components
                    ▼
┌─────────────────────────────────────────────────┐
│        Function Registry (Enhanced)              │
│  - Stores component classes                     │
│  - Executes load/transform/render server-side   │
│  - Returns JSON chart specs                     │
│  - Handles reactive parameter updates           │
│  - Stage selection (load, transform, render)    │
└─────────────────────────────────────────────────┘
                    │
                    │ REST API
                    ▼
┌─────────────────────────────────────────────────┐
│              UI Service                          │
│  - Renders dashboard layout                     │
│  - Displays selectors                           │
│  - Renders charts from JSON specs (Vega-Lite)   │
│  - Handles selector changes → triggers refresh  │
└─────────────────────────────────────────────────┘
```

## Component Model

### Base Component Class

Every component has three stages:

```python
class Component:
    def load(self, **params) -> Any:
        """Load/fetch data from source"""
        pass

    def transform(self, data: Any, **params) -> Any:
        """Transform/process the loaded data"""
        pass

    def render(self, data: Any, **params) -> dict:
        """Render data as JSON chart spec (Vega-Lite, etc.)"""
        pass
```

### Execution Stages

Callers can specify which stages to execute:
- `"load"` - Only execute load, return raw data
- `"load_transform"` - Execute load + transform, return processed data
- `"load_transform_render"` - Execute all stages, return chart spec (default)

### Component Registration

Components get registered to the function registry:
- Component class source code is stored
- Metadata includes: name, description, parameters, dependencies
- Each component gets a unique identifier

## Layout Hierarchy

```
Dashboard
├── Page (Tab 1)
│   ├── Section (must be first child)
│   │   ├── Row
│   │   │   ├── Column
│   │   │   │   └── Widget (Component instance)
│   │   │   └── Column
│   │   │       ├── DateSelector
│   │   │       └── Widget (Component instance)
│   │   └── Row
│   │       └── Column
│   │           └── Widget (Component instance)
│   └── Section
└── Page (Tab 2)
    └── Section
        └── Row
            └── Column
                └── Widget
```

### Layout Components

1. **Dashboard**
   - Top-level container
   - Contains multiple Pages
   - Has global configuration (title, theme)

2. **Page/View**
   - Represents a tab in the dashboard
   - Must have at least one Section as first child
   - Has title and optional description

3. **Section**
   - Groups related content
   - Can only be direct child of Page
   - Can contain Rows and Columns
   - Optional title and collapse functionality

4. **Row**
   - Horizontal layout container
   - Can contain Columns
   - Can be nested within Sections or Columns

5. **Column**
   - Vertical layout container
   - Can contain Widgets, Selectors, or nested Rows
   - Supports width specification (e.g., 1/2, 1/3, 1/4)

6. **Widget**
   - Wrapper around a Component instance
   - Handles parameter binding
   - Manages reactive updates

## Selectors

Selectors are interactive inputs that provide values to components.

### Selector Types

1. **DateSelector**
   - Single date picker
   - Date range picker
   - Returns: ISO date string or tuple of (start, end)

2. **DropdownSelector**
   - Single or multi-select dropdown
   - Options: static list or function that fetches options
   - Returns: selected value(s)

3. **TextInput**
   - Free-form text input
   - Optional validation regex
   - Returns: string

4. **NumericInput**
   - Number input with optional min/max
   - Optional step size
   - Returns: number

5. **RangeSelector** (future)
   - Slider for numeric range
   - Returns: number or tuple

### Selector Data Sources

Selectors can have a `data_source` function that gets registered:

```python
def get_available_dates():
    # Fetch available dates from database
    return ["2024-01-01", "2024-01-02", ...]

date_selector = DateSelector(
    name="report_date",
    data_source=get_available_dates,
    default="2024-01-01"
)
```

The data source function is registered in the function registry and called by the UI to populate the selector.

## Reactive Data Flow

### Parameter Binding

Components declare dependencies on selectors:

```python
class SalesChart(Component):
    def load(self, report_date: str, region: str):
        # Load sales data for given date and region
        query = f"SELECT * FROM sales WHERE date = '{report_date}' AND region = '{region}'"
        return execute_query(query)

    def transform(self, data, **params):
        # Transform data
        return process_sales_data(data)

    def render(self, data, **params):
        # Return Vega-Lite spec
        return {
            "mark": "bar",
            "encoding": {
                "x": {"field": "product", "type": "nominal"},
                "y": {"field": "sales", "type": "quantitative"}
            },
            "data": {"values": data}
        }

# Usage in dashboard
date_selector = DateSelector(name="report_date", default="2024-01-01")
region_selector = DropdownSelector(
    name="region",
    options=["North", "South", "East", "West"],
    default="North"
)

sales_chart = Widget(
    component=SalesChart(),
    params={
        "report_date": date_selector,
        "region": region_selector
    }
)
```

### Reactive Updates

1. User changes selector value in UI
2. UI service sends update to function registry
3. Function registry identifies dependent components
4. Re-executes dependent components with new parameter values
5. Returns updated results to UI
6. UI re-renders affected components

## Data Storage

### Enhanced Function Registry Schema

**Component Table** (extends existing Function table):
```sql
CREATE TABLE components (
    id SERIAL PRIMARY KEY,
    alias VARCHAR UNIQUE NOT NULL,
    type VARCHAR NOT NULL,  -- 'component', 'selector_data_source'
    class_name VARCHAR NOT NULL,
    source_code TEXT NOT NULL,
    description TEXT,
    owner_id INTEGER REFERENCES users(id),

    -- Component metadata
    parameters JSONB,  -- Parameter schema
    dependencies JSONB,  -- List of selector dependencies

    -- Resource configuration
    memory_limit_mb INTEGER DEFAULT 200,
    timeout_seconds INTEGER DEFAULT 30,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**Dashboard Table**:
```sql
CREATE TABLE dashboards (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    title VARCHAR NOT NULL,
    description TEXT,
    owner_id INTEGER REFERENCES users(id),

    -- Dashboard structure as JSON
    structure JSONB NOT NULL,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**Dashboard Structure JSON**:
```json
{
    "title": "Sales Dashboard",
    "pages": [
        {
            "id": "page1",
            "title": "Overview",
            "sections": [
                {
                    "id": "section1",
                    "title": "Sales Metrics",
                    "layout": {
                        "type": "row",
                        "children": [
                            {
                                "type": "column",
                                "width": "1/2",
                                "children": [
                                    {
                                        "type": "selector",
                                        "selector_type": "date",
                                        "name": "report_date",
                                        "default": "2024-01-01"
                                    }
                                ]
                            },
                            {
                                "type": "column",
                                "width": "1/2",
                                "children": [
                                    {
                                        "type": "widget",
                                        "component_id": "sales_chart_component",
                                        "params": {
                                            "report_date": {"type": "selector", "name": "report_date"}
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        }
    ]
}
```

## API Enhancements

### New Endpoints

**Component Registration**:
```
POST /components/
- Register a new component class
- Body: component source code, metadata, parameters

GET /components/
- List user's components

GET /components/{alias}
- Get component details

PUT /components/{alias}
- Update component code

DELETE /components/{alias}
- Delete component
```

**Component Execution**:
```
POST /execute/component/{alias}
- Execute component with stage selection
- Body: {
    "stage": "load" | "load_transform" | "load_transform_render",
    "params": {...}
  }
- Returns: execution result based on stage
```

**Dashboard Management**:
```
POST /dashboards/
- Create a new dashboard
- Body: dashboard structure JSON

GET /dashboards/
- List user's dashboards

GET /dashboards/{name}
- Get dashboard structure and metadata

PUT /dashboards/{name}
- Update dashboard structure

DELETE /dashboards/{name}
- Delete dashboard
```

**Dashboard Rendering**:
```
GET /dashboards/{name}/render
- Render entire dashboard
- Executes all components with current selector values
- Returns: component outputs ready for UI

POST /dashboards/{name}/update
- Update selector value and re-render affected components
- Body: {
    "selector": "report_date",
    "value": "2024-01-15"
  }
- Returns: updated component outputs
```

## Client Library API

### Example Usage

```python
from viz import Dashboard, Page, Section, Row, Column, Widget
from viz import DateSelector, DropdownSelector, NumericInput
from viz import Component, register

# Define a component
class SalesChart(Component):
    def load(self, start_date: str, end_date: str, region: str):
        # Load data from database
        return db.query(f"""
            SELECT date, product, sales
            FROM sales
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
            AND region = '{region}'
        """)

    def transform(self, data):
        # Process data
        return aggregate_by_product(data)

    def render(self, data):
        # Return Vega-Lite spec
        return {
            "mark": "bar",
            "encoding": {
                "x": {"field": "product", "type": "nominal"},
                "y": {"field": "sales", "type": "quantitative"}
            },
            "data": {"values": data}
        }

# Create dashboard
dashboard = Dashboard(
    name="sales_dashboard",
    title="Sales Analytics Dashboard"
)

# Add selectors
date_selector = DateSelector(
    name="report_date",
    default="2024-01-01",
    label="Report Date"
)

region_selector = DropdownSelector(
    name="region",
    options=["North", "South", "East", "West"],
    default="North",
    label="Region"
)

# Create page
overview_page = Page(
    title="Overview",
    sections=[
        Section(
            title="Sales Metrics",
            layout=Row([
                Column(
                    width="1/3",
                    children=[date_selector, region_selector]
                ),
                Column(
                    width="2/3",
                    children=[
                        Widget(
                            component=SalesChart(),
                            params={
                                "report_date": date_selector,
                                "region": region_selector
                            }
                        )
                    ]
                )
            ])
        )
    ]
)

dashboard.add_page(overview_page)

# Register and deploy
dashboard.register()  # Registers all components and dashboard structure
```

## Implementation Phases

### Phase 1: Function Registry Enhancement
- Update executor to support class-based components
- Add support for load/transform/render stages
- Update database schema (add components table)
- Update API endpoints for component registration
- Add stage selection to execution endpoint

### Phase 2: Client Library Core
- Base Component class
- Component registration mechanism
- Serialization utilities
- API client for interacting with function registry

### Phase 3: Layout Components
- Dashboard class
- Page class
- Section class
- Row and Column classes
- Widget wrapper
- Layout validation

### Phase 4: Selectors
- Base Selector class
- DateSelector
- DropdownSelector
- TextInput
- NumericInput
- Selector data source registration
- Parameter binding system

### Phase 5: Dashboard Management
- Dashboard registration API
- Dashboard CRUD endpoints
- Dashboard rendering logic
- Reactive update system

### Phase 6: UI Service (Future)
- React/Vue frontend
- Dashboard renderer
- Vega-Lite chart rendering
- Selector components
- Reactive update handling
- WebSocket for real-time updates

## Technology Stack

### Backend (Function Registry)
- FastAPI (existing)
- PostgreSQL (existing)
- ProcessPoolExecutor (existing)
- Pydantic for validation
- SQLAlchemy ORM

### Client Library
- Pure Python
- Minimal dependencies
- Serialization: JSON
- HTTP client: httpx

### UI Service (Future)
- Frontend: React/Svelte
- Chart rendering: Vega-Lite + react-vega
- State management: React Context / Zustand
- WebSocket: socket.io

## Security Considerations

1. **Code Execution Isolation**
   - Components execute in isolated processes (existing)
   - Resource limits enforced (existing)
   - Restricted imports and globals

2. **Authentication**
   - JWT authentication (existing)
   - Component ownership validation
   - Dashboard access control

3. **Input Validation**
   - Validate selector values
   - Sanitize SQL queries in components
   - Validate component parameters

4. **Rate Limiting**
   - Limit component execution frequency
   - Prevent abuse of reactive updates

## Future Enhancements

1. **Caching**
   - Cache component outputs
   - Invalidate on selector changes
   - TTL-based cache expiration

2. **Async Execution**
   - Long-running components execute async
   - Progress updates via WebSocket
   - Background job queue

3. **Collaboration**
   - Share dashboards with other users
   - Role-based access control
   - Comment system

4. **Versioning**
   - Component versioning
   - Dashboard versioning
   - Rollback capability

5. **Advanced Selectors**
   - Range selectors
   - Multi-date pickers
   - Cascading dropdowns
   - Search/autocomplete

6. **Export**
   - Export dashboard as PDF
   - Export data as CSV/Excel
   - Scheduled reports