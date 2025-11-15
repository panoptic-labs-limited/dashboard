#!/bin/bash

echo "🚀 Starting Function Execution Service..."
echo ""

# Check if PostgreSQL is running
if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "⚠️  PostgreSQL is not running on localhost:5432"
    echo ""
    echo "Options:"
    echo "  1. Start PostgreSQL locally"
    echo "  2. Run with Docker Compose: docker-compose up -d"
    echo ""
    exit 1
fi

echo "✓ PostgreSQL is running"

# Check if database exists
if ! psql -h localhost -U postgres -lqt | cut -d \| -f 1 | grep -qw funcexec; then
    echo "Creating database 'funcexec'..."
    createdb -h localhost -U postgres funcexec
    echo "✓ Database created"
else
    echo "✓ Database exists"
fi

echo ""
echo "Starting FastAPI server..."
echo "API will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""

# Activate venv and run
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
