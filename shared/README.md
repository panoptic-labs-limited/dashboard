# Viz Shared

Shared code, schemas, and types used by both the registry and client library.

## Contents

- **schemas.py**: Pydantic schemas for API communication
- **types.py**: Common type definitions
- **utils.py**: Shared utility functions

## Installation

```bash
pip install -e .
```

## Usage

```python
from viz_shared.schemas import ComponentSchema, DashboardSchema
from viz_shared.types import ExecutionStage
```