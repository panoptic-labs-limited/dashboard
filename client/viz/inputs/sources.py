"""Data sources for inputs.

DEPRECATED: This module is deprecated. Import from viz.core.datasource instead.

This module re-exports FunctionSource from viz.core.datasource for backward
compatibility. New code should import directly from viz.core.datasource.
"""

import warnings

# Re-export FunctionSource from new location for backward compatibility
from viz.core.datasource import FunctionSource

warnings.warn(
    "viz.inputs.sources is deprecated. Import FunctionSource from viz.core.datasource instead.",
    DeprecationWarning,
    stacklevel=2
)

__all__ = ["FunctionSource"]
