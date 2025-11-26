"""API endpoints for dashboard management and rendering."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import time

from app.database import get_db
from app.models import User, Dashboard, Component
from app.auth import get_current_user
from app.executor import executor
from viz_shared import (
    DashboardCreate,
    DashboardUpdate,
    DashboardResponse,
    DashboardRenderRequest,
    DashboardRenderResponse,
    WidgetRenderResult,
    WidgetSchema,
    ParameterBinding,
)

router = APIRouter(prefix="/dashboards", tags=["dashboards"])


@router.post("/", response_model=DashboardResponse, status_code=status.HTTP_201_CREATED)
def create_dashboard(
    dashboard_data: DashboardCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new dashboard."""
    # Check if id already exists
    if db.query(Dashboard).filter(Dashboard.dashboard_id == dashboard_data.id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Dashboard with id '{dashboard_data.id}' already exists"
        )

    # Create dashboard
    db_dashboard = Dashboard(
        dashboard_id=dashboard_data.id,
        title=dashboard_data.title,
        description=dashboard_data.description,
        structure=dashboard_data.structure.model_dump(),
        owner_id=current_user.id
    )
    db.add(db_dashboard)
    db.commit()
    db.refresh(db_dashboard)

    return db_dashboard


@router.get("/", response_model=List[DashboardResponse])
def list_dashboards(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all dashboards owned by the current user."""
    dashboards = db.query(Dashboard).filter(Dashboard.owner_id == current_user.id).all()
    return dashboards


@router.get("/{dashboard_id}", response_model=DashboardResponse)
def get_dashboard(
    dashboard_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a dashboard by ID."""
    dashboard = db.query(Dashboard).filter(
        Dashboard.dashboard_id == dashboard_id,
        Dashboard.owner_id == current_user.id
    ).first()

    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dashboard '{dashboard_id}' not found"
        )

    return dashboard


@router.put("/{dashboard_id}", response_model=DashboardResponse)
def update_dashboard(
    dashboard_id: str,
    dashboard_data: DashboardUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a dashboard."""
    dashboard = db.query(Dashboard).filter(
        Dashboard.dashboard_id == dashboard_id,
        Dashboard.owner_id == current_user.id
    ).first()

    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dashboard '{dashboard_id}' not found"
        )

    # Update fields
    update_data = dashboard_data.model_dump(exclude_unset=True)

    # Handle structure separately
    if "structure" in update_data and update_data["structure"]:
        update_data["structure"] = dashboard_data.structure.model_dump()

    for field, value in update_data.items():
        setattr(dashboard, field, value)

    db.commit()
    db.refresh(dashboard)

    return dashboard


@router.delete("/{dashboard_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dashboard(
    dashboard_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a dashboard."""
    dashboard = db.query(Dashboard).filter(
        Dashboard.dashboard_id == dashboard_id,
        Dashboard.owner_id == current_user.id
    ).first()

    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dashboard '{dashboard_id}' not found"
        )

    db.delete(dashboard)
    db.commit()

    return None


@router.post("/{dashboard_id}/render", response_model=DashboardRenderResponse)
def render_dashboard(
    dashboard_id: str,
    render_request: DashboardRenderRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render a dashboard by executing all its components."""
    # Get the dashboard
    dashboard = db.query(Dashboard).filter(
        Dashboard.dashboard_id == dashboard_id,
        Dashboard.owner_id == current_user.id
    ).first()

    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dashboard '{dashboard_id}' not found"
        )

    # Extract widgets from dashboard structure
    widgets = _extract_widgets_from_structure(dashboard.structure)

    # Track total execution time
    total_start_time = time.time()
    widget_results = []

    # Execute each widget
    for widget_data in widgets:
        widget_result = _execute_widget(
            widget_data,
            render_request.input_values,
            current_user.id,
            db
        )
        widget_results.append(widget_result)

    total_execution_time = (time.time() - total_start_time) * 1000  # Convert to ms

    return DashboardRenderResponse(
        dashboard_id=dashboard.dashboard_id,
        input_values=render_request.input_values,
        widgets=widget_results,
        total_execution_time_ms=total_execution_time
    )


def _extract_widgets_from_structure(structure: dict) -> List[dict]:
    """Recursively extract all widgets from dashboard structure."""
    widgets = []

    def extract_from_node(node):
        if isinstance(node, dict):
            if node.get("type") == "widget":
                widgets.append(node)
            # Recurse into children
            for key in ["children", "sections", "pages"]:
                if key in node:
                    if isinstance(node[key], list):
                        for child in node[key]:
                            extract_from_node(child)
                    else:
                        extract_from_node(node[key])
        elif isinstance(node, list):
            for item in node:
                extract_from_node(item)

    extract_from_node(structure)
    return widgets


def _execute_widget(
    widget_data: dict,
    input_values: dict,
    user_id: int,
    db: Session
) -> WidgetRenderResult:
    """Execute a single widget and return the result."""
    widget_id = widget_data.get("id")
    component_alias = widget_data.get("component_alias")
    params = widget_data.get("params", {})

    try:
        # Get the component
        component = db.query(Component).filter(
            Component.alias == component_alias,
            Component.owner_id == user_id
        ).first()

        if not component:
            return WidgetRenderResult(
                widget_id=widget_id,
                component_alias=component_alias,
                status="error",
                error_message=f"Component '{component_alias}' not found"
            )

        # Resolve parameter bindings
        resolved_params = {}
        for param_name, param_value in params.items():
            if isinstance(param_value, dict) and param_value.get("type") == "input":
                # Parameter is bound to an input
                input_id = param_value.get("input_id")
                if input_id in input_values:
                    resolved_params[param_name] = input_values[input_id]
                else:
                    # Input value not provided, skip or use default
                    pass
            elif isinstance(param_value, dict) and param_value.get("type") == "literal":
                # Literal value wrapped in binding structure
                resolved_params[param_name] = param_value.get("value")
            else:
                # Regular parameter value (backward compatibility)
                resolved_params[param_name] = param_value

        # Execute component (full render)
        status_result, result_data = executor.execute_component(
            code=component.source_code,
            class_name=component.class_name,
            stage="load_transform_render",
            params=resolved_params,
            timeout_seconds=component.timeout_seconds,
            memory_limit_mb=component.memory_limit_mb
        )

        if status_result == "success":
            return WidgetRenderResult(
                widget_id=widget_id,
                component_alias=component_alias,
                status="success",
                output=result_data.get("output"),
                execution_time_ms=result_data.get("execution_time_ms")
            )
        else:
            return WidgetRenderResult(
                widget_id=widget_id,
                component_alias=component_alias,
                status=status_result,
                error_message=result_data.get("error_message"),
                execution_time_ms=result_data.get("execution_time_ms")
            )

    except Exception as e:
        return WidgetRenderResult(
            widget_id=widget_id,
            component_alias=component_alias,
            status="error",
            error_message=str(e)
        )
