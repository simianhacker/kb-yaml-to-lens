"""Compile Control configurations into Kibana view models."""

from dashboard_compiler.controls import ControlTypes
from dashboard_compiler.controls.config import OptionsListControl, RangeSliderControl
from dashboard_compiler.controls.view import (
    KBN_DEFAULT_CONTROL_WIDTH,
    KBN_DEFAULT_SEARCH_TECHNIQUE,
    KbnControlGroupInput,
    KbnControlPanelsJson,
    KbnControlSort,
    KbnControlTypes,
    KbnIgnoreParentSettingsJson,
    KbnOptionsListControl,
    KbnOptionsListControlExplicitInput,
    KbnRangeSliderControl,
    KbnRangeSliderControlExplicitInput,
)
from dashboard_compiler.shared import stable_id_generator


def compile_options_list_control(order: int, control: OptionsListControl) -> KbnOptionsListControl:
    """Compile an OptionsListControl into its Kibana view model representation.

    Args:
        order (int): The order of the control in the dashboard.
        control (OptionsListControl): The OptionsListControl object to compile.

    Returns:
        KbnOptionsListControl: The compiled Kibana options list control view model.

    """
    return KbnOptionsListControl(
        grow=True,
        order=order,
        width=control.width or KBN_DEFAULT_CONTROL_WIDTH,
        explicitInput=KbnOptionsListControlExplicitInput(
            dataViewId=control.data_view,
            fieldName=control.field,
            title=control.label,
            searchTechnique=control.search_technique or KBN_DEFAULT_SEARCH_TECHNIQUE,
            selectedOptions=[],
            sort=KbnControlSort(by=control.sort.by, direction=control.sort.direction) if control.sort else None,
        ),
    )


def compile_range_slider_control(order: int, control: RangeSliderControl) -> KbnRangeSliderControl:
    """Compile a RangeSliderControl into its Kibana view model representation.

    Args:
        order (int): The order of the control in the dashboard.
        control (RangeSliderControl): The RangeSliderControl object to compile.

    Returns:
        KbnRangeSliderControl: The compiled Kibana range slider control view model.

    """
    return KbnRangeSliderControl(
        grow=True,
        order=order,
        width=control.width or 'medium',
        explicitInput=KbnRangeSliderControlExplicitInput(
            dataViewId=control.data_view,
            fieldName=control.field,
            step=control.step,
            title=control.label,
        ),
    )


def compile_control(order: int, control: ControlTypes) -> KbnControlTypes:
    """Compile a single control into its Kibana view model representation.

    Args:
        order (int): The order of the control in the dashboard.
        control (ControlTypes): The control object to compile.

    Returns:
        KbnControlTypes: The compiled Kibana control view model.

    """
    if isinstance(control, OptionsListControl):
        return compile_options_list_control(order, control)

    return compile_range_slider_control(order, control)


def compile_controls(controls: list[ControlTypes]) -> KbnControlGroupInput:
    """Compile the control group input for a Dashboard object into its Kibana view model representation.

    Args:
        controls (list[ControlTypes]): The list of control objects to compile.

    Returns:
        KbnControlGroupInput: The compiled Kibana control group input view model.

    """
    kbn_control_panels_json: KbnControlPanelsJson = KbnControlPanelsJson()

    for i, config_control in enumerate(controls):
        kbn_control_id = config_control.id or stable_id_generator(
            [config_control.type, config_control.label, config_control.data_view, config_control.field],
        )

        kbn_control_panels_json.add(kbn_control_id, compile_control(i, config_control))

    return KbnControlGroupInput(
        chainingSystem='HIERARCHICAL',
        controlStyle='oneLine',
        ignoreParentSettingsJSON=KbnIgnoreParentSettingsJson(),
        panelsJSON=kbn_control_panels_json,
        showApplySelections=False,
    )
