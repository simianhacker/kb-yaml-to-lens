"""Test the compilation of Lens dimensions from config models to view models."""

import pytest
from deepdiff import DeepDiff
from pydantic import BaseModel

from dashboard_compiler.panels.charts.dimensions.config import LensDimensionTypes
from dashboard_compiler.panels.charts.metrics.compile import compile_lens_metric
from dashboard_compiler.panels.charts.metrics.config import LensMetricTypes
from tests.conftest import DEEP_DIFF_DEFAULTS
from tests.panels.charts.dimensions.test_lens_dimensions_data import (
    TEST_CASE_IDS,
    TEST_CASES,
)

# Define fields to exclude from DeepDiff comparison
EXCLUDE_REGEX_PATHS = [
    # Add regex paths for fields to exclude, e.g., IDs
    r"root\['columns'\]\[\d+\]\['id'\]",  # Example: Exclude column IDs
    # Refer to links test exclude paths for more ideas
]


class MetricHolder(BaseModel):
    """A holder for metrics to be used in tests."""

    metric: LensMetricTypes


class DimensionHolder(BaseModel):
    """A holder for dimensions to be used in tests."""

    dimension: LensDimensionTypes


@pytest.mark.parametrize(('config', 'metric_config', 'desired_metric', 'desired_dimension'), TEST_CASES, ids=TEST_CASE_IDS)
async def test_compile_lens_dimension(config: dict, metric_config: dict, desired_metric: dict, desired_dimension: dict) -> None:
    """Test the compilation of various Lens dimension configurations to their Kibana view model."""
    metric_holder = MetricHolder.model_validate(**metric_config)

    # Ensure our metric compiles correctly before proceeding
    kbn_column = compile_lens_metric(metric_holder.metric)
    assert DeepDiff(kbn_column, desired_metric, exclude_regex_paths=EXCLUDE_REGEX_PATHS, **DEEP_DIFF_DEFAULTS) == {}  # type: ignore

    dimension_holder = DimensionHolder.model_validate(**config)

    # # Call the correct Lens dimension compile function
    kbn_references, kbn_columns = compile_lens_dimension(
        dimensions=dimensions_holder.dimensions,
        columns_by_name=columns_by_name,
    )

    assert DeepDiff(desired_output, kbn_columns, exclude_regex_paths=EXCLUDE_REGEX_PATHS, **DEEP_DIFF_DEFAULTS) == {}  # type: ignore

    kbn_references_as_dicts = [ref.model_dump(by_alias=True) for ref in kbn_references]
    kbn_references_as_dicts = kbn_references

    assert DeepDiff(desired_references, kbn_references_as_dicts, exclude_regex_paths=EXCLUDE_REGEX_PATHS, **DEEP_DIFF_DEFAULTS) == {}  # type: ignore
