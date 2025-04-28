from typing import Literal

from pydantic import BaseModel, Field


class BaseLensChart(BaseModel):
    """Base model for the 'chart' object within a Lens panel in the YAML schema."""

    id: str | None = Field(default=None, description="(Optional) Unique identifier for the chart.")
    type: Literal["bar", "pie", "area", "line"] = Field(
        ..., description="(Required) Visualization type (e.g., 'pie', 'bar_stacked')."
    )  # Added area and line


class BaseLensAxisFormat(BaseModel):
    """Base model for common axis formatting options in the YAML schema."""

    title: str | None = Field(None, description="Axis title. If not provided, title is auto-generated. Set to null to hide title.")
    scale: Literal["linear", "log", "square", "sqrt"] | None = Field(None, description="Axis scale type.")
    gridlines: bool | None = Field(None, description="Show gridlines for this axis.")
    tick_labels: bool | None = Field(None, description="Show tick labels for this axis.")
    orientation: Literal["horizontal", "vertical", "rotated"] | None = Field(None, description="Axis label orientation.")
    min: float | Literal["auto"] | None = Field(None, description="Minimum value for the axis.")  # Added min
    max: float | Literal["auto"] | None = Field(None, description="Maximum value for the axis.")  # Added max


class LensLegendFormat(BaseModel):
    """Model for legend formatting options in the YAML schema."""

    is_visible: bool = Field(True, description="Show legend.")
    position: Literal["right", "left", "top", "bottom"] = Field("right", description="Legend position.")


class LensAppearanceFormat(BaseModel):
    """Model for chart appearance formatting options in the YAML schema."""

    value_labels: Literal["hide", "show"] | None = Field(None, description="Show value labels on chart elements.")
    fitting_function: Literal["Linear"] | None = Field(None, description="Fitting function for line/area charts.")
    emphasize_fitting: bool | None = Field(None, description="Emphasize the fitting function.")  # Added emphasize_fitting
    curve_type: Literal["linear", "cardinal", "catmull-rom", "natural", "step", "step-after", "step-before", "monotone-x"] | None = Field(
        None, description="Curve type for line/area charts."
    )  # Added curve_type
    fill_opacity: float | None = Field(None, description="Fill opacity for area charts.")  # Added fill_opacity
    min_bar_height: float | None = Field(None, description="Minimum bar height for bar charts.")  # Added min_bar_height
    hide_endzones: bool | None = Field(None, description="Hide endzones for date_histogram.")  # Added hide_endzones
