"""Configuration schema for controls used in a dashboard."""

from typing import Literal

from pydantic import Field

from dashboard_compiler.shared.config import BaseCfgModel, Sort

type ControlTypes = RangeSliderControl | OptionsListControl


class BaseControl(BaseCfgModel):
    """Base class for defining controls within the YAML schema.

    These controls are used to filter data or adjust visualization settings
    on a dashboard.
    """

    id: str | None = Field(default=None)
    'A unique identifier for the control. If not provided, one may be generated.'

    width: Literal['small', 'medium', 'large'] | None = Field(default=None)
    "The width of the control in the dashboard layout. If not set, defaults to 'medium'."

    label: str | None = Field(default=None)
    'The display label for the control. If not provided, a label may be inferred.'

    data_view: str = Field(...)
    'The ID or title of the data view (index pattern) the control operates on.'

    field: str = Field(...)
    'The name of the field within the data view that the control is associated with.'


class OptionsListControl(BaseControl):
    """Represents an Options List control in the YAML schema.

    This control allows users to select one or more values from a list
    to filter data.
    """

    type: Literal['options'] = 'options'

    search_technique: str | None = Field(default=None)
    "The search technique used for filtering options (e.g., 'prefix')."

    sort: Sort | None = Field(default=None)
    'Configuration for sorting the list of options.'


class RangeSliderControl(BaseControl):
    """Represents a Range Slider control in the YAML schema.

    This control allows users to select a range of numeric or date values
    to filter data.
    """

    type: Literal['slider'] = 'slider'

    step: int | float | None = Field(default=None)
    'The step value for the slider, defining the granularity of selections.'
