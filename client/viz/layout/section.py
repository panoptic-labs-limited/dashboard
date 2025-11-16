"""Section layout component."""

import uuid
from typing import Optional, Union, List
from dataclasses import dataclass, field


@dataclass
class Section:
    """
    Groups related content within a Page.

    Must be a direct child of Page.
    Can contain Rows, Columns, or direct children.

    Example:
        Section(
            title="Sales Metrics",
            collapsible=True,
            layout=Row([...])
        )
    """
    layout: Union['Row', 'Column', List]
    title: Optional[str] = None
    collapsible: bool = False
    id: str = field(default_factory=lambda: f"section_{uuid.uuid4().hex[:8]}")

    def to_dict(self) -> dict:
        """Serialize to dictionary for dashboard structure."""
        # Convert layout to children array
        children = []

        if hasattr(self.layout, 'to_dict'):
            # Single Row or Column
            children = [self.layout.to_dict()]
        elif isinstance(self.layout, list):
            # List of Row/Column objects
            children = [
                child.to_dict() if hasattr(child, 'to_dict') else child
                for child in self.layout
            ]

        return {
            "id": self.id,
            "type": "section",
            "title": self.title,
            "collapsible": self.collapsible,
            "collapsed": False,
            "children": children
        }
