# Viz - Distributed Dashboarding Framework - Project Context

## Project Summary

Building a distributed dashboarding framework (like Streamlit but with distributed compute) that allows users to:
- Define reactive dashboards with Python components
- Execute components server-side with strong isolation
- Create interactive visualizations with Plotly/Vega-Lite
- Build reusable component libraries
- Deploy dashboards with automatic parameter binding

## Current State

✅ **Backend Complete** - Function registry with component execution
✅ **Client Library Core Complete** - Component base class with dataclass pattern
🚧 **In Progress** - Layout components (Dashboard, Page, Section, Row, Column)

### Key Design Decisions

1. **Dataclass Pattern for Components**
   - Components use class fields for parameters (no @dataclass needed)
   - ComponentMeta metaclass auto-applies dataclass conversion
   - Cleaner, more Pythonic API

2. **Server-Side Execution**
   - All component stages (load/transform/render) execute on server
   - Returns serialized output (Plotly JSON, Vega-Lite specs)
   - Strong process isolation with resource limits

3. **Dashboard-Scoped API**
   - RESTful design: `/dashboard/{name}/component/{id}/render`
   - Clear context for all operations
   - Better permission scoping

4. **Reactive Parameters**
   - Selectors bound to component parameters
   - Automatic re-execution on selector changes
   - Stateless components (functional approach)

## Architecture

```
Client → FastAPI (JWT Auth) → Process Pool Executor → Response
                ↓
         PostgreSQL (metadata, logs, metrics)
```

### Key Components

1. **FastAPI Service** (`app/main.py`)
   - REST API with JWT authentication
   - Auto-reload enabled for development

2. **Process Pool Executor** (`app/executor.py`)
   - Uses `ProcessPoolExecutor` for efficient execution
   - Reuses worker processes (6x performance improvement over spawning)
   - Enforces timeouts and monitors memory usage

3. **Database Models** (`app/models.py`)
   - Users, Functions, Executions
   - Tracks metadata and execution history

4. **Authentication** (`app/auth.py`, `app/api/auth.py`)
   - JWT-based auth with bcrypt password hashing
   - Login returns access token

## Project Structure

```
viz/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration (env vars)
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models (User, Function, Execution)
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # JWT authentication utilities
│   ├── executor.py          # Process pool executor (optimized!)
│   └── api/
│       ├── auth.py          # Auth endpoints (register, login)
│       ├── functions.py     # Function CRUD endpoints
│       └── execute.py       # Execution endpoints
├── test_api.py              # API integration tests
├── test_performance.py      # Performance benchmarking
├── requirements.txt         # Python dependencies
├── docker-compose.dev.yml   # PostgreSQL container
├── .env                     # Environment variables
└── .idea/runConfigurations/ # PyCharm run configs

```

## Running the Project

### Services

**PostgreSQL** (Docker):
```bash
docker-compose -f docker-compose.dev.yml up -d
```

**FastAPI Server** (Local):
```bash
.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use PyCharm run configurations:
- "FastAPI Server" - Normal mode
- "FastAPI Server (Debug)" - Debug mode with breakpoints

### Testing

```bash
# API Tests
.venv/bin/python test_api.py

# Performance Tests (1000 requests)
.venv/bin/python test_performance.py 1000 50
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login (returns JWT token)

### Functions
- `POST /functions/` - Create function
- `GET /functions/` - List user's functions
- `GET /functions/{alias}` - Get function details
- `PUT /functions/{alias}` - Update function
- `DELETE /functions/{alias}` - Delete function

### Execution
- `POST /execute/{alias}` - Execute function synchronously
- `GET /execute/history/{alias}` - Get execution history

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database

**Connection**: `postgresql://postgres:postgres@localhost:5432/funcexec`

**Tables**:
- `users` - User accounts
- `functions` - Stored functions with code and metadata
- `executions` - Execution history with metrics

## Key Dependencies

```
fastapi==0.115.5
uvicorn[standard]==0.32.1
sqlalchemy==2.0.36
psycopg2-binary==2.9.10
pydantic==2.10.3
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.1.3  # Pinned for compatibility
psutil==6.1.0
httpx==0.28.1  # For performance testing
email-validator==2.2.0
```

## Environment Variables

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/funcexec
JWT_SECRET_KEY=dev-secret-key-change-in-production-12345
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
MAX_MEMORY_MB=200
MAX_CPU_CORES=1
DEFAULT_TIMEOUT_SECONDS=30
MAX_TIMEOUT_SECONDS=60
```

## Test User

**Username**: `testuser`
**Password**: `testpassword123`
**Email**: `test@example.com`

## Performance Optimization History

### Before (Process Spawning)
- 20.15s for 1000 requests
- 49.62 req/s
- 990ms mean response time
- 99.6% success rate (4 failures)

### After (Process Pool)
- 3.34s for 1000 requests (**6x faster**)
- 299.58 req/s (**6x improvement**)
- 164ms mean response time (**83% faster**)
- 100% success rate (no failures)

## Recent Changes (Session: 2025-11-15)

### Phase 1: Project Restructuring
1. **Monorepo Structure**
   - Created subprojects: registry/, client/, shared/, examples/
   - Configured PyCharm source roots
   - Set up proper .gitignore

2. **Shared Package** (`viz_shared`)
   - Complete type system (ExecutionStage, SelectorType, etc.)
   - Comprehensive Pydantic schemas
   - Utility functions for serialization

### Phase 2: Registry Enhancement
3. **Enhanced Database Models**
   - Component model with class-based components
   - ComponentExecution model with stage tracking
   - Dashboard model with JSON structure storage

4. **Enhanced Executor** (`executor.py`)
   - Support for class-based components
   - Stage-based execution (load, load_transform, load_transform_render)
   - Auto-serialization of Plotly/Altair/Vega-Lite

5. **Complete API Endpoints**
   - Component CRUD: `/components/`
   - Dashboard CRUD: `/dashboards/`
   - Dashboard-scoped execution: `/dashboard/{name}/component/{id}/...`
   - Selector data: `/dashboard/{name}/input/{selector}/data`

### Phase 3: Client Library
6. **Component Base Class** (`viz/core/component.py`)
   - Dataclass pattern with ComponentMeta metaclass
   - No @dataclass decorator needed for users
   - Clean parameter definition via class fields

7. **API Client** (`viz/api/client.py`)
   - RegistryClient for authentication and CRUD
   - Context manager support
   - Auto-registration helpers

## Known Issues

None! All tests passing with 100% success rate.

## Next Steps (Production Roadmap)

1. **Add External Dependencies Support**
   - Allow pip packages in functions
   - Separate venvs per function or shared venv with requirements

2. **Implement Async Execution**
   - Job queue (Celery/RQ)
   - Webhook callbacks
   - Polling endpoint for status

3. **Add Function Versioning**
   - Track code changes
   - Roll back to previous versions

4. **Git Integration**
   - Deploy functions from Git repos
   - Auto-deploy on push

5. **Enhanced Monitoring**
   - Prometheus metrics
   - Grafana dashboards
   - Error tracking (Sentry)

6. **Rate Limiting**
   - Per-user rate limits
   - Prevent abuse

7. **Container-based Isolation**
   - Docker containers with gVisor
   - Better security for untrusted code

8. **Horizontal Scaling**
   - Deploy to GKE
   - Load balancer
   - Auto-scaling

## Development Tips

### Debugging
1. Use PyCharm's "FastAPI Server (Debug)" configuration
2. Set breakpoints in `app/api/execute.py` or `app/executor.py`
3. Make API request and step through code

### Database Inspection
```bash
# Connect to PostgreSQL
docker exec -it funcexec_postgres psql -U postgres -d funcexec

# List tables
\dt

# Query data
SELECT * FROM functions;
SELECT * FROM executions ORDER BY started_at DESC LIMIT 10;
```

### Logs
- API logs appear in terminal/PyCharm console
- PostgreSQL logs: `docker-compose -f docker-compose.dev.yml logs -f postgres`

## Useful Commands

```bash
# Start PostgreSQL
docker-compose -f docker-compose.dev.yml up -d

# Stop PostgreSQL
docker-compose -f docker-compose.dev.yml down

# View PostgreSQL logs
docker-compose -f docker-compose.dev.yml logs -f

# Install new dependency
.venv/bin/pip install package-name
# Don't forget to add to requirements.txt

# Run with different worker count
.venv/bin/python test_performance.py 1000 100  # 100 concurrent workers
```

---

**Last Updated**: 2025-11-15
**Status**: Production-ready MVP
**Python Version**: 3.13.0
**Author**: Built with Claude Code
