# Controls

Under `controls`, a list of controls can be added to the dashboard allowing users to interactively filter or modify the data displayed.

```yaml
# Controls configuration for a dashboard
dashboard:
  ...
  controls:
  - type: optionsList
    field: user.country
    data_view: metrics-*
  - type: optionsList
    field: user.language
    data_view: metrics-*
  - type: rangeSlider
    field: response_time
    data_view: metrics-*
```

## Controls Configuration

There are two types of controls that can be defined: `optionsList` and `rangeSlider`. Each control has a set of required and optional fields that define its behavior and appearance.

```yaml
controls: list        # (Optional) A list of control panels for the dashboard. Can be empty.
  - type: string      # (Required) Type of the control. Valid types: optionsList, rangeSlider.
    id: string        # (Optional) Unique identifier for the control.
    label: string     # (Optional) Display label for the control.
    width: string     # (Optional) Width of the control (small, medium, large). Defaults to "medium".
    data_view: string # (Required) Index pattern for the control.
    field: string     # (Required) Field name for the control.
    # Type-specific fields below
```

## Fields

*   `type` (required, string): The type of control. Valid values are `optionsList` and `rangeSlider`.
*   `id` (optional, string): A unique identifier for the control.
*   `label` (optional, string): A display label for the control.
*   `width` (optional, string): The width of the control. Valid values are `small`, `medium`, and `large`. Defaults to `medium`.
*   `data_view` (required, string): The index pattern that the control will use to fetch data for its options or range.
*   `field` (required, string): The field in the index pattern that the control will operate on.

## Control Types

### Options List Control

The `optionsList` control provides a dropdown or list of values from a specific field, allowing users to filter the dashboard data by selecting one or more options.

```yaml
- type: optionsList
  
  search_technique: string # (Optional) Search technique (e.g., 'prefix').
  sort: object      # (Optional) Sort configuration for optionsList.
    by: string      # (Required) Field to sort by.
    direction: string # (Required) Sort direction ('asc' or 'desc').
```

#### Fields

*   `type` (required, string): Must be `optionsList`.
*   `search_technique` (optional, string): Specifies the search technique used to find options for the list (e.g., `prefix`).
*   `sort` (optional, object): Defines how the options in the list are sorted. This object requires `by` (string, the field to sort by) and `direction` (string, the sort direction, 'asc' or 'desc').

#### Example

```yaml
controls:
  - type: optionsList
    label: Select Country
    data_view: users-*
    field: user.country.keyword
    sort:
      by: "_count"
      direction: desc
```

### Range Slider Control

The `rangeSlider` control provides a slider that allows users to filter data based on a numerical range of a specific field.

```yaml
- type: rangeSlider
  # Common control fields (id, label, width, data_view, field) also apply
  step: number      # (Optional) Step value for the slider.
```

#### Fields

*   `type` (required, string): Must be `rangeSlider`.
*   `step` (optional, number): The step value for the slider, determining the granularity of the range selection.

#### Example

```yaml
controls:
  - type: rangeSlider
    label: Filter by Response Time (ms)
    data_view: logs-*
    field: response_time
    step: 10
```

## Related Structures

*   [Sort Object](#sort-object)