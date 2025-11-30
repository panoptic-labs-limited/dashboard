"""
Extraction logic for finding components and functions in a dashboard.

This module traverses the dashboard layout tree to:
- Extract all Component classes from Widgets (via ComponentSource)
- Extract all function-based data sources from Inputs and Widgets
- Deduplicate components/functions
- Build mappings of objects to their names
"""

import inspect
from typing import Dict, Set, List, Tuple, Any

from viz.core.layout import Container
from viz.core.datasource import DataSource, ComponentSource, FunctionSource
from viz.inputs.base import Input
from viz.widgets import Widget
from viz.layout.dashboard import Dashboard


class ComponentExtractor:
    """
    Extracts components and functions from a dashboard for registration.

    Traverses the dashboard layout tree and collects:
    - All Component classes (from ComponentSource in widgets)
    - All function-based data sources (from FunctionSource in inputs/widgets)
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
        self.component_map: Dict[type, str] = {}  # Component class → name
        self.function_map: Dict[Any, str] = {}     # Function → name

        # Lists of classes/functions (for serialization)
        self.components: List[Tuple[type, str]] = []  # (Component class, name)
        self.functions: List[Tuple[Any, str]] = []     # (function, name)

    def extract(self) -> None:
        """
        Extract all components and functions from the dashboard.

        Populates:
        - self.components: List of (Component class, name) tuples
        - self.functions: List of (function, name) tuples
        - self.component_map: Component class → name mapping
        - self.function_map: Function → name mapping
        """
        # Traverse dashboard and collect components/functions
        self._traverse(self.dashboard)

    def _traverse(self, node: Any) -> None:
        """Recursively traverse layout tree and extract components/functions."""

        # Handle Inputs (check for DataSource)
        if isinstance(node, Input):
            self._extract_from_data_source(node.source)
            # Also check params for cascading Input references
            self._extract_from_params(node.params)

        # Handle Widgets (check for DataSource)
        elif isinstance(node, Widget):
            self._extract_from_data_source(node.data_source)
            # Also check params for cascading Input references
            self._extract_from_params(node.params)

        # Recursively traverse containers
        if isinstance(node, Container) and hasattr(node, 'children'):
            for child in node.children:
                self._traverse(child)

    def _extract_from_data_source(self, source: DataSource | None) -> None:
        """Extract component or function from a DataSource."""
        if source is None:
            return

        if isinstance(source, ComponentSource):
            # ComponentSource has a component class or string
            if source.component is not None and not isinstance(source.component, str):
                self._extract_component_class(source.component)

        elif isinstance(source, FunctionSource):
            self._extract_function_source(source)

    def _extract_from_params(self, params: dict[str, Any]) -> None:
        """Extract functions from params that reference Inputs with sources."""
        if not params:
            return

        for param_value in params.values():
            if isinstance(param_value, Input):
                # Recursively extract from cascaded inputs
                self._extract_from_data_source(param_value.source)
                self._extract_from_params(param_value.params)

    def _extract_component_class(self, component_class: type) -> None:
        """
        Extract a Component class.

        Args:
            component_class: Component class (Type[Component]) from a Widget
        """
        # Skip if already extracted
        if component_class in self._component_classes:
            return

        # Get component name
        if hasattr(component_class, '__name__'):
            # Check for explicit __component_name__ attribute first
            if hasattr(component_class, '__component_name__'):
                name = component_class.__component_name__
            else:
                # Fallback: convert class name to snake_case
                import re
                class_name = component_class.__name__
                s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', class_name)
                name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        else:
            name = str(component_class)

        # Record component class
        self._component_classes.add(component_class)
        self.component_map[component_class] = name
        self.components.append((component_class, name))

    def _extract_function_source(self, source: FunctionSource) -> None:
        """
        Extract a function from FunctionSource.

        Args:
            source: FunctionSource instance from an Input or Widget
        """
        func = source.func

        # Skip if already extracted
        if func in self._functions:
            return

        # Get function name (from decorator or function name)
        if hasattr(source, 'func_name'):
            name = source.func_name
        elif hasattr(func, '__name__'):
            name = func.__name__
        else:
            name = str(func)

        # Record function
        self._functions.add(func)
        self.function_map[func] = name
        self.functions.append((func, name))

    def get_components(self) -> List[Tuple[type, str]]:
        """
        Get list of extracted components.

        Returns:
            List of (Component class, name) tuples
        """
        return self.components

    def get_functions(self) -> List[Tuple[Any, str]]:
        """
        Get list of extracted functions.

        Returns:
            List of (function, name) tuples
        """
        return self.functions

    def get_component_name(self, component_class: type) -> str:
        """
        Get the name for a component class.

        Args:
            component_class: Component class

        Returns:
            Component name

        Raises:
            KeyError: If component not found (should call extract() first)
        """
        return self.component_map[component_class]

    def get_function_name(self, func: Any) -> str:
        """
        Get the name for a function.

        Args:
            func: Function object

        Returns:
            Function name

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


def serialize_function(func: Any, name: str) -> Dict[str, Any]:
    """
    Serialize a function to FunctionCreate schema.

    Args:
        func: Function object
        name: Function name

    Returns:
        Dictionary matching FunctionCreate schema
    """
    return {
        "name": name,
        "code": extract_function_code(func),
        "description": func.__doc__.strip() if func.__doc__ else None,
        "memory_limit_mb": 200,
        "timeout_seconds": 30
    }
