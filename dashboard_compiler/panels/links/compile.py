"""Compile links for a dashboard into their Kibana view models."""

from dashboard_compiler.panels.links.config import BaseLink, DashboardLink, LinksPanel, LinkTypes, UrlLink
from dashboard_compiler.panels.links.view import (
    KbnDashboardLink,
    KbnLinksPanel,
    KbnLinksPanelAttributes,
    KbnLinksPanelEmbeddableConfig,
    KbnLinkTypes,
    KbnWebLink,
)
from dashboard_compiler.panels.shared.compile import compile_panel_shared
from dashboard_compiler.shared.config import stable_id_generator
from dashboard_compiler.shared.view import KbnReference


def compile_dashboard_link(order: int, link: DashboardLink) -> tuple[KbnReference, KbnDashboardLink]:
    """Compile a DashboardLink into its Kibana view model representation.

    Args:
        order (int): The order of the link in the list.
        link (DashboardLink): The DashboardLink object to convert.

    Returns:
        Tuple[KbnReference, KbnDashboardLink]: A tuple containing the KbnReference and KbnDashboardLink objects.

    """
    link_id = stable_id_generator([link.label, str(order)])

    link_ref_id = f'link_{link_id}_dashboard'

    kbn_link = KbnDashboardLink(
        id=link_id,
        label=link.label,
        order=order,
        destinationRefName=link_ref_id,
    )

    # The id of the reference is supposed to be the target dashboard id,
    # the name of the reference is the link id
    kbn_reference = KbnReference(
        type='dashboard',
        id=link.dashboard,
        name=link_ref_id,
    )

    return kbn_reference, kbn_link


def compile_url_link(order: int, link: UrlLink) -> KbnWebLink:
    """Compile a UrlLink into its Kibana view model representation.

    Args:
        order (int): The order of the link in the list.
        link (UrlLink): The UrlLink object to convert.

    Returns:
        KbnWebLink: The compiled KbnWebLink object.

    """
    link_id = stable_id_generator([link.label, str(order)])

    return KbnWebLink(
        destination=link.url,
        id=link_id,
        label=link.label,
        order=order,
    )


def compile_link(link: BaseLink, order: int) -> tuple[KbnReference | None, KbnLinkTypes]:
    """Compile a single link into its Kibana view model representation.

    Args:
        link (BaseLink): The link object to compile.
        order (int): The order of the link in the list.

    Returns:
        KbnLinkTypes: The compiled Kibana link view model.

    """
    if isinstance(link, DashboardLink):
        return compile_dashboard_link(order, link)

    if isinstance(link, UrlLink):
        return None, compile_url_link(order, link)

    msg = f'Link type {type(link)} is not supported for compilation.'
    raise NotImplementedError(msg)


def compile_links(links: list[LinkTypes]) -> tuple[list[KbnReference], list[KbnLinkTypes]]:
    """Convert a list of KbnLink objects to a list of KbnReference objects.

    Args:
        links (list[KbnLink]): The list of KbnLink objects to convert.
        panel_index (str): The index of the panel to which these links belong.

    Returns:
        list[KbnReference]: The converted list of KbnReference objects.

    """
    kbn_references = []
    kbn_links = []
    for i, link in enumerate(links):
        kbn_reference, kbn_link = compile_link(link, i)

        if kbn_reference:
            kbn_references.append(kbn_reference)

        kbn_links.append(kbn_link)

    return kbn_references, kbn_links


def compile_links_panel(panel: LinksPanel) -> tuple[list[KbnReference], KbnLinksPanel]:
    """Compile a LinksPanel into its Kibana view model representation.

    Args:
        panel (LinksPanel): The Links panel to compile.

    Returns:
        KbnLinksPanel: The compiled Kibana Links panel view model.

    """
    panel_index, grid_data = compile_panel_shared(panel)

    kbn_references, kbn_links = compile_links(panel.links)

    return kbn_references, KbnLinksPanel(
        panelIndex=panel_index,
        gridData=grid_data,
        embeddableConfig=KbnLinksPanelEmbeddableConfig(
            hidePanelTitles=panel.hide_title,
            attributes=KbnLinksPanelAttributes(
                layout=panel.layout,
                links=kbn_links,
            ),
            enhancements={},
        ),
    )
