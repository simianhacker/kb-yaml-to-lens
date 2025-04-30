# Filters and Queries

This document describes the structure for defining filters and queries at both the dashboard and panel levels.

## Dashboard Filters

Dashboard filters are applied globally to all panels on the dashboard. They are defined within the `filters` list at the top level of the `dashboard` object.

```yaml
dashboard:
  filters: list         # (Optional) A list of filters to apply to the dashboard. Can be empty.
    - field: string     # (Required) Field to filter on.
      # Choose one of the following filter types:
      equals: any       # (Required for phrase filter) Value for a phrase filter.
      in: list          # (Required for phrases filter) List of values for a phrases filter.
      exists: boolean   # (Required for exists filter) Indicates if the field must exist.
      gte: any          # (Optional for range filter) Greater than or equal to value.
      gt: any           # (Optional for range filter) Greater than value.
      lte: any          # (Optional for range filter) Less than or equal to value.
      lt: any           # (Optional for range filter) Less than value.
    - not: object       # (Optional) Negates the following filter.
        # Nested filter object (phrase, phrases, or range)
```

### Filter Types

*   **Phrase Filter**: Filters documents where a specific field exactly matches a single value.
    ```yaml
    - field: status.keyword
      equals: active
    ```
*   **Phrases Filter**: Filters documents where a specific field matches any of the values in a list.
    ```yaml
    - field: event.category
      in: ["authentication", "network"]
    ```
*   **Exists Filter**: Filters documents based on whether a field exists or not.
    ```yaml
    - field: error.message
      exists: true # or false
    ```
*   **Range Filter**: Filters documents where a numerical or date field falls within a specified range.
    ```yaml
    - field: response_time
      gte: 100
      lt: 500
    ```
*   **Negation**: Negates the following filter.
    ```yaml
    - not:
        field: event.outcome
        equals: success
    ```

## Panel Filters

Panel filters are applied only to the specific panel they are defined within, in addition to any global dashboard filters. They are defined within the `filters` list of a panel object (currently only supported for `lens` panels).

```yaml
- panel:
    type: lens
    filters: list         # (Optional) Panel-specific filters.
      - field: string     # (Required) Field to filter on.
        type: string      # (Required) Filter type (e.g., phrase, phrases, range).
        value: any        # (Required) Value(s) for the filter (string for phrase, list of strings for phrases).
        operator: string  # (Required) Filter operator (equals, contains, startsWith, endsWith).
        negate: boolean   # (Optional) Whether to negate the filter. Defaults to false.
```

### Fields

*   `field` (required, string): The field to filter on.
*   `type` (required, string): The type of filter. Valid values are `phrase`, `phrases`, and `range`.
*   `value` (required, any): The value or list of values for the filter.
*   `operator` (required, string): The operator to use for the filter. Valid values are `equals`, `contains`, `startsWith`, and `endsWith`.
*   `negate` (optional, boolean): If set to `true`, the filter will be negated. Defaults to `false`.

### Example

```yaml
panels:
  - panel:
      type: lens
      # ... other panel fields ...
      filters:
        - field: http.response.status_code
          type: phrase
          value: 404
          operator: equals
        - field: url.full
          type: phrases
          value: ["/login", "/admin"]
          operator: contains
          negate: true
```