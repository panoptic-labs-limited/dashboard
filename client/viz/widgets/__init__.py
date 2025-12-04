"""
Widget components for dashboard visualizations.

Widgets are leaf nodes that display data. They combine:
- A DataSource (where data comes from)
- Visualization configuration (how to display it)
- Optional params (how to query the data source)

Widget Types:
- Frontend-native: LineChartWidget, BarChartWidget, AreaChartWidget, TableWidget, MetricWidget
- Server-rendered: PlotlyWidget (uses RenderableComponent)
"""

from .base import BaseWidget
from .charts import LineChartWidget, BarChartWidget, AreaChartWidget
from .metric import MetricWidget
from .plotly import PlotlyWidget
from .table import TableWidget

__all__ = [
    # Base
    "BaseWidget",
    # Charts (frontend-native)
    "LineChartWidget",
    "BarChartWidget",
    "AreaChartWidget",
    # Table (frontend-native)
    "TableWidget",
    # Metric (frontend-native)
    "MetricWidget",
    # Plotly (server-rendered)
    "PlotlyWidget",
]
