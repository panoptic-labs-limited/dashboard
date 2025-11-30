"""
PlotlyWidget for server-side rendered visualizations.

Uses RenderableComponent to generate Plotly JSON on the server.
The frontend simply displays the resulting figure.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from viz.core.datasource import ComponentSource
from .base import Widget


class PlotlyWidget(Widget):
    """
    Server-rendered Plotly visualization.

    Uses a RenderableComponent that implements load(), transform(), and render()
    to produce a Plotly figure on the server. The frontend displays the
    resulting JSON without modification.

    Use this when you need full control over the visualization, including
    custom Plotly configurations not available in frontend-native widgets.

    Note: The component referenced by data_source must be a RenderableComponent
    (i.e., must implement render() method). This is validated at runtime.

    Example:
        class SalesChart(RenderableComponent):
            region: str

            def load(self):
                return db.query(f"SELECT * FROM sales WHERE region = '{self.region}'")

            def transform(self, data):
                return aggregate_by_product(data)

            def render(self, data):
                import plotly.express as px
                fig = px.bar(data, x="product", y="sales", color="category")
                fig.update_layout(template="plotly_dark")
                return fig

        PlotlyWidget(
            title="Sales by Product",
            data_source=ComponentSource(component=SalesChart),
            params={"region": region_input}
        )
    """

    type: Literal["plotly"] = "plotly"

    # data_source should be a ComponentSource with a RenderableComponent
    # Runtime validation checks component has render() method
    data_source: ComponentSource = Field(
        ...,
        description="ComponentSource with a RenderableComponent"
    )
