"""Compile Lens panels into their Kibana view model representation."""
import re

from dashboard_compiler.panels import ESQLPanel, LensPanel
from dashboard_compiler.panels.lens.charts.config import BaseLensChart
from dashboard_compiler.panels.lens.charts.datatable.compile import (
    compile_esql_lens_datatable_chart,
    compile_lens_datatable_chart,
)
from dashboard_compiler.panels.lens.charts.datatable.config import ESQLDatatableChart, LensDatatableChart
from dashboard_compiler.panels.lens.charts.metric.compile import (
    compile_esql_lens_metrics_chart,
    compile_lens_metrics_chart,
)
from dashboard_compiler.panels.lens.charts.metric.config import ESQLMetricsChart, LensMetricsChart
from dashboard_compiler.panels.lens.charts.pie.compile import (
    compile_esql_lens_pie_chart,
    compile_lens_pie_chart,
)
from dashboard_compiler.panels.lens.charts.pie.config import ESQLPieChart, LensPieChart
from dashboard_compiler.panels.lens.charts.xy.compile import (
    compile_esql_lens_xy_chart,
    compile_lens_xy_chart,
)
from dashboard_compiler.panels.lens.charts.xy.config import ESQLXYChart, LensXYChart
from dashboard_compiler.panels.lens.components.compile import compile_dimensions, compile_metrics
from dashboard_compiler.panels.lens.metrics.compile import compile_lens_metrics
from dashboard_compiler.panels.lens.view import (
    KbnBaseStateVisualization,
    KbnColumn,
    KbnDataSourceState,
    KbnFormBasedDataSourceState,
    KbnLayerDataSourceState,
    KbnLayerDataSourceStateById,
    KbnLensPanel,
    KbnLensPanelAttributes,
    KbnLensPanelEmbeddableConfig,
    KbnLensPanelState,
    KbnTextBasedDataSourceState,
)
from dashboard_compiler.panels.shared.compile import compile_panel_shared
from dashboard_compiler.shared.view import KbnReference


def chart_type_to_kbn_type(chart: BaseLensChart) -> str:
    """Convert a BaseLensChart type to its corresponding Kibana visualization type.

    Args:
        chart (BaseLensChart): The chart object to convert.

    Returns:
        str: The Kibana visualization type.

    """
    if isinstance(chart, LensPieChart | ESQLPieChart):
        return 'lnsPie'
    if isinstance(chart, LensXYChart | ESQLXYChart):
        return 'lnsXY'
    if isinstance(chart, LensMetricsChart | ESQLMetricsChart):
        return 'lnsMetric'
    if isinstance(chart, LensDatatableChart | ESQLDatatableChart):
        return 'lnsDatatable'

    msg = f'Unsupported chart type: {type(chart)}'
    raise NotImplementedError(msg)


def compile_lens_panel(panel: LensPanel) -> tuple[list[KbnReference], KbnLensPanel]:
    """"Compile a Lens-based panel into its Kibana view model representation.

    Args:
        panel (LensPanel): The LensPanel object to compile.

    Returns:
        tuple[list[KbnReference], KbnLensPanel]: A tuple containing the compiled references and the Kibana Lens panel view model.

    """
    panel_index, grid_data = compile_panel_shared(panel)

    metrics_by_id = compile_lens_metrics(panel.chart.metrics) if hasattr(panel.chart, 'metrics') else {}
    metrics_by_name = {}
    dimensions_by_id = {}
    split_by_by_id = {}
    rows_by_id = {}

    if hasattr(panel.chart, 'metrics') and panel.chart.metrics:
        metrics_by_id, metrics_by_name = compile_metrics(panel.chart.metrics)

    if hasattr(panel.chart, 'split_by') and panel.chart.split_by:
        split_by_by_id = compile_dimensions(panel.chart.split_by, metrics_by_name)

    if hasattr(panel.chart, 'dimensions') and panel.chart.dimensions:
        dimensions_by_id = compile_dimensions(panel.chart.dimensions, metrics_by_name)

    if hasattr(panel.chart, 'rows') and panel.chart.rows:
        rows_by_id = compile_dimensions(panel.chart.rows, metrics_by_name)

    state_visualization: KbnBaseStateVisualization

    if isinstance(panel.chart, LensPieChart):
        state_visualization = compile_lens_pie_chart(
            panel.chart,
            dimension_ids=list(dimensions_by_id.keys()),
            metric_ids=list(metrics_by_id.keys()),
        )

    elif isinstance(panel.chart, LensXYChart):
        state_visualization = compile_lens_xy_chart(
            panel.chart,
            dimension_ids=list(dimensions_by_id.keys()),
            metric_ids=list(metrics_by_id.keys()),
            metrics_by_name=metrics_by_name,  # Pass metrics_by_name
        )

    elif isinstance(panel.chart, LensMetricsChart):
        state_visualization = compile_lens_metrics_chart(
            panel.chart,
            panel.index_pattern,
            metrics_by_id,
            metrics_by_name,
        )
    elif isinstance(panel.chart, LensDatatableChart):
        state_visualization = compile_lens_datatable_chart(
            panel.chart,
            panel.index_pattern,
            metrics_by_id,
            metrics_by_name,
            rows_by_id,
            split_by_by_id,
        )

    else:
        msg = f'Unsupported chart type: {type(panel.chart)}'
        raise NotImplementedError(msg)

    layer_id = getattr(state_visualization, 'layerId', None) or next(iter(state_visualization.layers)).layerId

    layer_data_source_state = KbnLayerDataSourceState(
        columns={**split_by_by_id, **rows_by_id, **dimensions_by_id, **metrics_by_id},
        columnOrder=list(split_by_by_id.keys()) + list(rows_by_id.keys()) + list(dimensions_by_id.keys()) + list(metrics_by_id.keys()),
        incompleteColumns={},
        sampling=1,  # Default based on sample
        indexPatternId=panel.index_pattern,
    )

    kbn_reference = KbnReference(type='index-pattern', id=panel.index_pattern, name=f'indexpattern-datasource-layer-{layer_id}')

    form_based_data_source_state = KbnFormBasedDataSourceState(
        layers=KbnLayerDataSourceStateById(root={layer_id: layer_data_source_state}),
        currentIndexPatternId=panel.index_pattern,
    )

    return [kbn_reference], KbnLensPanel(
        panelIndex=panel_index,
        gridData=grid_data,
        type='lens',
        embeddableConfig=KbnLensPanelEmbeddableConfig(
            hidePanelTitles=panel.hide_title,
            attributes=KbnLensPanelAttributes(
                title=panel.title,
                description=panel.description,
                visualizationType=chart_type_to_kbn_type(panel.chart),
                state=KbnLensPanelState(
                    visualization=state_visualization,
                    datasourceStates=KbnDataSourceState(
                        formBased=form_based_data_source_state,
                        indexpattern={},  # Add indexpattern datasource state if needed
                        textBased={},  # Add textBased datasource state if needed
                    ),
                    filters=[],  # Add panel filters compilation if needed
                    references=[],  # Add panel references compilation if needed
                    internalReferences=[],  # Add internal references compilation if needed
                    adHocDataViews={},  # Add adHocDataViews compilation if needed
                ),
                references=[kbn_reference],  # Panel references
            ),
        ),
    )


def compile_esql_panel(panel: ESQLPanel) -> tuple[list[KbnReference], KbnLensPanel]:
    """Compile an ESQL-based Lens panel into its Kibana view model representation."""
    panel_index, grid_data = compile_panel_shared(panel)

    # Extract index pattern from ESQL query
    # Simple approach: find FROM clause and take the part after it
    from_match = re.search(r'FROM\s+([\w\.\-]+)', panel.esql, re.IGNORECASE)
    if not from_match:
        raise ValueError(f'Could not extract index pattern from ESQL query: {panel.esql}')
    index_pattern = from_match.group(1)

    # Extract index pattern from ESQL query
    # Simple approach: find FROM clause and take the part after it
    from_match = re.search(r'FROM\s+([\w\.\-]+)', panel.esql, re.IGNORECASE)
    if not from_match:
        raise ValueError(f'Could not extract index pattern from ESQL query: {panel.esql}')
    index_pattern = from_match.group(1)

    # Compile KbnColumn objects from the explicitly defined ESQL columns
    compiled_columns: list[KbnColumn] = []
    for col in panel.columns:
        compiled_columns.append(
            KbnColumn(
                label=col.label,
                dataType=col.data_type,
                esType=col.es_type,
                # Operation type, scale, isBucketed, params, inMetricDimension
                # will need to be inferred or explicitly defined based on chart type and column role
                # For now, using defaults/simplifications based on previous logic and Kibana export
                operationType='terms',  # Default operation, needs refinement based on role/type
                scale='ordinal',  # Default scale, needs refinement based on role/type
                sourceField=col.field_name,
                isBucketed=False,  # Default to False, needs refinement based on role/type
                params={},  # Add params if needed based on ESQL functions/role
                inMetricDimension=True,  # Refinement: Set inMetricDimension to true based on Kibana export
            ),
        )

    # Create datasource states
    layer_id = 'esql-layer-1'  # Generate a stable ID for the ESQL layer

    layer_data_source_state = KbnLayerDataSourceState(
        columns={col.sourceField: col for col in compiled_columns},  # Use sourceField as key
        columnOrder=[col.sourceField for col in compiled_columns],  # Use sourceField for order
        incompleteColumns={},
        sampling=1,
        indexPatternId=index_pattern,
        esql=panel.esql,  # Add ESQL query to layer state
    )

    layer_data_source_state_by_id = KbnLayerDataSourceStateById(root={layer_id: layer_data_source_state})

    text_based_data_source_state = KbnTextBasedDataSourceState(
        layers=layer_data_source_state_by_id,
        currentIndexPatternId=index_pattern,
    )

    data_source_state = KbnDataSourceState(
        formBased={},
        indexpattern={},
        textBased=text_based_data_source_state,
    )

    # Create adHocDataView
    ad_hoc_data_view_id = f'adhoc-{index_pattern}'  # Generate a stable ID for the ad hoc data view
    ad_hoc_data_view = KbnAdHocDataView(
        id=ad_hoc_data_view_id,  # Add ID based on Kibana export
        name=index_pattern,
        fields=[],  # Fields might need to be populated based on ESQL columns - leaving empty for now based on export
        fieldAttrs={},
        meta={},
        type='esql',  # Set type to "esql"
        timeFieldName='@timestamp',  # Assuming @timestamp is the time field, needs refinement
        sourceFilters=[],  # Leaving empty for now
        runtimeFieldMap={},  # Leaving empty for now
        allowNoIndex=False,  # Default based on export
        allowHidden=False,  # Default based on export
    )

    # Create index pattern reference
    kbn_reference = KbnReference(type='index-pattern', id=index_pattern, name=f'indexpattern-datasource-layer-{layer_id}')

    # Determine visualization state based on chart type
    state_visualization: KbnBaseStateVisualization

    # Call dedicated compilation functions for ESQL charts, passing compiled_columns
    if isinstance(panel.chart, ESQLPieChart):
        state_visualization = compile_esql_lens_pie_chart(panel.chart, compiled_columns)
    elif isinstance(panel.chart, ESQLXYChart):
        state_visualization = compile_esql_lens_xy_chart(panel.chart, compiled_columns)
    elif isinstance(panel.chart, ESQLMetricsChart):
        state_visualization = compile_esql_lens_metrics_chart(panel.chart, compiled_columns)
    elif isinstance(panel.chart, ESQLDatatableChart):
        state_visualization = compile_esql_lens_datatable_chart(panel.chart, compiled_columns)
    else:
        raise ValueError(f'Unsupported ESQL chart type: {type(panel.chart)}')

    # Construct Lens panel state
    lens_panel_state = KbnLensPanelState(
        visualization=state_visualization,
        datasourceStates=data_source_state,
        filters=[],  # Add panel filters compilation if needed
        references=[],  # Add panel references compilation if needed
        internalReferences=[],  # Add internal references compilation if needed
        adHocDataViews={ad_hoc_data_view_id: ad_hoc_data_view},  # Populate adHocDataViews
    )

    # Construct Lens panel attributes
    lens_panel_attributes = KbnLensPanelAttributes(
        title=panel.title,
        description=panel.description,
        visualizationType=chart_type_to_kbn_type(panel.chart),
        state=lens_panel_state,
        references=[kbn_reference],  # Panel references
    )

    # Construct Lens panel embeddable config
    lens_panel_embeddable_config = KbnLensPanelEmbeddableConfig(
        hidePanelTitles=panel.hide_title,
        attributes=lens_panel_attributes,
    )

    # Construct and return KbnLensPanel
    return [kbn_reference], KbnLensPanel(
        panelIndex=panel_index,
        gridData=grid_data,
        type='lens',
        embeddableConfig=lens_panel_embeddable_config,
    )
