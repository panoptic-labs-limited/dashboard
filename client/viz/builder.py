"""
Fluent builder API for creating layouts.

Provides convenient factory methods and fluent interface
for building dashboard layouts.
"""

from typing import Optional, List, Any

from viz.layout.base import Container
from viz.layout.components import Widget
from viz.layout.containers import Row, Column, Tab, Tabs, Section
from viz.layout.dashboard import Page
from viz.layout.enums import WidgetType


class LayoutBuilder:
    """Fluent builder for creating layouts."""

    # Context stack for automatic parent tracking
    _context_stack: List['Container'] = []

    @classmethod
    def _current_context(cls) -> Optional['Container']:
        """Get the current context container."""
        return cls._context_stack[-1] if cls._context_stack else None

    @classmethod
    def _push_context(cls, container: 'Container'):
        """Push a container onto the context stack."""
        cls._context_stack.append(container)

    @classmethod
    def _pop_context(cls) -> Optional['Container']:
        """Pop a container from the context stack."""
        return cls._context_stack.pop() if cls._context_stack else None

    @classmethod
    def _add_to_context(cls, child):
        """Add a child to the current context container if one exists."""
        parent = cls._current_context()
        if parent is not None:
            parent.add(child)

    @classmethod
    def page(cls, title: str, description: Optional[str] = None, **kwargs) -> Page:
        """
        Create a new page.

        Args:
            title: Page title
            description: Optional description
            **kwargs: Additional fields (icon, etc.)

        Returns:
            Page instance

        Note:
            If called within a context manager, automatically adds to parent.
        """
        page = Page(title=title, description=description, **kwargs)
        cls._add_to_context(page)
        return page

    @classmethod
    def section(
        cls,
        title: Optional[str] = None,
        collapsible: bool = False,
        **kwargs
    ) -> Section:
        """
        Create a new section.

        Args:
            title: Optional section title
            collapsible: Whether section can be collapsed
            **kwargs: Additional fields

        Returns:
            Section instance

        Note:
            If called within a context manager, automatically adds to parent.
        """
        section = Section(title=title, collapsible=collapsible, **kwargs)
        cls._add_to_context(section)
        return section

    @classmethod
    def tabs(cls, default_tab: Optional[str] = None, **kwargs) -> Tabs:
        """
        Create a tabs container.

        Args:
            default_tab: ID of default active tab
            **kwargs: Additional fields

        Returns:
            Tabs instance

        Note:
            If called within a context manager, automatically adds to parent.
        """
        tabs = Tabs(default_tab=default_tab, **kwargs)
        cls._add_to_context(tabs)
        return tabs

    @classmethod
    def tab(cls, title: str, icon: Optional[str] = None, **kwargs) -> Tab:
        """
        Create a tab.

        Args:
            title: Tab title
            icon: Optional icon name
            **kwargs: Additional fields (disabled, etc.)

        Returns:
            Tab instance

        Note:
            If called within a context manager, automatically adds to parent.
        """
        tab = Tab(title=title, icon=icon, **kwargs)
        cls._add_to_context(tab)
        return tab

    @classmethod
    def row(cls, gap: Optional[str] = None, **kwargs) -> Row:
        """
        Create a row.

        Args:
            gap: Gap between children (CSS value)
            **kwargs: Additional fields (align, etc.)

        Returns:
            Row instance

        Example:
            >>> row = LayoutBuilder.row(gap="20px", align="center")

        Note:
            If called within a context manager, automatically adds to parent.
        """
        row = Row(gap=gap, **kwargs)
        cls._add_to_context(row)
        return row

    @classmethod
    def column(
        cls,
        weight: int = 1,
        gap: Optional[str] = None,
        **kwargs
    ) -> Column:
        """
        Create a column.

        Args:
            weight: Column weight for relative width (like CSS flex-grow)
            gap: Gap between children (CSS value)
            **kwargs: Additional fields

        Returns:
            Column instance

        Example:
            >>> col = LayoutBuilder.column(weight=2)

        Note:
            If called within a context manager, automatically adds to parent.
        """
        column = Column(weight=weight, gap=gap, **kwargs)
        cls._add_to_context(column)
        return column

    @classmethod
    def columns(cls, *weights: int) -> tuple[Column, ...]:
        """
        Create a row with columns of specified weights.

        Returns a tuple of Column instances that can be unpacked and used
        with context managers. The containing Row is automatically added
        to the current context.

        Args:
            *weights: Integer weights for each column (like CSS flex-grow).
                     E.g., columns(1, 2) creates two columns with 1/3 and 2/3 width.

        Returns:
            Tuple of Column instances

        Examples:
            # Create two equal columns
            col1, col2 = L.columns(1, 1)
            with col1:
                L.widget(...)
            with col2:
                L.widget(...)

            # Create three columns: 1/4, 1/2, 1/4
            left, center, right = L.columns(1, 2, 1)

        Note:
            The Row is automatically added to the current context (if any).
        """
        if not weights:
            raise ValueError("Must specify at least one weight")
        if any(w < 1 for w in weights):
            raise ValueError("Weights must be >= 1")

        # Create row and add to current context
        row = Row()
        cls._add_to_context(row)

        # Create columns with weights and add to row
        cols = tuple(Column(weight=w) for w in weights)
        for col in cols:
            row.add(col)

        return cols

    @classmethod
    def input(cls, input_instance):
        """
        Add an input to the current layout context.

        Args:
            input_instance: An input instance (Select, DateInput, etc.)

        Returns:
            The input instance (for convenience)

        Example:
            >>> from viz import Select
            >>> region = L.input(Select(
            ...     name="region",
            ...     options=["North", "South"]
            ... ))

        Note:
            The input is automatically added to the current context (if any).
            Returns the input instance so you can store it in a variable.
        """
        cls._add_to_context(input_instance)
        return input_instance

    @classmethod
    def widget(
        cls,
        widget_type: WidgetType,
        title: Optional[str] = None,
        component_alias: Optional[str] = None,
        params: Optional[dict[str, Any]] = None,
        **kwargs
    ) -> Widget:
        """
        Create a widget.

        Args:
            widget_type: Type of widget
            title: Optional widget title
            component_alias: Alias of component to render
            params: Component parameters
            **kwargs: Additional fields (description, config, etc.)

        Returns:
            Widget instance

        Example:
            >>> widget = LayoutBuilder.widget(
            ...     widget_type=WidgetType.CHART,
            ...     title="Sales Chart",
            ...     component_alias="sales_chart",
            ...     params={"region": "North"}
            ... )

        Note:
            If called within a context manager, automatically adds to parent.
        """
        widget = Widget(
            widget_type=widget_type,
            title=title,
            component_alias=component_alias,
            params=params or {},
            **kwargs
        )
        parent = cls._current_context()
        if parent is not None:
            parent.add(widget)
        return widget


# Convenience alias
L = LayoutBuilder
