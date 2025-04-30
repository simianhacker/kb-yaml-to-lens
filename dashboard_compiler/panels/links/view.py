"""Types for Kibana Links panel in the dashboard compiler.

Reference: https://github.com/elastic/kibana/blob/main/src/platform/plugins/private/links/common/content_management/v1/types.ts
"""

from typing import Literal
from warnings import deprecated

from pydantic import Field

from dashboard_compiler.panels.view import KbnBasePanel, KbnBasePanelEmbeddableConfig
from dashboard_compiler.shared.view import BaseVwModel

# The following is an example of the JSON structure that these models represent. Do not remove:
# {                                                 <-- KbnLinksPanel
#     "type": "links",
#     "embeddableConfig": {                         <-- KbnLinksPanelEmbeddableConfig
#         "attributes": {                           <-- KbnLinksPanelAttributes
#             "layout": "horizontal",
#             "links": [                            <-- list[KbnLinkTypes]
#                 {
#                     "type": "dashboardLink",
#                     "id": "9f2896f6-9ca0-4f63-9960-631d5af3840c",
#                     "order": 0,
#                     "destinationRefName": "link_9f2896f6-9ca0-4f63-9960-631d5af3840c_dashboard"
#                 }
#             ]
#         },
#         "enhancements": {}
#     },
#     "panelIndex": "e19a731d-0163-490a-a691-0bd1b1264d0b",
#     "gridData": {
#         "i": "e19a731d-0163-490a-a691-0bd1b1264d0b",
#         "y": 0,
#         "x": 0,
#         "w": 48,
#         "h": 2
#     }
# }


class KbnBaseLink(BaseVwModel):
    id: str = Field(...)
    """The unique identifier for the link."""

    order: int = Field(...)
    """Order of the link in the list."""

    label: str | None = Field(default=None)
    """Friendly label for the link. Optional, can be used for display purposes."""


# Define nested models for Links panel embeddableConfig based on samples
@deprecated('KbnLink is deprecated, use KbnDashboardLink or KbnWebLink instead.')
class KbnLink(BaseVwModel):
    type: Literal['dashboardLink', 'externalLink']
    id: str
    """The unique identifier for the link."""

    destination: str | None = Field(default=None)
    """The destination URL for the link."""

    label: str | None = None
    """Friendly label for the link."""

    order: int
    """Order of the link in the list."""

    destinationRefName: str | None = None
    """Destination dashboard KbnReference name"""


type KbnLinkTypes = KbnDashboardLink | KbnWebLink


class KbnDashboardLink(KbnBaseLink):
    """Represents a link to a dashboard."""

    type: Literal['dashboardLink'] = 'dashboardLink'
    """Type of the link, specifically for dashboard links."""

    destinationRefName: str = Field(...)
    """Reference name for the destination dashboard."""


class KbnWebLink(KbnBaseLink):
    """Represents a link to an external web resource."""

    type: Literal['externalLink'] = 'externalLink'
    """Type of the link, specifically for web links."""

    destination: str = Field(...)
    """The URL to which the link points."""


class KbnLinksPanelAttributes(BaseVwModel):
    layout: Literal['horizontal', 'vertical']
    links: list[KbnLinkTypes] = Field(default_factory=list)


class KbnLinksPanelEmbeddableConfig(KbnBasePanelEmbeddableConfig):
    attributes: KbnLinksPanelAttributes


class KbnLinksPanel(KbnBasePanel):
    """Represents a Links panel in the Kibana Kbn structure."""

    type: Literal['links'] = 'links'
    embeddableConfig: KbnLinksPanelEmbeddableConfig
