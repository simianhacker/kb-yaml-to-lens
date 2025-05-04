from pydantic import Field

from dashboard_compiler.shared.model import BaseModel


class BaseChart(BaseModel):
    """Base model for defining chart objects."""

    id: str | None = Field(
        default=None,
        description='A unique identifier for the chart. If not provided, one may be generated during compilation.',
    )
