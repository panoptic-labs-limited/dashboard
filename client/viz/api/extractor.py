"""
Extraction logic for finding components and functions in a dashboard.

This module traverses the dashboard layout tree to:
- Extract all Component instances from Widgets
- Extract all function-based data sources from Inputs
- Deduplicate components/functions
- Build mappings of objects to their aliases
"""

from typing import Dict, Set, List, Tuple, Any
import inspect

from viz.inputs.base import Input
from viz.inputs.sources import FunctionSource
from viz.core.component import Component
from viz.layout.dashboard import Dashboard
from viz.layout.containers import Section, Row, Column, Tabs, Tab
from viz.layout.components import Widget
from viz.layout.base import Container


class ComponentExtractor:
    """
    Extracts components and functions from a dashboard for registration.

    Traverses the dashboard layout tree and collects:
    - All Component instances (class-based components)
    - All function-based data sources (from FunctionSource)
    - Maintains deduplication to avoid re-registering the same component
    """

    def __init__(self, dashboard: Dashboard):
        """
        Initialize extractor with a dashboard.

        Args:
            dashboard: Dashboard instance to extract from
        """
        self.dashboard = dashboard

        # Tracking sets (use class/function objects as keys for deduplication)
        self._component_classes: Set[type] = set()
        self._functions: Set[Any] = set()

        # Maps for serialization
        self.component_map: Dict[type, str] = {}  # Component class → alias
        self.function_map: Dict[Any, str] = {}     # Function → alias

        # Lists of instances (for serialization)
        self.components: List[Tuple[Component, str]] = []  # (instance, alias)
        self.functions: List[Tuple[Any, str]] = []          # (function, alias)

    def extract(self) -> None:
        """
        Extract all components and functions from the dashboard.

        Populates:
        - self.components: List of (Component instance, alias) tuples
        - self.functions: List of (function, alias) tuples
        - self.component_map: Component class → alias mapping
        - self.function_map: Function → alias mapping
        """
        # Traverse dashboard and collect components/functions
        self._traverse(self.dashboard)

    def _traverse(self, node: Any) -> None:
        """Recursively traverse layout tree and extract components/functions."""

        # Handle Inputs (check for FunctionSource)
        if isinstance(node, Input):
            if node.source and isinstance(node.source, FunctionSource):
                self._extract_function_source(node.source)

        # Handle Widgets (check for Component instances)
        elif isinstance(node, Widget):
            if node.component:
                self._extract_component(node.component)

        # Recursively traverse containers
        if isinstance(node, Container) and hasattr(node, 'children'):
            for child in node.children:
                self._traverse(child)

    def _extract_component(self, component: Component) -> None:
        """
        Extract a Component instance.

        Args:
            component: Component instance from a Widget
        """
        cls = component.__class__

        # Skip if already extracted
        if cls in self._component_classes:
            return

        # Get component alias
        if hasattr(cls, '__id__'):
            alias = cls.__id__
        else:
            # Fallback to lowercase class name
            alias = cls.__name__.lower()

        # Record component
        self._component_classes.add(cls)
        self.component_map[cls] = alias
        self.components.append((component, alias))

    def _extract_function_source(self, source: FunctionSource) -> None:
        """
        Extract a function from FunctionSource.

        Args:
            source: FunctionSource instance from an Input
        """
        func = source.func

        # Skip if already extracted
        if func in self._functions:
            return

        # Get function alias (from decorator or function name)
        if hasattr(source, 'func_id'):
            alias = source.func_id
        else:
            alias = func.__name__

        # Record function
        self._functions.add(func)
        self.function_map[func] = alias
        self.functions.append((func, alias))

        # Also check function params for cascading Input references
        if source.params:
            for param_value in source.params.values():
                if isinstance(param_value, Input):
                    # Recursively extract functions from cascaded inputs
                    if param_value.source and isinstance(param_value.source, FunctionSource):
                        self._extract_function_source(param_value.source)

    def get_components(self) -> List[Tuple[Component, str]]:
        """
        Get list of extracted components.

        Returns:
            List of (Component instance, alias) tuples
        """
        return self.components

    def get_functions(self) -> List[Tuple[Any, str]]:
        """
        Get list of extracted functions.

        Returns:
            List of (function, alias) tuples
        """
        return self.functions

    def get_component_alias(self, component: Component) -> str:
        """
        Get the alias for a component instance.

        Args:
            component: Component instance

        Returns:
            Component alias

        Raises:
            KeyError: If component not found (should call extract() first)
        """
        cls = component.__class__
        return self.component_map[cls]

    def get_function_alias(self, func: Any) -> str:
        """
        Get the alias for a function.

        Args:
            func: Function object

        Returns:
            Function alias

        Raises:
            KeyError: If function not found (should call extract() first)
        """
        return self.function_map[func]


def extract_function_code(func: Any) -> str:
    """
    Extract source code from a function.

    Args:
        func: Function object

    Returns:
        Function source code as string
    """
    try:
        return inspect.getsource(func)
    except (OSError, TypeError) as e:
        raise ValueError(f"Could not extract source code for function {func.__name__}: {e}")


def serialize_function(func: Any, alias: str) -> Dict[str, Any]:
    """
    Serialize a function to FunctionCreate schema.

    Args:
        func: Function object
        alias: Function alias/ID

    Returns:
        Dictionary matching FunctionCreate schema
    """
    return {
        "alias": alias,
        "code": extract_function_code(func),
        "description": func.__doc__.strip() if func.__doc__ else None,
        "memory_limit_mb": 200,
        "timeout_seconds": 30
    }
