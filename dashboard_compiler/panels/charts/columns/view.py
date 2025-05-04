from typing import Annotated, Any, Literal

from pydantic import Field

from dashboard_compiler.queries.view import KbnQuery
from dashboard_compiler.shared.view import BaseVwModel, OmitIfNone

type KbnLensColumnTypes = KbnLensMetricColumnTypes | KbnLensDimensionColumnTypes

type KbnLensDimensionColumnTypes = None

type KbnLensMetricColumnTypes = KbnLensFieldMetricColumn

type KbnLensMetricFormatTypes = KbnLensMetricFormat

class KbnLensMetricFormatParams(BaseVwModel):
    """The parameters of the format."""

    decimals: int
    """The number of decimal places to display."""

    suffix: Annotated[str | None, OmitIfNone()] = Field(default=None)
    """The suffix to display after the number."""

    compact: Annotated[bool | None, OmitIfNone()] = Field(default=None)
    """Whether to display the number in a compact format."""

    pattern: Annotated[str | None, OmitIfNone()] = Field(default=None)
    """The pattern to display the number in."""

class KbnLensMetricFormat(BaseVwModel):
    """The format of the column."""

    id: Literal['number','bytes','bits','percent', 'duration', 'custom']

    params: KbnLensMetricFormatParams
    """The parameters of the format."""

class KbnLensMetricColumnParams(BaseVwModel):
    """Additional parameters for the column."""

    format: Annotated[KbnLensMetricFormat | None, OmitIfNone()] = Field(default=None)
    """The format of the column."""

    emptyAsNull: Annotated[bool | None, OmitIfNone()] = Field(default=None)

    sortField: Annotated[str | None, OmitIfNone()] = Field(default=None)

    value: Annotated[int | None, OmitIfNone()] = Field(default=None)

    percentile: Annotated[int | None, OmitIfNone()] = Field(default=None)

class KbnLensBaseMetricColumn(BaseVwModel):
    """Base class for column definitions in the Kibana JSON structure."""

    label: str
    """The display label for the column."""

    dataType: str
    """The data type of the column, such as 'date', 'number', 'string', etc."""

    customLabel: Annotated[bool | None, OmitIfNone()]
    """Whether the column has a custom label. Should be set to true if a custom label was provided."""

    operationType: str
    """The type of aggregation performed by the column, such as 'count', 'average', 'terms', etc."""

    isBucketed: bool = Field(default=False)
    """Whether the column is bucketed. Bucketed columns are used for grouping data, while non-bucketed columns are used for metrics."""

    filter: Annotated[KbnQuery | None, OmitIfNone()] = Field(default=None)

    scale: str
    """The scale of the column, such as 'ordinal', 'ratio', 'interval', etc."""

    params: KbnLensMetricColumnParams
    """Additional parameters for the column."""


class KbnLensFieldMetricColumn(KbnLensBaseMetricColumn):
    """Represents a field-sourced Lens column in the Kibana JSON structure."""

    sourceField: str
    """The field that this column is based on."""

class KbnESQLFieldMetricColumn(BaseVwModel):
    """Represents a field-sourced ESQL column in the Kibana JSON structure."""

    fieldName: str
    """The field that this column is based on."""

    columnId: str
    """The ID of the column."""
