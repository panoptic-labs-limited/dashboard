"""
Serialization layer for converting client Python objects to registry API schemas.

With the new architecture, most serialization is handled by Pydantic's model_dump().
DataSource objects (ComponentSource, TimeseriesSource) serialize themselves correctly.

This module provides:
- serialize_dashboard(): Full dashboard serialization with source file
- serialize_params(): Handle Input references in params
- Helper functions for specific use cases
"""

import uuid
from typing import Any, Dict, List

from pydantic_core import PydanticUndefined

from viz.core.component import Component
from viz.core.layout import Container
from viz.inputs.base import Input
from viz.layout.containers import Section, Row, Column, Tabs, Tab
from viz.layout.dashboard import Dashboard, Page
from viz.widgets import Widget


def serialize_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Serialize widget/input params, handling Input references.

    Args:
        params: Dictionary of parameter name to value (may include Input refs)

    Returns:
        Serialized params with Input references converted to {input_ref: id}
    """
    serialized = {}
    for param_name, param_value in params.items():
        if isinstance(param_value, Input):
            # Reference to an input (for reactive binding)
            serialized[param_name] = {"input_ref": param_value.id}
        else:
            # Literal value
            serialized[param_name] = param_value
    return serialized


def serialize_input(input_obj: Input) -> Dict[str, Any]:
    """
    Serialize an Input object to API schema format.

    Uses Pydantic model_dump() and handles params serialization.
    """
    data = input_obj.model_dump(exclude_none=True)

    # Serialize params (may contain Input references)
    if input_obj.params:
        data["params"] = serialize_params(input_obj.params)

    return data


def serialize_widget(widget: Widget) -> Dict[str, Any]:
    """
    Serialize a Widget to API schema format.

    Uses Pydantic model_dump() and handles params serialization.
    """
    data = widget.model_dump(exclude_none=True)

    # Serialize params (may contain Input references)
    if widget.params:
        data["params"] = serialize_params(widget.params)

    return data


def serialize_component(component_class: type[Component], name: str) -> Dict[str, Any]:
    """
    Serialize a Component class to ComponentCreate schema.

    Extracts source code and parameter definitions from a Component class.

    Args:
        component_class: Component class (Type[Component])
        name: Unique identifier for this component

    Returns:
        Dictionary matching ComponentCreate schema
    """
    return {
        "name": name,
        "class_name": component_class.get_class_name(),
        "source_code": component_class.get_source_code(),
        "description": component_class.__doc__.strip() if component_class.__doc__ else None,
        "parameters": _extract_component_parameters(component_class),
        "metadata": {
            "class_name": component_class.__name__,
            "version": "1.0.0",
            "tags": []
        },
        "memory_limit_mb": 200,
        "timeout_seconds": 30
    }


def _extract_component_parameters(cls: type[Component]) -> List[Dict[str, Any]]:
    """Extract parameter definitions from Component class fields."""
    parameters = []

    for field_name, field_info in cls.model_fields.items():
        param = {
            "name": field_name,
            "type": str(field_info.annotation).replace("typing.", ""),
            "required": field_info.is_required(),
        }

        if field_info.description:
            param["description"] = field_info.description

        # Handle default values
        if not field_info.is_required():
            if field_info.default is not PydanticUndefined and field_info.default is not None:
                param["default"] = field_info.default
            elif field_info.default_factory is not None:
                try:
                    param["default"] = field_info.default_factory()
                except Exception:
                    pass

        parameters.append(param)

    return parameters


def serialize_dashboard(dashboard: Dashboard) -> Dict[str, Any]:
    """
    Serialize a Dashboard to DashboardStructure schema.

    Recursively converts the entire layout hierarchy to JSON format.
    Uses model_dump() where possible, with special handling for:
    - Input references in params
    - Auto-generating IDs for containers without them

    Args:
        dashboard: Dashboard instance

    Returns:
        Dictionary matching DashboardStructure schema
    """
    return {
        "type": "dashboard",
        "id": dashboard.id,
        "title": dashboard.title,
        "description": dashboard.description,
        "version": dashboard.version,
        "pages": [_serialize_page(page) for page in dashboard.children]
    }


def _serialize_page(page: Page) -> Dict[str, Any]:
    """Serialize a Page to schema format."""
    return {
        "type": "page",
        "id": page.id,
        "title": page.title,
        "description": page.description,
        "icon": page.icon,
        "children": [_serialize_node(child) for child in page.children]
    }


def _serialize_node(node: Any) -> Dict[str, Any]:
    """
    Serialize any layout node to schema format.

    Handles: Section, Row, Column, Tabs, Tab, Widget, Input
    """
    if isinstance(node, Input):
        return serialize_input(node)

    elif isinstance(node, Widget):
        return serialize_widget(node)

    elif isinstance(node, Section):
        return {
            "type": "section",
            "id": node.id or _generate_id("section"),
            "title": node.title,
            "collapsible": node.collapsible,
            "collapsed": node.collapsed,
            "children": [_serialize_node(child) for child in node.children]
        }

    elif isinstance(node, Row):
        return {
            "type": "row",
            "id": node.id or _generate_id("row"),
            "gap": node.gap,
            "align": node.align,
            "children": [_serialize_node(child) for child in node.children]
        }

    elif isinstance(node, Column):
        return {
            "type": "column",
            "id": node.id or _generate_id("column"),
            "weight": node.weight,
            "gap": node.gap,
            "children": [_serialize_node(child) for child in node.children]
        }

    elif isinstance(node, Tabs):
        return {
            "type": "tabs",
            "id": node.id or _generate_id("tabs"),
            "default_tab": node.default_tab,
            "children": [_serialize_tab(tab) for tab in node.children]
        }

    elif isinstance(node, Tab):
        return _serialize_tab(node)

    else:
        raise ValueError(f"Unknown layout node type: {type(node)}")


def _serialize_tab(tab: Tab) -> Dict[str, Any]:
    """Serialize a Tab to schema format."""
    return {
        "type": "tab",
        "id": tab.id or _generate_id("tab"),
        "title": tab.title,
        "icon": tab.icon,
        "disabled": tab.disabled,
        "children": [_serialize_node(child) for child in tab.children]
    }


def _generate_id(prefix: str) -> str:
    """Generate a unique ID with prefix."""
    return f"{prefix}_auto_{uuid.uuid4().hex[:8]}"
