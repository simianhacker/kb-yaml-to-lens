"""Configuration for a Lens and ESQL Metric."""

from typing import Literal

from pydantic import Field

from dashboard_compiler.shared.config import BaseCfgModel


class BaseMetric(BaseCfgModel):
    """Base class for metric configurations in Lens charts."""

    id: str | None = Field(default=None)
    """A unique identifier for the metric. If not provided, one may be generated during compilation."""

    label: str | None = Field(None)
    """The display label for the metric. If not provided, a label may be inferred from the type and field."""


class BaseMetricFormat(BaseCfgModel):
    """Base class for metric format configurations in Lens charts."""


type ESQLMetricTypes = ESQLMetric


class ESQLMetric(BaseMetric):
    """Represents a metric configuration for an ES|QL based Lens chart in the YAML schema.

    Metrics are typically used for calculating and displaying quantitative values
    in visualizations.
    """


type LensMetricTypes = LensFormulaMetric | LensAggregatedMetricTypes


class LensFormulaMetric(BaseMetric):
    """Represents a formula metric configuration within a Lens chart in the YAML schema.

    Formula metrics allow for custom calculations based on other fields or metrics.
    """

    type: Literal['formula'] = 'formula'

    formula: str = Field(...)
    """The formula string to be evaluated for this metric."""


type LensAggregatedMetricTypes = LensOtherAggregatedMetric | LensLastValueAggregatedMetric | LensCountAggregatedMetric


class LensCountAggregatedMetric(BaseMetric):
    """Represents a count metric configuration within a Lens chart.

    Count metrics are used to count the number of documents in a data view.
    """

    type: Literal['count'] = 'count'
    """The aggregation type for the metric, which is 'count' for this class."""

    field: Literal['___records___'] = Field(default='___records___')
    """The field used for counting documents. This is a special value indicating a count of all records."""


class LensOtherAggregatedMetric(BaseMetric):
    """Represents various aggregated metric configurations within a Lens chart."""

    type: Literal['count', 'max', 'average', 'unique_count', 'last_value'] = Field(...)
    """The aggregation type for the metric (e.g., 'count', 'max', 'average', 'unique_count')."""

    field: str = Field(...)


class LensLastValueAggregatedMetric(BaseMetric):
    """Represents a last value metric configuration within a Lens chart.

    Last value metrics are used to retrieve the most recent value of a field based on a specified sort order.
    """

    type: Literal['last_value'] = 'last_value'

    field: str = Field(...)

    sort_field: str | None = Field(default=None)
    """The field used to determine the 'last' value."""

    filter: str | None = Field(default=None)
    """A KQL filter applied before determining the last value."""
