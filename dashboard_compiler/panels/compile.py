"""Compile Dashboard Panels to Kibana View Models."""

from dashboard_compiler.panels import LinksPanel, MarkdownPanel, PanelTypes #,  ESQLPanel, LensPanel
#from dashboard_compiler.panels.lens.compile import compile_esql_panel, compile_lens_panel
from dashboard_compiler.panels.links.compile import compile_links_panel
from dashboard_compiler.panels.markdown.compile import compile_markdown_panel
from dashboard_compiler.panels.search.config import SearchPanel
from dashboard_compiler.panels.view import KbnBasePanel, KbnPanelTypes
from dashboard_compiler.shared.view import KbnReference


def convert_to_panel_reference(kbn_reference: KbnReference, panel_index: str) -> KbnReference:
    """Convert a KbnReference object to a panel reference.

    Args:
        kbn_reference (KbnReference): The KbnReference object to convert.
        panel_index (str): The index (id) of the panel to which the reference belongs.

    Returns:
        KbnReference: The converted panel reference.

    """
    return KbnReference(
        type=kbn_reference.type,
        id=kbn_reference.id,
        name=panel_index + ':' + kbn_reference.name,
    )


def compile_dashboard_panel(panel: PanelTypes) -> tuple[list[KbnReference], KbnPanelTypes]:
    """Compile a single panel into its Kibana view model representation.

    Args:
        panel (PanelTypes): The panel object to compile.

    Returns:
        tuple: A tuple containing the compiled references and the Kibana panel view model.

    """
    if isinstance(panel, MarkdownPanel):
        return [], compile_markdown_panel(panel)

    # if isinstance(panel, LensPanel):
    #     return compile_lens_panel(panel)

    # if isinstance(panel, ESQLPanel):
    #     return compile_esql_panel(panel)

    if isinstance(panel, SearchPanel):
        msg = 'SearchPanel compilation is not implemented yet.'
        raise NotImplementedError(msg)

    return compile_links_panel(panel)


def compile_dashboard_panels(panels: list[PanelTypes]) -> tuple[list[KbnReference], list[KbnBasePanel]]:
    """Compile the panels of a Dashboard object into their Kibana view model representation.

    Args:
        panels (list): The list of panel objects to compile.

    Returns:
        list: The compiled list of Kibana panel view models.

    """
    kbn_panels: list[KbnBasePanel] = []
    kbn_references: list[KbnReference] = []

    for panel in panels:
        new_references: list[KbnReference] = []
        new_panel: KbnBasePanel

        if isinstance(panel, MarkdownPanel):
            new_panel = compile_markdown_panel(panel)

        # elif isinstance(panel, LensPanel):
        #     new_references, new_panel = compile_lens_panel(panel)

        # elif isinstance(panel, ESQLPanel):
        #     new_references, new_panel = compile_esql_panel(panel)

        elif isinstance(panel, LinksPanel):
            new_references, new_panel = compile_links_panel(panel)

        elif isinstance(panel, SearchPanel):
            msg = 'SearchPanel compilation is not implemented yet.'
            raise NotImplementedError(msg)

        else:
            msg = f'Panel type {type(panel)} is not supported in the dashboard compilation.'
            raise NotImplementedError(msg)

        kbn_panels.append(new_panel)

        kbn_references.extend([convert_to_panel_reference(ref, new_panel.panelIndex) for ref in new_references])

    return kbn_references, kbn_panels
