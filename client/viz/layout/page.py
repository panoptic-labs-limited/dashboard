"""Page layout component."""

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

    def to_dict(self) -> dict:
        """Serialize to dictionary for dashboard structure."""
        return {
            "type": "page",
            "title": self.title,
            "description": self.description,
            "sections": [
                section.to_dict() if hasattr(section, 'to_dict') else section
                for section in self.sections
            ]
        }
