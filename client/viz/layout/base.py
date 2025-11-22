"""
Base classes for layout framework.

Provides the foundational LayoutNode and Container classes that all
layout components inherit from.
"""

from __future__ import annotations
from typing import TypeVar, Generic, Iterator
from pydantic import BaseModel, Field, ConfigDict
import uuid


# ============================================================================
# Base Classes
# ============================================================================

class LayoutNode(BaseModel):
    """Base class for all layout nodes."""

    model_config = ConfigDict(
        extra='forbid',
        use_enum_values=True,
        validate_assignment=True
    )

    id: str = Field(default_factory=lambda: f"layout_{uuid.uuid4().hex[:8]}")
    type: str = Field(..., description="Discriminator for union types")


T = TypeVar('T', bound=LayoutNode)


class Container(LayoutNode, Generic[T]):
    """
    Generic container that can hold children of type T.

    Provides:
    - Type-safe children management
    - Iterator protocol
    - Context manager
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
        # Import here to avoid circular dependency
        from .builder import LayoutBuilder
        LayoutBuilder._push_context(self)
        return self

    def __exit__(self, *args):
        """
        Context manager exit.

        Pops this container from the context stack.
        """
        from .builder import LayoutBuilder
        LayoutBuilder._pop_context()
