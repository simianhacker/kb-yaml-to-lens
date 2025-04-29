from typing import Literal

from pydantic import BaseModel, Field

from dashboard_compiler.models.config.panels.lens_charts.base import BaseLensChart
from dashboard_compiler.models.config.panels.lens_charts.components.dimension import Dimension
from dashboard_compiler.models.config.panels.lens_charts.components.metric import Metric


class PaginationConfig(BaseModel):
    """Represents pagination configuration for a datatable."""

    page_size: int = Field(..., description="(Required) Number of rows per page.")


class TableSortConfig(BaseModel):
    """Represents sorting configuration for a datatable column."""

    column_label: str = Field(..., description="(Required) The label of the column to sort by.")
    direction: Literal["asc", "desc"] = Field(..., description="(Required) Sort direction.")


class LensDatatableChart(BaseLensChart):
    """Represents a Datatable chart within a Lens panel in the YAML schema."""

    type: Literal["datatable"] = "datatable"
    rows: list[Dimension] = Field(default_factory=list, description="(Optional) List of row dimensions.")
    metrics: list[Metric] = Field(default_factory=list, description="(Optional) List of metric columns.")
    split_by: list[Dimension] = Field(default_factory=list, description="(Optional) List of split-by dimensions.")
    show_row_numbers: bool | None = Field(None, description="(Optional) Show row numbers. Defaults to None.")
    show_toolbar: bool | None = Field(None, description="(Optional) Show toolbar. Defaults to None.")
    show_total: bool | None = Field(None, description="(Optional) Show total row. Defaults to None.")
    pagination: PaginationConfig | None = Field(None, description="(Optional) Pagination configuration.")
    sort: TableSortConfig | None = Field(None, description="(Optional) Default sort configuration.")
