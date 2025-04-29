from typing import Literal

from pydantic import Field

from dashboard_compiler.models.config.panels.base import BasePanel


class MarkdownPanel(BasePanel):
    """
    Represents a Markdown panel configuration in the YAML schema.

    Markdown panels are used to display rich text content using Markdown syntax.
    """

    type: Literal["markdown"] = "markdown"
    content: str = Field(
        ..., description="The Markdown content to be displayed in the panel."
    )
