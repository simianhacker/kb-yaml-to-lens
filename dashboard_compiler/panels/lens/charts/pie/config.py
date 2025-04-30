from typing import Literal

from pydantic import BaseModel, Field

from dashboard_compiler.panels.lens.charts.config import (
    BaseLensChart,
    LensLegendMixin,
)  # Added BaseLensPieChart
from dashboard_compiler.panels.lens.dimension.config import Dimension
from dashboard_compiler.panels.lens.metrics.config import Metric


class LensPieChartAppearance(BaseModel):
    """Represents chart appearance formatting options for Lens charts in the YAML schema."""

    donut: Literal['small', 'medium', 'large'] | None = Field(
        None,
        description="The size of the donut hole in the pie chart. Options are 'small', 'medium', or 'large'.",
    )


class BaseLensPieChart(BaseLensChart, LensLegendMixin):
    """Base model for defining Pie chart objects within a Lens panel in the YAML schema."""

    appearance: LensPieChartAppearance | None = Field(
        None,
        description='Formatting options for the chart appearance, including donut size.',
    )


class LensPieChart(BaseLensChart):
    """Represents a Pie chart configuration within a Lens panel in the YAML schema.

    Pie charts are used to visualize the proportion of categories.
    """

    metric: Metric = Field(..., description='A metric that determins the size of the slice of the pie chart.')
    dimensions: list[Dimension] = Field(
        ...,
        description="Defines the 'Slice by' dimension for the pie chart. Typically, this is a single 'terms' aggregation.",
        max_length=1,
    )
    metrics: list[Metric] = Field(
        ...,
        description="Defines the 'Size by' metric for the pie chart. Typically, this is a single metric.",
        max_length=1,
    )


class ESQLPieChart(BaseLensPieChart):
    """Represents an ES|QL based Pie chart configuration within a Lens panel in the YAML schema."""

    type: Literal['pie'] = 'pie'
    slice_by_column: str = Field(..., description="The field name from the ESQL query result to use for the 'Slice by' dimension.")
    size_by_column: str = Field(..., description="The field name from the ESQL query result to use for the 'Size by' metric.")
