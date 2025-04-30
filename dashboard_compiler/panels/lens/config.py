"""Config model for Lens and ES|QL panels."""

from typing import Literal, Self

from pydantic import Field

from dashboard_compiler.filters.config import BaseFilter
from dashboard_compiler.panels.config import BasePanel
from dashboard_compiler.panels.lens.charts.config import ESQLChartTypes, LensChartTypes


class LensBasePanel(BasePanel):
    """Base class for Lens and ESQL panels in the YAML schema."""


class LensPanel(LensBasePanel):
    """Represents a Lens panel configuration in the YAML schema.

    Lens panels are used to display various types of visualizations
    (e.g., bar charts, pie charts, metrics, data tables) based on data
    from a specified index pattern.
    """

    type: Literal['lens'] = 'lens'

    chart: LensChartTypes = Field(...)
    """The nested chart definition for the Lens visualization."""

    data_view: str = Field(...)
    """The ID or title of the index pattern used by the Lens visualization."""

    query: str = Field('')
    """A panel-specific KQL query to filter data for this visualization. Defaults to an empty string."""

    filters: list[BaseFilter] = Field(default_factory=list)
    """A list of panel-specific filters applied to this visualization. Defaults to an empty list."""

    def add_filter(self, filter: BaseFilter) -> Self:  # noqa: A002
        """Add a filter to the Lens panel's filters list.

        Args:
            filter (BaseFilter): The filter object to add.

        Returns:
            Self: The current instance of the LensPanel for method chaining.

        """
        self.filters.append(filter)

        return self


class ESQLPanel(LensBasePanel):
    """Represents an ES|QL based Lens panel configuration in the YAML schema."""

    type: Literal['esql'] = 'esql'

    chart: ESQLChartTypes = Field(...)
    """The nested chart definition for the ES|QL Lens visualization."""

    esql: str = Field(...)
    """The ES|QL query for the Lens visualization."""
