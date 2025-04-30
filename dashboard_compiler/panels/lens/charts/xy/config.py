from typing import Literal

from pydantic import BaseModel, Field, model_validator

from dashboard_compiler.panels.lens.charts.config import (
    BaseLensAxisFormat,
    BaseLensChart,
    BaseLensChartAppearance,
    LensAppearanceFormat,
    LensAxisFormat,
    LensLegendFormat,
)
from dashboard_compiler.panels.lens.dimension.config import Dimension
from dashboard_compiler.panels.lens.metrics.config import Metric

type XYChart = LensXYChart | ESQLXYChart


class LensBottomAxisFormat(BaseLensAxisFormat):
    """Represents formatting options for the bottom axis of an XY chart."""

    show_current_time_marker: bool | None = Field(
        default=None,
        description='If `true`, show a marker on the bottom axis indicating the current time. Defaults to `false`.',
    )


class LensLeftAxisFormat(BaseLensAxisFormat):
    """Represents formatting options for the left axis of an XY chart."""


class LensRightAxisFormat(BaseLensAxisFormat):
    """Represents formatting options for the right axis of an XY chart."""

    metrics: list[Metric] = Field(
        default_factory=list,
        description='A list of metric configurations to be displayed on the right axis. Defaults to an empty list.',
    )


class LensAxisFormat(BaseModel):
    """Groups formatting options for the axes of an XY chart."""

    bottom: LensBottomAxisFormat | None = Field(default_factory=LensBottomAxisFormat, description='Formatting options for the bottom axis.')
    left: LensLeftAxisFormat | None = Field(default_factory=LensLeftAxisFormat, description='Formatting options for the left axis.')
    right: LensRightAxisFormat | None = Field(
        default_factory=LensRightAxisFormat,
        description='Formatting options for the right axis (optional).',
    )


class LensXYChart(BaseLensChart):
    """Represents a Bar, Line, or Area chart configuration within a Lens panel in the YAML schema."""

    type: Literal['bar', 'area', 'line'] = Field('bar', description="The type of XY chart to display. Defaults to 'bar'.")
    mode: Literal['stacked', 'unstacked', 'percentage'] = Field(
        'unstacked',
        description="The stacking mode for bar and area charts. Defaults to 'unstacked'.",
    )
    dimensions: list[Dimension] = Field(
        ...,
        description='Defines the dimensions (typically the x-axis or split/breakdown) for the chart.',
        min_length=1,
    )
    metrics: list[Metric] = Field(..., description='Defines the metrics (typically the y-axis values) for the chart.', min_length=1)

    breakdown: Dimension | None = Field(
        None,
        description='An optional dimension to split the series by. If provided, it will be used to break down the data into multiple series.',
    )

    axis: LensAxisFormat = Field(default_factory=LensAxisFormat, description="Formatting options for the chart's axes.")
    legend: LensLegendFormat = Field(default_factory=LensLegendFormat, description="Formatting options for the chart's legend.")
    appearance: LensAppearanceFormat = Field(default_factory=LensAppearanceFormat, description='Appearance options for the chart.')

    @model_validator(mode='after')
    def check_mode_for_chart_type(self) -> 'LensXYChart':
        """Validates that the 'mode' field is only used for 'bar' or 'area' chart types."""
        if self.mode is not None and self.type not in ['bar', 'area']:
            raise ValueError("Mode can only be specified for 'bar' or 'area' chart types.")
        return self

    def add_dimension(self, dimension: Dimension) -> None:
        """Adds a dimension to the chart's dimensions list.

        Args:
            dimension (Dimension): The dimension object to add.

        """
        self.dimensions.append(dimension)

    def add_metric(self, metric: Metric) -> None:
        """Adds a metric to the chart's metrics list.

        Args:
            metric (Metric): The metric object to add.

        """
        self.metrics.append(metric)


class BaseLensXYChart(BaseLensChart):
    """Base model for defining XY chart objects within a Lens panel in the YAML schema."""

    axis: LensAxisFormat = Field(default_factory=LensAxisFormat, description='Formatting options for the chart axes.')
    legend: LensLegendFormat = Field(default_factory=LensLegendFormat, description='Formatting options for the chart legend.')
    appearance: LensAppearanceFormat = Field(
        default_factory=LensAppearanceFormat,
        description='Formatting options for the chart appearance.',
    )


class ESQLXYChart(BaseLensXYChart):
    """Represents an ES|QL based Bar, Line, or Area chart configuration within a Lens panel in the YAML schema."""

    type: Literal['bar', 'area', 'line'] = Field('bar', description="The type of XY chart to display. Defaults to 'bar'.")
    mode: Literal['stacked', 'unstacked', 'percentage'] = Field(
        'unstacked',
        description="The stacking mode for bar and area charts. Defaults to 'unstacked'.",
    )
    x_axis_column: str = Field(..., description='The field name from the ESQL query result to use for the x-axis.')
    y_axis_columns: list[str] = Field(..., description='A list of field names from the ESQL query result to use as accessors (y-axis).')
    split_column: str | None = Field(
        default=None,
        description='An optional field name from the ESQL query result to use for splitting the series.',
    )


class LensBarChartAppearance(BaseLensChartAppearance):
    """Represents bar chart appearance formatting options for Lens charts in the YAML schema."""

    min_bar_height: float | None = Field(default=None, description='The minimum height for bars in bar charts.')


class LensLineChartAppearance(BaseLensChartAppearance):
    """Represents line chart appearance formatting options for Lens charts in the YAML schema."""

    fitting_function: Literal['Linear'] | None = Field(default=None, description='The fitting function to apply to line/area charts.')
    emphasize_fitting: bool | None = Field(default=None, description='If `true`, emphasize the fitting function line. Defaults to `false`.')
    curve_type: Literal['linear', 'cardinal', 'catmull-rom', 'natural', 'step', 'step-after', 'step-before', 'monotone-x'] | None = Field(
        default=None,
        description='The curve type for line/area charts.',
    )


class LensAreaChartAppearance(LensLineChartAppearance):
    """Represents area chart appearance formatting options for Lens charts in the YAML schema."""

    fill_opacity: float | None = Field(default=None, description='The fill opacity for area charts (0.0 to 1.0).')
