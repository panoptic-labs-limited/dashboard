"""
Extraction logic for finding local components in a dashboard.

This module traverses the dashboard layout tree to:
- Extract all local Component classes from Widgets/Inputs (via ComponentSource)
- Deduplicate components
- Build mappings of component classes to their names

Note: With the new architecture, the Dashboard Service handles most of
the extraction logic. This module is primarily for CLI-side validation
and source file collection.
"""

from typing import Dict, Set, List, Tuple, Any

from viz.core.datasource import DataSource, ComponentSource
from viz.core.layout import Container
from viz.dashboard import Dashboard
from viz.inputs.base import Input
from viz.widgets import Widget


class ComponentExtractor:
    """
    Extracts local components from a dashboard for registration.

    Traverses the dashboard layout tree and collects all Component classes
    that are referenced via ComponentSource (i.e., local components that
    need to be registered with the Component Registry).

    External components (referenced by name string) are not extracted.
    """

    def __init__(self, dashboard: Dashboard):
        """
        Initialize extractor with a dashboard.

        Args:
            dashboard: Dashboard instance to extract from
        """
        self.dashboard = dashboard

        # Tracking sets (use class objects as keys for deduplication)
        self._component_classes: Set[type] = set()

        # Maps for serialization
        self.component_map: Dict[type, str] = {}  # Component class → name

        # List of classes (for serialization)
        self.components: List[Tuple[type, str]] = []  # (Component class, name)

    def extract(self) -> None:
        """
        Extract all local components from the dashboard.

        Populates:
        - self.components: List of (Component class, name) tuples
        - self.component_map: Component class → name mapping
        """
        self._traverse(self.dashboard)

    def _traverse(self, node: Any) -> None:
        """Recursively traverse layout tree and extract components."""

        # Handle Dashboard (has pages, not children)
        if isinstance(node, Dashboard):
            for page in node.pages:
                self._traverse(page)
            return

        # Handle Inputs (check for DataSource)
        if isinstance(node, Input):
            self._extract_from_data_source(node.source)
            self._extract_from_params(node.params)

        # Handle Widgets (check for DataSource)
        elif isinstance(node, Widget):
            self._extract_from_data_source(node.data_source)
            self._extract_from_params(node.params)

        # Recursively traverse containers
        if isinstance(node, Container) and hasattr(node, 'children'):
            for child in node.children:
                self._traverse(child)

    def _extract_from_data_source(self, source: DataSource | None) -> None:
        """Extract component class from a DataSource if it's a local ComponentSource."""
        if source is None:
            return

        if isinstance(source, ComponentSource):
            # Only extract if it's a class (local), not a string (external)
            if source.class_name is not None:
                self._extract_component_class(source.component)

    def _extract_from_params(self, params: dict[str, Any]) -> None:
        """Extract components from params that reference Inputs with sources."""
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
            component_class: Component class (Type[Component]) from a Widget/Input
        """
        # Skip if already extracted
        if component_class in self._component_classes:
            return

        # Get component name using the class method if available
        if hasattr(component_class, 'get_component_name'):
            name = component_class.get_component_name()
        else:
            # Fallback: use class name
            name = component_class.__name__

        # Record component class
        self._component_classes.add(component_class)
        self.component_map[component_class] = name
        self.components.append((component_class, name))

    def get_components(self) -> List[Tuple[type, str]]:
        """
        Get list of extracted components.

        Returns:
            List of (Component class, name) tuples
        """
        return self.components

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
