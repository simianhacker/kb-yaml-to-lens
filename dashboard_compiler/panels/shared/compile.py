"""Helpers for compiling panels."""

from dashboard_compiler.panels.config import PanelTypes
from dashboard_compiler.panels.view import KbnGridData
from dashboard_compiler.shared.config import stable_id_generator


def compile_panel_shared(panel: PanelTypes) -> tuple[str, KbnGridData]:
    """Compile shared properties of a panel into its Kibana view model representation.

    Args:
        panel (LensPanel | ESQLPanel): The panel object to compile.

    Returns:
        tuple[str, KbnGridData]: A tuple containing the panel index and the grid data.

    """
    panel_index = panel.id or stable_id_generator([panel.type, panel.title, str(panel.grid)])

    grid_data = KbnGridData(x=panel.grid.x, y=panel.grid.y, w=panel.grid.w, h=panel.grid.h, i=panel_index)

    return panel_index, grid_data
