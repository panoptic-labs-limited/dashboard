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

        # Lists of classes/functions (for serialization)
        self.components: List[Tuple[type, str]] = []  # (Component class, alias)
        self.functions: List[Tuple[Any, str]] = []     # (function, alias)

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

        # Handle Widgets (check for Component class or string alias)
        elif isinstance(node, Widget):
            if node.component is not None and not isinstance(node.component, str):
                # Only extract if it's a Component class (not a string alias)
                self._extract_component_class(node.component)

        # Recursively traverse containers
        if isinstance(node, Container) and hasattr(node, 'children'):
            for child in node.children:
                self._traverse(child)

    def _extract_component_class(self, component_class: type) -> None:
        """
        Extract a Component class.

        Args:
            component_class: Component class (Type[Component]) from a Widget
        """
        # Skip if already extracted
        if component_class in self._component_classes:
            return

        # Get component alias
        if hasattr(component_class, '__id__'):
            alias = component_class.__id__
        else:
            # Fallback: convert class name to snake_case
            import re
            name = component_class.__name__
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            alias = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

        # Record component class
        self._component_classes.add(component_class)
        self.component_map[component_class] = alias
        self.components.append((component_class, alias))

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

    def get_components(self) -> List[Tuple[type, str]]:
        """
        Get list of extracted components.

        Returns:
            List of (Component class, alias) tuples
        """
        return self.components

    def get_functions(self) -> List[Tuple[Any, str]]:
        """
        Get list of extracted functions.

        Returns:
            List of (function, alias) tuples
        """
        return self.functions

    def get_component_alias(self, component_class: type) -> str:
        """
        Get the alias for a component class.

        Args:
            component_class: Component class

        Returns:
            Component alias

        Raises:
            KeyError: If component not found (should call extract() first)
        """
        return self.component_map[component_class]

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
