"""Test data for Lens dimensions compilation tests."""

from typing import Any

type InputDimensionType = dict[str, Any]

type OutputDimensionType = dict[str, Any]

type InputMetricType = dict[str, Any]

type OutputMetricType = dict[str, Any]

type TestCaseType = tuple[InputDimensionType, InputMetricType, OutputMetricType, OutputDimensionType]

## Test cases in this file are organized in the following format:
# (input_dimension, input_metric, output_metric, output_dimension)

# Add more test cases for different dimension operations and field types.

INPUT_METRIC = {
    'aggregation': 'count',
}

OUTPUT_METRIC = {
    'label': 'Count of records',
    'dataType': 'number',
    'operationType': 'count',
    'isBucketed': False,
    'scale': 'ratio',
    'sourceField': '___records___',
}

CASE_DATE_HISTOGRAM_DIMENSION: TestCaseType = (
    # Input dimension
    {
        'type': 'date_histogram',
        'label': '@timestamp',
        'field': '@timestamp',
        'operation': 'date_histogram',
        'interval': 'auto',
    },
    INPUT_METRIC,
    OUTPUT_METRIC,
    # Output dimension
    {
        'label': '@timestamp',
        'dataType': 'date',
        'operationType': 'date_histogram',
        'sourceField': '@timestamp',
        'isBucketed': True,
        'scale': 'interval',
        'params': {
            'interval': 'auto',
            'includeEmptyRows': True,
            'dropPartials': False,
        },
    },
)
"""Tuple[InDimension, InMetric, OutMetric, OutDimension] for date histogram dimension."""

CASE_TERMS_DIMENSION_SORTED: TestCaseType = (
    # Input dimension
    {
        'type': 'values',
        'label': 'Top 5 values of agent.type',
        'field': 'agent.type',
        'operation': 'terms',
        'sort': {
            'by': 'Count',
            'direction': 'desc',
        },
    },
    INPUT_METRIC,
    OUTPUT_METRIC,
    # Output dimension
    {
        'label': 'Top 5 values of agent.type',
        'dataType': 'string',
        'operationType': 'terms',
        'scale': 'ordinal',
        'sourceField': 'agent.type',
        'isBucketed': True,
        'params': {
            'size': 5,
            'orderBy': {'type': 'column', 'columnId': '87416118-6032-41a2-aaf9-173fc0e525eb'},
            'orderDirection': 'desc',
            'otherBucket': True,
            'missingBucket': False,
            'parentFormat': {'id': 'terms'},
            'include': [],
            'exclude': [],
            'includeIsRegex': False,
            'excludeIsRegex': False,
        },
    },
)
"""Tuple[InDimension, InMetric, OutMetric, OutDimension] for terms dimension with sorting."""

CASE_FILTERS_DIMENSION: TestCaseType = (
    # Input dimension
    {
        'type': 'filters',
        'label': 'Filter by Status',
        'filters': [
            {'query': 'agent.version: 8.*', 'language': 'kuery'},
            {'query': 'agent.version: 7.*', 'language': 'kuery'},
        ],
    },
    INPUT_METRIC,
    OUTPUT_METRIC,
    # Output dimension
    {
        'label': 'Filters',
        'dataType': 'string',
        'operationType': 'filters',
        'scale': 'ordinal',
        'isBucketed': True,
        'params': {
            'filters': [
                {'label': '', 'input': {'query': 'agent.version: 8.*', 'language': 'kuery'}},
                {'input': {'query': 'agent.version: 7.*', 'language': 'kuery'}, 'label': ''},
            ]
        },
    },
)
"""Tuple[InDimension, InMetric, OutMetric, OutDimension] for filters dimension."""

CASE_INTERVALS_DIMENSION: TestCaseType = (
    # Input dimension
    {
        'type': 'intervals',
        'label': 'Interval by agent.version',
    },
    INPUT_METRIC,
    OUTPUT_METRIC,
    {
        'label': 'apache.uptime',
        'dataType': 'number',
        'operationType': 'range',
        'sourceField': 'apache.uptime',
        'isBucketed': True,
        'scale': 'interval',
        'params': {'includeEmptyRows': True, 'type': 'histogram', 'ranges': [{'from': 0, 'to': 1000, 'label': ''}], 'maxBars': 'auto'},
    },
)
"""Tuple[InDimension, InMetric, OutMetric, OutDimension] for intervals dimension."""

CASE_INTERVALS_DIMENSION_CUSTOM_GRANULARITY: TestCaseType = (
    # Input dimension
    {
        'type': 'intervals',
        'field': 'agent.version',
        'granularity': 1,
    },
    INPUT_METRIC,
    OUTPUT_METRIC,
    {
        'label': 'apache.uptime',
        'dataType': 'number',
        'operationType': 'range',
        'sourceField': 'apache.uptime',
        'isBucketed': True,
        'scale': 'interval',
        'params': {'includeEmptyRows': True, 'type': 'histogram', 'ranges': [{'from': 0, 'to': 1000, 'label': ''}], 'maxBars': 167.5},
    },
)
"""Tuple[InDimension, InMetric, OutMetric, OutDimension] for intervals dimension with custom granularity."""

TEST_CASES = [
    CASE_DATE_HISTOGRAM_DIMENSION,
    CASE_TERMS_DIMENSION_SORTED,
    CASE_FILTERS_DIMENSION,
    CASE_INTERVALS_DIMENSION,
    CASE_INTERVALS_DIMENSION_CUSTOM_GRANULARITY,
]

TEST_CASE_IDS = [
    'Date Histogram Dimension',
    'Terms Dimension with Sorting',
    'Filters Dimension',
    'Intervals Dimension',
    'Intervals Dimension with Custom Granularity',
]
