"""
Base LayoutNode class.

This module contains the foundational LayoutNode class that all layout
and input components inherit from.
"""

from __future__ import annotations

import uuid

from pydantic import BaseModel, Field, ConfigDict


class LayoutNode(BaseModel):
    """
    Base class for all layout nodes.

    Provides common fields for all layout and input components:
    - id: Unique identifier
    - type: Discriminator for union types (used for serialization)

    All layout containers (Row, Column, etc.) and input components
    (Select, TextInput, etc.) extend this class.
    """

    model_config = ConfigDict(
        extra='forbid',
        use_enum_values=True,
        validate_assignment=True
    )

    id: str = Field(default_factory=lambda: f"layout_{uuid.uuid4().hex[:8]}")
    type: str = Field(..., description="Discriminator for union types")
