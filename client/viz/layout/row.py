"""Row layout component."""

from typing import List
from dataclasses import dataclass, field


@dataclass
class Row:
    """
    Horizontal layout container.

    Contains columns arranged horizontally.
    Can be nested within Sections or Columns.

    Example:
        Row([
            Column(width="1/3", children=[selector1, selector2]),
            Column(width="2/3", children=[widget1])
        ])
    """
    columns: List = field(default_factory=list)

    def __init__(self, columns: List = None):
        """Initialize with list of columns."""
        self.columns = columns or []

    def to_dict(self) -> dict:
        """Serialize to dictionary for dashboard structure."""
        return {
            "type": "row",
            "children": [
                col.to_dict() if hasattr(col, 'to_dict') else col
                for col in self.columns
            ]
        }
