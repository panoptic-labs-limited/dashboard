"""
Serialization layer for converting client Python objects to registry API schemas.

This module handles the conversion of:
- Input objects → InputSchema (for API registration)
- Component instances → ComponentCreate schema
- Dashboard hierarchy → DashboardStructure schema

The serializer replaces Python object references with aliases/IDs for the registry.
"""

from typing import Any, Dict, List, Union
import uuid
import inspect

from viz.inputs.base import Input
from viz.inputs.sources import FunctionSource
from viz.core.component import Component
from viz.layout.dashboard import Dashboard, Page
from viz.layout.containers import Section, Row, Column, Tabs, Tab
from viz.layout.components import Widget
from viz.layout.base import Container


def serialize_input(input_obj: Input) -> Dict[str, Any]:
    """
    Serialize an Input object to API schema format.

    Converts Input instances to flat dictionaries suitable for API registration.
    - Flattens all fields to top level (no nested config)
    - Converts FunctionSource to {"type": "function", "alias": "..."}
    - Handles cascading input params

    Args:
        input_obj: Input instance (Select, DateInput, etc.)

    Returns:
        Dictionary matching InputSchema format from registry
    """
    # Start with base serialization from Pydantic
    data = input_obj.model_dump(exclude_none=True)

    # Ensure type is "input" for layout purposes (not the specific input_type like "select")
    data["type"] = "input"

    # Handle FunctionSource in source field
    if input_obj.source and isinstance(input_obj.source, FunctionSource):
        source = input_obj.source
        data["source"] = {
            "type": "function",
            "alias": source.func_id if hasattr(source, 'func_id') else source.func.__name__,
        }

        # Serialize params (handle Input references)
        if source.params:
            serialized_params = {}
            for param_name, param_value in source.params.items():
                if isinstance(param_value, Input):
                    # Reference to another input (cascading)
                    serialized_params[param_name] = {
                        "type": "input",
                        "id": param_value.id
                    }
                else:
                    # Literal value
                    serialized_params[param_name] = param_value
            data["source"]["params"] = serialized_params

    return data


def serialize_component(component_class: type, alias: str) -> Dict[str, Any]:
    """
    Serialize a Component class to ComponentCreate schema.

    Extracts source code and parameter definitions from a Component class.

    Args:
        component_class: Component class (Type[Component])
        alias: Unique identifier for this component

    Returns:
        Dictionary matching ComponentCreate schema
    """
    return {
        "alias": alias,
        "class_name": component_class.get_class_name(),
        "source_code": component_class.get_source_code(),
        "description": component_class.__doc__.strip() if component_class.__doc__ else None,
        "parameters": _extract_component_parameters(component_class),
        "metadata": {
            "name": component_class.__name__,
            "version": "1.0.0",
            "tags": []
        },
        "memory_limit_mb": 200,
        "timeout_seconds": 30
    }


def _extract_component_parameters(cls: type[Component]) -> List[Dict[str, Any]]:
    """Extract parameter definitions from Component class fields."""
    from pydantic_core import PydanticUndefined

    parameters = []

    for field_name, field_info in cls.model_fields.items():
        param = {
            "name": field_name,
            "type": str(field_info.annotation).replace("typing.", ""),
            "required": field_info.is_required(),
        }

        if field_info.description:
            param["description"] = field_info.description

        # Handle default values (skip if undefined or has default_factory)
        if not field_info.is_required():
            if field_info.default is not PydanticUndefined and field_info.default is not None:
                param["default"] = field_info.default
            elif field_info.default_factory is not None:
                # Call default_factory to get the actual default value
                try:
                    param["default"] = field_info.default_factory()
                except:
                    # If factory fails, skip default
                    pass

        parameters.append(param)

    return parameters


def serialize_widget(widget: Widget, input_map: Dict[str, str]) -> Dict[str, Any]:
    """
    Serialize a Widget to API schema format.

    Converts Widget with Component class/alias to schema with component_alias and
    parameter bindings.

    Args:
        widget: Widget instance
        input_map: Mapping of Input objects to their IDs

    Returns:
        Dictionary matching WidgetSchema format
    """
    data = {
        "type": "widget",
        "id": widget.id,
        "widget_type": widget.widget_type,
        "title": widget.title,
        "description": widget.description,
        "config": widget.config or {}
    }

    # Get component alias from either class or string
    component_alias = None
    if widget.component is not None:
        if isinstance(widget.component, str):
            # String alias provided directly
            component_alias = widget.component
        else:
            # Component class provided - extract alias
            component_alias = _get_component_alias(widget.component)

    if component_alias:
        data["component_alias"] = component_alias

        # Serialize widget params (which may contain Input bindings)
        params = {}
        for param_name, param_value in widget.params.items():
            if isinstance(param_value, Input):
                # Parameter bound to an input
                params[param_name] = {
                    "type": "input",
                    "input_id": param_value.id
                }
            else:
                # Literal value
                params[param_name] = param_value

        data["params"] = params

    return data


def _get_component_alias(component_class: type) -> str:
    """Get component alias, using __id__ if available, otherwise convert class name to snake_case."""
    # Check for explicit __id__ attribute first
    if hasattr(component_class, '__id__'):
        return component_class.__id__

    # Fallback: convert class name to snake_case
    import re
    name = component_class.__name__
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def serialize_dashboard(dashboard: Dashboard) -> Dict[str, Any]:
    """
    Serialize a Dashboard to DashboardStructure schema.

    Recursively converts the entire layout hierarchy to JSON format suitable
    for registry storage. Auto-generates IDs for containers that don't have them.

    Args:
        dashboard: Dashboard instance

    Returns:
        Dictionary matching DashboardStructure schema
    """
    # Build input map (Input object → ID)
    input_map = _build_input_map(dashboard)

    # Serialize dashboard structure
    structure = {
        "type": "dashboard",
        "id": dashboard.id,
        "title": dashboard.title,
        "description": dashboard.description,
        "version": dashboard.version,
        "children": [_serialize_page(page, input_map) for page in dashboard.children]
    }

    return structure


def _build_input_map(node: Any) -> Dict[str, str]:
    """
    Build a mapping of Input objects to their IDs by traversing the layout tree.

    Args:
        node: Dashboard or Container node

    Returns:
        Dictionary mapping Input objects to their IDs
    """
    input_map = {}

    def traverse(n):
        if isinstance(n, Input):
            input_map[id(n)] = n.id
        if isinstance(n, Container) and hasattr(n, 'children'):
            for child in n.children:
                traverse(child)
        # Note: Widgets use component_alias (string), not embedded Component instances
        # No need to check n.component since it doesn't exist

    traverse(node)
    return input_map


def _serialize_page(page: Page, input_map: Dict[str, str]) -> Dict[str, Any]:
    """Serialize a Page to schema format."""
    return {
        "type": "page",
        "id": page.id,
        "title": page.title,
        "description": page.description,
        "icon": page.icon,
        "children": [_serialize_node(child, input_map) for child in page.children]
    }


def _serialize_node(node: Any, input_map: Dict[str, str]) -> Dict[str, Any]:
    """
    Serialize any layout node to schema format.

    Handles: Section, Row, Column, Tabs, Tab, Widget, Input
    Auto-generates IDs for containers if not present.
    """
    if isinstance(node, Input):
        return serialize_input(node)

    elif isinstance(node, Widget):
        return serialize_widget(node, input_map)

    elif isinstance(node, Section):
        return {
            "type": "section",
            "id": node.id or _generate_id("section"),
            "title": node.title,
            "collapsible": node.collapsible,
            "collapsed": node.collapsed,
            "children": [_serialize_node(child, input_map) for child in node.children]
        }

    elif isinstance(node, Row):
        return {
            "type": "row",
            "id": node.id or _generate_id("row"),
            "gap": node.gap,
            "align": node.align,
            "children": [_serialize_node(child, input_map) for child in node.children]
        }

    elif isinstance(node, Column):
        return {
            "type": "column",
            "id": node.id or _generate_id("column"),
            "weight": node.weight,
            "gap": node.gap,
            "children": [_serialize_node(child, input_map) for child in node.children]
        }

    elif isinstance(node, Tabs):
        return {
            "type": "tabs",
            "id": node.id or _generate_id("tabs"),
            "default_tab": node.default_tab,
            "children": [_serialize_tab(tab, input_map) for tab in node.children]
        }

    elif isinstance(node, Tab):
        return _serialize_tab(node, input_map)

    else:
        raise ValueError(f"Unknown layout node type: {type(node)}")


def _serialize_tab(tab: Tab, input_map: Dict[str, str]) -> Dict[str, Any]:
    """Serialize a Tab to schema format."""
    return {
        "type": "tab",
        "id": tab.id or _generate_id("tab"),
        "title": tab.title,
        "icon": tab.icon,
        "disabled": tab.disabled,
        "children": [_serialize_node(child, input_map) for child in tab.children]
    }


def _generate_id(prefix: str) -> str:
    """Generate a unique ID with prefix."""
    return f"{prefix}_auto_{uuid.uuid4().hex[:8]}"
