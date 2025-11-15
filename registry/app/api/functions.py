from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, Function
from app.schemas import FunctionCreate, FunctionUpdate, FunctionResponse
from app.auth import get_current_user

router = APIRouter(prefix="/functions", tags=["functions"])


@router.post("/", response_model=FunctionResponse, status_code=status.HTTP_201_CREATED)
def create_function(
    function_data: FunctionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new function."""
    # Check if alias already exists
    if db.query(Function).filter(Function.alias == function_data.alias).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Function with alias '{function_data.alias}' already exists"
        )

    # Validate the code (basic check)
    try:
        compile(function_data.code, '<string>', 'exec')
    except SyntaxError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid Python code: {str(e)}"
        )

    # Create function
    db_function = Function(
        alias=function_data.alias,
        code=function_data.code,
        description=function_data.description,
        memory_limit_mb=function_data.memory_limit_mb,
        timeout_seconds=function_data.timeout_seconds,
        owner_id=current_user.id
    )
    db.add(db_function)
    db.commit()
    db.refresh(db_function)

    return db_function


@router.get("/", response_model=List[FunctionResponse])
def list_functions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all functions owned by the current user."""
    functions = db.query(Function).filter(Function.owner_id == current_user.id).all()
    return functions


@router.get("/{alias}", response_model=FunctionResponse)
def get_function(
    alias: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a function by alias."""
    function = db.query(Function).filter(
        Function.alias == alias,
        Function.owner_id == current_user.id
    ).first()

    if not function:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Function '{alias}' not found"
        )

    return function


@router.put("/{alias}", response_model=FunctionResponse)
def update_function(
    alias: str,
    function_data: FunctionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a function."""
    function = db.query(Function).filter(
        Function.alias == alias,
        Function.owner_id == current_user.id
    ).first()

    if not function:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Function '{alias}' not found"
        )

    # Validate code if provided
    if function_data.code:
        try:
            compile(function_data.code, '<string>', 'exec')
        except SyntaxError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid Python code: {str(e)}"
            )

    # Update fields
    update_data = function_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(function, field, value)

    db.commit()
    db.refresh(function)

    return function


@router.delete("/{alias}", status_code=status.HTTP_204_NO_CONTENT)
def delete_function(
    alias: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a function."""
    function = db.query(Function).filter(
        Function.alias == alias,
        Function.owner_id == current_user.id
    ).first()

    if not function:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Function '{alias}' not found"
        )

    db.delete(function)
    db.commit()

    return None
