"""
Fluent builder API for creating layouts.

Provides convenient factory methods and fluent interface
for building dashboard layouts.
"""

from typing import Optional, List, Any
from .base import (
    Dashboard, Page, Section, Tabs, Tab,
    Row, Column, Widget, Selector,
    WidgetType, SelectorType, ColumnWidth
)


class LayoutBuilder:
    """Fluent builder for creating layouts."""

    @staticmethod
    def dashboard(title: str, description: Optional[str] = None, **kwargs) -> Dashboard:
        """
        Create a new dashboard.

        Args:
            title: Dashboard title
            description: Optional description
            **kwargs: Additional fields (version, etc.)

        Returns:
            Dashboard instance

        Example:
            >>> dashboard = LayoutBuilder.dashboard(
            ...     title="Sales Dashboard",
            ...     description="Q1 2024 sales analytics"
            ... )
        """
        return Dashboard(title=title, description=description, **kwargs)

    @staticmethod
    def page(title: str, description: Optional[str] = None, **kwargs) -> Page:
        """
        Create a new page.

        Args:
            title: Page title
            description: Optional description
            **kwargs: Additional fields (icon, etc.)

        Returns:
            Page instance
        """
        return Page(title=title, description=description, **kwargs)

    @staticmethod
    def section(
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
        """
        return Section(title=title, collapsible=collapsible, **kwargs)

    @staticmethod
    def tabs(default_tab: Optional[str] = None, **kwargs) -> Tabs:
        """
        Create a tabs container.

        Args:
            default_tab: ID of default active tab
            **kwargs: Additional fields

        Returns:
            Tabs instance
        """
        return Tabs(default_tab=default_tab, **kwargs)

    @staticmethod
    def tab(title: str, icon: Optional[str] = None, **kwargs) -> Tab:
        """
        Create a tab.

        Args:
            title: Tab title
            icon: Optional icon name
            **kwargs: Additional fields (disabled, etc.)

        Returns:
            Tab instance
        """
        return Tab(title=title, icon=icon, **kwargs)

    @staticmethod
    def row(gap: Optional[str] = None, **kwargs) -> Row:
        """
        Create a row.

        Args:
            gap: Gap between children (CSS value)
            **kwargs: Additional fields (align, etc.)

        Returns:
            Row instance

        Example:
            >>> row = LayoutBuilder.row(gap="20px", align="center")
        """
        return Row(gap=gap, **kwargs)

    @staticmethod
    def column(
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
        """
        return Column(width=width, gap=gap, **kwargs)

    @staticmethod
    def widget(
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
        """
        return Widget(
            widget_type=widget_type,
            title=title,
            component_alias=component_alias,
            params=params or {},
            **kwargs
        )

    @staticmethod
    def selector(
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
        """
        return Selector(
            selector_type=selector_type,
            name=name,
            label=label,
            default=default,
            options=options,
            **kwargs
        )


# Convenience alias
L = LayoutBuilder
