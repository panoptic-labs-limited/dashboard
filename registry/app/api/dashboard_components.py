"""Dashboard-scoped component and selector API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, Literal, Any, Dict

from app.database import get_db
from app.models import User, Dashboard, Component
from app.auth import get_current_user
from app.executor import executor
from viz_shared import WidgetRenderRequest

router = APIRouter(prefix="/dashboard", tags=["dashboard-components"])


def _find_widget_in_dashboard(dashboard_structure: dict, widget_id: str) -> Optional[dict]:
    """Recursively find a widget by ID in dashboard structure."""
    def search_node(node):
        if isinstance(node, dict):
            if node.get("type") == "widget" and node.get("id") == widget_id:
                return node
            # Recurse into children
            for key in ["children", "sections", "pages"]:
                if key in node:
                    if isinstance(node[key], list):
                        for child in node[key]:
                            result = search_node(child)
                            if result:
                                return result
                    else:
                        result = search_node(node[key])
                        if result:
                            return result
        elif isinstance(node, list):
            for item in node:
                result = search_node(item)
                if result:
                    return result
        return None

    return search_node(dashboard_structure)


def _find_selector_in_dashboard(dashboard_structure: dict, selector_name: str) -> Optional[dict]:
    """Recursively find a selector by name in dashboard structure."""
    def search_node(node):
        if isinstance(node, dict):
            if node.get("type") == "selector":
                selector_config = node.get("selector", {})
                if selector_config.get("name") == selector_name:
                    return selector_config
            # Recurse into children
            for key in ["children", "sections", "pages"]:
                if key in node:
                    if isinstance(node[key], list):
                        for child in node[key]:
                            result = search_node(child)
                            if result:
                                return result
                    else:
                        result = search_node(node[key])
                        if result:
                            return result
        elif isinstance(node, list):
            for item in node:
                result = search_node(item)
                if result:
                    return result
        return None

    return search_node(dashboard_structure)


@router.post("/{dashboard_name}/component/{widget_id}/render")
def render_component(
    dashboard_name: str,
    widget_id: str,
    request: WidgetRenderRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Render a component (full execution: load → transform → render).

    Args:
        dashboard_name: Name of the dashboard
        widget_id: ID of the widget to render
        request: Widget render request containing selector values

    Returns the final rendered output (Plotly figure, Vega-Lite spec, etc.)
    """
    # Get dashboard
    dashboard = db.query(Dashboard).filter(
        Dashboard.name == dashboard_name,
        Dashboard.owner_id == current_user.id
    ).first()

    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dashboard '{dashboard_name}' not found"
        )

    # Find widget in dashboard structure
    widget = _find_widget_in_dashboard(dashboard.structure, widget_id)
    if not widget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Widget '{widget_id}' not found in dashboard '{dashboard_name}'"
        )

    # Get the component
    component_alias = widget.get("component_alias")
    component = db.query(Component).filter(
        Component.alias == component_alias,
        Component.owner_id == current_user.id
    ).first()

    if not component:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Component '{component_alias}' not found"
        )

    # Resolve parameter bindings from widget params
    widget_params = widget.get("params", {})
    resolved_params = {}

    for param_name, param_value in widget_params.items():
        if isinstance(param_value, dict) and param_value.get("type") == "selector":
            # Parameter is bound to a selector
            selector_name = param_value.get("name")
            if selector_name in request.selector_values:
                resolved_params[param_name] = request.selector_values[selector_name]
            # If selector value not provided, skip (don't include in params)
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

    if status_result != "success":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result_data.get("error_message", "Execution failed")
        )

    return {
        "widget_id": widget_id,
        "component_alias": component_alias,
        "output": result_data.get("output"),
        "execution_time_ms": result_data.get("execution_time_ms"),
        "memory_used_mb": result_data.get("memory_used_mb")
    }


@router.get("/{dashboard_name}/component/{widget_id}/data")
def get_component_data(
    dashboard_name: str,
    widget_id: str,
    mode: Literal["raw", "transformed"] = Query("transformed"),
    params: Optional[str] = Query(None, description="JSON-encoded params"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get component data without rendering.

    Args:
        mode: "raw" = load only, "transformed" = load + transform
        params: Optional JSON string of parameters

    Returns the data from load() or transform() stage.
    """
    import json as json_module

    # Get dashboard
    dashboard = db.query(Dashboard).filter(
        Dashboard.name == dashboard_name,
        Dashboard.owner_id == current_user.id
    ).first()

    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dashboard '{dashboard_name}' not found"
        )

    # Find widget
    widget = _find_widget_in_dashboard(dashboard.structure, widget_id)
    if not widget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Widget '{widget_id}' not found in dashboard"
        )

    # Get component
    component_alias = widget.get("component_alias")
    component = db.query(Component).filter(
        Component.alias == component_alias,
        Component.owner_id == current_user.id
    ).first()

    if not component:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Component '{component_alias}' not found"
        )

    # Parse params
    widget_params = widget.get("params", {})
    if params:
        try:
            provided_params = json_module.loads(params)
            final_params = {**widget_params, **provided_params}
        except json_module.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON in params"
            )
    else:
        final_params = widget_params

    # Determine execution stage
    stage = "load" if mode == "raw" else "load_transform"

    # Execute component
    status_result, result_data = executor.execute_component(
        code=component.source_code,
        class_name=component.class_name,
        stage=stage,
        params=final_params,
        timeout_seconds=component.timeout_seconds,
        memory_limit_mb=component.memory_limit_mb
    )

    if status_result != "success":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result_data.get("error_message", "Execution failed")
        )

    return {
        "widget_id": widget_id,
        "component_alias": component_alias,
        "mode": mode,
        "data": result_data.get("output"),
        "execution_time_ms": result_data.get("execution_time_ms"),
        "memory_used_mb": result_data.get("memory_used_mb")
    }


@router.get("/{dashboard_name}/input/{selector_name}/data")
def get_selector_data(
    dashboard_name: str,
    selector_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get data for a selector (e.g., dropdown options from a data source function).

    Returns the options/data to populate the selector in the UI.
    """
    # Get dashboard
    dashboard = db.query(Dashboard).filter(
        Dashboard.name == dashboard_name,
        Dashboard.owner_id == current_user.id
    ).first()

    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dashboard '{dashboard_name}' not found"
        )

    # Find selector
    selector = _find_selector_in_dashboard(dashboard.structure, selector_name)
    if not selector:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Selector '{selector_name}' not found in dashboard"
        )

    # Check if selector has a data source
    data_source = selector.get("data_source")
    if not data_source:
        # Selector has static options
        return {
            "selector_name": selector_name,
            "type": "static",
            "options": selector.get("options", [])
        }

    # Selector has dynamic data source (function)
    function_alias = data_source.get("alias")
    function_params = data_source.get("params", {})

    # Get the data source function/component
    component = db.query(Component).filter(
        Component.alias == function_alias,
        Component.owner_id == current_user.id
    ).first()

    if not component:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data source '{function_alias}' not found"
        )

    # Execute the data source function (load only)
    status_result, result_data = executor.execute_component(
        code=component.source_code,
        class_name=component.class_name,
        stage="load",
        params=function_params,
        timeout_seconds=component.timeout_seconds,
        memory_limit_mb=component.memory_limit_mb
    )

    if status_result != "success":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load selector data: {result_data.get('error_message')}"
        )

    return {
        "selector_name": selector_name,
        "type": "dynamic",
        "options": result_data.get("output"),
        "execution_time_ms": result_data.get("execution_time_ms")
    }
