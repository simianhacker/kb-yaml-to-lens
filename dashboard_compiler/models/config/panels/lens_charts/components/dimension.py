from pydantic import BaseModel, Field

from dashboard_compiler.models.config.shared import Sort


class Dimension(BaseModel):
    """Represents a dimension object within a Lens chart in the YAML schema."""

    id: str = Field(default=None, description="(Optional) Unique identifier for the metric.")
    field: str = Field(..., description="(Required) Field name.")
    type: str = Field(..., description="(Required) Aggregation type (e.g., date_histogram, terms).")
    label: str | None = Field(None, description="(Optional) Display label for the dimension. Defaults to field name.")
    interval: str | None = Field(
        None, description="(Optional, for date_histogram or histogram) Time or number interval."
    )  # Updated description
    size: int | None = Field(None, description="(Optional, for terms) Number of terms to show.")
    sort: Sort | None = Field(None, description="(Optional, for terms) Sort configuration for the terms.")
    other_bucket: bool | None = Field(None, description="(Optional, for terms) Show 'Other' bucket.")  # Added other_bucket
    missing_bucket: bool | None = Field(None, description="(Optional, for terms) Show 'Missing' bucket.")  # Added missing_bucket
    include: list[str] | None = Field(None, description="(Optional, for terms) Include terms matching these values/regex.")  # Added include
    exclude: list[str] | None = Field(None, description="(Optional, for terms) Exclude terms matching these values/regex.")  # Added exclude
    include_is_regex: bool | None = Field(
        None, description="(Optional, for terms) Treat include values as regex."
    )  # Added include_is_regex
    exclude_is_regex: bool | None = Field(
        None, description="(Optional, for terms) Treat exclude values as regex."
    )  # Added exclude_is_regex
