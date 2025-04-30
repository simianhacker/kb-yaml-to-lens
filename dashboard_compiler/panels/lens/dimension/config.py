from typing import Literal

from pydantic import BaseModel, Field

from dashboard_compiler.shared.config import Sort


class BaseDimension(BaseModel):
    id: str | None = Field(
        default=None,
        description='A unique identifier for the dimension. If not provided, one may be generated during compilation.',
    )
    field: str = Field(..., description='The name of the field in the data view that this dimension is based on.')
    label: str | None = Field(
        None,
        description='The display label for the dimension. If not provided, a label may be inferred from the field and type.',
    )


class ESQLDimension(BaseDimension):
    """The configuration of a dimension within an ES|QL Lens chart."""


class NonESQLDimension(BaseDimension):
    """The configuration of a dimension within a non-ES|QL Lens chart."""


class TermsDimension(NonESQLDimension):
    """Represents a terms dimension configuration within a Lens chart in the YAML schema.

    Terms dimensions are used for aggregating data based on unique values of a field.
    """

    type: Literal['terms'] = 'terms'
    size: int | None = Field(default=None, description="For 'terms' aggregation, the number of top terms to display.")
    sort: Sort | None = Field(default=None, description="For 'terms' aggregation, the sort configuration for the terms.")
    other_bucket: bool | None = Field(
        None,
        description="For 'terms' aggregation, if `true`, show a bucket for terms not included in the top size. Defaults to `false`.",
    )
    missing_bucket: bool | None = Field(
        None,
        description="For 'terms' aggregation, if `true`, show a bucket for documents with a missing value for the field. Defaults to `false`.",
    )
    include: list[str] | None = Field(
        None,
        description="For 'terms' aggregation, a list of terms to include. Can be used with or without `include_is_regex`.",
    )
    exclude: list[str] | None = Field(
        None,
        description="For 'terms' aggregation, a list of terms to exclude. Can be used with or without `exclude_is_regex`.",
    )
    include_is_regex: bool | None = Field(
        None,
        description="For 'terms' aggregation, if `true`, treat the values in the `include` list as regular expressions. Defaults to `false`.",
    )
    exclude_is_regex: bool | None = Field(
        None,
        description="For 'terms' aggregation, if `true`, treat the values in the `exclude` list as regular expressions. Defaults to `false`.",
    )


class HistogramDimension(NonESQLDimension):
    """Represents a histogram dimension configuration within a Lens chart in the YAML schema.

    Histogram dimensions are used for aggregating data into buckets based on numeric ranges.
    """

    type: Literal['histogram'] = 'histogram'
    interval: str = Field(..., description='The numeric interval for the histogram buckets.')


class Dimension(BaseDimension):
    """Represents a dimension configuration within a Lens chart in the YAML schema.

    Dimensions are typically used for grouping or splitting data in visualizations.
    """

    type: str = Field(..., description="The aggregation type for the dimension (e.g., 'date_histogram', 'terms', 'histogram').")
    interval: str | None = Field(default=None, description="For 'date_histogram' or 'histogram' aggregations, the time or number interval.")
    size: int | None = Field(default=None, description="For 'terms' aggregation, the number of top terms to display.")
    sort: Sort | None = Field(default=None, description="For 'terms' aggregation, the sort configuration for the terms.")
    other_bucket: bool | None = Field(
        None,
        description="For 'terms' aggregation, if `true`, show a bucket for terms not included in the top size. Defaults to `false`.",
    )
    missing_bucket: bool | None = Field(
        None,
        description="For 'terms' aggregation, if `true`, show a bucket for documents with a missing value for the field. Defaults to `false`.",
    )
    include: list[str] | None = Field(
        None,
        description="For 'terms' aggregation, a list of terms to include. Can be used with or without `include_is_regex`.",
    )
    exclude: list[str] | None = Field(
        None,
        description="For 'terms' aggregation, a list of terms to exclude. Can be used with or without `exclude_is_regex`.",
    )
    include_is_regex: bool | None = Field(
        None,
        description="For 'terms' aggregation, if `true`, treat the values in the `include` list as regular expressions. Defaults to `false`.",
    )
    exclude_is_regex: bool | None = Field(
        None,
        description="For 'terms' aggregation, if `true`, treat the values in the `exclude` list as regular expressions. Defaults to `false`.",
    )
