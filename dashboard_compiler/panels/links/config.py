"""Configuration for Links Panel."""
from typing import Literal, Self

from pydantic import Field

from dashboard_compiler.panels.config import BasePanel
from dashboard_compiler.shared.config import BaseCfgModel


class BaseLink(BaseCfgModel):
    """Base class for defining link objects within a Links panel in the YAML schema.

    Specific link types (e.g., DashboardLink, UrlLink) inherit from this base class.
    """

    label: str | None = Field(default=None, description='The display text for the link. If not provided, a label may be inferred.')


type LinkTypes = DashboardLink | UrlLink


class DashboardLink(BaseLink):
    """Represents a link to another dashboard or saved object within a Links panel."""

    dashboard: str = Field(..., description='The ID of the target dashboard or saved object.')


class UrlLink(BaseLink):
    """Represents a link to an external URL within a Links panel."""

    url: str = Field(..., description='The URL that the link points to.')


class LinksPanel(BasePanel):
    """Represents a Links panel configuration in the YAML schema.

    Links panels are used to display a collection of links to other dashboards,
    saved objects, or external URLs.
    """

    type: Literal['links'] = 'links'

    layout: Literal['horizontal', 'vertical'] = Field(default='horizontal')
    """The layout of the links in the panel, either 'horizontal' or 'vertical'. Defaults to 'horizontal' if not set."""

    links: list[LinkTypes] = Field(...)
    """A list of link objects to be displayed in the panel."""

    def add_link(self, link: LinkTypes) -> Self:
        """Add a link object to the Links panel's links list.

        Args:
            link (LinkTypes): The link object to add.

        Returns:
            Self: The current instance of the LinksPanel for method chaining.

        """
        self.links.append(link)
        return self
