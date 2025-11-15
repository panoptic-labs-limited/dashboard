"""Section layout component."""

from typing import Optional, Union, List
from dataclasses import dataclass


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

    def to_dict(self) -> dict:
        """Serialize to dictionary for dashboard structure."""
        # Handle layout
        if hasattr(self.layout, 'to_dict'):
            layout_dict = self.layout.to_dict()
        elif isinstance(self.layout, list):
            # List of children
            layout_dict = {
                "type": "container",
                "children": [
                    child.to_dict() if hasattr(child, 'to_dict') else child
                    for child in self.layout
                ]
            }
        else:
            layout_dict = self.layout

        return {
            "type": "section",
            "title": self.title,
            "collapsible": self.collapsible,
            "layout": layout_dict
        }
