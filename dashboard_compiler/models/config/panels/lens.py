from typing import Literal

from pydantic import Field

from dashboard_compiler.models.config.panels.base import BasePanel
from dashboard_compiler.models.config.panels.lens_charts.datatable import LensDatatableChart
from dashboard_compiler.models.config.panels.lens_charts.metrics import LensMetricsChart
from dashboard_compiler.models.config.panels.lens_charts.pie import LensPieChart
from dashboard_compiler.models.config.panels.lens_charts.xy import LensXYChart
from dashboard_compiler.models.config.shared import BaseFilter


class LensPanel(BasePanel):
    """
    Represents a Lens panel configuration in the YAML schema.

    Lens panels are used to display various types of visualizations
    (e.g., bar charts, pie charts, metrics, data tables) based on data
    from a specified index pattern.
    """

    type: Literal["lens"] = "lens"

    chart: LensXYChart | LensPieChart | LensMetricsChart | LensDatatableChart = Field(
        ..., description="The nested chart definition for the Lens visualization."
    )
    index_pattern: str = Field(
        ..., description="The ID or title of the index pattern used by the Lens visualization."
    )
    query: str = Field(
        "", description="A panel-specific KQL query to filter data for this visualization. Defaults to an empty string."
    )
    filters: list[BaseFilter] = Field(
        default_factory=list,
        description="A list of panel-specific filters applied to this visualization. Defaults to an empty list."
    )

    def add_filter(self, filter: BaseFilter) -> None:
        """
        Adds a filter to the Lens panel's filters list.

        Args:
            filter (BaseFilter): The filter object to add.
        """
        self.filters.append(filter)
