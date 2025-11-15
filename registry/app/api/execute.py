from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import User, Function, Execution
from app.schemas import ExecutionRequest, ExecutionResponse
from app.auth import get_current_user
from app.executor import executor

router = APIRouter(prefix="/execute", tags=["execute"])


@router.post("/{alias}", response_model=ExecutionResponse)
def execute_function(
    alias: str,
    execution_request: ExecutionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Execute a function by alias."""
    # Get the function
    function = db.query(Function).filter(
        Function.alias == alias,
        Function.owner_id == current_user.id
    ).first()

    if not function:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Function '{alias}' not found"
        )

    # Create execution record
    execution = Execution(
        function_id=function.id,
        input_params=execution_request.params,
        status="running",
        started_at=datetime.utcnow()
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)

    try:
        # Execute the function
        status_result, result_data = executor.execute(
            code=function.code,
            params=execution_request.params,
            timeout_seconds=function.timeout_seconds,
            memory_limit_mb=function.memory_limit_mb
        )

        # Update execution record
        execution.status = status_result
        execution.completed_at = datetime.utcnow()

        if status_result == "success":
            execution.output = {"result": result_data.get("output")}
            execution.execution_time_ms = result_data.get("execution_time_ms")
            execution.memory_used_mb = result_data.get("memory_used_mb")

            # Add stdout/stderr if present
            if result_data.get("stdout"):
                execution.output["stdout"] = result_data["stdout"]
            if result_data.get("stderr"):
                execution.output["stderr"] = result_data["stderr"]
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


@router.get("/history/{alias}", response_model=list[ExecutionResponse])
def get_execution_history(
    alias: str,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get execution history for a function."""
    # Get the function
    function = db.query(Function).filter(
        Function.alias == alias,
        Function.owner_id == current_user.id
    ).first()

    if not function:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Function '{alias}' not found"
        )

    # Get executions
    executions = db.query(Execution).filter(
        Execution.function_id == function.id
    ).order_by(Execution.started_at.desc()).limit(limit).all()

    return executions
