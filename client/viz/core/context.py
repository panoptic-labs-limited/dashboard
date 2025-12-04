"""
Context stack for the builder pattern.

Provides a global context stack that allows containers to automatically
track parent-child relationships when used as context managers.

This module exists to break circular dependencies between BaseContainer
and LayoutBuilder.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .layout import BaseContainer

# Global context stack
_context_stack: list['BaseContainer'] = []


def push_context(container: 'BaseContainer') -> None:
    """Push a container onto the context stack."""
    _context_stack.append(container)


def pop_context() -> Optional['BaseContainer']:
    """Pop a container from the context stack."""
    return _context_stack.pop() if _context_stack else None


def current_context() -> Optional['BaseContainer']:
    """Get the current context container (top of stack)."""
    return _context_stack[-1] if _context_stack else None


def add_to_context(child) -> None:
    """Add a child to the current context container if one exists."""
    parent = current_context()
    if parent is not None:
        parent.add(child)
