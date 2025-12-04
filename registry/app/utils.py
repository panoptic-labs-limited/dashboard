"""Utility functions for Viz framework."""

import json
from typing import Any, Dict, Union

from .types import RenderOutputType
from .schemas import RenderOutput


def serialize_render_output(output: Any) -> RenderOutput:
    """
    Serialize render output from components.

    Handles:
    - Plotly figures (plotly.graph_objects.Figure)
    - Altair charts (altair.Chart)
    - Vega-Lite specs (dict)
    - Custom JSON (dict)

    Args:
        output: The render output from a component

    Returns:
        RenderOutput: Serialized output with type and data

    Raises:
        ValueError: If output type is not supported
    """
    # Check if it's a Plotly figure
    if hasattr(output, 'to_json') and hasattr(output, 'data'):
        # It's likely a Plotly figure
        try:
            import plotly.io as pio
            plotly_json = pio.to_json(output)
            return RenderOutput(
                type=RenderOutputType.PLOTLY,
                data=json.loads(plotly_json)  # Convert to dict
            )
        except ImportError:
            raise ValueError("Plotly is not installed but output appears to be a Plotly figure")

    # Check if it's an Altair chart
    if hasattr(output, 'to_dict') and hasattr(output, 'mark'):
        # It's likely an Altair chart
        try:
            vega_spec = output.to_dict()
            return RenderOutput(
                type=RenderOutputType.ALTAIR,
                data=vega_spec
            )
        except Exception as e:
            raise ValueError(f"Failed to serialize Altair chart: {e}")

    # Check if it's a dict (Vega-Lite spec or custom)
    if isinstance(output, dict):
        # Try to detect if it's a Vega-Lite spec
        if any(key in output for key in ['mark', 'layer', 'hconcat', 'vconcat', 'facet']):
            return RenderOutput(
                type=RenderOutputType.VEGA_LITE,
                data=output
            )
        else:
            # Treat as custom
            return RenderOutput(
                type=RenderOutputType.CUSTOM,
                data=output
            )

    # Unsupported type
    raise ValueError(
        f"Unsupported render output type: {type(output)}. "
        "Expected Plotly figure, Altair chart, or dict."
    )


def validate_component_source(source_code: str) -> Dict[str, Any]:
    """
    Validate component source code.

    Checks:
    - Syntax is valid Python
    - Contains a class definition
    - Class has load, transform, and render methods

    Args:
        source_code: Python source code to validate

    Returns:
        Dict with validation results:
        - valid: bool
        - class_name: str (if found)
        - methods: List[str] (methods found)
        - errors: List[str] (validation errors)
    """
    import ast
    import inspect

    result = {
        "valid": False,
        "class_name": None,
        "methods": [],
        "errors": []
    }

    try:
        # Parse the source code
        tree = ast.parse(source_code)

        # Find class definitions
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

        if not classes:
            result["errors"].append("No class definition found in source code")
            return result

        # Use the first class found
        class_def = classes[0]
        result["class_name"] = class_def.name

        # Get methods
        methods = [node.name for node in class_def.body if isinstance(node, ast.FunctionDef)]
        result["methods"] = methods

        # Check for required methods
        required_methods = ["load", "transform", "render"]
        missing_methods = [m for m in required_methods if m not in methods]

        if missing_methods:
            result["errors"].append(f"Missing required methods: {', '.join(missing_methods)}")
            return result

        # All checks passed
        result["valid"] = True

    except SyntaxError as e:
        result["errors"].append(f"Syntax error: {e}")
    except Exception as e:
        result["errors"].append(f"Validation error: {e}")

    return result


def extract_component_parameters(source_code: str, class_name: str) -> list:
    """
    Extract parameter definitions from component's load method.

    Args:
        source_code: Component source code
        class_name: Name of the component class

    Returns:
        List of parameter dicts with name, type, and default info
    """
    import ast
    import inspect
    from typing import get_type_hints

    try:
        # Parse and execute the source code to get the class
        namespace = {}
        exec(source_code, namespace)
        component_class = namespace.get(class_name)

        if not component_class:
            return []

        # Get the load method
        load_method = getattr(component_class, 'load', None)
        if not load_method:
            return []

        # Get signature
        sig = inspect.signature(load_method)
        params = []

        for param_name, param in sig.parameters.items():
            if param_name in ['self', 'cls']:
                continue

            param_info = {
                "name": param_name,
                "type": "Any",
                "required": param.default == inspect.Parameter.empty,
                "default": None if param.default == inspect.Parameter.empty else param.default,
                "description": None
            }

            # Try to get type annotation
            if param.annotation != inspect.Parameter.empty:
                param_info["type"] = str(param.annotation).replace("<class '", "").replace("'>", "")

            params.append(param_info)

        return params

    except Exception:
        return []


def generate_unique_id(prefix: str = "") -> str:
    """Generate a unique ID for containers nodes."""
    import uuid
    unique = str(uuid.uuid4())[:8]
    return f"{prefix}_{unique}" if prefix else unique
