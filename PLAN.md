# Registry API Refactor & CLI Implementation Plan

**Status**: Finalized - Ready for Implementation
**Date**: 2025-11-25
**Phase**: Registry API Update + CLI Development

## Decisions Summary

### Naming & Identification (Q1-Q3)
- ✅ Use `id` field everywhere (no separate `name` field)
- ✅ **Required IDs**: Dashboard, Page, Widget, Input (user must specify)
- ✅ **Optional IDs**: Section, Row, Column, Tabs, Tab (auto-generated if not provided)
- ✅ Input `id` serves as both unique identifier AND parameter binding key
- ✅ API endpoints use `id`: `GET /dashboards/{id}`, not `{name}`

### Component System (Q2, Q7, Q8)
- ✅ **Two component types**:
  1. **Class-based**: Full load/transform/render pipeline
     - Use `__id__ = "component_alias"` class variable for identification
     - Auto-extract parameters from type hints via Pydantic
     - Support default values and optional parameters
  2. **Function-based**: Data-only (no rendering)
     - Use `@component(id="function_alias")` decorator
     - Current scope: Input data sources only
     - Future scope: Data sources for predefined widgets (LinePlot, etc.)
- ✅ **Update detection**: Registry handles it (compare source_code on PUT)
  - Client always PUTs, registry only writes if changed
  - Returns `{"updated": true/false}` to indicate if update occurred

### Input System (Q4-Q6, Q10)
- ✅ **Cascading inputs supported**: FunctionSource can reference other inputs
  - Example: `FunctionSource(func=get_regions, params={"country": country_input})`
  - Serializes as: `{"type": "input", "id": "country"}`
- ✅ **Static + dynamic options**: Static shown initially, replaced when source loads
  - Provides immediate UI, progressive enhancement
  - Static acts as fallback if source fails
- ✅ **Field serialization**: Flatten all fields to top level (no nested `config`)
  - Core fields (options, default) + display fields (searchable, clear_button) at same level

### Serialization & Schema (Q9, Q11)
- ✅ **Consistent `type` field** everywhere for discriminated unions
- ✅ **Widget fields**: `id`, `widget_type`, `component_alias`, `params`, `title`, `description`, `config` (optional)
- ✅ **Type + subtype pattern**: `type: "input"` + `input_type: "select"`

### CLI Behavior (Q12-Q14)
- ✅ **File watching**: Main file + local imports (not stdlib/packages)
- ✅ **Validation errors**: Abort and show clear errors (fail fast)
- ✅ **Alias conflicts**: Auto-update/replace existing (idempotent)

### Layout System (Q15-Q16)
- ✅ **Container children**: Pydantic type hints auto-enforce valid children
- ✅ **Input placement**: Inputs can be placed anywhere in layout

### Future Enhancements
- 🔮 **Namespace support**: `streamviz serve --namespace=dev` for environment isolation
- 🔮 **Predefined widgets**: LinePlot, BarChart, Table (use function-based components as data sources)
- 🔮 **Advanced validation**: Semantic validation, dependency analysis

## Overview

Update the registry API to match the refactored client library and implement a Streamlit-like CLI for dashboard development. The client has been significantly refactored with the new Input system and Pydantic layout models. The registry needs to be updated to support the new client architecture.

## Current State

### ✅ Client Library (Complete):
- New Input system (Select, DateInput, NumericInput, etc.)
- Input config classes with inheritance pattern
- FunctionSource pattern for dynamic options
- Pydantic layout system (Dashboard, Page, Section, Row, Column, Widget, Tabs, Tab)
- LayoutBuilder with context manager API (`L.dashboard()`, `L.input()`, etc.)

### 🚧 Registry (Needs Update):
- Still uses "Selector" terminology (need to rename to "Input")
- API schemas need alignment with new client Input classes
- Dashboard structure schemas need update for new layout system
- Need clear separation between Python executor and dashboard registry

### ⭐ New Requirements:
1. Update registry API to match new client library
2. Implement CLI (`streamviz serve <path>`)
3. Recognize two logical services within registry
4. Generate client API code from registry OpenAPI spec (no shared schemas)

## Code Generation Strategy

**Single Source of Truth**: Registry owns the API contract via OpenAPI specification.

**Client Code Generation**:
```bash
# Registry exposes OpenAPI spec
GET /openapi.json

# Option A: Generate schemas only
datamodel-code-generator \
  --url http://localhost:8000/openapi.json \
  --output viz/api/generated/schemas.py \
  --input-file-type openapi

# Option B: Generate full client (schemas + typed API methods) ✅ Recommended
openapi-python-client generate \
  --url http://localhost:8000/openapi.json \
  --output-path viz/api/generated \
  --overwrite
```

**Benefits**:
- ✅ Registry is single source of truth (no `viz_shared` needed)
- ✅ Client schemas auto-sync with registry API
- ✅ Type-safe API client with autocomplete
- ✅ No manual schema maintenance or duplication
- ✅ Generated code committed to git for IDE support

**Generated Files**:
- `viz/api/generated/schemas.py` - Pydantic models for API requests/responses
- `viz/api/generated/client.py` - Auto-generated API client (optional)

**Workflow**:
1. Update registry API endpoints and schemas
2. Run code generator to update client
3. Commit generated code to git
4. Client uses generated schemas for type safety

## Architecture: Two Logical Services

While implemented as a single FastAPI service, we have two distinct domains:

### Service 1: Distributed Python Executor
**Purpose**: Store and execute Python code (functions and components) with isolation

**Responsibilities**:
- Store function/component source code
- Execute code in isolated processes
- Track execution history and metrics
- Enforce resource limits

**Models**: `Function`, `Component`, `Execution`, `ComponentExecution`

### Service 2: Dashboard Schema Registry
**Purpose**: Store and manage dashboard layout definitions (pure JSON schemas)

**Responsibilities**:
- Store dashboard structures (layout hierarchy)
- Validate dashboard schemas
- Orchestrate component rendering
- Manage dashboard CRUD operations

**Models**: `Dashboard`

## Registration Flow

The client library has raw references (Python objects), but the registry stores aliases:

```python
# Client code (user writes this)
from viz import L, Select, Component, component

# Define a data source function
@component(id="get_regions")
def get_regions():
    return ["North", "South", "East", "West"]

# Define an input with dynamic source
region = L.input(Select(
    id="region",
    label="Region",
    source=get_regions  # Function reference
))

# Define a component
class SalesMetrics(Component):
    __id__ = "sales_metrics"

    region: str

    def load(self):
        return fetch_sales(self.region)

    def transform(self, data):
        return process_data(data)

    def render(self, data):
        import plotly.express as px
        return px.bar(data, x="product", y="sales")

# Use in dashboard
with L.dashboard(id="sales_dashboard", title="Sales Dashboard"):
    with L.page(id="overview", title="Overview"):
        with L.section(title="Metrics"):
            with L.row():
                L.input(region)  # Already defined above
                L.widget(SalesMetrics(region=region), id="sales_chart")

# Register everything
dashboard = L.get_dashboard()
dashboard.register(client=registry_client)
```

**Registration Process** (what happens during `dashboard.register()`):

1. **Extract all function-based components**
   - Find all functions decorated with `@component(id=...)`
   - Register each function → `PUT /functions/{id}`
   - Store mapping: function object → alias

2. **Extract all class-based components**
   - Find all Component instances in widgets
   - Register each component class → `PUT /components/{alias}` (using `__id__`)
   - Store mapping: component class → alias

3. **Build Dashboard Schema**
   - Serialize layout hierarchy to JSON
   - Replace all raw Python references with aliases
   - Input sources: `source=get_regions` → `"source": {"type": "function", "alias": "get_regions"}`
   - Input params: `country=country_input` → `"params": {"country": {"type": "input", "id": "country"}}`
   - Widget components: `SalesMetrics(region=region)` → `{"component_alias": "sales_metrics", "params": {"region": {"type": "input", "id": "region"}}}`
   - Auto-generate IDs for layout elements (Section, Row, Column) if not provided

4. **Register Dashboard**
   - POST dashboard schema (pure JSON, no Python code) to registry
   - Schema contains only aliases and IDs, no executable code

## Updated API Specification

### Common Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

---

## Service 1: Distributed Python Executor

### Functions API

#### `POST /functions/`
Create/register a function (for data sources, utilities, etc.)

**Request**:
```json
{
  "alias": "get_regions",
  "code": "def get_regions():\n    return ['North', 'South', 'East', 'West']",
  "description": "Get available regions",
  "memory_limit_mb": 200,
  "timeout_seconds": 30
}
```

**Response** (201):
```json
{
  "id": 1,
  "alias": "get_regions",
  "code": "def get_regions():\n    ...",
  "description": "Get available regions",
  "owner_id": 1,
  "memory_limit_mb": 200,
  "timeout_seconds": 30,
  "created_at": "2025-11-25T10:00:00Z",
  "updated_at": "2025-11-25T10:00:00Z"
}
```

#### `GET /functions/`
List all functions owned by current user

**Response** (200):
```json
[
  {
    "id": 1,
    "alias": "get_regions",
    "description": "Get available regions",
    ...
  }
]
```

#### `GET /functions/{alias}`
Get function details

**Response** (200):
```json
{
  "id": 1,
  "alias": "get_regions",
  "code": "def get_regions():\n    ...",
  ...
}
```

#### `PUT /functions/{alias}`
Update function code/config

**Request**:
```json
{
  "code": "def get_regions():\n    return ['North', 'South']",
  "description": "Updated regions"
}
```

#### `DELETE /functions/{alias}`
Delete function (204 No Content)

---

### Components API

#### `POST /components/`
Create/register a component

**Request**:
```json
{
  "alias": "sales_metrics",
  "class_name": "SalesMetrics",
  "source_code": "class SalesMetrics(Component):\n    region: str\n    ...",
  "description": "Sales metrics by region",
  "parameters": [
    {
      "name": "region",
      "type": "str",
      "required": true,
      "description": "Region to filter by"
    }
  ],
  "metadata": {
    "name": "Sales Metrics",
    "author": "Data Team",
    "version": "1.0.0",
    "tags": ["sales", "metrics"]
  },
  "memory_limit_mb": 200,
  "timeout_seconds": 30
}
```

**Response** (201):
```json
{
  "id": 1,
  "alias": "sales_metrics",
  "class_name": "SalesMetrics",
  "source_code": "class SalesMetrics(Component):\n    ...",
  "description": "Sales metrics by region",
  "parameters": [...],
  "metadata": {...},
  "owner_id": 1,
  "memory_limit_mb": 200,
  "timeout_seconds": 30,
  "created_at": "2025-11-25T10:00:00Z",
  "updated_at": "2025-11-25T10:00:00Z"
}
```

#### `GET /components/`
List all components

#### `GET /components/{alias}`
Get component details

#### `PUT /components/{alias}`
Update component

#### `DELETE /components/{alias}`
Delete component

---

### Execution API

#### `POST /execute/function/{alias}`
Execute a function

**Request**:
```json
{
  "params": {}
}
```

**Response** (200):
```json
{
  "id": 1,
  "function_id": 1,
  "status": "success",
  "output": {
    "result": ["North", "South", "East", "West"]
  },
  "execution_time_ms": 15.3,
  "memory_used_mb": 12.5,
  "started_at": "2025-11-25T10:00:00Z",
  "completed_at": "2025-11-25T10:00:01Z"
}
```

#### `POST /execute/component/{alias}`
Execute a component with stage selection

**Request**:
```json
{
  "stage": "load_transform_render",
  "params": {
    "region": "North"
  }
}
```

**Response** (200):
```json
{
  "id": 1,
  "component_id": 1,
  "status": "success",
  "stage": "load_transform_render",
  "output": {
    "type": "plotly",
    "data": {...}  // Serialized Plotly figure
  },
  "execution_time_ms": 234.5,
  "memory_used_mb": 45.2,
  "started_at": "2025-11-25T10:00:00Z",
  "completed_at": "2025-11-25T10:00:01Z"
}
```

---

## Service 2: Dashboard Schema Registry

### Dashboards API

#### `POST /dashboards/`
Create/register a dashboard

**Request**:
```json
{
  "id": "sales_dashboard",
  "title": "Sales Analytics Dashboard",
  "description": "Track sales metrics by region",
  "structure": {
    "type": "dashboard",
    "id": "sales_dashboard",
    "title": "Sales Analytics Dashboard",
    "pages": [
      {
        "type": "page",
        "id": "overview",
        "title": "Overview",
        "children": [
          {
            "type": "section",
            "id": "metrics_section_auto_123",
            "title": "Metrics",
            "children": [
              {
                "type": "row",
                "id": "row_auto_456",
                "children": [
                  {
                    "type": "column",
                    "id": "col_auto_789",
                    "width": "1/3",
                    "children": [
                      {
                        "type": "input",
                        "id": "region",
                        "input_type": "select",
                        "label": "Region",
                        "options": [],
                        "source": {
                          "type": "function",
                          "alias": "get_regions"
                        },
                        "default": "North",
                        "searchable": false,
                        "clear_button": false
                      }
                    ]
                  },
                  {
                    "type": "column",
                    "id": "col_auto_abc",
                    "width": "2/3",
                    "children": [
                      {
                        "type": "widget",
                        "id": "sales_chart",
                        "widget_type": "chart",
                        "component_alias": "sales_metrics",
                        "title": "Sales by Product",
                        "params": {
                          "region": {
                            "type": "input",
                            "id": "region"
                          }
                        }
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
}
```

**Response** (201):
```json
{
  "id": "sales_dashboard",
  "title": "Sales Analytics Dashboard",
  "description": "Track sales metrics by region",
  "structure": {...},
  "owner_id": 1,
  "created_at": "2025-11-25T10:00:00Z",
  "updated_at": "2025-11-25T10:00:00Z"
}
```

#### `GET /dashboards/`
List all dashboards

#### `GET /dashboards/{id}`
Get dashboard details

#### `PUT /dashboards/{id}`
Update dashboard schema

#### `DELETE /dashboards/{id}`
Delete dashboard

---

### Dashboard Rendering API

#### `POST /dashboards/{id}/render`
Render entire dashboard (execute all components)

**Request**:
```json
{
  "input_values": {
    "region": "North",
    "date": "2025-01-01"
  }
}
```

**Response** (200):
```json
{
  "dashboard_id": "sales_dashboard",
  "input_values": {
    "region": "North",
    "date": "2025-01-01"
  },
  "widgets": [
    {
      "widget_id": "sales_chart",
      "component_alias": "sales_metrics",
      "status": "success",
      "output": {
        "type": "plotly",
        "data": {...}
      },
      "execution_time_ms": 234.5
    }
  ],
  "total_execution_time_ms": 250.0
}
```

#### `POST /dashboards/{id}/widgets/{widget_id}/render`
Render a single widget (for reactive updates)

**Request**:
```json
{
  "input_values": {
    "region": "South"
  }
}
```

**Response** (200):
```json
{
  "widget_id": "sales_chart",
  "component_alias": "sales_metrics",
  "status": "success",
  "output": {
    "type": "plotly",
    "data": {...}
  },
  "execution_time_ms": 234.5,
  "memory_used_mb": 45.2
}
```

#### `GET /dashboards/{id}/inputs/{input_id}/data`
Get data for a dynamic input (execute data source function)

**Query Parameters**:
- `input_values` (optional): JSON object of current input values for cascading inputs

**Response** (200):
```json
{
  "input_id": "region",
  "type": "dynamic",
  "options": ["North", "South", "East", "West"],
  "execution_time_ms": 15.3
}
```

---

## CLI Implementation: `streamviz`

### Overview
A Click-based CLI similar to Streamlit/FastAPI for dashboard development.

### Commands

#### `streamviz serve <path>`
Start development server with auto-reload

**Usage**:
```bash
streamviz serve examples/sales_dashboard.py

# With options
streamviz serve examples/sales_dashboard.py --registry-url http://localhost:8000 --watch
```

**Options**:
- `--registry-url URL`: Registry API URL (default: `http://localhost:8000`)
- `--username TEXT`: Registry username (or use env `VIZ_USERNAME`)
- `--password TEXT`: Registry password (or use env `VIZ_PASSWORD`)
- `--watch / --no-watch`: Enable file watching (default: enabled)
- `--validate / --no-validate`: Enable validation (default: enabled)
- `--port INTEGER`: Port for local preview server (default: 3000)

**Behavior**:
1. Load dashboard file (execute Python code)
2. Validate dashboard structure
3. Extract functions, components, inputs
4. Register everything with registry
5. Watch file for changes
6. On change detected:
   - Re-execute dashboard file
   - Re-register functions/components (if changed)
   - Update dashboard schema
   - Print summary of changes

**Output**:
```
✓ Loaded dashboard: Sales Analytics Dashboard
✓ Registered 3 functions
✓ Registered 2 components
✓ Registered dashboard: sales_dashboard
✓ Dashboard URL: http://localhost:8000/dashboards/sales_dashboard

Watching for changes... (Press Ctrl+C to stop)

[10:05:32] File changed: examples/sales_dashboard.py
[10:05:32] Re-registering...
[10:05:33] ✓ Updated component: sales_metrics
[10:05:33] ✓ Updated dashboard schema
```

#### `streamviz validate <path>`
Validate dashboard file without registering

**Usage**:
```bash
streamviz validate examples/sales_dashboard.py
```

**Checks**:
- Python syntax errors
- Import errors
- Dashboard structure validation
- Input name uniqueness
- Component parameter bindings
- Missing function/component definitions

**Output**:
```
✓ No syntax errors
✓ All imports resolved
✓ Dashboard structure valid
⚠ Warning: Input 'region' has no default value
⚠ Warning: Component 'sales_metrics' parameter 'region' not bound to input
✗ Error: Input name 'date' used twice

Validation failed with 1 error, 2 warnings
```

#### `streamviz init <name>`
Create a new dashboard from template

**Usage**:
```bash
streamviz init my_dashboard
```

**Creates**:
```
my_dashboard/
├── dashboard.py          # Main dashboard file
├── components/           # Custom components
│   └── __init__.py
└── data_sources/         # Data source functions
    └── __init__.py
```

**Note**: No `requirements.txt` - executor runs in pre-built environment with pre-installed packages.

#### `streamviz list`
List registered dashboards

**Usage**:
```bash
streamviz list --registry-url http://localhost:8000
```

**Output**:
```
Registered Dashboards:
- sales_dashboard (Sales Analytics Dashboard)
  URL: http://localhost:8000/dashboards/sales_dashboard
  Updated: 2025-11-25 10:05:33

- marketing_dashboard (Marketing Metrics)
  URL: http://localhost:8000/dashboards/marketing_dashboard
  Updated: 2025-11-24 15:30:00
```

---

## Implementation Tasks

### Phase 1: Update Registry API Schemas & Models
- [ ] Define new Pydantic schemas in registry for updated API
  - [ ] `InputType` enum (was `SelectorType`)
  - [ ] Input-related request/response schemas
  - [ ] Dashboard structure schemas with new layout format
  - [ ] Parameter binding schemas (use `input_id` not `selector_name`)
- [ ] Update registry database models
- [ ] Update Dashboard model to store new structure format
- [ ] Add migration script (if needed)
- [ ] Update example dashboard structures in tests

### Phase 2: Update Registry API Endpoints
- [ ] Update endpoint paths to use `{id}` instead of `{name}`
- [ ] Rename parameter names: `selector_values` → `input_values`
- [ ] Update `/dashboards/{id}/render` request/response schemas
- [ ] Add `/dashboards/{id}/widgets/{widget_id}/render` endpoint
- [ ] Update `/dashboards/{id}/inputs/{input_id}/data` endpoint
  - [ ] Support cascading inputs via query parameters
- [ ] Update helper functions: `_find_selector_in_dashboard` → `_find_input_in_dashboard`
- [ ] Add `PUT /components/{alias}` idempotent update logic
- [ ] Add `PUT /functions/{alias}` idempotent update logic

### Phase 3: Generate Client API Code
- [ ] Choose generation tool:
  - Option A: `datamodel-code-generator` (schemas only)
  - Option B: `openapi-python-client` (full client with typed methods) ✅ **Recommended**
- [ ] Install generator in client dev dependencies
- [ ] Create generation script: `scripts/generate_api_client.sh`
- [ ] Generate client from registry OpenAPI spec → `viz/api/generated/`
  - [ ] Generates schemas (Pydantic models)
  - [ ] Generates client class with typed methods for each endpoint
  - [ ] Generates error types
- [ ] Configure `.gitignore` to commit generated code
- [ ] Add CI step to verify generated code is up-to-date

### Phase 4: Client Serialization Layer
- [ ] Create `viz/api/serializer.py` module
- [ ] Implement `serialize_input(input: Input) -> InputSchema`
  - [ ] Import generated `InputSchema` from `viz.api.generated.models`
  - [ ] Handle all input types (Select, DateInput, etc.)
  - [ ] Flatten fields to top level (no nested config)
  - [ ] Convert FunctionSource to `{"type": "function", "alias": "..."}`
  - [ ] Handle cascading input params
  - [ ] Return typed Pydantic model (not dict)
- [ ] Implement `serialize_component(component: Component) -> ComponentCreateSchema`
  - [ ] Extract `__id__` and source code
  - [ ] Auto-extract parameters from Pydantic fields
  - [ ] Return typed schema model
- [ ] Implement `serialize_dashboard(dashboard: Dashboard) -> DashboardCreateSchema`
  - [ ] Recursively serialize layout hierarchy
  - [ ] Auto-generate IDs for optional elements (Section, Row, Column)
  - [ ] Replace Python object references with aliases/IDs
  - [ ] Return typed schema model
- [ ] Create `viz/api/extractor.py` module
  - [ ] Extract all function-based components (find `@component` decorators)
  - [ ] Extract all class-based components (find Component subclasses in widgets)
  - [ ] Deduplicate functions used in multiple inputs
  - [ ] Return mappings: object → alias

### Phase 5: Client Registration System
- [ ] Create `viz/api/registry.py` module
- [ ] Create `RegistryClient` class (or use generated client directly)
  - [ ] Wraps generated API client from Phase 3
  - [ ] Handles authentication (username/password → JWT)
  - [ ] Provides convenient registration methods
- [ ] Implement registration flow:
  - [ ] `register_functions()` - Serialize and PUT using generated client
  - [ ] `register_components()` - Serialize and PUT using generated client
  - [ ] `register_dashboard()` - Serialize and POST using generated client
- [ ] Add `Dashboard.register(client)` convenience method
- [ ] Handle errors and provide clear, actionable feedback
- [ ] Add progress indicators (using `rich`)

### Phase 6: CLI Implementation
- [ ] Set up Click CLI structure (`viz/cli/__init__.py`)
- [ ] Implement `streamviz serve` command
- [ ] Add file watching with `watchdog`
- [ ] Implement validation logic
- [ ] Implement `streamviz validate` command
- [ ] Implement `streamviz init` command
- [ ] Implement `streamviz list` command
- [ ] Add console output formatting with `rich`
- [ ] Add configuration file support (.streamviz.toml)

### Phase 7: Documentation & Testing
- [ ] Update ARCHITECTURE.md with new API
- [ ] Update PROJECT_CONTEXT.md
- [ ] Add API documentation to README
- [ ] Add CLI documentation
- [ ] Add integration tests for registration flow
- [ ] Add CLI tests
- [ ] Update examples to use new API

---

## Dashboard Structure Schema (New Format)

This is what gets stored in the database after registration:

```json
{
  "type": "dashboard",
  "id": "sales_dashboard",
  "title": "Sales Analytics Dashboard",
  "description": "Track sales metrics",
  "version": "1.0.0",
  "pages": [
    {
      "type": "page",
      "id": "overview",
      "title": "Overview",
      "description": null,
      "children": [
        {
          "type": "section",
          "id": "section_auto_abc123",
          "title": "Metrics",
          "collapsible": false,
          "collapsed": false,
          "children": [
            {
              "type": "row",
              "id": "row_auto_def456",
              "gap": "16px",
              "children": [
                {
                  "type": "column",
                  "id": "col_auto_ghi789",
                  "width": "1/3",
                  "gap": "8px",
                  "children": [
                    {
                      "type": "input",
                      "id": "region",
                      "input_type": "select",
                      "label": "Region",
                      "default": "North",
                      "required": true,
                      "options": ["North", "South"],
                      "source": {
                        "type": "function",
                        "alias": "get_regions"
                      },
                      "searchable": false,
                      "clear_button": false
                    }
                  ]
                },
                {
                  "type": "column",
                  "id": "col_auto_jkl012",
                  "width": "2/3",
                  "children": [
                    {
                      "type": "widget",
                      "id": "sales_chart",
                      "widget_type": "chart",
                      "component_alias": "sales_metrics",
                      "title": "Sales by Product",
                      "description": "Bar chart showing sales by product category",
                      "params": {
                        "region": {
                          "type": "input",
                          "id": "region"
                        }
                      }
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

**Key Points**:
- Dashboard, Page, Widget, Input IDs are user-specified (required)
- Section, Row, Column IDs are auto-generated with `_auto_` prefix (optional)
- Input fields are flattened (no nested `config` object)
- Input `id` matches component parameter names for binding
- Widget params reference inputs by `id` using `{"type": "input", "id": "..."}`
- Source functions referenced by `alias` from function registry

---

## Implementation Notes

### Function Deduplication
If multiple inputs use the same function-based component, register once and reuse alias across all inputs.

### Component Updates
When component code changes, update in-place (same alias). All dashboards using that component automatically use the new version on next render.

### CLI Preview Server
Phase 1: `streamviz serve` just registers with registry and prints dashboard URL.
Phase 2 (future): Add local preview server that proxies to registry.

### Validation Depth
Start with basic validation (syntax, structure, required fields). Add semantic validation (parameter binding, dependency analysis) in later iterations.

### Execution Environment
Dashboards execute in a **pre-built Python environment** with pre-installed packages. Users cannot specify custom dependencies per dashboard. The executor environment should include common data science packages (pandas, numpy, plotly, etc.) but users must work within those constraints.

---

## Technology Stack Updates

### Client Dependencies (Production)
- `httpx` - HTTP client (already in project)
- `pydantic` - Data validation (already in project)

### Client Dependencies (Development)
- `click` - CLI framework
- `watchdog` - File watching
- `rich` - Console output formatting
- `toml` - Configuration file parsing
- `openapi-python-client` - Generate full API client from OpenAPI spec (recommended)
- OR `datamodel-code-generator` - Generate schemas only (alternative)

### Code Generation

**Option A: Full Client (Recommended)**
```bash
# Install generator
pip install openapi-python-client

# Generate complete client (schemas + typed methods)
openapi-python-client generate \
  --url http://localhost:8000/openapi.json \
  --output-path viz/api/generated \
  --overwrite

# Usage:
# from viz.api.generated import Client
# client = Client(base_url="http://localhost:8000")
# client.dashboards.create_dashboard(...)
```

**Option B: Schemas Only**
```bash
# Install generator
pip install datamodel-code-generator[http]

# Generate schemas only
datamodel-code-generator \
  --url http://localhost:8000/openapi.json \
  --output viz/api/generated/schemas.py \
  --input-file-type openapi \
  --output-model-type pydantic_v2.BaseModel \
  --use-standard-collections \
  --use-union-operator

# Then manually implement HTTP client using httpx
```

---

## Summary

This plan outlines a comprehensive refactor of the registry API and implementation of a CLI tool for the Viz dashboarding framework.

**Key Achievements**:
1. ✅ Aligned naming conventions (`id` instead of `name`, "Input" instead of "Selector")
2. ✅ Designed dual component system (class-based + function-based)
3. ✅ Specified cascading input support with parameter bindings
4. ✅ Defined complete API specification for both services
5. ✅ Designed Streamlit-like CLI with file watching
6. ✅ Planned serialization and registration flow
7. ✅ Eliminated shared schemas - use OpenAPI code generation instead
8. ✅ Scoped 7 implementation phases with detailed tasks

**Next Steps**:
1. Begin Phase 1: Update registry API schemas and models
2. Implement Phase 2: Update registry API endpoints
3. Phase 3: Generate client code from OpenAPI
4. Continue through remaining phases sequentially

**Estimated Effort**: 7 phases × ~3-5 days each = 3-5 weeks for complete implementation

---

**Status**: ✅ Finalized and Ready for Implementation
**Last Updated**: 2025-11-25
