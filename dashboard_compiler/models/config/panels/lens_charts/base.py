from typing import Literal

from pydantic import BaseModel, Field


class BaseLensChart(BaseModel):
    """
    Base model for defining chart objects within a Lens panel in the YAML schema.

    Specific chart types (e.g., XY, Pie, Metric, Datatable) inherit from this base class.
    """

    id: str | None = Field(
        default=None,
        description="A unique identifier for the chart. If not provided, one may be generated during compilation."
    )
    type: Literal["bar", "pie", "area", "line", "metric", "datatable"] = Field(
        ..., description="The type of visualization to display in the Lens panel."
    )


class BaseLensAxisFormat(BaseModel):
    """
    Base model for common axis formatting options in the YAML schema.

    Specific axis formats (e.g., bottom, left, right) inherit from this base class.
    """

    title: str | None = Field(
        None,
        description="The title for the axis. If not provided, the title is auto-generated. Set to `null` to hide the title."
    )
    scale: Literal["linear", "log", "square", "sqrt"] | None = Field(
        None, description="The scale type for the axis."
    )
    gridlines: bool | None = Field(
        None, description="If `true`, show gridlines for this axis. Defaults to `false`."
    )
    tick_labels: bool | None = Field(
        None, description="If `true`, show tick labels for this axis. Defaults to `true`."
    )
    orientation: Literal["horizontal", "vertical", "rotated"] | None = Field(
        None, description="The orientation of the axis labels."
    )
    min: float | Literal["auto"] | None = Field(
        None, description="The minimum value for the axis. Use 'auto' for automatic scaling."
    )
    max: float | Literal["auto"] | None = Field(
        None, description="The maximum value for the axis. Use 'auto' for automatic scaling."
    )


class LensLegendFormat(BaseModel):
    """
    Represents legend formatting options for Lens charts in the YAML schema.
    """

    is_visible: bool = Field(
        True, description="If `true`, the legend will be shown. Defaults to `true`."
    )
    position: Literal["right", "left", "top", "bottom"] = Field(
        "right", description="The position of the legend relative to the chart. Defaults to 'right'."
    )


class LensAppearanceFormat(BaseModel):
    """
    Represents chart appearance formatting options for Lens charts in the YAML schema.
    """

    value_labels: Literal["hide", "show"] | None = Field(
        None, description="Controls the visibility of value labels on chart elements."
    )
    fitting_function: Literal["Linear"] | None = Field(
        None, description="The fitting function to apply to line/area charts."
    )
    emphasize_fitting: bool | None = Field(
        None, description="If `true`, emphasize the fitting function line. Defaults to `false`."
    )
    curve_type: Literal["linear", "cardinal", "catmull-rom", "natural", "step", "step-after", "step-before", "monotone-x"] | None = Field(
        None, description="The curve type for line/area charts."
    )
    fill_opacity: float | None = Field(
        None, description="The fill opacity for area charts (0.0 to 1.0)."
    )
    min_bar_height: float | None = Field(
        None, description="The minimum height for bars in bar charts."
    )
    hide_endzones: bool | None = Field(
        None, description="If `true`, hide the endzones for date_histogram axes. Defaults to `false`."
    )
