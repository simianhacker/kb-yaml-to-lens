from typing import Literal

from pydantic import BaseModel, Field

from dashboard_compiler.panels.lens.charts.config import BaseLensChart
from dashboard_compiler.panels.lens.dimension.config import Dimension, ESQLDimension
from dashboard_compiler.panels.lens.metrics.config import ESQLMetric, Metric


class BaseLensDatatableChart(BaseLensChart):
    """Base model for defining Datatable chart objects within a Lens panel in the YAML schema."""

    # Datatable charts don't have axes, legends, or appearance options in the same way
    """
    Base model for common axis formatting options in the YAML schema.

    Specific axis formats (e.g., bottom, left, right) inherit from this base class.
    """

    title: str | None = Field(
        None,
        description='The title for the axis. If not provided, the title is auto-generated. Set to `null` to hide the title.',
    )
    scale: Literal['linear', 'log', 'square', 'sqrt'] | None = Field(default=None, description='The scale type for the axis.')
    gridlines: bool | None = Field(default=None, description='If `true`, show gridlines for this axis. Defaults to `false`.')
    tick_labels: bool | None = Field(default=None, description='If `true`, show tick labels for this axis. Defaults to `true`.')
    orientation: Literal['horizontal', 'vertical', 'rotated'] | None = Field(
        default=None,
        description='The orientation of the axis labels.',
    )
    min: float | Literal['auto'] | None = Field(
        default=None,
        description="The minimum value for the axis. Use 'auto' for automatic scaling.",
    )
    max: float | Literal['auto'] | None = Field(
        default=None,
        description="The maximum value for the axis. Use 'auto' for automatic scaling.",
    )


class LensDatatablePaginationConfig(BaseModel):
    """Represents pagination configuration for a Datatable chart."""

    page_size: int = Field(..., description='The number of rows to display per page in the datatable.')


class LensDatatableSortConfig(BaseModel):
    """Represents sorting configuration for a column in a Datatable chart."""

    column_label: str = Field(..., description='The display label of the column to sort the datatable by.')
    direction: Literal['asc', 'desc'] = Field(
        ...,
        description="The sort direction. Must be either 'asc' for ascending or 'desc' for descending.",
    )


class LensDatatableChart(BaseLensChart):
    """Represents a Datatable chart configuration within a Lens panel in the YAML schema.

    Datatable charts display data in a tabular format.
    """

    rows: list[Dimension] = Field(
        default_factory=list,
        description='A list of dimension configurations for the rows of the datatable. Defaults to an empty list.',
    )
    metrics: list[Metric] = Field(
        default_factory=list,
        description='A list of metric configurations for the columns of the datatable. Defaults to an empty list.',
    )
    split_by: list[Dimension] = Field(
        default_factory=list,
        description='A list of dimension configurations to split the data by, creating separate tables or sections. Defaults to an empty list.',
    )


class ESQLDatatableChart(BaseLensDatatableChart):
    """Represents an ES|QL based Datatable chart configuration within a Lens panel in the YAML schema."""

    rows: list[ESQLDimension] = Field(
        default_factory=list,
        description='A list of dimension configurations for the rows of the datatable. Defaults to an empty list.',
    )
    metrics: list[ESQLMetric] = Field(
        default_factory=list,
        description='A list of metric configurations for the columns of the datatable. Defaults to an empty list.',
    )
    split_by: list[ESQLDimension] = Field(
        default_factory=list,
        description='A list of dimension configurations to split the data by, creating separate tables or sections. Defaults to an empty list.',
    )
