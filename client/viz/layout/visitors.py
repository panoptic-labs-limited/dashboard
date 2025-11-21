"""
Common visitor implementations for layout traversal.

Provides useful visitors for analyzing and transforming layout trees.
"""

from typing import List, Dict, Any
from .base import (
    LayoutVisitor, Dashboard, Page, Section,
    Tabs, Tab, Row, Column, Widget, Selector
)


class BaseTraversalVisitor(LayoutVisitor):
    """
    Base visitor that traverses entire tree.

    Override specific methods to add custom behavior while
    maintaining automatic traversal of children.
    """

    def visit_dashboard(self, node: Dashboard) -> Any:
        for child in node.children:
            child.accept(self)

    def visit_page(self, node: Page) -> Any:
        for child in node.children:
            child.accept(self)

    def visit_section(self, node: Section) -> Any:
        for child in node.children:
            child.accept(self)

    def visit_tabs(self, node: Tabs) -> Any:
        for child in node.children:
            child.accept(self)

    def visit_tab(self, node: Tab) -> Any:
        for child in node.children:
            child.accept(self)

    def visit_row(self, node: Row) -> Any:
        for child in node.children:
            child.accept(self)

    def visit_column(self, node: Column) -> Any:
        for child in node.children:
            child.accept(self)

    def visit_widget(self, node: Widget) -> Any:
        pass  # Leaf node

    def visit_selector(self, node: Selector) -> Any:
        pass  # Leaf node


class WidgetCollector(BaseTraversalVisitor):
    """
    Collects all widgets in the layout tree.

    Example:
        >>> collector = WidgetCollector()
        >>> dashboard.accept(collector)
        >>> widgets = collector.widgets
    """

    def __init__(self):
        self.widgets: List[Widget] = []

    def visit_widget(self, node: Widget) -> Any:
        self.widgets.append(node)


class SelectorCollector(BaseTraversalVisitor):
    """
    Collects all selectors in the layout tree.

    Example:
        >>> collector = SelectorCollector()
        >>> dashboard.accept(collector)
        >>> selectors = collector.selectors
    """

    def __init__(self):
        self.selectors: List[Selector] = []

    def visit_selector(self, node: Selector) -> Any:
        self.selectors.append(node)


class ComponentDependencyAnalyzer(BaseTraversalVisitor):
    """
    Analyzes component dependencies in the dashboard.

    Collects all component aliases and their parameters.
    """

    def __init__(self):
        self.components: Dict[str, List[Dict[str, Any]]] = {}

    def visit_widget(self, node: Widget) -> Any:
        if node.component_alias:
            if node.component_alias not in self.components:
                self.components[node.component_alias] = []

            self.components[node.component_alias].append({
                'widget_id': node.id,
                'params': node.params,
                'widget_type': node.widget_type
            })


class LayoutStatistics(BaseTraversalVisitor):
    """
    Collects statistics about the layout.

    Example:
        >>> stats = LayoutStatistics()
        >>> dashboard.accept(stats)
        >>> print(stats.summary())
    """

    def __init__(self):
        self.page_count = 0
        self.section_count = 0
        self.tab_count = 0
        self.widget_count = 0
        self.selector_count = 0
        self.max_depth = 0
        self._current_depth = 0

    def _enter_container(self):
        """Track depth when entering a container."""
        self._current_depth += 1
        self.max_depth = max(self.max_depth, self._current_depth)

    def _exit_container(self):
        """Track depth when exiting a container."""
        self._current_depth -= 1

    def visit_page(self, node: Page) -> Any:
        self.page_count += 1
        self._enter_container()
        super().visit_page(node)
        self._exit_container()

    def visit_section(self, node: Section) -> Any:
        self.section_count += 1
        self._enter_container()
        super().visit_section(node)
        self._exit_container()

    def visit_tab(self, node: Tab) -> Any:
        self.tab_count += 1
        self._enter_container()
        super().visit_tab(node)
        self._exit_container()

    def visit_widget(self, node: Widget) -> Any:
        self.widget_count += 1

    def visit_selector(self, node: Selector) -> Any:
        self.selector_count += 1

    def summary(self) -> Dict[str, int]:
        """Get statistics summary."""
        return {
            'pages': self.page_count,
            'sections': self.section_count,
            'tabs': self.tab_count,
            'widgets': self.widget_count,
            'selectors': self.selector_count,
            'max_depth': self.max_depth
        }


class JsonSerializer(BaseTraversalVisitor):
    """
    Serialize layout to dictionary (for JSON export).

    This is redundant with Pydantic's model_dump() but shows
    how custom serialization could be implemented.
    """

    def __init__(self):
        self.result = None

    def _serialize_container(self, node) -> dict:
        """Serialize a container node."""
        return {
            'id': node.id,
            'type': node.type,
            'children': [self._serialize_node(child) for child in node.children]
        }

    def _serialize_node(self, node) -> dict:
        """Serialize any node."""
        if isinstance(node, (Dashboard, Page, Section, Tabs, Tab, Row, Column)):
            base = node.model_dump(exclude={'children'})
            base['children'] = [self._serialize_node(child) for child in node.children]
            return base
        else:
            return node.model_dump()

    def visit_dashboard(self, node: Dashboard) -> dict:
        self.result = self._serialize_node(node)
        return self.result
