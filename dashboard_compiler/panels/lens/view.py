"""Base view components for Lens panels."""

from typing import Any, Literal
from warnings import deprecated

from pydantic import BaseModel, Field, RootModel

from dashboard_compiler.filters.view import KbnFilter
from dashboard_compiler.panels.view import KbnBasePanel, KbnBasePanelEmbeddableConfig
from dashboard_compiler.shared.view import BaseVwModel, KbnReference

# Model relationships:
# - KbnLensPanel
#   - KbnLensPanelEmbeddableConfig
#     - KbnLensPanelAttributes
#       - KbnLensPanelState
#         - KbnBaseStateVisualization <--- The subclassed visualizations replace this
#           - KbnBaseStateVisualizationLayer <--- The subclassed visualizations replace this
#         - KbnDataSourceState
#           - KbnLayerDataSourceState
#             - KbnColumn


# Inheriting modules must inherit from:
#  - KbnBaseStateVisualization for visualization state
#  - KbnBaseStateVisualizationLayer for layer state


class KbnESQLColumnMetaSourceParams(BaseVwModel):
    indexPattern: str = Field(...)


class KbnESQLColumnMeta(BaseVwModel):
    type: Literal['number'] = Field(...)

    es_type: Literal['long'] = Field(...)

    sourceParams: KbnESQLColumnMetaSourceParams = Field(...)


class KbnESQLBaseColumn(BaseVwModel):
    columnId: str = Field(...)

    fieldName: str = Field(...)

    label: str | None = Field(None)


class KbnLensBaseColumn(BaseVwModel):
    """Base class for column definitions in the Kibana JSON structure."""

    label: str | None = None
    """The display label for the column. If not provided, a label is inferred from the field name."""

    dataType: str
    """The data type of the column, such as 'date', 'number', 'string', etc."""

    customLabel: bool | None = None
    """Whether the column has a custom label. Should be set to true if a custom label was provided."""

    operationType: str
    """The type of aggregation performed by the column, such as 'count', 'average', 'terms', etc."""

    isBucketed: bool
    """Whether the column is bucketed. Bucketed columns are used for grouping data, while non-bucketed columns are used for metrics."""

    scale: str
    """The scale of the column, such as 'ordinal', 'ratio', 'interval', etc."""

    params: dict[str, Any] = Field(default_factory=dict)
    """Additional parameters for the column."""


type KbnLensColumnTypes = KbnLensFieldSourcedColunn | KbnLensFormulaSourcedColumn


class KbnLensFieldSourcedColunn(KbnLensBaseColumn):
    """Represents a field-sourced Lens column in the Kibana JSON structure."""

    sourceField: str
    """The field that this column is based on."""


class KbnLensFormulaSourcedColumn(KbnLensBaseColumn):
    """Represents a formula-sourced Lens column in the Kibana JSON structure."""

    formula: str
    """The Lens formula used to calculate the value of this column."""


@deprecated('KbnColumn is deprecated, use KbnLens*Column instead.')
class KbnColumn(BaseModel):
    """Represents a column definition within KbnDataSourceStates.formBased.layers.<layerId>.columns in the Kibana JSON structure."""

    label: str | None = None
    dataType: str
    customLabel: bool | None = None
    operationType: str
    sourceField: str
    isBucketed: bool
    scale: str
    params: dict[str, Any] = Field(default_factory=dict)


class KbnLayerDataSourceState(BaseModel):
    """Represents the datasource state for a single layer within a Lens panel in the Kibana JSON structure."""

    columns: dict[str, KbnColumn] = Field(default_factory=dict)
    columnOrder: list[str] = Field(default_factory=list)
    incompleteColumns: dict[str, Any] = Field(default_factory=dict)
    sampling: int
    indexPatternId: str | None = None


class KbnLayerDataSourceStateById(RootModel):
    """Represents a mapping of layer IDs to their corresponding KbnLayerDataSourceState objects."""

    root: dict[str, KbnLayerDataSourceState] = Field(default_factory=dict)


class KbnFormBasedDataSourceState(BaseModel):
    layers: KbnLayerDataSourceStateById = Field(default_factory=KbnLayerDataSourceStateById)
    currentIndexPatternId: str | None = None


class KbnTextBasedDataSourceState(BaseModel):
    layers: KbnLayerDataSourceStateById = Field(default_factory=KbnLayerDataSourceStateById)


class KbnIndexPatternDataSourceState(BaseModel):
    layers: KbnLayerDataSourceStateById = Field(default_factory=KbnLayerDataSourceStateById)


class KbnDataSourceState(BaseModel):
    """Represents the overall datasource states for a Lens panel in the Kibana JSON structure."""

    formBased: KbnFormBasedDataSourceState = Field(
        default_factory=KbnFormBasedDataSourceState,
    )  # Structure: formBased -> layers -> {layerId: KbnLayerDataSourceState}
    indexpattern: KbnIndexPatternDataSourceState = Field(
        default_factory=KbnIndexPatternDataSourceState,
    )  # Structure: indexpattern -> layers -> {layerId: KbnLayerDataSourceState}
    textBased: KbnTextBasedDataSourceState = Field(
        default_factory=KbnTextBasedDataSourceState,
    )  # Structure: textBased -> layers -> {layerId: KbnLayerDataSourceState}


class KbnLayerColorMappingRule(BaseModel):
    type: str = 'other'


class KbnLayerColorMappingColor(BaseModel):
    type: str = 'loop'


class KbnLayerColorMappingSpecialAssignment(BaseModel):
    rule: KbnLayerColorMappingRule = Field(default_factory=KbnLayerColorMappingRule)
    color: KbnLayerColorMappingColor = Field(default_factory=KbnLayerColorMappingColor)
    touched: bool = False


class KbnLayerColorMapping(BaseModel):
    assignments: list[Any] = Field(default_factory=list)
    specialAssignments: list[KbnLayerColorMappingSpecialAssignment] = Field(
        default_factory=lambda: [KbnLayerColorMappingSpecialAssignment()],
    )
    paletteId: str = 'default'
    colorMode: dict[str, str] = Field(default_factory=lambda: {'type': 'categorical'})


class KbnBaseStateVisualizationLayer(BaseModel):
    layerId: str
    layerType: str
    colorMapping: KbnLayerColorMapping | None = None


class KbnBaseStateVisualization(BaseModel):
    layers: list[KbnBaseStateVisualizationLayer] | None = Field(default=None)


class KbnLensPanelState(BaseModel):
    """Represents the 'state' object within a Lens panel in the Kibana JSON structure."""

    visualization: KbnBaseStateVisualization
    query: dict[str, str] = Field(default_factory=lambda: {'query': '', 'language': 'kuery'})
    filters: list[KbnFilter] = Field(default_factory=list)
    datasourceStates: KbnDataSourceState = Field(default_factory=KbnDataSourceState)
    internalReferences: list[Any] = Field(default_factory=list)
    adHocDataViews: dict[str, Any] = Field(default_factory=dict)


class KbnLensPanelAttributes(BaseModel):
    title: str = ''
    visualizationType: Literal['lnsXY', 'lnsPie', 'lnsMetric', 'lnsDatatable']
    type: Literal['lens'] = 'lens'
    references: list[KbnReference] = Field(default_factory=list)
    state: KbnLensPanelState


class KbnLensPanelEmbeddableConfig(KbnBasePanelEmbeddableConfig):
    attributes: KbnLensPanelAttributes
    # syncColors: bool = Field(
    #     default=False,
    #     description="(Optional) Whether to sync colors across visualizations. Defaults to False.",
    # )
    # syncCursor: bool = Field(
    #     default=True,
    #     description="(Optional) Whether to sync cursor across visualizations. Defaults to True.",
    # )
    # syncTooltips: bool = Field(
    #     default=False,
    #     description="(Optional) Whether to sync tooltips across visualizations. Defaults to False.",
    # )
    # filters: list = Field(
    #     default_factory=list,
    #     description="(Optional) List of filters applied to the Lens visualization. Defaults to empty list.",
    # )
    # query: dict[str, Any] = Field(
    #     default_factory=lambda: {"query": "", "language": "kuery"},
    #     description="(Optional) Query object for the Lens visualization. Defaults to empty query with 'kuery' language.",
    # )


class KbnLensPanel(KbnBasePanel):
    type: Literal['lens'] = 'lens'
    embeddableConfig: KbnLensPanelEmbeddableConfig
