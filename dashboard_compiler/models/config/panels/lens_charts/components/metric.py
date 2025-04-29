from pydantic import BaseModel, Field


class Metric(BaseModel):
    """
    Represents a metric configuration within a Lens chart in the YAML schema.

    Metrics are typically used for calculating and displaying quantitative values
    in visualizations.
    """

    id: str | None = Field(
        default=None,
        description="A unique identifier for the metric. If not provided, one may be generated during compilation."
    )
    type: str = Field(
        ..., description="The aggregation type for the metric (e.g., 'count', 'max', 'average', 'unique_count', 'formula', 'last_value')."
    )
    label: str | None = Field(
        None, description="The display label for the metric. If not provided, a label may be inferred from the type and field."
    )
    field: str | None = Field(
        None,
        description="The name of the field in the data view that this metric is based on. Required for most metric types except 'count'. Use '___records___' for a count of documents."
    )
    formula: str | None = Field(
        None, description="For 'formula' type metrics, the formula string to be evaluated."
    )
    sort_field: str | None = Field(
        None, description="For 'last_value' aggregation, the field used to determine the 'last' value."
    )
    filter: str | None = Field(
        None, description="For 'last_value' aggregation, a KQL filter applied before determining the last value."
    )
