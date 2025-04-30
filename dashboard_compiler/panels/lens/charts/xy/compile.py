from typing import Any

from dashboard_compiler.panels.lens.charts.xy.config import ESQLXYChart, LensXYChart, XYChart  # Import LensESQLXYChart
from dashboard_compiler.panels.lens.charts.xy.view import (
    KbnXYVisualizationState,
    SeriesTypeEnum,
    XYDataLayerConfig,
)
from dashboard_compiler.panels.lens.components.compile import compile_dimensions
from dashboard_compiler.panels.lens.metrics.compile import compile_lens_metrics
from dashboard_compiler.panels.lens.view import KbnColumn  # Import KbnColumn
from dashboard_compiler.shared.config import stable_id_generator

ORIENTATION_MAP = {
    'horizontal': 0,
    'vertical': 90,
    'rotated': 45,
}


def chart_to_series_type(chart_type: str, mode: str | None = None) -> SeriesTypeEnum:
    """Convert Lens chart type and mode to Kibana SeriesType."""
    if chart_type == 'line':
        return SeriesTypeEnum.line

    if chart_type == 'bar' and mode == 'unstacked':
        return SeriesTypeEnum.bar
    if chart_type == 'bar' and mode == 'percentage':
        return SeriesTypeEnum.bar_percentage_stacked
    if chart_type == 'bar' and mode in (None, 'stacked'):
        return SeriesTypeEnum.bar_stacked

    if chart_type == 'area' and mode == 'unstacked':
        return SeriesTypeEnum.area
    if chart_type == 'area' and mode == 'percentage':
        return SeriesTypeEnum.area_percentage_stacked
    if chart_type == 'area' and mode in (None, 'stacked'):
        return SeriesTypeEnum.area_stacked

    raise ValueError(f'Unsupported chart type: {chart_type} / {mode}')


def axis_titles_visibility_from_chart(chart: XYChart) -> dict[str, Any] | None:
    """Extract axis titles visibility settings from the chart configuration."""
    visibility = {}

    if chart.axis.bottom and chart.axis.bottom.title:
        visibility['x'] = chart.axis.bottom.title

    if chart.axis.left and chart.axis.left.title:
        visibility['yLeft'] = chart.axis.left.title

    if chart.axis.right and chart.axis.right.title:
        visibility['yRight'] = chart.axis.right.title

    return visibility if visibility else None


def tick_labels_visibility_from_chart(chart: XYChart) -> dict[str, Any] | None:
    """Extract tick labels visibility settings from the chart configuration."""
    visibility = {}

    if chart.axis.bottom and chart.axis.bottom.tick_labels:
        visibility['x'] = chart.axis.bottom.tick_labels

    if chart.axis.left and chart.axis.left.tick_labels:
        visibility['yLeft'] = chart.axis.left.tick_labels

    if chart.axis.right and chart.axis.right.tick_labels:
        visibility['yRight'] = chart.axis.right.tick_labels

    return visibility if visibility else None


def gridlines_visibility_from_chart(chart: XYChart) -> dict[str, Any] | None:
    """Extract gridlines visibility settings from the chart configuration."""
    visibility = {}

    if chart.axis.bottom and chart.axis.bottom.gridlines:
        visibility['x'] = chart.axis.bottom.gridlines

    if chart.axis.left and chart.axis.left.gridlines:
        visibility['yLeft'] = chart.axis.left.gridlines

    if chart.axis.right and chart.axis.right.gridlines:
        visibility['yRight'] = chart.axis.right.gridlines

    return visibility if visibility else None


def labels_orientation_from_chart(chart: XYChart) -> dict[str, Any] | None:
    """Extract label orientations from the chart configuration."""
    orientations = {}
    if chart.axis.bottom and chart.axis.bottom.orientation:
        orientations['x'] = ORIENTATION_MAP.get(chart.axis.bottom.orientation, 0)
    if chart.axis.left and chart.axis.left.orientation:
        orientations['yLeft'] = ORIENTATION_MAP.get(chart.axis.left.orientation, 90)
    if chart.axis.right and chart.axis.right.orientation:
        orientations['yRight'] = ORIENTATION_MAP.get(chart.axis.right.orientation, 0)
    return orientations if orientations else None


def bottom_axis_from_chart(chart: XYChart) -> dict[str, Any] | None:
    """Extract x-axis extent from the chart configuration."""
    if chart.axis.bottom:
        return {
            'min': chart.axis.bottom.min,
            'max': chart.axis.bottom.max,
        }
    return None


def left_axis_from_chart(chart: XYChart) -> dict[str, Any] | None:
    """Extract y-axis extent from the chart configuration for the specified axis."""
    if chart.axis.left:
        return {
            'min': chart.axis.left.min,
            'max': chart.axis.left.max,
        }

    return None


def right_axis_from_chart(chart: XYChart) -> dict[str, Any] | None:
    """Extract right y-axis extent from the chart configuration."""
    if chart.axis.right:
        return {
            'min': chart.axis.right.min,
            'max': chart.axis.right.max,
        }
    return None


def legend_from_chart(chart: XYChart) -> dict[str, Any] | None:
    """Extract legend settings from the chart configuration."""
    if chart.legend:
        return {
            'isVisible': chart.legend.is_visible,
            'position': chart.legend.position,
        }
    return None

    # Compile yConfig for metrics
    # y_configs: list[YConfig] = []
    # for metric in chart.metrics:
    #     metric_id = metrics_by_name.get(metric.label)  # Get the generated ID for the metric
    #     if metric_id:
    #         # Determine axis mode based on whether a right axis is defined and if the metric should use it
    #         axis_mode_name = "left"
    #         if chart.axis.right and metric.label in [m.label for m in chart.axis.right.metrics]:  # Assuming metrics in right axis config
    #             axis_mode_name = "right"

    #         y_configs.append(YConfig(forAccessor=metric_id, axisMode=YAxisMode(name=axis_mode_name)))


def compile_lens_xy_chart(
    chart: LensXYChart,
    dimension_ids: list[str],
    metric_ids: list[str],
    metrics_by_name: dict[str, str],
) -> KbnXYVisualizationState:
    layer_id = chart.id or stable_id_generator([chart.type, chart.mode or '', *dimension_ids, *metric_ids])

    metrics_by_id, metrics_by_name = compile_lens_metrics(chart.metrics)
    split_by_by_id = compile_dimensions(chart.split_by, metrics_by_name)

    kbn_series_type: SeriesTypeEnum = chart_to_series_type(chart.type, chart.mode)

    axis_titles_visibility = axis_titles_visibility_from_chart(chart)
    tick_labels_visibility = tick_labels_visibility_from_chart(chart)
    gridlines_visibility = gridlines_visibility_from_chart(chart)

    label_orientations = labels_orientation_from_chart(chart)

    bottom_axis = bottom_axis_from_chart(chart)
    left_axis = left_axis_from_chart(chart)
    right_axis = right_axis_from_chart(chart)

    legend = legend_from_chart(chart)

    value_labels = chart.appearance.value_labels if chart.appearance else None
    fitting_function = chart.appearance.fitting_function if chart.appearance else None
    emphasize_fitting = chart.appearance.emphasize_fitting if chart.appearance else False  # Default to False

    xy_data_layer = XYDataLayerConfig(  # Corrected model name
        layerId=layer_id,
        accessors=metric_ids,  # Metrics are accessors (Y-axis)
        xAccessor=dimension_ids[0] if dimension_ids else None,  # Assuming first dimension is x-axis
        position='top',  # Default based on sample
        seriesType=kbn_series_type,
        showGridlines=chart.axis.bottom.gridlines
        if chart.axis.bottom
        else True,  # Assuming bottom axis gridlines control layer gridlines, default to True
        layerType='data',  # Data layer
        colorMapping=None,  # Add color mapping compilation if needed
        splitAccessor=dimension_ids[1] if len(dimension_ids) > 1 else None,
    )

    kbn_state_visualization = KbnXYVisualizationState(
        preferredSeriesType=kbn_series_type,
        legend=legend,
        valueLabels=value_labels,
        fittingFunction=fitting_function,
        emphasizeFitting=emphasize_fitting,
        endValue=None,  # Not in config model, default to None
        xExtent=bottom_axis,  # Mapped from config
        yLeftExtent=left_axis,  # Mapped from config
        yRightExtent=right_axis,  # Mapped from config
        layers=[
            XYDataLayerConfig(  # Corrected model name
                layerId=layer_id,
                accessors=metric_ids,  # Metrics are accessors (Y-axis)
                xAccessor=dimension_ids[0] if dimension_ids else None,  # Assuming first dimension is x-axis
                position='top',  # Default based on sample
                seriesType=kbn_series_type,
                showGridlines=chart.axis.bottom.gridlines
                if chart.axis.bottom
                else True,  # Assuming bottom axis gridlines control layer gridlines, default to True
                layerType='data',  # Data layer
                colorMapping=None,  # Add color mapping compilation if needed
                splitAccessor=dimension_ids[1] if len(dimension_ids) > 1 else None,  # Assuming second dimension is split
                # yConfig=y_configs,  # Added yConfig
            ),
        ],
        xTitle=chart.axis.bottom.title if chart.axis.bottom else None,
        yTitle=chart.axis.left.title if chart.axis.left else None,
        yRightTitle=chart.axis.right.title if chart.axis.right else None,
        yLeftScale={'type': chart.axis.left.scale} if chart.axis.left and chart.axis.left.scale else None,  # Default to linear
        yRightScale={'type': chart.axis.right.scale} if chart.axis.right and chart.axis.right.scale else None,  # Default to linear
        axisTitlesVisibilitySettings=axis_titles_visibility,
        tickLabelsVisibilitySettings=tick_labels_visibility,
        labelsOrientation=label_orientations,
        gridlinesVisibilitySettings=gridlines_visibility,
        showCurrentTimeMarker=chart.axis.bottom.show_current_time_marker if chart.axis.bottom else False,  # Default to False
        curveType={'type': chart.appearance.curve_type} if chart.appearance and chart.appearance.curve_type else None,
        fillOpacity=chart.appearance.fill_opacity if chart.appearance else None,
        minBarHeight=chart.appearance.min_bar_height if chart.appearance else None,
        hideEndzones=chart.appearance.hide_endzones if chart.appearance else None,
    )

    return kbn_state_visualization


def compile_esql_lens_xy_chart(chart: ESQLXYChart, columns: list[KbnColumn]) -> KbnXYVisualizationState:
    """Compile an ESQL-based Lens XY chart into its Kibana view model representation."""
    # Generate a stable layer ID
    layer_id = chart.id or stable_id_generator(['esql-xy', chart.type, chart.mode or ''])

    # Determine Kibana seriesType based on chart type and mode
    kbn_series_type: SeriesType
    if chart.type == 'line':
        kbn_series_type = 'line'
    elif chart.type == 'bar':
        if chart.mode == 'unstacked':
            kbn_series_type = 'bar'
        elif chart.mode == 'percentage':
            kbn_series_type = 'bar_percentage_stacked'
        else:  # stacked or None
            kbn_series_type = 'bar_stacked'
    elif chart.type == 'area':
        if chart.mode == 'unstacked':
            kbn_series_type = 'area'
        elif chart.mode == 'percentage':
            kbn_series_type = 'area_percentage_stacked'
        else:  # stacked or None
            kbn_series_type = 'area_stacked'
    else:
        raise ValueError(f'Unsupported ESQL XY chart type: {chart.type}')

    # Map columns to accessors, xAccessor, and splitAccessor based on chart config
    x_accessor = chart.x_axis_column
    split_accessor = chart.split_column
    accessors = chart.y_axis_columns

    # Default axis formatting settings based on Kibana export
    axis_titles_visibility = {'x': True, 'yLeft': True, 'yRight': True}
    tick_labels_visibility = {'x': True, 'yLeft': True, 'yRight': True}
    label_orientations = {'x': 0, 'yLeft': 0, 'yRight': 0}
    gridlines_visibility = {'x': True, 'yLeft': True, 'yRight': True}

    kbn_state_visualization = KbnXYVisualizationState(
        preferredSeriesType=kbn_series_type,
        legend={  # Default legend formatting based on Kibana export
            'isVisible': True,
            'position': 'right',
        },
        valueLabels='hide',  # Default based on Kibana export
        fittingFunction={'type': 'Linear'},  # Default based on Kibana export
        emphasizeFitting=False,  # Default based on Kibana export
        endValue=None,
        xExtent={},  # No extent in ESQL export example
        yLeftExtent={},  # No extent in ESQL export example
        yRightExtent={},  # No extent in ESQL export example
        layers=[
            XYDataLayerConfig(
                layerId=layer_id,
                accessors=accessors,
                xAccessor=x_accessor,
                position='top',  # Default based on sample
                seriesType=kbn_series_type,
                showGridlines=True,  # Default based on Kibana export
                layerType='data',
                colorMapping={
                    'assignments': [],
                    'specialAssignments': [{'rule': {'type': 'other'}, 'color': {'type': 'loop'}, 'touched': False}],
                    'paletteId': 'eui_amsterdam_color_blind',
                    'colorMode': {'type': 'categorical'},
                },  # Default based on Kibana export
                splitAccessor=split_accessor,
            ),
        ],
        xTitle=None,  # No explicit titles in ESQL export example
        yTitle=None,  # No explicit titles in ESQL export example
        yRightTitle=None,  # No explicit titles in ESQL export example
        yLeftScale=None,  # Default to linear
        yRightScale=None,  # Default to linear
        axisTitlesVisibilitySettings=axis_titles_visibility,
        tickLabelsVisibilitySettings=tick_labels_visibility,
        labelsOrientation=label_orientations,
        gridlinesVisibilitySettings=gridlines_visibility,
        showCurrentTimeMarker=False,  # Default based on Kibana export
        curveType=None,  # Not in ESQL export example
        fillOpacity=None,  # Not in ESQL export example
        minBarHeight=None,  # Not in ESQL export example
        hideEndzones=None,  # Not in ESQL export example
    )

    return kbn_state_visualization
