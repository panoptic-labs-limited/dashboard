"""API endpoints for component execution."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app.database import get_db
from app.models import User, Component, ComponentExecution
from app.auth import get_current_user
from app.executor import executor
from app.schemas import (
    ComponentExecutionRequest,
    ComponentExecutionResponse,
)
from app.types import ExecutionStage

router = APIRouter(prefix="/execute/component", tags=["component-execution"])


@router.post("/{alias}", response_model=ComponentExecutionResponse)
def execute_component(
    alias: str,
    execution_request: ComponentExecutionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Execute a component by alias with specified stage."""
    # Get the component
    component = db.query(Component).filter(
        Component.alias == alias,
        Component.owner_id == current_user.id
    ).first()

    if not component:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Component '{alias}' not found"
        )

    # Create execution record
    execution = ComponentExecution(
        component_id=component.id,
        stage=execution_request.stage.value,
        input_params=execution_request.params,
        status="running",
        started_at=datetime.utcnow()
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)

    try:
        # Execute the component
        status_result, result_data = executor.execute_component(
            code=component.source_code,
            class_name=component.class_name,
            stage=execution_request.stage.value,
            params=execution_request.params,
            timeout_seconds=component.timeout_seconds,
            memory_limit_mb=component.memory_limit_mb
        )

        # Update execution record
        execution.status = status_result
        execution.completed_at = datetime.utcnow()

        if status_result == "success":
            execution.output = result_data.get("output")
            execution.execution_time_ms = result_data.get("execution_time_ms")
            execution.memory_used_mb = result_data.get("memory_used_mb")

            # Add stdout/stderr if present
            stdout = result_data.get("stdout")
            stderr = result_data.get("stderr")
            if stdout or stderr:
                if not execution.output:
                    execution.output = {}
                if stdout:
                    execution.output["stdout"] = stdout
                if stderr:
                    execution.output["stderr"] = stderr

        else:
            execution.error_message = result_data.get("error_message", "Unknown error")
            if "traceback" in result_data:
                execution.output = {"traceback": result_data["traceback"]}

        db.commit()
        db.refresh(execution)

        return execution

    except Exception as e:
        # Update execution with error
        execution.status = "error"
        execution.error_message = str(e)
        execution.completed_at = datetime.utcnow()
        db.commit()
        db.refresh(execution)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Execution failed: {str(e)}"
        )


@router.get("/history/{alias}", response_model=List[ComponentExecutionResponse])
def get_execution_history(
    alias: str,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get execution history for a component."""
    # Get the component
    component = db.query(Component).filter(
        Component.alias == alias,
        Component.owner_id == current_user.id
    ).first()

    if not component:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Component '{alias}' not found"
        )

    # Get executions
    executions = db.query(ComponentExecution).filter(
        ComponentExecution.component_id == component.id
    ).order_by(ComponentExecution.started_at.desc()).limit(limit).all()

    return executions
