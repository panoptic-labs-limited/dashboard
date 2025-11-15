"""Page layout component."""

import uuid
from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class Page:
    """
    Represents a tab/view within a Dashboard.

    Must contain at least one Section.
    Pages appear as tabs in the dashboard UI.

    Example:
        Page(
            title="Overview",
            description="Sales overview and metrics",
            sections=[
                Section(title="Metrics", layout=Row([...]))
            ]
        )
    """
    title: str
    sections: List = field(default_factory=list)
    description: Optional[str] = None
    id: str = field(default_factory=lambda: f"page_{uuid.uuid4().hex[:8]}")

    def to_dict(self) -> dict:
        """Serialize to dictionary for dashboard structure."""
        return {
            "id": self.id,
            "type": "page",
            "title": self.title,
            "description": self.description,
            "sections": [
                section.to_dict() if hasattr(section, 'to_dict') else section
                for section in self.sections
            ]
        }
