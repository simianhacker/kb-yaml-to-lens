"""Compile Markdown panels into their Kibana representations."""

from dashboard_compiler.panels.markdown.config import MarkdownPanel
from dashboard_compiler.panels.markdown.view import (
    KBN_MARKDOWN_DEFAULT_FONT_SIZE,
    KBN_MARKDOWN_DEFAULT_OPEN_LINKS_IN_NEW_TAB,
    KbnMarkdownEmbeddableConfig,
    KbnMarkdownPanel,
    KbnMarkdownSavedVis,
    KbnMarkdownSavedVisData,
    KbnMarkdownSavedVisDataSearchSource,
    KbnMarkdownSavedVisParams,
)
from dashboard_compiler.panels.shared.compile import compile_panel_shared
from dashboard_compiler.queries.view import KbnQuery


def compile_markdown_saved_vis_data() -> KbnMarkdownSavedVisData:
    """Compile the saved visualization data for a MarkdownPanel.

    Args:
        panel (MarkdownPanel): The Markdown panel to compile.

    Returns:
        KbnMarkdownSavedVisData: The compiled saved visualization data.

    """
    return KbnMarkdownSavedVisData(
        aggs=[],
        searchSource=KbnMarkdownSavedVisDataSearchSource(
            query=KbnQuery(query='', language='kuery'),
            filter=[],
        ),
    )


def compile_markdown_saved_vis_params(panel: MarkdownPanel) -> KbnMarkdownSavedVisParams:
    """Compile the saved visualization parameters for a MarkdownPanel.

    Args:
        panel (MarkdownPanel): The Markdown panel to compile.

    Returns:
        KbnMarkdownSavedVisParams: The compiled saved visualization parameters.

    """
    return KbnMarkdownSavedVisParams(
        fontSize=panel.font_size or KBN_MARKDOWN_DEFAULT_FONT_SIZE,
        openLinksInNewTab=panel.links_in_new_tab or KBN_MARKDOWN_DEFAULT_OPEN_LINKS_IN_NEW_TAB,
        markdown=panel.content,
    )


def compile_markdown_saved_vis(panel: MarkdownPanel) -> KbnMarkdownSavedVis:
    """Compile a MarkdownPanel into its Kibana saved visualization representation.

    Args:
        panel (MarkdownPanel): The Markdown panel to compile.

    Returns:
        KbnMarkdownSavedVis: The compiled Kibana Markdown saved visualization.

    """
    return KbnMarkdownSavedVis(
        title=panel.title,
        description=panel.description,
        type='markdown',
        params=compile_markdown_saved_vis_params(panel),
        uiState={},
        data=compile_markdown_saved_vis_data(),
    )


def compile_markdown_panel(panel: MarkdownPanel) -> KbnMarkdownPanel:
    """Compile a MarkdownPanel into its Kibana view model representation.

    Args:
        panel (MarkdownPanel): The Markdown panel to compile.

    Returns:
        KbnMarkdownPanel: The compiled Kibana Markdown panel view model.

    """
    panel_index, grid_data = compile_panel_shared(panel)

    return KbnMarkdownPanel(
        type='visualization',
        panelIndex=panel_index,
        gridData=grid_data,
        embeddableConfig=KbnMarkdownEmbeddableConfig(
            hidePanelTitles=panel.hide_title,
            savedVis=compile_markdown_saved_vis(panel),
        ),
    )
