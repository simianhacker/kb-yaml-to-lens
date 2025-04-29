from typing import Literal

from pydantic import BaseModel, Field

from dashboard_compiler.models.config.panels.base import BasePanel


class BaseLink(BaseModel):
    """
    Base class for defining link objects within a Links panel in the YAML schema.

    Specific link types (e.g., DashboardLink, UrlLink) inherit from this base class.
    """

    label: str | None = Field(
        None, description="The display text for the link. If not provided, a label may be inferred."
    )


class DashboardLink(BaseLink):
    """
    Represents a link to another dashboard or saved object within a Links panel.
    """

    dashboard: str = Field(
        ..., description="The ID of the target dashboard or saved object."
    )


class UrlLink(BaseLink):
    """
    Represents a link to an external URL within a Links panel.
    """

    url: str = Field(
        ..., description="The URL that the link points to."
    )


class LinksPanel(BasePanel):
    """
    Represents a Links panel configuration in the YAML schema.

    Links panels are used to display a collection of links to other dashboards,
    saved objects, or external URLs.
    """

    type: Literal["links"] = "links"
    layout: Literal["horizontal", "vertical"] = Field(
        "horizontal", description="The layout direction of the links within the panel. Defaults to 'horizontal'."
    )
    links: list[DashboardLink | UrlLink] = Field(
        ..., description="A list of link objects to be displayed in the panel."
    )

    def add_link(self, link: DashboardLink | UrlLink) -> None:
        """
        Adds a link object to the Links panel's links list.

        Args:
            link (DashboardLink | UrlLink): The link object to add.
        """
        self.links.append(link)
