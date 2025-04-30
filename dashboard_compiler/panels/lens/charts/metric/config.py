from typing import Literal

from pydantic import Field

from dashboard_compiler.panels.lens.charts.config import BaseLensChart
from dashboard_compiler.panels.lens.metrics.config import ESQLMetric, LensMetric


class BaseLensMetricsChart(BaseLensChart):
    """Base model for defining a Metric chart object within a Lens panel in the YAML schema."""


class LensMetricsChart(BaseLensChart):
    """Represents a Metric chart configuration within a Lens panel in the YAML schema.

    Metric charts display a single value or a list of values, often representing
    key performance indicators.
    """

    primary: LensMetric = Field(
        ...,
        description='The primary metric to display in the chart. This is the main value shown in the metric visualization.',
        alias='metric',
    )
    secondary: LensMetric | None = Field(default=None, description='An optional secondary metric to display alongside the primary metric.')
    maximum: LensMetric | None = Field(None, description='An optional maximum metric to display, often used for comparison or thresholds.')


class ESQLMetricsChart(BaseLensMetricsChart):
    """Represents an ES|QL based Metric chart configuration within a Lens panel in the YAML schema."""

    type: Literal['metric'] = 'metric'
    primary: ESQLMetric = Field(
        ...,
        description='The primary metric to display in the chart. This is the main value shown in the metric visualization.',
    )

    second: ESQLMetric | None = Field(default=None, description='An optional secondary metric to display alongside the primary metric.')

    maximum: ESQLMetric | None = Field(
        default=None,
        description='An optional maximum metric to display, often used for comparison or thresholds.',
    )
