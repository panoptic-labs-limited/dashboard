"""Column layout component."""

import uuid
from typing import List, Union, Optional, Literal
from dataclasses import dataclass, field


WidthSpec = Literal["1/1", "1/2", "1/3", "2/3", "1/4", "3/4", "1/6", "5/6"]


@dataclass
class Column:
    """
    Vertical layout container.

    Can contain:
    - Widgets (component instances)
    - Selectors (input elements)
    - Nested Rows

    Example:
        Column(
            width="1/3",
            children=[date_selector, region_selector]
        )
    """
    children: List = field(default_factory=list)
    width: WidthSpec = "1/1"
    id: str = field(default_factory=lambda: f"column_{uuid.uuid4().hex[:8]}")

    def to_dict(self) -> dict:
        """Serialize to dictionary for dashboard structure."""
        return {
            "id": self.id,
            "type": "column",
            "width": self.width,
            "children": [
                child.to_dict() if hasattr(child, 'to_dict') else child
                for child in self.children
            ]
        }
