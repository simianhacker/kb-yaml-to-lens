from typing import Literal

from pydantic import BaseModel, Field


class Column(BaseModel):
    """
    Represents a column configuration within a Lens Datatable chart in the YAML schema.
    """

    id: str | None = Field(
        default=None,
        description="A unique identifier for the column. If not provided, one may be generated during compilation."
    )
    field: str | None = Field(
        None,
        description="The name of the field in the data view that this column is based on. Required for dimension and metric columns. Use '___records___' for a count of documents."
    )
    type: str = Field(
        ..., description="The aggregation type for the column (e.g., 'terms', 'count', 'last_value', 'max', 'average')."
    )
    label: str | None = Field(
        None, description="The display label for the column header. If not provided, a label may be inferred from the field and type."
    )
    size: int | None = Field(
        None, description="For 'terms' aggregation, the number of top terms to display."
    )
    order_by_metric: str | None = Field(
        None, description="For 'terms' aggregation, the label of a metric column to use for sorting the terms."
    )
    order_direction: Literal["asc", "desc"] = Field(
        "desc", description="For 'terms' aggregation, the sort direction ('asc' or 'desc'). Defaults to 'desc'."
    )
    sort_field: str | None = Field(
        None, description="For 'last_value' aggregation, the field used to determine the 'last' value."
    )
    filter: str | None = Field(
        None, description="For 'last_value' aggregation, a KQL filter applied before determining the last value."
    )
