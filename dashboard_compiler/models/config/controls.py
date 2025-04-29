from typing import Literal

from pydantic import BaseModel, Field

from dashboard_compiler.models.config.shared import Sort


class BaseControl(BaseModel):
    """
    Base class for defining controls within the YAML schema.

    These controls are used to filter data or adjust visualization settings
    on a dashboard.
    """

    id: str | None = Field(
        default=None,
        description="A unique identifier for the control. If not provided, one may be generated."
    )
    type: Literal["optionsList", "rangeSlider"] = Field(
        ..., description="The type of control to display. Must be either 'optionsList' or 'rangeSlider'."
    )
    width: Literal["small", "medium", "large"] = Field(
        "medium", description="The width of the control in the dashboard layout. Defaults to 'medium'."
    )
    label: str | None = Field(
        None, description="The display label for the control. If not provided, a label may be inferred."
    )
    data_view: str = Field(
        ..., description="The ID or title of the data view (index pattern) the control operates on."
    )
    field: str = Field(
        ..., description="The name of the field within the data view that the control is associated with."
    )


class OptionsListControl(BaseControl):
    """
    Represents an Options List control in the YAML schema.

    This control allows users to select one or more values from a list
    to filter data.
    """

    type: Literal["optionsList"] = "optionsList"
    search_technique: str | None = Field(
        None, description="The search technique used for filtering options (e.g., 'prefix')."
    )
    sort: Sort | None = Field(
        None, description="Configuration for sorting the list of options."
    )


class RangeSliderControl(BaseControl):
    """
    Represents a Range Slider control in the YAML schema.

    This control allows users to select a range of numeric or date values
    to filter data.
    """

    type: Literal["rangeSlider"] = "rangeSlider"
    step: int | float | None = Field(
        None, description="The step value for the slider, defining the granularity of selections."
    )
