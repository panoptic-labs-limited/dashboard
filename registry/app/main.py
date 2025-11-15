from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import (
    auth,
    functions,
    execute,
    components,
    execute_component,
    dashboards,
    dashboard_components,
)
from app.database import engine, Base
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Viz Function Registry",
    description="Distributed dashboarding framework - Function and Component Registry with execution engine",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(functions.router)
app.include_router(execute.router)
app.include_router(components.router)
app.include_router(execute_component.router)
app.include_router(dashboards.router)
app.include_router(dashboard_components.router)  # Dashboard-scoped component execution


@app.get("/")
def root():
    return {
        "message": "Viz Function Registry",
        "version": "2.0.0",
        "description": "Distributed dashboarding framework with component execution",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "auth": "/auth",
            "functions": "/functions",
            "components": "/components",
            "dashboards": "/dashboards"
        }
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
