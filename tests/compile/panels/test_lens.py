from dashboard_compiler.compile.panels.lens import compile_dimensions, compile_lens_xy_chart, compile_metrics
from dashboard_compiler.compile.utils import stable_id_generator
from dashboard_compiler.models.config.panels.lens_charts.base import LensAppearanceFormat, LensLegendFormat
from dashboard_compiler.models.config.panels.lens_charts.components.dimension import Dimension
from dashboard_compiler.models.config.panels.lens_charts.components.metric import Metric
from dashboard_compiler.models.config.panels.lens_charts.xy import (
    LensAxisFormat,
    LensBottomAxisFormat,
    LensLeftAxisFormat,
    LensRightAxisFormat,
    LensXYChart,
)
from dashboard_compiler.models.views.panels.lens_chart.xy import (
    KbnXYVisualizationState,
    LabelsOrientationConfig,
    SeriesType,
    XYDataLayerConfig,
    YAxisMode,
    YConfig,
)


# Helper function to create a basic LensXYChart config for testing
def create_basic_xy_chart_config():
    return LensXYChart(
        type="bar",
        dimensions=[Dimension(field="@timestamp", type="date_histogram", label="@timestamp", interval="auto")],
        metrics=[Metric(type="count", field="___records___", label="Count of records")],
        axis=LensAxisFormat(
            bottom=LensBottomAxisFormat(
                title="@timestamp", orientation="horizontal", gridlines=True, tick_labels=True, show_current_time_marker=False
            ),
            left=LensLeftAxisFormat(title="Count of records", orientation="vertical", gridlines=True, tick_labels=True, scale="linear"),
            right=None,
        ),
        legend=LensLegendFormat(is_visible=True, position="right"),
        appearance=LensAppearanceFormat(
            value_labels="hide",
            fitting_function="Linear",
            emphasize_fitting=False,
            curve_type=None,
            fill_opacity=None,
            min_bar_height=None,
            hide_endzones=None,
        ),
    )


# Helper function to generate expected IDs for a given config
def generate_expected_ids(config_chart: LensXYChart):
    metrics_by_id, metrics_by_name = compile_metrics(config_chart.metrics)
    dimensions_by_id = compile_dimensions(config_chart.dimensions, metrics_by_name)

    dimension_ids = list(dimensions_by_id.keys())
    metric_ids = list(metrics_by_id.keys())

    layer_id = config_chart.id or stable_id_generator([config_chart.type, config_chart.mode or "", *dimension_ids, *metric_ids])

    return dimension_ids, metric_ids, layer_id, dimensions_by_id, metrics_by_id, metrics_by_name


# Helper function to create the expected KbnXYVisualizationState for a given config and IDs
def create_expected_xy_visualization_state(
    config_chart: LensXYChart, dimension_ids: list[str], metric_ids: list[str], layer_id: str, metrics_by_name: dict[str, str]
):
    # Determine Kibana seriesType based on chart type and mode
    kbn_series_type: SeriesType
    if config_chart.type == "line":
        kbn_series_type = SeriesType(type="line")
    elif config_chart.type == "bar":
        if config_chart.mode == "unstacked":
            kbn_series_type = SeriesType(type="bar")
        elif config_chart.mode == "percentage":
            kbn_series_type = SeriesType(type="bar_percentage_stacked")
        else:  # stacked or None
            kbn_series_type = SeriesType(type="bar_stacked")
    elif config_chart.type == "area":
        if config_chart.mode == "unstacked":
            kbn_series_type = SeriesType(type="area")
        elif config_chart.mode == "percentage":
            kbn_series_type = SeriesType(type="area_percentage_stacked")
        else:  # stacked or None
            kbn_series_type = SeriesType(type="area_stacked")
    else:
        raise ValueError(f"Unsupported XY chart type: {config_chart.type}")

    # Compile yConfig for metrics
    y_configs: list[YConfig] = []
    for metric in config_chart.metrics:
        metric_id = metrics_by_name.get(metric.label)  # Get the generated ID for the metric
        if metric_id:
            # Determine axis mode based on whether a right axis is defined and if the metric should use it
            axis_mode_name = "left"
            if config_chart.axis.right and metric.label in [
                m.label for m in config_chart.axis.right.metrics
            ]:  # Assuming metrics in right axis config
                axis_mode_name = "right"

            y_configs.append(YConfig(forAccessor=metric_id, axisMode=YAxisMode(name=axis_mode_name)))

    # Map axis formatting
    axis_titles_visibility = {
        "x": config_chart.axis.bottom.title is not None if config_chart.axis.bottom else False,
        "yLeft": config_chart.axis.left.title is not None if config_chart.axis.left else False,
        "yRight": config_chart.axis.right is not None and config_chart.axis.right.title is not None if config_chart.axis.right else False,
    }

    tick_labels_visibility = {
        "x": config_chart.axis.bottom.tick_labels if config_chart.axis.bottom else True,  # Default to True
        "yLeft": config_chart.axis.left.tick_labels if config_chart.axis.left else True,  # Default to True
        "yRight": config_chart.axis.right.tick_labels if config_chart.axis.right else False,
    }

    gridlines_visibility = {
        "x": config_chart.axis.bottom.gridlines if config_chart.axis.bottom else True,  # Default to True
        "yLeft": config_chart.axis.left.gridlines if config_chart.axis.left else True,  # Default to True
        "yRight": config_chart.axis.right.gridlines if config_chart.axis.right else False,
    }

    # Map orientation (assuming 0 for horizontal, 90 for vertical, 45 for rotated - adjust if needed)
    orientation_map = {"horizontal": 0, "vertical": 90, "rotated": 45}
    labels_orientation = LabelsOrientationConfig(
        x=orientation_map.get(config_chart.axis.bottom.orientation, 0) if config_chart.axis.bottom else 0,
        yLeft=orientation_map.get(config_chart.axis.left.orientation, 90) if config_chart.axis.left else 90,  # Default yLeft to 90
        yRight=orientation_map.get(config_chart.axis.right.orientation, 0) if config_chart.axis.right else 0,
    )

    # Map axis extents
    x_extent = (
        {"min": config_chart.axis.bottom.min, "max": config_chart.axis.bottom.max}
        if config_chart.axis.bottom and (config_chart.axis.bottom.min is not None or config_chart.axis.bottom.max is not None)
        else None
    )
    y_left_extent = (
        {"min": config_chart.axis.left.min, "max": config_chart.axis.left.max}
        if config_chart.axis.left and (config_chart.axis.left.min is not None or config_chart.axis.left.max is not None)
        else None
    )
    y_right_extent = (
        {"min": config_chart.axis.right.min, "max": config_chart.axis.right.max}
        if config_chart.axis.right and (config_chart.axis.right.min is not None or config_chart.axis.right.max is not None)
        else None
    )

    return KbnXYVisualizationState(
        preferredSeriesType=kbn_series_type,
        legend={  # Map legend formatting
            "isVisible": config_chart.legend.is_visible if config_chart.legend else True,  # Default to True
            "position": config_chart.legend.position if config_chart.legend else "right",  # Default to right
        },
        valueLabels=config_chart.appearance.value_labels if config_chart.appearance else "hide",  # Default to hide
        fittingFunction={"type": config_chart.appearance.fitting_function}
        if config_chart.appearance and config_chart.appearance.fitting_function
        else None,
        emphasizeFitting=config_chart.appearance.emphasize_fitting if config_chart.appearance else False,  # Default to False
        endValue=None,  # Not in config model, default to None
        xExtent=x_extent,  # Mapped from config
        yLeftExtent=y_left_extent,  # Mapped from config
        yRightExtent=y_right_extent,  # Mapped from config
        layers=[
            XYDataLayerConfig(  # Corrected model name
                layerId=layer_id,
                accessors=metric_ids,  # Metrics are accessors (Y-axis)
                xAccessor=dimension_ids[0] if dimension_ids else None,  # Assuming first dimension is x-axis
                position="top",  # Default based on sample
                seriesType=kbn_series_type,
                showGridlines=config_chart.axis.bottom.gridlines
                if config_chart.axis.bottom
                else True,  # Assuming bottom axis gridlines control layer gridlines, default to True
                layerType="data",  # Data layer
                colorMapping={},  # Add color mapping compilation if needed
                splitAccessor=dimension_ids[1] if len(dimension_ids) > 1 else None,  # Assuming second dimension is split
                yConfig=y_configs,  # Added yConfig
            )
        ],
        xTitle=config_chart.axis.bottom.title if config_chart.axis.bottom else None,
        yTitle=config_chart.axis.left.title if config_chart.axis.left else None,
        yRightTitle=config_chart.axis.right.title if config_chart.axis.right else None,
        yLeftScale={"type": config_chart.axis.left.scale}
        if config_chart.axis.left and config_chart.axis.left.scale
        else {"type": "linear"},  # Default to linear
        yRightScale={"type": config_chart.axis.right.scale}
        if config_chart.axis.right and config_chart.axis.right.scale
        else {"type": "linear"},  # Default to linear
        axisTitlesVisibilitySettings=axis_titles_visibility,
        tickLabelsVisibilitySettings=tick_labels_visibility,
        labelsOrientation=labels_orientation,
        gridlinesVisibilitySettings=gridlines_visibility,
        showCurrentTimeMarker=config_chart.axis.bottom.show_current_time_marker if config_chart.axis.bottom else False,  # Default to False
        curveType={"type": config_chart.appearance.curve_type} if config_chart.appearance and config_chart.appearance.curve_type else None,
        fillOpacity=config_chart.appearance.fill_opacity if config_chart.appearance else None,
        minBarHeight=config_chart.appearance.min_bar_height if config_chart.appearance else None,
        hideEndzones=config_chart.appearance.hide_endzones if config_chart.appearance else None,
    )


class TestLensCompilation:
    def test_compile_lens_xy_chart_basic(self):
        config_chart = create_basic_xy_chart_config()
        dimension_ids, metric_ids, layer_id, dimensions_by_id, metrics_by_id, metrics_by_name = generate_expected_ids(config_chart)
        expected_state = create_expected_xy_visualization_state(config_chart, dimension_ids, metric_ids, layer_id, metrics_by_name)

        compiled_state = compile_lens_xy_chart(config_chart, dimension_ids, metric_ids, metrics_by_name)  # Pass metrics_by_name

        # Assert the compiled state matches the expected state
        assert compiled_state.model_dump(exclude_none=True) == expected_state.model_dump(exclude_none=True)

    def test_compile_lens_xy_chart_line(self):
        config_chart = create_basic_xy_chart_config()
        config_chart.type = "line"
        config_chart.appearance.fitting_function = "None"

        dimension_ids, metric_ids, layer_id, dimensions_by_id, metrics_by_id, metrics_by_name = generate_expected_ids(config_chart)
        expected_state = create_expected_xy_visualization_state(config_chart, dimension_ids, metric_ids, layer_id, metrics_by_name)

        compiled_state = compile_lens_xy_chart(config_chart, dimension_ids, metric_ids, metrics_by_name)  # Pass metrics_by_name

        assert compiled_state.model_dump(exclude_none=True) == expected_state.model_dump(exclude_none=True)

    def test_compile_lens_xy_chart_area_percentage(self):
        config_chart = create_basic_xy_chart_config()
        config_chart.type = "area"
        config_chart.mode = "percentage"
        config_chart.axis.left.scale = "linear"

        dimension_ids, metric_ids, layer_id, dimensions_by_id, metrics_by_id, metrics_by_name = generate_expected_ids(config_chart)
        expected_state = create_expected_xy_visualization_state(config_chart, dimension_ids, metric_ids, layer_id, metrics_by_name)

        compiled_state = compile_lens_xy_chart(config_chart, dimension_ids, metric_ids, metrics_by_name)  # Pass metrics_by_name

        assert compiled_state.model_dump(exclude_none=True) == expected_state.model_dump(exclude_none=True)

    def test_compile_lens_xy_chart_multi_metric(self):
        config_chart = create_basic_xy_chart_config()
        config_chart.metrics.append(Metric(type="sum", field="bytes", label="Sum of bytes"))

        dimension_ids, metric_ids, layer_id, dimensions_by_id, metrics_by_id, metrics_by_name = generate_expected_ids(config_chart)
        expected_state = create_expected_xy_visualization_state(
            config_chart, dimension_ids=dimension_ids, metric_ids=metric_ids, layer_id=layer_id, metrics_by_name=metrics_by_name
        )

        compiled_state = compile_lens_xy_chart(config_chart, dimension_ids, metric_ids, metrics_by_name)  # Pass metrics_by_name

        assert compiled_state.model_dump(exclude_none=True) == expected_state.model_dump(exclude_none=True)

    def test_compile_lens_xy_chart_split_dimension(self):
        config_chart = create_basic_xy_chart_config()
        config_chart.dimensions.append(Dimension(field="extension", type="terms", label="Extension"))

        dimension_ids, metric_ids, layer_id, dimensions_by_id, metrics_by_id, metrics_by_name = generate_expected_ids(config_chart)
        expected_state = create_expected_xy_visualization_state(
            config_chart, dimension_ids=dimension_ids, metric_ids=metric_ids, layer_id=layer_id, metrics_by_name=metrics_by_name
        )

        compiled_state = compile_lens_xy_chart(config_chart, dimension_ids, metric_ids, metrics_by_name)  # Pass metrics_by_name

        assert compiled_state.model_dump(exclude_none=True) == expected_state.model_dump(exclude_none=True)

    def test_compile_lens_xy_chart_right_y_axis(self):
        config_chart = create_basic_xy_chart_config()
        # Add a metric that will be assigned to the right axis
        right_axis_metric = Metric(type="rate", field="bytes", label="Rate of bytes")
        config_chart.metrics.append(right_axis_metric)
        config_chart.axis.right = LensRightAxisFormat(
            title="Rate", orientation="vertical", gridlines=False, tick_labels=False, scale="log", metrics=[right_axis_metric]
        )

        dimension_ids, metric_ids, layer_id, dimensions_by_id, metrics_by_id, metrics_by_name = generate_expected_ids(config_chart)
        expected_state = create_expected_xy_visualization_state(
            config_chart, dimension_ids=dimension_ids, metric_ids=metric_ids, layer_id=layer_id, metrics_by_name=metrics_by_name
        )

        compiled_state = compile_lens_xy_chart(config_chart, dimension_ids, metric_ids, metrics_by_name)  # Pass metrics_by_name

        assert compiled_state.model_dump(exclude_none=True) == expected_state.model_dump(exclude_none=True)

    # Add new test cases here

    def test_compile_lens_xy_chart_bar_stacked(self):
        config_chart = create_basic_xy_chart_config()
        config_chart.type = "bar"
        config_chart.mode = "stacked"
        dimension_ids, metric_ids, layer_id, dimensions_by_id, metrics_by_id, metrics_by_name = generate_expected_ids(config_chart)
        expected_state = create_expected_xy_visualization_state(config_chart, dimension_ids, metric_ids, layer_id, metrics_by_name)
        compiled_state = compile_lens_xy_chart(config_chart, dimension_ids, metric_ids, metrics_by_name)  # Pass metrics_by_name
        assert compiled_state.model_dump(exclude_none=True) == expected_state.model_dump(exclude_none=True)

    def test_compile_lens_xy_chart_area_unstacked(self):
        config_chart = create_basic_xy_chart_config()
        config_chart.type = "area"
        config_chart.mode = "unstacked"
        dimension_ids, metric_ids, layer_id, dimensions_by_id, metrics_by_id, metrics_by_name = generate_expected_ids(config_chart)
        expected_state = create_expected_xy_visualization_state(config_chart, dimension_ids, metric_ids, layer_id, metrics_by_name)
        compiled_state = compile_lens_xy_chart(config_chart, dimension_ids, metric_ids, metrics_by_name)  # Pass metrics_by_name
        assert compiled_state.model_dump(exclude_none=True) == expected_state.model_dump(exclude_none=True)

    def test_compile_lens_xy_chart_terms_dimension(self):
        config_chart = create_basic_xy_chart_config()
        config_chart.dimensions = [
            Dimension(field="event.dataset", type="terms", label="Dataset", size=5, other_bucket=True, missing_bucket=False)
        ]
        dimension_ids, metric_ids, layer_id, dimensions_by_id, metrics_by_id, metrics_by_name = generate_expected_ids(config_chart)
        expected_state = create_expected_xy_visualization_state(config_chart, dimension_ids, metric_ids, layer_id, metrics_by_name)
        compiled_state = compile_lens_xy_chart(config_chart, dimension_ids, metric_ids, metrics_by_name)  # Pass metrics_by_name
        assert compiled_state.model_dump(exclude_none=True) == expected_state.model_dump(exclude_none=True)

    def test_compile_lens_xy_chart_appearance_options(self):
        config_chart = create_basic_xy_chart_config()
        config_chart.appearance = LensAppearanceFormat(
            value_labels="show",
            fitting_function="None",
            emphasize_fitting=True,
            curve_type="linear",  # Corrected curve_type value
            fill_opacity=0.5,
            min_bar_height=2,
            hide_endzones=True,
        )
        dimension_ids, metric_ids, layer_id, dimensions_by_id, metrics_by_id, metrics_by_name = generate_expected_ids(config_chart)
        expected_state = create_expected_xy_visualization_state(config_chart, dimension_ids, metric_ids, layer_id, metrics_by_name)
        compiled_state = compile_lens_xy_chart(config_chart, dimension_ids, metric_ids, metrics_by_name)  # Pass metrics_by_name
        assert compiled_state.model_dump(exclude_none=True) == expected_state.model_dump(exclude_none=True)

    def test_compile_lens_xy_chart_axis_options(self):
        config_chart = create_basic_xy_chart_config()
        config_chart.axis.bottom.orientation = "rotated"
        config_chart.axis.bottom.gridlines = False
        config_chart.axis.left.tick_labels = False
        config_chart.axis.left.scale = "log"
        config_chart.axis.bottom.show_current_time_marker = True
        config_chart.axis.bottom.min = 0
        config_chart.axis.bottom.max = 100
        config_chart.axis.left.min = 1
        config_chart.axis.left.max = 1000

        dimension_ids, metric_ids, layer_id, dimensions_by_id, metrics_by_id, metrics_by_name = generate_expected_ids(config_chart)
        expected_state = create_expected_xy_visualization_state(config_chart, dimension_ids, metric_ids, layer_id, metrics_by_name)
        compiled_state = compile_lens_xy_chart(config_chart, dimension_ids, metric_ids, metrics_by_name)  # Pass metrics_by_name
        assert compiled_state.model_dump(exclude_none=True) == expected_state.model_dump(exclude_none=True)
