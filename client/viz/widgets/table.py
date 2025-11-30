"""
Table widget for displaying tabular data.

Frontend-native rendering with sorting, pagination, and column configuration.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from .base import Widget


class TableWidget(Widget):
    """
    Frontend-native data table.

    Displays data in a tabular format with optional sorting, pagination,
    and column configuration.

    Example:
        TableWidget(
            title="Transaction History",
            data_source=TimeseriesSource(name="finance.transactions"),
            params={"account": account_input},
            columns=["date", "description", "amount", "balance"],
            page_size=20,
            sortable=True
        )
    """

    type: Literal["table"] = "table"

    columns: list[str] | None = Field(
        None,
        description="Columns to display (None = auto from data)"
    )

    # Pagination
    page_size: int = Field(10, description="Rows per page", ge=1)
    paginated: bool = Field(True, description="Enable pagination")

    # Interactivity
    sortable: bool = Field(True, description="Allow column sorting")
    filterable: bool = Field(False, description="Allow column filtering")

    # Styling
    striped: bool = Field(True, description="Alternate row colors")
    compact: bool = Field(False, description="Reduce row height")
