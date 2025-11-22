"""
Core layout framework using Pydantic.

Type-safe, hierarchical layout system with:
- Generic containers for type safety
- Discriminated unions for serialization
- Flexible nesting and composition
"""

from __future__ import annotations
from typing import (
    TypeVar, Generic, Union, Literal,
    List, Optional, Any, Iterator
)
from pydantic import (
    BaseModel, Field, ConfigDict,
    field_validator
)
from enum import Enum
import uuid


# ============================================================================
# Base Classes
# ============================================================================

class LayoutNode(BaseModel):
    """Base class for all layout nodes."""

    model_config = ConfigDict(
        extra='forbid',
        use_enum_values=True,
        validate_assignment=True
    )

    id: str = Field(default_factory=lambda: f"layout_{uuid.uuid4().hex[:8]}")
    type: str = Field(..., description="Discriminator for union types")


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

    children: List[T] = Field(default_factory=list)

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

    def __enter__(self) -> 'Container[T]':
        """
        Context manager entry.

        Pushes this container onto the context stack so children
        created within the context are automatically added.
        """
        # Import here to avoid circular dependency
        from .builder import LayoutBuilder
        LayoutBuilder._push_context(self)
        return self

    def __exit__(self, *args):
        """
        Context manager exit.

        Pops this container from the context stack.
        """
        from .builder import LayoutBuilder
        LayoutBuilder._pop_context()


# ============================================================================
# Enums
# ============================================================================

class WidgetType(str, Enum):
    """Supported widget types."""
    CHART = "chart"
    TABLE = "table"
    METRIC = "metric"
    TEXT = "text"
    IMAGE = "image"
    CUSTOM = "custom"


class SelectorType(str, Enum):
    """Supported selector types."""
    DROPDOWN = "dropdown"
    MULTI_SELECT = "multi_select"
    DATE = "date"
    DATE_RANGE = "date_range"
    SLIDER = "slider"
    TEXT_INPUT = "text_input"
    CHECKBOX = "checkbox"
    NUMERIC_INPUT = "numeric_input"


class ColumnWidth(str, Enum):
    """Standard column widths."""
    FULL = "1/1"
    HALF = "1/2"
    THIRD = "1/3"
    TWO_THIRDS = "2/3"
    QUARTER = "1/4"
    THREE_QUARTERS = "3/4"
    SIXTH = "1/6"
    FIVE_SIXTHS = "5/6"


# ============================================================================
# Leaf Components (No children)
# ============================================================================

class Widget(LayoutNode):
    """
    Leaf node representing a visualization or content widget.

    Examples: charts, tables, metrics, images
    """

    type: Literal["widget"] = "widget"
    widget_type: WidgetType
    title: Optional[str] = None
    description: Optional[str] = None

    # Component reference
    component_alias: Optional[str] = None
    params: dict[str, Any] = Field(default_factory=dict)

    # Widget-specific configuration
    config: dict[str, Any] = Field(default_factory=dict)


class Selector(LayoutNode):
    """
    Leaf node for user input components.

    Examples: dropdowns, date pickers, sliders
    """

    type: Literal["selector"] = "selector"
    selector_type: SelectorType
    name: str = Field(..., description="Parameter name")
    label: str
    default: Any = None
    options: Optional[List[Any]] = None

    # Selector-specific configuration
    config: dict[str, Any] = Field(default_factory=dict)


# ============================================================================
# Layout Containers (Forward references for recursive types)
# ============================================================================

# Forward reference types
RowChild = Union['Row', 'Column', Widget, Selector]
ColumnChild = Union['Row', 'Column', Widget, Selector]
TabChild = Union['Row', 'Column', Widget, Selector]
SectionChild = Union['Row', 'Column', 'Tabs', Widget, Selector]
PageChild = Union['Section', 'Row', 'Column', 'Tabs', Widget, Selector]


class Row(Container[RowChild]):
    """
    Horizontal layout container.

    Children are arranged left-to-right.
    Can contain: Rows, Columns, Widgets, Selectors
    """

    type: Literal["row"] = "row"
    gap: Optional[str] = Field(None, description="Gap between children (CSS)")
    align: Optional[Literal["start", "center", "end", "stretch"]] = None


class Column(Container[ColumnChild]):
    """
    Vertical layout container.

    Children are arranged top-to-bottom.
    Can contain: Rows, Columns, Widgets, Selectors
    """

    type: Literal["column"] = "column"
    width: ColumnWidth = ColumnWidth.FULL
    gap: Optional[str] = Field(None, description="Gap between children (CSS)")


class Tab(Container[TabChild]):
    """
    Individual tab within a Tabs container.

    Can contain: Rows, Columns, Widgets, Selectors
    """

    type: Literal["tab"] = "tab"
    title: str
    icon: Optional[str] = None
    disabled: bool = False


class Tabs(Container[Tab]):
    """
    Tab container holding multiple Tab components.

    Can only contain: Tab objects
    """

    type: Literal["tabs"] = "tabs"
    default_tab: Optional[str] = Field(
        None,
        description="ID of default active tab"
    )


class Section(Container[SectionChild]):
    """
    Section for organizing content within a Page.

    Can contain: Rows, Columns, Tabs, Widgets, Selectors
    """

    type: Literal["section"] = "section"
    title: Optional[str] = None
    collapsible: bool = False
    collapsed: bool = False


class Page(Container[PageChild]):
    """
    Page container representing a dashboard page/view.

    Can contain: Sections, Rows, Columns, Tabs, Widgets, Selectors
    """

    type: Literal["page"] = "page"
    title: str
    description: Optional[str] = None
    icon: Optional[str] = None


class Dashboard(Container[Page]):
    """
    Top-level dashboard container.

    Can only contain: Page objects
    """

    type: Literal["dashboard"] = "dashboard"
    title: str
    description: Optional[str] = None
    version: str = "1.0.0"

    @field_validator('children')
    @classmethod
    def validate_has_pages(cls, v: List[Page]) -> List[Page]:
        """Ensure dashboard has at least one page."""
        if not v:
            raise ValueError("Dashboard must have at least one page")
        return v

    def page(self, title: str, description: Optional[str] = None, **kwargs) -> Page:
        """
        Create and add a page to this dashboard.

        Args:
            title: Page title
            description: Optional description
            **kwargs: Additional page fields

        Returns:
            The created Page instance

        Example:
            >>> dashboard = Dashboard(title='My Dashboard')
            >>> with dashboard.page(title='Overview'):
            ...     L.widget(...)
        """
        page = Page(title=title, description=description, **kwargs)
        self.add(page)
        return page


# ============================================================================
# Discriminated Union for Serialization
# ============================================================================

# Define the discriminated union of all layout components
LayoutComponent = Union[
    Dashboard,
    Page,
    Section,
    Tabs,
    Tab,
    Row,
    Column,
    Widget,
    Selector
]

# Update forward references to resolve recursive types
Row.model_rebuild()
Column.model_rebuild()
Tab.model_rebuild()
Section.model_rebuild()
Page.model_rebuild()
