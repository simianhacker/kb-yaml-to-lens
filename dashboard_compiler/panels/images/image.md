# Image Panel

The `image` panel is used to display images on the dashboard.

```yaml
- panel:
    type: image
    # Common panel fields (id, title, description, grid, hide_title) also apply
    content: string       # (Required) The markdown content to display.
```

## Fields

*   `type` (required, string): Must be `markdown`.
*   `content` (required, string): The markdown content to be rendered within the panel. You can use YAML multi-line string syntax (e.g., `|`) for readability with longer content.

## Example

```yaml
dashboard:
  title: Dashboard with Markdown
  panels:
    - panel:
        type: markdown
        grid: { x: 0, y: 0, w: 24, h: 10 }
        title: Important Information
        content: |
          # Project Status

          - **Status:** In Progress
          - **Deadline:** End of Q3