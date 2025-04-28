from dashboard_compiler.compile.utils import stable_id_generator
from dashboard_compiler.models.config.panels.lens_charts.pie import LensPieChart
from dashboard_compiler.models.views.panels.lens import (
    KbnBaseStateVisualization,
)
from dashboard_compiler.models.views.panels.lens_chart.pie import KbnPieStateVisualizationLayer, KbnPieVisualizationState


def compile_lens_pie_chart(chart: LensPieChart, dimension_ids: list[str], metric_ids: list[str]) -> KbnBaseStateVisualization:
    layer_id = chart.id or stable_id_generator(["pie", *dimension_ids, *metric_ids])

    kbn_state_visualization_layer = KbnPieStateVisualizationLayer(
        layerId=layer_id,
        primaryGroups=dimension_ids,
        metrics=metric_ids,
        numberDisplay="percent",  # Default based on sample
        categoryDisplay="default",  # Default based on sample
        legendDisplay="default",  # Default based on sample
        nestedLegend=False,  # Default based on sample
    )

    kbn_state_visualization = KbnPieVisualizationState(
        shape="pie",
        layers=[kbn_state_visualization_layer],
        # palette={} # Add palette compilation if needed
    )

    return kbn_state_visualization
