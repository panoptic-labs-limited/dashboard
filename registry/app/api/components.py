"""API endpoints for component management."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import User, Component
from app.auth import get_current_user
from viz_shared import (
    ComponentCreate,
    ComponentUpdate,
    ComponentResponse,
    ComponentParameter,
    validate_component_source,
    extract_component_parameters,
)

router = APIRouter(prefix="/components", tags=["components"])


@router.post("/", response_model=ComponentResponse, status_code=status.HTTP_201_CREATED)
def create_component(
    component_data: ComponentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new component."""
    # Check if alias already exists
    if db.query(Component).filter(Component.alias == component_data.alias).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Component with alias '{component_data.alias}' already exists"
        )

    # Validate the source code
    validation = validate_component_source(component_data.source_code)
    if not validation["valid"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid component source code: {', '.join(validation['errors'])}"
        )

    # Extract class name if not provided
    class_name = component_data.class_name
    if not class_name and validation["class_name"]:
        class_name = validation["class_name"]

    # Auto-extract parameters if not provided
    parameters = component_data.parameters
    if not parameters:
        extracted = extract_component_parameters(component_data.source_code, class_name)
        parameters = [ComponentParameter(**p) for p in extracted]

    # Create component
    db_component = Component(
        alias=component_data.alias,
        class_name=class_name,
        source_code=component_data.source_code,
        description=component_data.description,
        parameters=[p.model_dump() for p in parameters],
        metadata=component_data.metadata.model_dump() if component_data.metadata else {},
        memory_limit_mb=component_data.memory_limit_mb,
        timeout_seconds=component_data.timeout_seconds,
        owner_id=current_user.id
    )
    db.add(db_component)
    db.commit()
    db.refresh(db_component)

    return db_component


@router.get("/", response_model=List[ComponentResponse])
def list_components(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all components owned by the current user."""
    components = db.query(Component).filter(Component.owner_id == current_user.id).all()
    return components


@router.get("/{alias}", response_model=ComponentResponse)
def get_component(
    alias: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a component by alias."""
    component = db.query(Component).filter(
        Component.alias == alias,
        Component.owner_id == current_user.id
    ).first()

    if not component:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Component '{alias}' not found"
        )

    return component


@router.put("/{alias}", response_model=ComponentResponse)
def update_component(
    alias: str,
    component_data: ComponentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a component."""
    component = db.query(Component).filter(
        Component.alias == alias,
        Component.owner_id == current_user.id
    ).first()

    if not component:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Component '{alias}' not found"
        )

    # Validate source code if provided
    if component_data.source_code:
        validation = validate_component_source(component_data.source_code)
        if not validation["valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid component source code: {', '.join(validation['errors'])}"
            )

    # Update fields
    update_data = component_data.model_dump(exclude_unset=True)

    # Handle nested models
    if "parameters" in update_data and update_data["parameters"]:
        update_data["parameters"] = [p.model_dump() for p in component_data.parameters]
    if "metadata" in update_data and update_data["metadata"]:
        update_data["metadata"] = component_data.metadata.model_dump()

    for field, value in update_data.items():
        setattr(component, field, value)

    db.commit()
    db.refresh(component)

    return component


@router.delete("/{alias}", status_code=status.HTTP_204_NO_CONTENT)
def delete_component(
    alias: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a component."""
    component = db.query(Component).filter(
        Component.alias == alias,
        Component.owner_id == current_user.id
    ).first()

    if not component:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Component '{alias}' not found"
        )

    db.delete(component)
    db.commit()

    return None
