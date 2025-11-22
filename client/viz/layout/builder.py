"""
Fluent builder API for creating layouts.

Provides convenient factory methods and fluent interface
for building dashboard layouts.
"""

from typing import Optional, List, Any

from .base import Container
from .enums import WidgetType, SelectorType, ColumnWidth
from .components import Widget, Selector
from .containers import Row, Column, Tab, Tabs, Section
from .dashboard import Page


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
        width: ColumnWidth = ColumnWidth.FULL,
        gap: Optional[str] = None,
        **kwargs
    ) -> Column:
        """
        Create a column.

        Args:
            width: Column width (fraction)
            gap: Gap between children (CSS value)
            **kwargs: Additional fields

        Returns:
            Column instance

        Example:
            >>> col = LayoutBuilder.column(width=ColumnWidth.HALF)

        Note:
            If called within a context manager, automatically adds to parent.
        """
        column = Column(width=width, gap=gap, **kwargs)
        cls._add_to_context(column)
        return column

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

    @classmethod
    def selector(
        cls,
        selector_type: SelectorType,
        name: str,
        label: str,
        default: Any = None,
        options: Optional[List[Any]] = None,
        **kwargs
    ) -> Selector:
        """
        Create a selector.

        Args:
            selector_type: Type of selector
            name: Parameter name
            label: Display label
            default: Default value
            options: List of options (for dropdown/multi-select)
            **kwargs: Additional fields (config, etc.)

        Returns:
            Selector instance

        Example:
            >>> selector = LayoutBuilder.selector(
            ...     selector_type=SelectorType.DROPDOWN,
            ...     name="region",
            ...     label="Select Region",
            ...     options=["North", "South", "East", "West"],
            ...     default="North"
            ... )

        Note:
            If called within a context manager, automatically adds to parent.
        """
        selector = Selector(
            selector_type=selector_type,
            name=name,
            label=label,
            default=default,
            options=options,
            **kwargs
        )
        parent = cls._current_context()
        if parent is not None:
            parent.add(selector)
        return selector


# Convenience alias
L = LayoutBuilder
