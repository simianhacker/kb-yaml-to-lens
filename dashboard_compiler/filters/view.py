"""View models for filters in the Kibana JSON structure."""

from typing import Annotated, Any, Literal

from pydantic import ConfigDict, Field, model_serializer

from dashboard_compiler.shared.view import BaseVwModel, OmitIfNone

# The following is an example of the JSON structure that these models represent. Do not remove:
# {
#   "filter": [
#     {
#       "meta": {
#         "disabled": false,
#         "negate": false,
#         "alias": null,
#         "key": "aerospike.namespace",
#         "field": "aerospike.namespace",
#         "params": {
#           "query": "test"
#         },
#         "type": "phrase",
#         "indexRefName": "kibanaSavedObjectMeta.searchSourceJSON.filter[0].meta.index"
#       },
#       "query": {
#         "match_phrase": {
#           "aerospike.namespace": "test"
#         }
#       },
#       "$state": {
#         "store": "appState"
#       }
#     }
#   ]
# }


class KbnFilterMeta(BaseVwModel):
    """Represents the meta information of a filter in the Kibana JSON structure."""

    disabled: bool
    """Indicates whether the filter is disabled."""

    negate: bool
    """Indicates whether the filter is negated (i.e., it filters out the specified values)."""

    alias: str | None = None
    """An optional alias for the filter, used for display purposes."""

    key: str
    """The key of the filter, typically the field name being filtered on."""

    field: str
    """The field name being filtered on, same as `key` in most cases."""

    params: Annotated[dict[str, Any] | list[str] | None, OmitIfNone()] = Field(default=None)
    """Parameters for the filter, such as the value to match against."""

    type: str
    """The type of filter, e.g., 'combined', 'phrase', 'phrases', 'range', 'exists', etc."""

    relation: Annotated[Literal["AND","OR"] | None, OmitIfNone()] = Field(default=None)
    """The relation of the 'combined' filter, if applicable. Can be 'AND' or 'OR'."""

    index: Annotated[str | None, OmitIfNone()] = Field(default=None)
    """The data view / index associated with the filter, if applicable."""


class KbnFilterState(BaseVwModel):
    """Represents the $state of a filter."""

    store: str = Field(default='appState')


class KbnFilter(BaseVwModel):
    """Represents a filter object within state.filters in the Kibana JSON structure."""

    model_config = ConfigDict(serialize_by_alias=True)
    """Configuration for the model to serialize using aliases for the $state field."""

    state: KbnFilterState = Field(..., serialization_alias='$state')
    meta: KbnFilterMeta
    query: dict[str, Any]
