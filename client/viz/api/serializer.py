"""
Serialization layer for converting client Python objects to registry API schemas.

This module handles the conversion of:
- Input objects → InputSchema (for API registration)
- Component instances → ComponentCreate schema
- Dashboard hierarchy → DashboardStructure schema
- DataSource objects → DataSourceSchema
- Widget objects → WidgetSchema (various types)

The serializer replaces Python object references with names/IDs for the registry.
"""

import uuid
from typing import Any, Dict, List

from viz.core.component import Component
from viz.core.datasource import DataSource, TimeseriesSource, ComponentSource, FunctionSource
from viz.core.layout import Container
from viz.inputs.base import Input
from viz.layout.containers import Section, Row, Column, Tabs, Tab
from viz.layout.dashboard import Dashboard, Page
from viz.widgets import (
    Widget,
    LineChartWidget,
    BarChartWidget,
    AreaChartWidget,
    TableWidget,
    MetricWidget,
)


def serialize_data_source(source: DataSource) -> Dict[str, Any]:
    """
    Serialize a DataSource to API schema format.

    Handles all DataSource types:
    - TimeseriesSource: {"type": "timeseries", "name": "..."}
    - ComponentSource: {"type": "component", "name": "..."}
    - FunctionSource: {"type": "function", "name": "..."}

    Args:
        source: DataSource instance

    Returns:
        Dictionary matching DataSourceSchema format
    """
    if isinstance(source, TimeseriesSource):
        return {
            "type": "timeseries",
            "name": source.name
        }

    elif isinstance(source, ComponentSource):
        # Get component name from class or string
        if isinstance(source.component, str):
            component_name = source.component
        else:
            component_name = _get_component_name(source.component)
        return {
            "type": "component",
            "name": component_name
        }

    elif isinstance(source, FunctionSource):
        # Get function name
        if hasattr(source, 'func_name'):
            func_name = source.func_name
        elif hasattr(source.func, '__name__'):
            func_name = source.func.__name__
        else:
            func_name = str(source.func)
        return {
            "type": "function",
            "name": func_name
        }

    else:
        raise ValueError(f"Unknown DataSource type: {type(source)}")


def serialize_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Serialize widget/input params, handling Input references.

    Args:
        params: Dictionary of parameter name to value (may include Input refs)

    Returns:
        Serialized params with Input references replaced
    """
    serialized = {}
    for param_name, param_value in params.items():
        if isinstance(param_value, Input):
            # Reference to an input (for cascading/binding)
            serialized[param_name] = {
                "type": "input",
                "input_id": param_value.id
            }
        else:
            # Literal value
            serialized[param_name] = param_value
    return serialized


def serialize_input(input_obj: Input) -> Dict[str, Any]:
    """
    Serialize an Input object to API schema format.

    Converts Input instances to flat dictionaries suitable for API registration.
    - Flattens all fields to top level (no nested config)
    - Serializes DataSource with serialize_data_source()
    - Serializes params with serialize_params()

    Args:
        input_obj: Input instance (Select, DateInput, etc.)

    Returns:
        Dictionary matching InputSchema format from registry
    """
    # Start with base serialization from Pydantic
    data = input_obj.model_dump(exclude_none=True)

    # Ensure type is "input" for layout purposes (not the specific input_type like "select")
    data["type"] = "input"

    # Serialize source if present
    if input_obj.source is not None:
        data["source"] = serialize_data_source(input_obj.source)

    # Serialize params (may contain Input references)
    if input_obj.params:
        data["params"] = serialize_params(input_obj.params)

    return data


def serialize_component(component_class: type, name: str) -> Dict[str, Any]:
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

    Args:
        widget: Widget instance (LineChartWidget, PlotlyWidget, etc.)
        input_map: Mapping of Input objects to their IDs

    Returns:
        Dictionary matching WidgetSchema format
    """
    # Get widget type from the concrete class
    widget_type = getattr(widget, 'type', 'widget')

    data = {
        "type": "widget",
        "id": widget.id,
        "widget_type": widget_type,
        "title": widget.title,
        "description": widget.description,
    }

    # Serialize data_source
    data["data_source"] = serialize_data_source(widget.data_source)

    # Serialize params (may contain Input references)
    if widget.params:
        data["params"] = serialize_params(widget.params)

    # Add widget-specific config based on widget type
    config = _extract_widget_config(widget)
    if config:
        data["config"] = config

    return data


def _extract_widget_config(widget: Widget) -> Dict[str, Any]:
    """Extract widget-specific configuration fields."""
    config = {}

    if isinstance(widget, (LineChartWidget, BarChartWidget, AreaChartWidget)):
        # Chart widgets have x, y, series, etc.
        if hasattr(widget, 'x') and widget.x:
            config["x"] = widget.x
        if hasattr(widget, 'y') and widget.y:
            config["y"] = widget.y
        if hasattr(widget, 'series') and widget.series:
            config["series"] = widget.series
        if hasattr(widget, 'color') and widget.color:
            config["color"] = widget.color

    elif isinstance(widget, TableWidget):
        # Table widgets have columns, pagination, etc.
        if hasattr(widget, 'columns') and widget.columns:
            config["columns"] = widget.columns
        if hasattr(widget, 'page_size'):
            config["page_size"] = widget.page_size
        if hasattr(widget, 'sortable'):
            config["sortable"] = widget.sortable
        if hasattr(widget, 'filterable'):
            config["filterable"] = widget.filterable

    elif isinstance(widget, MetricWidget):
        # Metric widgets have value_field, comparison, etc.
        if hasattr(widget, 'value_field') and widget.value_field:
            config["value_field"] = widget.value_field
        if hasattr(widget, 'format') and widget.format:
            config["format"] = widget.format
        if hasattr(widget, 'comparison_value') and widget.comparison_value is not None:
            config["comparison_value"] = widget.comparison_value
        if hasattr(widget, 'comparison_label') and widget.comparison_label:
            config["comparison_label"] = widget.comparison_label

    # PlotlyWidget doesn't have additional config - the render() produces the figure

    return config


def _get_component_name(component_class: type) -> str:
    """Get component name, using __component_name__ if available, otherwise convert class name to snake_case."""
    # Check for explicit __component_name__ attribute first
    if hasattr(component_class, '__component_name__'):
        return component_class.__component_name__

    # Fallback: convert class name to snake_case
    import re
    class_name = component_class.__name__
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', class_name)
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
        # Note: Widget.data_source contains DataSource objects (not embedded components)
        # Components/functions are extracted separately by ComponentExtractor

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
