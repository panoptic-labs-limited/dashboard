# Viz - Distributed Dashboarding Framework

A distributed dashboarding framework with reactive components, similar to Streamlit but with distributed compute capabilities.

## Project Structure

This is a monorepo containing:

- **registry/** - Function Registry backend (FastAPI)
- **client/** - Viz Python client library
- **shared/** - Shared code between registry and client
- **examples/** - Example dashboards

## Features

### Function Registry (Backend)
- Component and function storage with version control
- Process pool execution with strong isolation
- Resource limits (memory, timeout, CPU)
- JWT authentication
- Execution history and metrics

### Viz Client Library
- Declarative dashboard definitions
- Component-based architecture (load/transform/render)
- Reactive selectors and parameter binding
- Flexible layout system (Dashboard/Page/Section/Row/Column)
- Automatic registration with function registry

## Architecture

```
Client Library (Python) → Function Registry (FastAPI) → Process Pool Executor
                                    ↓
                              PostgreSQL
                                    ↓
                           UI Service (Future)
                        (React + Vega-Lite rendering)
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed architecture documentation.

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 16+ (via Docker Compose)

### 1. Start the Function Registry

```bash
cd registry

# Copy environment file
cp .env.example .env

# Start PostgreSQL
docker-compose -f docker-compose.dev.yml up -d

# Install dependencies
pip install -r requirements.txt

# Start the service
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Install the Client Library

```bash
# Install shared package
cd shared
pip install -e .

# Install client library
cd ../client
pip install -e .
```

### 3. Create Your First Dashboard

```python
from viz import Dashboard, Page, Section, Row, Column, Widget
from viz import DateSelector, Component

class SalesChart(Component):
    def load(self, date: str):
        return {"sales": 1000, "date": date}

    def transform(self, data):
        return data

    def render(self, data):
        return {"mark": "bar", "data": {"values": [data]}}

dashboard = Dashboard(name="sales", title="Sales Dashboard")
# ... add components
dashboard.register()
```

See [examples/](./examples/) for complete examples.

## API Usage

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  --user "testuser:securepassword"
```

Response:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### 3. Create a Function

```bash
curl -X POST "http://localhost:8000/functions/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "alias": "add_numbers",
    "code": "def add_numbers(a, b):\n    return a + b",
    "description": "Adds two numbers",
    "memory_limit_mb": 200,
    "timeout_seconds": 30
  }'
```

### 4. Execute a Function

```bash
curl -X POST "http://localhost:8000/execute/add_numbers" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "params": {
      "a": 5,
      "b": 3
    }
  }'
```

Response:
```json
{
  "id": 1,
  "function_id": 1,
  "status": "success",
  "output": {
    "result": 8
  },
  "execution_time_ms": 0.123,
  "memory_used_mb": 45.2,
  "started_at": "2024-01-15T10:30:00",
  "completed_at": "2024-01-15T10:30:01"
}
```

### 5. List Functions

```bash
curl -X GET "http://localhost:8000/functions/" \
  -H "Authorization: Bearer <your_token>"
```

### 6. Get Function Details

```bash
curl -X GET "http://localhost:8000/functions/add_numbers" \
  -H "Authorization: Bearer <your_token>"
```

### 7. Update a Function

```bash
curl -X PUT "http://localhost:8000/functions/add_numbers" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def add_numbers(a, b):\n    return a + b + 1",
    "description": "Adds two numbers plus one"
  }'
```

### 8. Get Execution History

```bash
curl -X GET "http://localhost:8000/execute/history/add_numbers?limit=10" \
  -H "Authorization: Bearer <your_token>"
```

### 9. Delete a Function

```bash
curl -X DELETE "http://localhost:8000/functions/add_numbers" \
  -H "Authorization: Bearer <your_token>"
```

## Function Code Format

Functions should be defined as standard Python functions:

```python
def my_function(param1, param2):
    # Your code here
    result = param1 + param2
    return result
```

**Important**:
- Only one function should be defined per code submission
- The function can use Python builtins and the `json` module
- No external dependencies are available (by design for MVP)
- Functions must be stateless

## Security & Isolation

The service implements several security measures:

1. **Process Isolation**: Each function runs in a separate process
2. **Resource Limits**:
   - Memory monitoring (warning if exceeded)
   - CPU limits (1 core per execution)
   - Timeout enforcement (terminates runaway processes)
3. **User Isolation**: Users can only access their own functions
4. **JWT Authentication**: Secure token-based auth
5. **Code Validation**: Syntax checking before storage

## Configuration

Edit `.env` file to configure:

```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/funcexec

# JWT Settings
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30

# Resource Limits
MAX_MEMORY_MB=200
MAX_CPU_CORES=1
DEFAULT_TIMEOUT_SECONDS=30
MAX_TIMEOUT_SECONDS=60
```

## Development

### Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # JWT authentication
│   ├── executor.py          # Function executor with isolation
│   └── api/
│       ├── __init__.py
│       ├── auth.py          # Auth endpoints
│       ├── functions.py     # Function CRUD endpoints
│       └── execute.py       # Execution endpoints
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

### Running Tests

```bash
# TODO: Add pytest tests
pytest
```

## Production Deployment

For production deployment on GCP:

### Option 1: Cloud Run
- Build and push Docker image to GCR
- Deploy to Cloud Run
- Use Cloud SQL for PostgreSQL
- Set environment variables

### Option 2: GKE with gVisor
- Deploy to GKE cluster
- Enable gVisor for enhanced isolation
- Use Cloud SQL or PostgreSQL on GKE
- Configure resource quotas

## Roadmap

- [ ] Add support for external dependencies (pip packages)
- [ ] Implement async execution with job queue
- [ ] Add function versioning
- [ ] Implement Git integration for function deployment
- [ ] Add more detailed metrics and monitoring
- [ ] Implement rate limiting
- [ ] Add WebSocket support for real-time execution updates
- [ ] Enhanced security with gVisor or Firecracker

## License

MIT
