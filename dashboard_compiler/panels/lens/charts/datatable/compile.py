from dashboard_compiler.panels.lens.charts.datatable.config import (
    ESQLDatatableChart,
    LensDatatableChart,
)  # Import LensESQLDatatableChart
from dashboard_compiler.panels.lens.charts.datatable.view import (
    KbnDatatableColumn,
    KbnDatatablePagination,
    KbnDatatableSort,
    KbnDatatableVisualizationState,
)
from dashboard_compiler.shared.config import stable_id_generator


def compile_lens_datatable_chart(
    chart: LensDatatableChart,
    index_pattern: str,
    metrics_by_id,
    metrics_by_name,
    rows_by_id,
    split_by_by_id,
) -> KbnDatatableVisualizationState:
    """Compile a LensDatatableChart config object into Kibana view models."""
    # Generate layer ID
    layer_id = chart.id or stable_id_generator(['datatable', index_pattern, *metrics_by_id.keys()])

    visualization_columns = []

    for id, _ in rows_by_id.items():
        visualization_columns.append(
            KbnDatatableColumn(
                columnId=id,
                isTransposed=False,
                isMetric=False,
            ),
        )

    for id, _ in metrics_by_id.items():
        visualization_columns.append(
            KbnDatatableColumn(
                columnId=id,
                isTransposed=False,
                isMetric=True,
            ),
        )

    for id, _ in split_by_by_id.items():
        visualization_columns.append(
            KbnDatatableColumn(
                columnId=id,
                isTransposed=True,
                isMetric=False,
            ),
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
        layerType='data',
        columns=visualization_columns,
        sort=sort_state,
        pagination=pagination_state,
        showRowNumbers=chart.show_row_numbers,  # Mapped from config
        showToolbar=chart.show_toolbar,  # Mapped from config
        showTotal=chart.show_total,  # Mapped from config
    )

    return kbn_state_visualization


def compile_esql_lens_datatable_chart(chart: ESQLDatatableChart, columns: list[KbnDatatableColumn]) -> KbnDatatableVisualizationState:
    """Compile an ESQL-based Lens Datatable chart into its Kibana view model representation."""
    # Generate layer ID
    layer_id = chart.id or stable_id_generator(['esql-datatable'])  # No index pattern/metrics in ESQL chart config

    # Filter compiled columns based on the columns defined in the chart config
    visualization_columns: list[KbnDatatableColumn] = []
    for col_name in chart.columns:
        # Find the corresponding KbnColumn object by sourceField
        kbn_col = next((c for c in columns if c.sourceField == col_name), None)
        if kbn_col:
            # Determine if the column is a metric based on its dataType (simple heuristic for now)
            is_metric = kbn_col.dataType in ['number']  # Add other numeric types if needed

            visualization_columns.append(
                KbnDatatableColumn(
                    columnId=kbn_col.sourceField,  # Use sourceField as columnId
                    isTransposed=False,  # Default to False for datatable columns
                    isMetric=is_metric,
                ),
            )
        else:
            # This should not happen if the columns in chart config match compiled columns
            raise ValueError(f"Column '{col_name}' not found in compiled ESQL columns.")

    # Handle pagination
    pagination_state: KbnDatatablePagination | None = None
    if chart.pagination:
        pagination_state = KbnDatatablePagination(page=0, pageSize=chart.pagination.page_size)  # Start at page 0

    # Handle sort - ESQL datatable sort is not explicitly defined in the config model,
    # so we'll omit it for now based on the Kibana export example.
    sort_state: KbnDatatableSort | None = None
    # if chart.sort:
    #     # Find the columnId for the sort column label
    #     sort_column_id = None
    #     for col in visualization_columns:
    #         # Need to find the corresponding KbnColumn in datasource_columns to get the label
    #         datasource_col = next((c for c in columns if c.sourceField == col.columnId), None)
    #         if datasource_col and datasource_col.label == chart.sort.column_label:
    #             sort_column_id = col.columnId
    #             break

    #     if sort_column_id:
    #         sort_state = KbnDatatableSort(columnId=sort_column_id, direction=chart.sort.direction)

    # Create KbnDatatableVisualizationState
    kbn_state_visualization = KbnDatatableVisualizationState(
        layerId=layer_id,
        layerType='data',
        columns=visualization_columns,
        sort=sort_state,
        pagination=pagination_state,
        showRowNumbers=chart.show_row_numbers,  # Mapped from config
        showToolbar=chart.show_toolbar,  # Mapped from config
        showTotal=chart.show_total,  # Mapped from config
    )

    return kbn_state_visualization
