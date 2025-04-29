from typing import Literal

from pydantic import Field

from dashboard_compiler.models.config.panels.lens_charts.base import BaseLensChart
from dashboard_compiler.models.config.panels.lens_charts.components.dimension import Dimension
from dashboard_compiler.models.config.panels.lens_charts.components.metric import Metric


class LensPieChart(BaseLensChart):
    """
    Represents a Pie chart configuration within a Lens panel in the YAML schema.

    Pie charts are used to visualize the proportion of categories.
    """

    type: Literal["pie"] = "pie"
    dimensions: list[Dimension] = Field(
        ...,
        description="Defines the 'Slice by' dimension for the pie chart. Typically, this is a single 'terms' aggregation.",
        max_length=1
    )
    metrics: list[Metric] = Field(
        ...,
        description="Defines the 'Size by' metric for the pie chart. Typically, this is a single metric.",
        max_length=1
    )
