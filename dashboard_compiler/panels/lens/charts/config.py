from typing import TYPE_CHECKING, Literal
from warnings import deprecated

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from .datatable.config import ESQLDatatableChart, LensDatatableChart
    from .metric.config import ESQLMetricsChart, LensMetricsChart
    from .pie.config import ESQLPieChart, LensPieChart
    from .xy.config import ESQLXYChart, LensXYChart

type LensChartTypes = LensXYChart | LensPieChart | LensMetricsChart | LensDatatableChart

type ESQLChartTypes = ESQLXYChart | ESQLPieChart | ESQLMetricsChart | ESQLDatatableChart


class BaseLensChart(BaseModel):
    """Base model for defining chart objects within a Lens panel in the YAML schema.

    Specific chart types (e.g., XY, Pie, Metric, Datatable) inherit from this base class.
    """

    id: str | None = Field(
        default=None,
        description='A unique identifier for the chart. If not provided, one may be generated during compilation.',
    )


class BaseLensChartAppearance:
    """Base class for common appearance formatting options in the YAML schema.

    Specific chart appearance formats (e.g., LensAppearanceFormat) inherit from this base class.
    """

    hide_endzones: bool | None = Field(
        default=None,
        description='If `true`, hide the endzones for date_histogram axes. Defaults to `false`.',
    )
    value_labels: Literal['hide', 'show'] | None = Field(
        default=None,
        description='Controls the visibility of value labels on chart elements.',
    )


@deprecated('LensChartAppearanceFormat is deprecated, use Lens*AppearanceFormat instead.')
class LensAppearanceFormat(BaseModel):
    """Represents chart appearance formatting options for Lens charts in the YAML schema."""

    value_labels: Literal['hide', 'show'] | None = Field(
        default=None,
        description='Controls the visibility of value labels on chart elements.',
    )
    fitting_function: Literal['Linear'] | None = Field(default=None, description='The fitting function to apply to line/area charts.')
    emphasize_fitting: bool | None = Field(default=None, description='If `true`, emphasize the fitting function line. Defaults to `false`.')
    curve_type: Literal['linear', 'cardinal', 'catmull-rom', 'natural', 'step', 'step-after', 'step-before', 'monotone-x'] | None = Field(
        default=None,
        description='The curve type for line/area charts.',
    )
    fill_opacity: float | None = Field(default=None, description='The fill opacity for area charts (0.0 to 1.0).')
    min_bar_height: float | None = Field(default=None, description='The minimum height for bars in bar charts.')
    hide_endzones: bool | None = Field(
        default=None,
        description='If `true`, hide the endzones for date_histogram axes. Defaults to `false`.',
    )


class BaseLensAxisFormat(BaseModel):
    """Base model for common axis formatting options in the YAML schema.

    Specific axis formats (e.g., bottom, left, right) inherit from this base class.
    """

    title: str | None = Field(
        default=None,
        description='The title for the axis. If not provided, the title is auto-generated. Set to `null` to hide the title.',
    )
    scale: Literal['linear', 'log', 'square', 'sqrt'] | None = Field(default=None, description='The scale type for the axis.')
    gridlines: bool | None = Field(default=None, description='If `true`, show gridlines for this axis. Defaults to `false`.')
    tick_labels: bool | None = Field(default=None, description='If `true`, show tick labels for this axis. Defaults to `true`.')
    orientation: Literal['horizontal', 'vertical', 'rotated'] | None = Field(
        default=None,
        description='The orientation of the axis labels.',
    )
    min: float | Literal['auto'] | None = Field(
        default=None,
        description="The minimum value for the axis. Use 'auto' for automatic scaling.",
    )
    max: float | Literal['auto'] | None = Field(
        default=None,
        description="The maximum value for the axis. Use 'auto' for automatic scaling.",
    )


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


class LensAxisFormat(BaseModel):
    """Groups formatting options for the axes of an XY chart."""

    bottom: LensBottomAxisFormat = Field(default_factory=LensBottomAxisFormat, description='Formatting options for the bottom axis.')
    left: LensLeftAxisFormat = Field(default_factory=LensLeftAxisFormat, description='Formatting options for the left axis.')
    right: LensRightAxisFormat = Field(default_factory=LensRightAxisFormat, description='Formatting options for the right axis (optional).')


class LensLegendFormat(BaseModel):
    """Represents legend formatting options for Lens charts in the YAML schema."""

    is_visible: bool = Field(default=True, description='If `true`, the legend will be shown. Defaults to `true`.')
    position: Literal['right', 'left', 'top', 'bottom'] = Field(
        default='right',
        description="The position of the legend relative to the chart. Defaults to 'right'.",
    )


class LensLegendMixin(BaseModel):
    """Mixin for common legend formatting options in the YAML schema.

    This mixin can be used in various chart types to provide consistent legend formatting.
    """

    legend: LensLegendFormat = Field(default_factory=LensLegendFormat, description='Formatting options for the chart legend.')


class LensAppearanceMixin(BaseModel):
    """Mixin for common appearance formatting options in the YAML schema."""

    appearance: LensAppearanceFormat = Field(
        default_factory=LensAppearanceFormat,
        description='Formatting options for the chart appearance.',
    )
