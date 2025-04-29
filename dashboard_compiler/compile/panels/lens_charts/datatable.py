
from dashboard_compiler.compile.utils import stable_id_generator
from dashboard_compiler.models.config.panels.lens_charts.datatable import LensDatatableChart
from dashboard_compiler.models.views.panels.lens_chart.datatable import (
    KbnDatatableColumn,
    KbnDatatablePagination,
    KbnDatatableSort,
    KbnDatatableVisualizationState,
)


def compile_lens_datatable_chart(
    chart: LensDatatableChart,
    index_pattern: str,
    metrics_by_id,
    metrics_by_name,
    rows_by_id,
    split_by_by_id,
) -> KbnDatatableVisualizationState:
    """
    Compile a LensDatatableChart config object into Kibana view models.
    """
    # Generate layer ID
    layer_id = chart.id or stable_id_generator(["datatable", index_pattern, *metrics_by_id.keys()])

    visualization_columns = []

    for id, row in rows_by_id.items():
        visualization_columns.append(
            KbnDatatableColumn(
                columnId=id,
                isTransposed=False,
                isMetric=False,
            )
        )

    for id, metric in metrics_by_id.items():
        visualization_columns.append(
            KbnDatatableColumn(
                columnId=id,
                isTransposed=False,
                isMetric=True,
            )
        )

    for id, split in split_by_by_id.items():
        visualization_columns.append(
            KbnDatatableColumn(
                columnId=id,
                isTransposed=True,
                isMetric=False,
            )
        )

    # Handle pagination
    pagination_state: KbnDatatablePagination | None = None
    if chart.pagination:
        pagination_state = KbnDatatablePagination(page=0, pageSize=chart.pagination.page_size)  # Start at page 0

    # Handle sort
    sort_state: KbnDatatableSort | None = None
    # if chart.sort:
    #     # Find the columnId for the sort column label
    #     sort_column_id = None
    #     for col in visualization_columns:
    #         # Need to find the corresponding KbnColumn in datasource_columns to get the label
    #         datasource_col = datasource_columns.get(col.columnId)
    #         if datasource_col and datasource_col.label == chart.sort.column_label:
    #             sort_column_id = col.columnId
    #             break

    #     if sort_column_id:
    #         sort_state = KbnDatatableSort(columnId=sort_column_id, direction=chart.sort.direction)

    # Create KbnDatatableVisualizationState
    kbn_state_visualization = KbnDatatableVisualizationState(
        layerId=layer_id,
        layerType="data",
        columns=visualization_columns,
        sort=sort_state,
        pagination=pagination_state,
        showRowNumbers=chart.show_row_numbers,  # Mapped from config
        showToolbar=chart.show_toolbar,  # Mapped from config
        showTotal=chart.show_total,  # Mapped from config
    )

    return kbn_state_visualization
