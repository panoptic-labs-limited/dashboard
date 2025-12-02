# Architecture Proposal: Split Dashboard & Component Services

## Overview

Split the current registry service into two services:

1. **Dashboard Service (gRPC/Java)** - Orchestration, structure storage, dependency tracking, permissions
2. **Component Registry (Python/gRPC)** - Code storage, sandboxed execution, compute

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                              Frontend                                │
│  - Fetches dashboard structure from Dashboard Service               │
│  - Requests component data/renders through Dashboard Service        │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Dashboard Service (gRPC/Java)                    │
│                                                                     │
│  Storage:                                                           │
│  - Dashboard structures (versioned)                                 │
│  - Dashboard → Component mappings                                   │
│  - Permissions (user/group → dashboard → components)                │
│                                                                     │
│  On Register:                                                       │
│  1. Store dashboard structure                                       │
│  2. Forward source file + component metadata to Component Registry  │
│  3. Store mapping: dashboard_id → [component_names]                 │
│  4. Propagate dashboard permissions to components                   │
│                                                                     │
│  On Execute:                                                        │
│  1. Check user has permission to dashboard                          │
│  2. Proxy request to Component Registry                             │
│  3. Return result to frontend                                       │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  Component Registry (Python/gRPC)                   │
│                                                                     │
│  Storage:                                                           │
│  - Source files (versioned, keyed by hash or version)               │
│  - Component index: name → (source_file, class_name, parameters)    │
│                                                                     │
│  On Register:                                                       │
│  1. Receive source file + component metadata from Dashboard Service │
│  2. Parse source to extract full parameter info                     │
│  3. Store source file, index components                             │
│  4. Return component details (params, version) to Dashboard Service │
│                                                                     │
│  On Execute:                                                        │
│  1. Load component by name                                          │
│  2. Execute in sandbox with provided params                         │
│  3. Return data or rendered Plotly JSON                             │
└─────────────────────────────────────────────────────────────────────┘
```

## Design Decisions

### Component Extraction
- Component metadata (names, class names) is serialized by the CLI into protos
- Java service forwards the Python file + known metadata to Python service
- Python service extracts full parameter info from the source

### Source File Granularity
- One Python file per dashboard (initial implementation)
- Future: Support dashboards spread across multiple files/modules

### Versioning
- Components versioned independently when they change
- Dashboard versions track which component versions they use

### Permissions
- Frontend makes all requests through Dashboard Service
- Dashboard Service checks permissions before proxying to Component Registry
- Dashboard permissions propagate down to components

## Proto Structure

Three proto files in `proto/` at repo root:

### common.proto
Shared types used by both services:
- Dashboard structure (pages, sections, rows, columns)
- Widgets (LineChart, BarChart, Table, Metric, Plotly)
- Inputs (Select, Slider, Toggle, etc.)
- Data sources (Timeseries, Component, Function)
- Parameters (literal values and input references)

### dashboard_service.proto
Java service API:
- `RegisterDashboard` - Store structure, forward to component registry
- `GetDashboard` - Retrieve dashboard structure
- `ListDashboards` - List available dashboards
- `RenderWidget` - Proxy component execution requests
- `UpdatePermissions` - Manage access control

### component_registry.proto
Python service API:
- `RegisterComponents` - Store source file, index components
- `ExecuteComponent` - Run component with params, return data/render
- `GetComponentMetadata` - Get parameter info for a component

## Example Proto Definitions

```protobuf
// dashboard_service.proto
syntax = "proto3";
package viz.dashboard;

service DashboardService {
  rpc RegisterDashboard(RegisterDashboardRequest) returns (RegisterDashboardResponse);
  rpc GetDashboard(GetDashboardRequest) returns (Dashboard);
  rpc ListDashboards(ListDashboardsRequest) returns (ListDashboardsResponse);
  rpc RenderWidget(RenderWidgetRequest) returns (RenderWidgetResponse);
}

message RegisterDashboardRequest {
  Dashboard dashboard = 1;
  bytes source_file = 2;  // Python source code
  repeated ComponentInfo components = 3;  // Metadata from CLI
}

message ComponentInfo {
  string name = 1;
  string class_name = 2;
  bool is_renderable = 3;  // RenderableComponent vs Component
}
```

```protobuf
// component_registry.proto
syntax = "proto3";
package viz.component;

service ComponentRegistry {
  rpc RegisterComponents(RegisterComponentsRequest) returns (RegisterComponentsResponse);
  rpc ExecuteComponent(ExecuteComponentRequest) returns (ExecuteComponentResponse);
  rpc GetComponentMetadata(GetComponentMetadataRequest) returns (ComponentMetadata);
}

message RegisterComponentsRequest {
  bytes source_file = 1;
  repeated ComponentInfo components = 2;
  string dashboard_id = 3;  // For tracking provenance
}

message ExecuteComponentRequest {
  string component_name = 1;
  map<string, ParamValue> params = 2;
  bool render = 3;  // If true, call render() for RenderableComponents
}

message ExecuteComponentResponse {
  oneof result {
    bytes data_json = 1;    // JSON-serialized DataFrame/dict
    bytes plotly_json = 2;  // Plotly figure JSON (if render=true)
  }
}
```

## Next Steps

1. Create full proto definitions in `proto/` directory
2. Set up proto generation for Python (grpcio-tools)
3. Update Python client to serialize to proto instead of JSON
4. Create Java Dashboard Service skeleton
5. Refactor Python registry to be Component Registry only
