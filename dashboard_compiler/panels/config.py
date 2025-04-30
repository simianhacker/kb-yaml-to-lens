"""Configuration for dashboard panels."""

from typing import TYPE_CHECKING
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    #from dashboard_compiler.panels.lens import LensPanel
    from dashboard_compiler.panels.links import LinksPanel
    from dashboard_compiler.panels.markdown import MarkdownPanel
    from dashboard_compiler.panels.search import SearchPanel

type PanelTypes = 'MarkdownPanel | SearchPanel | LinksPanel'  # | LensPanel  # noqa: TC008


class Grid(BaseModel):
    """Represents the grid layout configuration for a panel in the YAML schema.

    This determines the panel's position and size on the dashboard grid.
    """

    x: int = Field(..., description='The horizontal starting position of the panel on the grid (0-based).')
    y: int = Field(..., description='The vertical starting position of the panel on the grid (0-based).')
    w: int = Field(..., description='The width of the panel in grid units.')
    h: int = Field(..., description='The height of the panel in grid units.')


class BasePanel(BaseModel):
    """Base model for all panel types defined in the YAML schema.

    All specific panel types (e.g., Markdown, Search, Lens) inherit from this base class
    to include common configuration fields.
    """

    id: str | None = Field(
        default=None,
        description='A unique identifier for the panel. If not provided, one may be generated during compilation.',
    )
    title: str = Field('', description='The title displayed on the panel header. Can be an empty string.')
    hide_title: bool | None = Field(
        default=None,
        description='If `true`, the panel title will be hidden. Defaults to `false` (title is shown).',
    )
    description: str = Field('', description="A brief description of the panel's content or purpose. Defaults to an empty string.")
    # type: str = Field(..., description="The type of panel. This field is used to determine the specific panel implementation.")
    grid: Grid = Field(..., description="Defines the panel's position and size on the dashboard grid.")
