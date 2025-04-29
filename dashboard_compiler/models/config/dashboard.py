from pydantic import BaseModel, Field

from dashboard_compiler.models.config.controls import OptionsListControl, RangeSliderControl
from dashboard_compiler.models.config.panels import LensPanel, LinksPanel, MarkdownPanel, SearchPanel
from dashboard_compiler.models.config.shared import ExistsFilter, KqlQuery, LuceneQuery, PhraseFilter, PhrasesFilter, RangeFilter


class Dashboard(BaseModel):
    """
    Represents the top-level dashboard configuration in the YAML schema.

    This model defines the structure for an entire dashboard, including its
    metadata, global query and filters, controls, and the list of panels
    it contains.
    """

    id: str | None = Field(
        default=None,
        description="A unique identifier for the dashboard. If not provided, one may be generated during compilation."
    )
    title: str = Field(
        ..., description="The title of the dashboard, displayed at the top of the page."
    )
    description: str = Field(
        "", description="A brief description of the dashboard's purpose or content. Defaults to an empty string."
    )

    query: KqlQuery | LuceneQuery = Field(
        default_factory=KqlQuery,
        description="A global query string (KQL or Lucene) applied to all panels on the dashboard unless overridden at the panel level. Defaults to an empty KQL query."
    )

    filters: list[ExistsFilter | PhraseFilter | PhrasesFilter | RangeFilter] = Field(
        default_factory=list,
        description="A list of global filters applied to all panels on the dashboard unless overridden at the panel level. Can be empty."
    )

    controls: list[RangeSliderControl | OptionsListControl] = Field(
        default_factory=list,
        description="A list of control panel configurations for the dashboard. These controls can interact with dashboard filters or queries. Can be empty."
    )

    panels: list[MarkdownPanel | SearchPanel | LinksPanel | LensPanel] = Field(
        default_factory=list,
        description="A list of panel objects defining the content and layout of the dashboard. This field is required but the list can be empty."
    )

    def add_filter(self, filter: ExistsFilter | PhraseFilter | PhrasesFilter | RangeFilter) -> None:
        """
        Adds a filter to the dashboard's global filters list.

        Args:
            filter (ExistsFilter | PhraseFilter | PhrasesFilter | RangeFilter): The filter object to add.
        """
        self.filters.append(filter)

    def add_control(self, control: RangeSliderControl | OptionsListControl) -> None:
        """
        Adds a control panel configuration to the dashboard's controls list.

        Args:
            control (RangeSliderControl | OptionsListControl): The control object to add.
        """
        self.controls.append(control)

    def add_panel(self, panel: MarkdownPanel | SearchPanel | LinksPanel | LensPanel) -> None:
        """
        Adds a panel object to the dashboard's panels list.

        Args:
            panel (MarkdownPanel | SearchPanel | LinksPanel | LensPanel): The panel object to add.
        """
        self.panels.append(panel)
