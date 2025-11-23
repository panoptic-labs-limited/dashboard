"""
Container class for layout framework.

Provides the Container class that layout components use for managing children.
LayoutNode has been moved to viz/core/layout.py to avoid circular imports.
"""

from __future__ import annotations

from typing import TypeVar, Generic, Iterator

from pydantic import Field

from viz.core.layout import LayoutNode

# ============================================================================
# Container Class
# ============================================================================

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
        from viz.builder import LayoutBuilder
        LayoutBuilder._push_context(self)
        return self

    def __exit__(self, *args):
        """
        Context manager exit.

        Pops this container from the context stack.
        """
        from viz.builder import LayoutBuilder
        LayoutBuilder._pop_context()
