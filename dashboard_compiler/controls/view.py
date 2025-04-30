"""View models for Kibana controls used in dashboards."""

from typing import Any

from pydantic import BaseModel, Field, model_serializer

from dashboard_compiler.shared.view import RootDict

# The following is an example of the JSON structure that these models represent. Do not remove:
# "controlGroupInput": {                                <-- KbnControlGroupInput
#     "chainingSystem": "HIERARCHICAL",
#     "controlStyle": "oneLine",
#     "ignoreParentSettingsJSON": {
#         "ignoreFilters": false,
#         "ignoreQuery": false,
#         "ignoreTimerange": false,
#         "ignoreValidations": false
#     },
#     "panelsJSON": {                                   <-- KbnControlPanelsJson -- this needs to end up as stringified JSON
#         "0086b299-caf9-4d42-a574-31eec9226a48": {     <-- KbnOptionsListControl
#             "grow": false,
#             "order": 0,
#             "type": "optionsListControl",
#             "width": "medium",
#             "explicitInput": {                        <-- KbnOptionsListControlExplicitInput
#                 "dataViewId": "metrics-*",
#                 "fieldName": "host.architecture",
#                 "searchTechnique": "prefix",
#                 "selectedOptions": [],
#                 "sort": {                             <-- KbnControlSort
#                     "by": "_count",
#                     "direction": "desc"
#                 }
#             }
#         },
#         "4094a542-c799-47ba-9d20-e1ad557924f6": {     <-- KbnRangeSliderControl
#             "grow": false,
#             "order": 1,
#             "type": "rangeSliderControl",
#             "width": "medium",
#             "explicitInput": {                        <-- KbnRangeSliderControlExplicitInput
#                 "dataViewId": "metrics-*",
#                 "fieldName": "severity_number",
#                 "step": 1
#             }
#         }
#     },
#     "showApplySelections": false
# },

KBN_DEFAULT_CONTROL_WIDTH = 'medium'
KBN_DEFAULT_SEARCH_TECHNIQUE = 'prefix'


class KbnControlSort(BaseModel):
    """Sorting configuration for options in a control."""

    by: str
    direction: str


class KbnBaseControlExplicitInput(BaseModel):
    """Base class for the `explicitInput` part of Kbn controls."""

    dataViewId: str
    fieldName: str
    title: str | None = None


class KbnOptionsListControlExplicitInput(KbnBaseControlExplicitInput):
    """Explicit input for options list controls."""

    searchTechnique: str
    selectedOptions: list[Any] = Field(default_factory=list)
    sort: KbnControlSort | None = None


class KbnRangeSliderControlExplicitInput(KbnBaseControlExplicitInput):
    """Explicit input for range slider controls."""

    step: int | float | None


class KbnBaseControl(BaseModel):
    """Base class for Kibana controls."""

    grow: bool
    order: int
    width: str


class KbnRangeSliderControl(KbnBaseControl):
    """Range slider control for a Kibana Dashboard."""

    type: str = 'rangeSliderControl'
    explicitInput: KbnRangeSliderControlExplicitInput


class KbnOptionsListControl(KbnBaseControl):
    """Options list control for a Kibana Dashboard."""

    type: str = 'optionsListControl'
    explicitInput: KbnOptionsListControlExplicitInput


class KbnIgnoreParentSettingsJson(BaseModel):
    """Settings that control whether to ignore inherited values from the dashboard."""

    ignoreFilters: bool = False
    ignoreQuery: bool = False
    ignoreTimerange: bool = False
    ignoreValidations: bool = False

    @model_serializer(when_used='always')
    def stringify(self) -> str:
        """Kibana wants this field to be stringified JSON.

        Returns:
            str: The JSON string representation of the ignore settings.

        """
        return self.model_dump_json()


type KbnControlTypes = KbnRangeSliderControl | KbnOptionsListControl


class KbnControlPanelsJson(RootDict[KbnControlTypes]):
    """A dictionary mapping control IDs to their respective control configurations."""

    @model_serializer(when_used='always')
    def stringify(self) -> str:
        """Kibana wants this field to be stringified JSON.

        Returns:
            str: The JSON string representation of the control panels.

        """
        return self.model_dump_json()


class KbnControlGroupInput(BaseModel):
    """Definition for the Controls part of a Kibana Dashboard."""

    chainingSystem: str
    controlStyle: str
    ignoreParentSettingsJSON: KbnIgnoreParentSettingsJson
    panelsJSON: KbnControlPanelsJson
    showApplySelections: bool
