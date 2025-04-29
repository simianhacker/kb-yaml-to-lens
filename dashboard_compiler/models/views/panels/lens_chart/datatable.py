from typing import Literal

from pydantic import BaseModel, Field, field_serializer

from dashboard_compiler.models.views.panels.lens import KbnBaseStateVisualization


class KbnDatatableColumn(BaseModel):
    """Represents a column in the KbnLensDatatableVisualizationState."""

    columnId: str
    isTransposed: bool
    isMetric: bool
    width: float | None = None


class KbnDatatableSort(BaseModel):
    """Represents the sort state in the KbnLensDatatableVisualizationState."""

    columnId: str
    direction: Literal["asc", "desc"]


class KbnDatatablePagination(BaseModel):
    """Represents the pagination state in the KbnLensDatatableVisualizationState."""

    page: int
    pageSize: int


class KbnDatatableVisualizationState(KbnBaseStateVisualization):
    """Represents the 'visualization' object for a Datatable in the Kibana JSON structure."""

    layerId: str
    layerType: Literal["data"] = "data"
    columns: list[KbnDatatableColumn] = Field(default_factory=list)
    sort: KbnDatatableSort | None = None
    pagination: KbnDatatablePagination | None = None
    # Add other fields as needed based on Kibana JSON structure

    @field_serializer("layers", when_used="always")
    def serialize_layers(self, layers):
        """dont serialize layers."""
        return None
