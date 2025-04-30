from dashboard_compiler.panels.lens.charts.pie.config import LensPieChart
from dashboard_compiler.panels.lens.charts.pie.view import KbnPieStateVisualizationLayer, KbnPieVisualizationState
from dashboard_compiler.panels.lens.view import (
    KbnBaseStateVisualization,
)
from dashboard_compiler.shared.config import stable_id_generator


def compile_lens_pie_chart(chart: LensPieChart, dimension_ids: list[str], metric_ids: list[str]) -> KbnBaseStateVisualization:
    layer_id = chart.id or stable_id_generator(['pie', *dimension_ids, *metric_ids])

    kbn_state_visualization_layer = KbnPieStateVisualizationLayer(
        layerId=layer_id,
        primaryGroups=dimension_ids,
        metrics=metric_ids,
        numberDisplay='percent',  # Default based on sample
        categoryDisplay='default',  # Default based on sample
        legendDisplay='default',  # Default based on sample
        nestedLegend=False,  # Default based on sample
    )

    kbn_state_visualization = KbnPieVisualizationState(
        shape='pie',
        layers=[kbn_state_visualization_layer],
        # palette={} # Add palette compilation if needed
    )

    return kbn_state_visualization


from dashboard_compiler.panels.lens.charts.pie.config import ESQLPieChart, LensPieChart  # Import LensESQLPieChart
from dashboard_compiler.panels.lens.view import (
    KbnBaseStateVisualization,
    KbnColumn,  # Import KbnColumn
)


def compile_lens_pie_chart(chart: LensPieChart, dimension_ids: list[str], metric_ids: list[str]) -> KbnBaseStateVisualization:
    layer_id = chart.id or stable_id_generator(['pie', *dimension_ids, *metric_ids])

    kbn_state_visualization_layer = KbnPieStateVisualizationLayer(
        layerId=layer_id,
        primaryGroups=dimension_ids,
        metrics=metric_ids,
        numberDisplay='percent',  # Default based on sample
        categoryDisplay='default',  # Default based on sample
        legendDisplay='default',  # Default based on sample
        nestedLegend=False,  # Default based on sample
    )

    kbn_state_visualization = KbnPieVisualizationState(
        shape='pie',
        layers=[kbn_state_visualization_layer],
        # palette={} # Add palette compilation if needed
    )

    return kbn_state_visualization


def compile_esql_lens_pie_chart(chart: ESQLPieChart, compiled_columns: list[KbnColumn]) -> KbnBaseStateVisualization:
    """Compile an ESQL-based Lens Pie chart into its Kibana view model representation."""
    # Generate a stable layer ID
    layer_id = chart.id or stable_id_generator(['esql-pie'])

    # Map columns to primaryGroups and metrics based on chart config, looking up column IDs
    slice_by_column_id = next((col.columnId for col in compiled_columns if col.sourceField == chart.slice_by_column), None)
    size_by_column_id = next((col.columnId for col in compiled_columns if col.sourceField == chart.size_by_column), None)

    if not slice_by_column_id:
        raise ValueError(f"Slice by column '{chart.slice_by_column}' not found in compiled ESQL columns.")
    if not size_by_column_id:
        raise ValueError(f"Size by column '{chart.size_by_column}' not found in compiled ESQL columns.")

    primary_groups = [slice_by_column_id]
    metrics = [size_by_column_id]

    kbn_state_visualization_layer = KbnPieStateVisualizationLayer(
        layerId=layer_id,
        primaryGroups=primary_groups,
        metrics=metrics,
        numberDisplay='percent',  # Default based on sample
        categoryDisplay='default',  # Default based on sample
        legendDisplay='default',  # Default based on sample
        nestedLegend=False,  # Default based on sample
        layerType='data',  # Default based on sample
        colorMapping={
            'assignments': [],
            'specialAssignments': [{'rule': {'type': 'other'}, 'color': {'type': 'loop'}, 'touched': False}],
            'paletteId': 'default',
            'colorMode': {'type': 'categorical'},
        },  # Default based on Kibana export
    )

    kbn_state_visualization = KbnPieVisualizationState(
        shape='pie',
        layers=[kbn_state_visualization_layer],
        # palette={} # Add palette compilation if needed
    )

    return kbn_state_visualization
