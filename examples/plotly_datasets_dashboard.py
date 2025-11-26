"""
Rich Example Dashboard using Plotly Built-in Datasets

This example showcases the Viz framework's capabilities:
- Multiple components with load/transform/render pipeline
- Various input types (Select, DateRange, Slider, etc.)
- Data sources with cascading inputs
- Rich visualizations using Plotly Express

To serve this dashboard:
    export VIZ_USERNAME=your_username
    export VIZ_PASSWORD=your_password
    streamviz serve examples/plotly_datasets_dashboard.py
"""

import plotly.express as px
import pandas as pd
from datetime import datetime
from pydantic import Field

from viz import (
    Component, L, Dashboard,
    Select, DateRangeInput, Slider, MultiSelect, Toggle
)
from viz.layout import WidgetType


# ==============================================================================
# Data Source Functions (for dynamic input options)
# ==============================================================================

def get_available_datasets():
    """Get list of available Plotly datasets."""
    return [
        {"value": "gapminder", "label": "Gapminder (Countries)"},
        {"value": "tips", "label": "Tips (Restaurant)"},
        {"value": "iris", "label": "Iris (Flowers)"},
        {"value": "stocks", "label": "Stock Prices"},
    ]


def get_countries():
    """Get list of countries from gapminder dataset."""
    df = px.data.gapminder()
    countries = sorted(df['country'].unique().tolist())
    return [{"value": c, "label": c} for c in countries]


def get_continents():
    """Get list of continents."""
    df = px.data.gapminder()
    continents = sorted(df['continent'].unique().tolist())
    return [{"value": c, "label": c} for c in continents]


# ==============================================================================
# Components (with load/transform/render pipeline)
# ==============================================================================

class GapminderTrends(Component):
    """
    Show GDP per capita and life expectancy trends over time.

    Demonstrates: Multi-series line charts, filtering by continent
    """
    __id__ = "gapminder_trends"

    continent: str = "Asia"
    show_population: bool = False

    def load(self):
        """Load gapminder dataset."""
        return px.data.gapminder()

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Filter by continent and aggregate."""
        filtered = data[data['continent'] == self.continent].copy()

        # Calculate weighted averages by year
        grouped = filtered.groupby('year', as_index=False).apply(
            lambda x: pd.Series({
                'gdpPercap': (x['gdpPercap'] * x['pop']).sum() / x['pop'].sum(),
                'lifeExp': (x['lifeExp'] * x['pop']).sum() / x['pop'].sum(),
                'pop': x['pop'].sum()
            }), include_groups=False
        ).reset_index()

        return grouped

    def render(self, data: pd.DataFrame):
        """Create dual-axis line chart."""
        from plotly.subplots import make_subplots
        import plotly.graph_objects as go

        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add GDP trace
        fig.add_trace(
            go.Scatter(x=data['year'], y=data['gdpPercap'],
                      name="GDP per Capita", line=dict(color='blue')),
            secondary_y=False,
        )

        # Add Life Expectancy trace
        fig.add_trace(
            go.Scatter(x=data['year'], y=data['lifeExp'],
                      name="Life Expectancy", line=dict(color='red')),
            secondary_y=True,
        )

        if self.show_population:
            # Normalize population for display
            data['pop_normalized'] = data['pop'] / data['pop'].max() * data['lifeExp'].max()
            fig.add_trace(
                go.Scatter(x=data['year'], y=data['pop_normalized'],
                          name="Population (scaled)",
                          line=dict(color='green', dash='dash')),
                secondary_y=True,
            )

        # Set axis titles
        fig.update_xaxes(title_text="Year")
        fig.update_yaxes(title_text="GDP per Capita (USD)", secondary_y=False)
        fig.update_yaxes(title_text="Life Expectancy (years)", secondary_y=True)

        fig.update_layout(
            title=f"{self.continent} Economic & Health Trends",
            hovermode='x unified'
        )

        return fig


class CountryComparison(Component):
    """
    Compare multiple countries across metrics.

    Demonstrates: Multi-country comparison, bar charts
    """
    __id__ = "country_comparison"

    countries: list[str] = Field(default_factory=lambda: ["United States", "China", "India"])
    year: int = 2007
    metric: str = "gdpPercap"

    def load(self):
        """Load gapminder data."""
        return px.data.gapminder()

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Filter by year and countries."""
        filtered = data[
            (data['year'] == self.year) &
            (data['country'].isin(self.countries))
        ].copy()

        return filtered.sort_values(self.metric, ascending=False)

    def render(self, data: pd.DataFrame):
        """Create bar chart."""
        metric_labels = {
            'gdpPercap': 'GDP per Capita (USD)',
            'lifeExp': 'Life Expectancy (years)',
            'pop': 'Population'
        }

        fig = px.bar(
            data,
            x='country',
            y=self.metric,
            color='country',
            title=f"Country Comparison - {metric_labels.get(self.metric, self.metric)} ({self.year})",
            labels={self.metric: metric_labels.get(self.metric, self.metric)}
        )

        fig.update_layout(showlegend=False)
        return fig


class IrisClassification(Component):
    """
    Visualize Iris dataset with scatter plots.

    Demonstrates: Scatter plots, species classification
    """
    __id__ = "iris_classification"

    x_axis: str = "sepal_length"
    y_axis: str = "sepal_width"

    def load(self):
        """Load iris dataset."""
        return px.data.iris()

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """No transformation needed."""
        return data

    def render(self, data: pd.DataFrame):
        """Create scatter plot."""
        axis_labels = {
            'sepal_length': 'Sepal Length (cm)',
            'sepal_width': 'Sepal Width (cm)',
            'petal_length': 'Petal Length (cm)',
            'petal_width': 'Petal Width (cm)',
        }

        fig = px.scatter(
            data,
            x=self.x_axis,
            y=self.y_axis,
            color='species',
            size='petal_length',
            hover_data=['species'],
            title="Iris Flower Classification",
            labels={
                self.x_axis: axis_labels.get(self.x_axis, self.x_axis),
                self.y_axis: axis_labels.get(self.y_axis, self.y_axis),
            }
        )

        return fig


class TipsAnalysis(Component):
    """
    Restaurant tips analysis.

    Demonstrates: Box plots, categorical analysis
    """
    __id__ = "tips_analysis"

    groupby: str = "day"
    min_tip: float = 0.0

    def load(self):
        """Load tips dataset."""
        return px.data.tips()

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Filter by minimum tip."""
        return data[data['tip'] >= self.min_tip].copy()

    def render(self, data: pd.DataFrame):
        """Create box plot."""
        fig = px.box(
            data,
            x=self.groupby,
            y='tip',
            color=self.groupby,
            title=f"Tip Distribution by {self.groupby.title()}",
            labels={'tip': 'Tip Amount ($)', self.groupby: self.groupby.title()}
        )

        return fig


class StockPriceChart(Component):
    """
    Stock price trends over time.

    Demonstrates: Time series, multiple stocks
    """
    __id__ = "stock_prices"

    stocks: list[str] = Field(default_factory=lambda: ["GOOG", "AAPL"])

    def load(self):
        """Load stock data."""
        return px.data.stocks()

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Melt data for selected stocks."""
        # Melt from wide to long format
        selected_cols = ['date'] + [s for s in self.stocks if s in data.columns]
        melted = data[selected_cols].melt(
            id_vars=['date'],
            var_name='stock',
            value_name='price'
        )
        return melted

    def render(self, data: pd.DataFrame):
        """Create line chart."""
        fig = px.line(
            data,
            x='date',
            y='price',
            color='stock',
            title="Stock Price Trends",
            labels={'price': 'Price ($)', 'date': 'Date'}
        )

        fig.update_layout(hovermode='x unified')
        return fig


# ==============================================================================
# Build Dashboard Layout
# ==============================================================================

# Create dashboard
dashboard = Dashboard(id="plotly_datasets", title="Plotly Datasets Explorer")

# Page 1: Gapminder Analysis
with dashboard.page(id="gapminder", title="Gapminder Analysis", icon="🌍"):

    with L.section(title="Economic & Health Trends"):
        with L.row():
            # Inputs
            with L.column(weight=1):
                continent_input = L.input(Select(
                    name="continent",
                    label="Continent",
                    options=get_continents(),
                    default="Asia"
                ))

                show_pop_input = L.input(Toggle(
                    name="show_population",
                    label="Show Population",
                    default=False
                ))

            # Chart
            with L.column(weight=3):
                L.widget(
                    widget_type=WidgetType.CHART,
                    title="Trends Over Time",
                    component=GapminderTrends,
                    params={
                        "continent": continent_input,
                        "show_population": show_pop_input
                    }
                )

    with L.section(title="Country Comparison"):
        with L.row():
            # Inputs
            with L.column(weight=1):
                countries_input = L.input(MultiSelect(
                    name="countries",
                    label="Select Countries",
                    options=get_countries(),
                    default=["United States", "China", "India", "Brazil", "Germany"],
                    max_selections=10
                ))

                year_input = L.input(Slider(
                    name="year",
                    label="Year",
                    min_value=1952,
                    max_value=2007,
                    step=5,
                    default=2007,
                    show_value=True
                ))

                metric_input = L.input(Select(
                    name="metric",
                    label="Metric",
                    options=[
                        {"value": "gdpPercap", "label": "GDP per Capita"},
                        {"value": "lifeExp", "label": "Life Expectancy"},
                        {"value": "pop", "label": "Population"}
                    ],
                    default="gdpPercap"
                ))

            # Chart
            with L.column(weight=2):
                L.widget(
                    widget_type=WidgetType.CHART,
                    title="Country Metrics",
                    component=CountryComparison,
                    params={
                        "countries": countries_input,
                        "year": year_input,
                        "metric": metric_input
                    }
                )

# Page 2: Iris Classification
with dashboard.page(id="iris", title="Iris Dataset", icon="🌸"):

    with L.section(title="Flower Measurements"):
        with L.row():
            # Inputs
            with L.column(weight=1):
                x_axis_input = L.input(Select(
                    name="x_axis",
                    label="X-Axis",
                    options=[
                        {"value": "sepal_length", "label": "Sepal Length"},
                        {"value": "sepal_width", "label": "Sepal Width"},
                        {"value": "petal_length", "label": "Petal Length"},
                        {"value": "petal_width", "label": "Petal Width"},
                    ],
                    default="sepal_length"
                ))

                y_axis_input = L.input(Select(
                    name="y_axis",
                    label="Y-Axis",
                    options=[
                        {"value": "sepal_length", "label": "Sepal Length"},
                        {"value": "sepal_width", "label": "Sepal Width"},
                        {"value": "petal_length", "label": "Petal Length"},
                        {"value": "petal_width", "label": "Petal Width"},
                    ],
                    default="sepal_width"
                ))

            # Chart
            with L.column(weight=3):
                L.widget(
                    widget_type=WidgetType.CHART,
                    title="Species Classification",
                    component=IrisClassification,
                    params={
                        "x_axis": x_axis_input,
                        "y_axis": y_axis_input
                    }
                )

# Page 3: Restaurant Tips
with dashboard.page(id="tips", title="Restaurant Tips", icon="💵"):

    with L.section(title="Tip Analysis"):
        with L.row():
            # Inputs
            with L.column(weight=1):
                groupby_input = L.input(Select(
                    name="groupby",
                    label="Group By",
                    options=[
                        {"value": "day", "label": "Day of Week"},
                        {"value": "time", "label": "Time (Lunch/Dinner)"},
                        {"value": "sex", "label": "Gender"},
                        {"value": "smoker", "label": "Smoker"}
                    ],
                    default="day"
                ))

                min_tip_input = L.input(Slider(
                    name="min_tip",
                    label="Minimum Tip ($)",
                    min_value=0,
                    max_value=10,
                    step=0.5,
                    default=0,
                    show_value=True
                ))

            # Chart
            with L.column(weight=3):
                L.widget(
                    widget_type=WidgetType.CHART,
                    title="Tip Distribution",
                    component=TipsAnalysis,
                    params={
                        "groupby": groupby_input,
                        "min_tip": min_tip_input
                    }
                )

# Page 4: Stock Prices
with dashboard.page(id="stocks", title="Stock Prices", icon="📈"):

    with L.section(title="Stock Trends"):
        with L.row():
            # Inputs
            with L.column(weight=1):
                stocks_input = L.input(MultiSelect(
                    name="stocks",
                    label="Select Stocks",
                    options=[
                        {"value": "GOOG", "label": "Google"},
                        {"value": "AAPL", "label": "Apple"},
                        {"value": "AMZN", "label": "Amazon"},
                        {"value": "FB", "label": "Facebook"},
                        {"value": "NFLX", "label": "Netflix"},
                        {"value": "MSFT", "label": "Microsoft"}
                    ],
                    default=["GOOG", "AAPL"],
                    max_selections=6
                ))

            # Chart
            with L.column(weight=3):
                L.widget(
                    widget_type=WidgetType.CHART,
                    title="Price Trends",
                    component=StockPriceChart,
                    params={
                        "stocks": stocks_input
                    }
                )
