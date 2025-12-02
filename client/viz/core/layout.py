"""
Core layout node classes.

This module contains the foundational classes that all layout
and input components inherit from:
- LayoutNode: Base class for all nodes
- LeafNode: Base class for nodes without children (Widget, Input)
- Container: Base class for nodes with children (Row, Column, etc.)
"""

from __future__ import annotations

import uuid
from typing import Any, TypeVar, Generic, Iterator

from pydantic import BaseModel, Field, ConfigDict, field_serializer

from viz.core.reference import NamedReference


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


class LeafNode(LayoutNode):
    """
    Base class for leaf nodes in the layout tree.

    Leaf nodes do not contain children. Examples include:
    - Widget
    - Input (Select, TextInput, etc.)

    This class exists to differentiate leaf nodes from container nodes.
    """

    pass


class ParameterizedNode(LeafNode):
    """
    Base class for leaf nodes that accept parameters.

    Provides the params field and serialization logic for converting
    NamedReference instances to {ref: name} format.

    Extended by Widget and Input.
    """

    params: dict[str, Any] = Field(
        default_factory=dict,
        description="Parameters (can reference Inputs via NamedReference)"
    )

    @field_serializer('params')
    def serialize_params(self, params: dict[str, Any]) -> dict[str, Any]:
        """Serialize params, converting NamedReference instances to {ref: name}."""
        serialized = {}
        for key, value in params.items():
            if isinstance(value, NamedReference):
                serialized[key] = {"ref": value.name}
            else:
                serialized[key] = value
        return serialized


# Type variable for Container's children
T = TypeVar('T', bound=LayoutNode)


class Container(LayoutNode, Generic[T]):
    """
    Generic container that can hold children of type T.

    Base class for all layout containers (Row, Column, Section, etc.).

    Provides:
    - Type-safe children management
    - Iterator protocol
    - Context manager (for builder pattern)
    - Indexing
    """

    children: list[T] = Field(default_factory=list)

    def add(self, child: T) -> Container[T]:
        """Add a child component."""
        self.children.append(child)
        return self

    def remove(self, child: T) -> Container[T]:
        """Remove a child component."""
        self.children.remove(child)
        return self

    def clear(self) -> Container[T]:
        """Remove all children."""
        self.children.clear()
        return self

    def __iter__(self) -> Iterator[T]:
        """Iterate over children."""
        return iter(self.children)

    def __len__(self) -> int:
        """Number of children."""
        return len(self.children)

    def __getitem__(self, index: int) -> T:
        """Get child by index."""
        return self.children[index]

    def __enter__(self) -> Container[T]:
        """
        Context manager entry.

        Pushes this container onto the context stack so children
        created within the context are automatically added.
        """
        from viz.core.context import push_context
        push_context(self)
        return self

    def __exit__(self, *args):
        """
        Context manager exit.

        Pops this container from the context stack.
        """
        from viz.core.context import pop_context
        pop_context()
