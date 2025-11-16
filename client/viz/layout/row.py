"""Row layout component."""

import uuid
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
    id: str = field(default_factory=lambda: f"row_{uuid.uuid4().hex[:8]}")

    def __init__(self, columns: List = None, id: str = None):
        """Initialize with list of columns."""
        self.columns = columns or []
        self.id = id or f"row_{uuid.uuid4().hex[:8]}"

    def to_dict(self) -> dict:
        """Serialize to dictionary for dashboard structure."""
        return {
            "id": self.id,
            "type": "row",
            "children": [
                col.to_dict() if hasattr(col, 'to_dict') else col
                for col in self.columns
            ]
        }
