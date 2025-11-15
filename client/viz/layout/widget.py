"""Widget wrapper for components."""

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from viz.core.component import Component


class Widget:
    """
    Wrapper around a Component instance.

    Handles parameter binding and manages component metadata
    for rendering in dashboards.

    Example:
        widget = Widget(
            component=SalesChart(
                start_date=date_selector,
                region=region_selector
            ),
            title="Sales by Region"
        )
    """

    def __init__(self, component: 'Component', title: Optional[str] = None):
        """
        Initialize widget with a component instance.

        Args:
            component: Component instance with parameters bound
            title: Optional title to display above the widget
        """
        self.component = component
        self.title = title or component.__class__.__name__

    def to_dict(self) -> dict:
        """Serialize to dictionary for dashboard structure."""
        # Extract component class info
        component_class = self.component.__class__
        component_alias = getattr(component_class, '_registry_alias', component_class.__name__)

        # Extract parameter values (bound selectors or literal values)
        params = {}
        if hasattr(component_class, '__dataclass_fields__'):
            for field_name in component_class.__dataclass_fields__.keys():
                value = getattr(self.component, field_name)

                # Check if value is a selector (has a 'name' attribute)
                if hasattr(value, 'name') and hasattr(value, 'to_dict'):
                    # It's a selector - bind to it
                    params[field_name] = {
                        "type": "selector",
                        "name": value.name
                    }
                else:
                    # It's a literal value
                    params[field_name] = {
                        "type": "literal",
                        "value": value
                    }

        return {
            "type": "widget",
            "title": self.title,
            "component_alias": component_alias,
            "params": params
        }
