from typing import Literal

from pydantic import BaseModel, Field

from dashboard_compiler.models.config.panels.lens_charts.base import BaseLensChart
from dashboard_compiler.models.config.panels.lens_charts.components.dimension import Dimension
from dashboard_compiler.models.config.panels.lens_charts.components.metric import Metric


class PaginationConfig(BaseModel):
    """
    Represents pagination configuration for a Datatable chart.
    """

    page_size: int = Field(
        ..., description="The number of rows to display per page in the datatable."
    )


class TableSortConfig(BaseModel):
    """
    Represents sorting configuration for a column in a Datatable chart.
    """

    column_label: str = Field(
        ..., description="The display label of the column to sort the datatable by."
    )
    direction: Literal["asc", "desc"] = Field(
        ..., description="The sort direction. Must be either 'asc' for ascending or 'desc' for descending."
    )


class LensDatatableChart(BaseLensChart):
    """
    Represents a Datatable chart configuration within a Lens panel in the YAML schema.

    Datatable charts display data in a tabular format.
    """

    type: Literal["datatable"] = "datatable"
    rows: list[Dimension] = Field(
        default_factory=list,
        description="A list of dimension configurations for the rows of the datatable. Defaults to an empty list."
    )
    metrics: list[Metric] = Field(
        default_factory=list,
        description="A list of metric configurations for the columns of the datatable. Defaults to an empty list."
    )
    split_by: list[Dimension] = Field(
        default_factory=list,
        description="A list of dimension configurations to split the data by, creating separate tables or sections. Defaults to an empty list."
    )
    show_row_numbers: bool | None = Field(
        None, description="If `true`, display row numbers in the datatable. Defaults to `false`."
    )
    show_toolbar: bool | None = Field(
        None, description="If `true`, display the toolbar with options like filtering and column selection. Defaults to `false`."
    )
    show_total: bool | None = Field(
        None, description="If `true`, display a row showing the total for metric columns. Defaults to `false`."
    )
    pagination: PaginationConfig | None = Field(
        None, description="Pagination configuration for the datatable."
    )
    sort: TableSortConfig | None = Field(
        None, description="Default sort configuration to apply when the datatable is initially displayed."
    )
