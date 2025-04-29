from typing import Literal

from pydantic import Field

from dashboard_compiler.models.config.panels.lens_charts.base import BaseLensChart
from dashboard_compiler.models.config.panels.lens_charts.components.metric import Metric


class LensMetricsChart(BaseLensChart):
    """
    Represents a Metric chart configuration within a Lens panel in the YAML schema.

    Metric charts display a single value or a list of values, often representing
    key performance indicators.
    """

    type: Literal["metric"] = "metric"
    metrics: list[Metric] = Field(
        ..., description="A list of metric configurations to be displayed in the chart."
    )
