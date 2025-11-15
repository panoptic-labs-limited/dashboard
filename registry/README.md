# Function Registry

Backend service for storing and executing Python functions and components with strong isolation and resource limits.

## Features

- Function and component storage
- Process pool execution with isolation
- Resource limits (memory, timeout)
- JWT authentication
- Execution history and metrics

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL
docker-compose -f docker-compose.dev.yml up -d

# Run the service
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

```bash
# Run API tests
python test_api.py

# Run performance tests
python test_performance.py 1000 50
```

See [PROJECT_CONTEXT.md](../PROJECT_CONTEXT.md) for detailed documentation.