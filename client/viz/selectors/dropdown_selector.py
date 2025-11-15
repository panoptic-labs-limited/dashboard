"""Dropdown selector component."""

from typing import Optional, List, Callable, Union
from dataclasses import dataclass


@dataclass
class DropdownSelector:
    """
    Dropdown/select selector for dashboards.

    Provides single or multi-select dropdown that can be bound
    to component parameters.

    Example:
        # Static options
        region_selector = DropdownSelector(
            name="region",
            label="Region",
            options=["North", "South", "East", "West"],
            default="North"
        )

        # Dynamic options from data source
        product_selector = DropdownSelector(
            name="product",
            label="Product",
            data_source=get_available_products,
            default=None
        )

        # Multi-select
        categories = DropdownSelector(
            name="categories",
            label="Categories",
            options=["Electronics", "Clothing", "Food"],
            multi=True,
            default=["Electronics"]
        )
    """
    name: str
    label: Optional[str] = None
    options: Optional[List[str]] = None
    data_source: Optional[Callable] = None
    default: Optional[Union[str, List[str]]] = None
    multi: bool = False

    def __post_init__(self):
        """Validate and set defaults."""
        if self.label is None:
            self.label = self.name.replace("_", " ").title()

        if self.options is None and self.data_source is None:
            raise ValueError("Either 'options' or 'data_source' must be provided")

        if self.options is not None and self.data_source is not None:
            raise ValueError("Cannot specify both 'options' and 'data_source'")

    def to_dict(self) -> dict:
        """Serialize to dictionary for dashboard structure."""
        result = {
            "type": "selector",
            "selector_type": "dropdown",
            "name": self.name,
            "label": self.label,
            "multi": self.multi,
            "default": self.default
        }

        if self.options:
            result["options"] = self.options
        elif self.data_source:
            # If there's a data source function, include reference
            result["data_source"] = getattr(
                self.data_source,
                '_registry_alias',
                self.data_source.__name__
            )

        return result
