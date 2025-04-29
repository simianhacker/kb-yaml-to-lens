from typing import Literal

from pydantic import BaseModel, Field, model_validator

from dashboard_compiler.models.config.panels.lens_charts.base import (
    BaseLensAxisFormat,
    BaseLensChart,
    LensAppearanceFormat,
    LensLegendFormat,
)
from dashboard_compiler.models.config.panels.lens_charts.components.dimension import Dimension
from dashboard_compiler.models.config.panels.lens_charts.components.metric import Metric


class LensBottomAxisFormat(BaseLensAxisFormat):
    """
    Represents formatting options for the bottom axis of an XY chart.
    """

    show_current_time_marker: bool | None = Field(
        None, description="If `true`, show a marker on the bottom axis indicating the current time. Defaults to `false`."
    )


class LensLeftAxisFormat(BaseLensAxisFormat):
    """
    Represents formatting options for the left axis of an XY chart.
    """

    pass


class LensRightAxisFormat(BaseLensAxisFormat):
    """
    Represents formatting options for the right axis of an XY chart.
    """

    metrics: list[Metric] = Field(
        default_factory=list,
        description="A list of metric configurations to be displayed on the right axis. Defaults to an empty list."
    )


class LensAxisFormat(BaseModel):
    """
    Groups formatting options for the axes of an XY chart.
    """

    bottom: LensBottomAxisFormat = Field(
        default_factory=LensBottomAxisFormat, description="Formatting options for the bottom axis."
    )
    left: LensLeftAxisFormat = Field(
        default_factory=LensLeftAxisFormat, description="Formatting options for the left axis."
    )
    right: LensRightAxisFormat | None = Field(
        None, description="Formatting options for the right axis (optional)."
    )


class LensXYChart(BaseLensChart):
    """
    Represents a Bar, Line, or Area chart configuration within a Lens panel in the YAML schema.
    """

    type: Literal["bar", "area", "line"] = Field(
        "bar", description="The type of XY chart to display. Defaults to 'bar'."
    )
    mode: Literal["stacked", "unstacked", "percentage"] = Field(
        "unstacked", description="The stacking mode for bar and area charts. Defaults to 'unstacked'."
    )
    dimensions: list[Dimension] = Field(
        ...,
        description="Defines the dimensions (typically the x-axis or split/breakdown) for the chart.",
        min_length=1
    )
    metrics: list[Metric] = Field(
        ...,
        description="Defines the metrics (typically the y-axis values) for the chart.",
        min_length=1
    )

    axis: LensAxisFormat = Field(
        default_factory=LensAxisFormat, description="Formatting options for the chart's axes."
    )
    legend: LensLegendFormat = Field(
        default_factory=LensLegendFormat, description="Formatting options for the chart's legend."
    )
    appearance: LensAppearanceFormat = Field(
        default_factory=LensAppearanceFormat, description="Appearance options for the chart."
    )

    @model_validator(mode="after")
    def check_mode_for_chart_type(self) -> "LensXYChart":
        """
        Validates that the 'mode' field is only used for 'bar' or 'area' chart types.
        """
        if self.mode is not None and self.type not in ["bar", "area"]:
           raise ValueError("Mode can only be specified for 'bar' or 'area' chart types.")
        return self

    def add_dimension(self, dimension: Dimension) -> None:
        """
        Adds a dimension to the chart's dimensions list.

        Args:
            dimension (Dimension): The dimension object to add.
        """
        self.dimensions.append(dimension)

    def add_metric(self, metric: Metric) -> None:
        """
        Adds a metric to the chart's metrics list.

        Args:
            metric (Metric): The metric object to add.
        """
        self.metrics.append(metric)
