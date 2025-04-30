"""Configuration schema for Dashboard filters."""

from typing import Self

from pydantic import Field, model_validator

from dashboard_compiler.shared.config import BaseCfgModel

type FilterTypes = ExistsFilter | PhraseFilter | PhrasesFilter | RangeFilter

type FilterJunctionTypes = AndFilter | OrFilter | NegateFilter

type AllFilterTypes = FilterTypes | FilterJunctionTypes

class BaseFilter(BaseCfgModel):
    """Base class for all filter configurations in the Config schema."""

    alias: str | None = Field(None)
    """An optional alias for the filter, used for display purposes."""

    disabled: bool | None = Field(None)
    """Indicates whether the filter is disabled. If `true`, the filter will not be applied."""


class ExistsFilter(BaseFilter):
    """Represents an 'exists' filter configuration in the Config schema.

    This filter checks for the existence or non-existence of a specific field.
    """

    exists: str = Field(...)
    """The field name to check for existence. If the field exists in a document, it will match that document."""


class PhraseFilter(BaseFilter):
    """Represents a 'phrase' filter configuration in the Config schema.

    This filter matches documents where a specific field contains an exact phrase.
    """

    field: str = Field(...)
    """The field name to apply the filter to."""

    equals: str = Field(...)
    """The exact phrase value that the field must match."""


class PhrasesFilter(BaseFilter):
    """Represents a 'phrases' filter configuration in the Config schema.

    This filter matches documents where a specific field contains one or more
    of the specified phrases.
    """

    field: str = Field(...)
    """The field name to apply the filter to."""

    in_list: list[str] = Field(..., alias='in')
    """A list of phrases. Documents must match at least one of these phrases in the specified field."""


class RangeFilter(BaseFilter):
    """Represents a 'range' filter configuration in the Config schema.

    This filter matches documents where a numeric or date field falls within a specified range.
    """

    field: str = Field(...)
    """The field name to apply the filter to."""

    gte: str | None = Field(default=None)
    """Greater than or equal to value for the range filter."""

    lte: str | None = Field(default=None)
    """Less than or equal to value for the range filter."""

    lt: str | None = Field(default=None)
    """Less than value for the range filter."""

    gt: str | None = Field(default=None)
    """Greater than value for the range filter."""

    @model_validator(mode='after')
    def at_least_one_value(self) -> Self:
        """Ensure at least one of gte, lte, gt, or lt is provided."""  # noqa: DOC201, DOC501
        if not any([self.lte, self.gte, self.gt, self.lt]):
            msg = "At least one of 'gte', 'lte', 'gt', or 'lt' must be provided for RangeFilter."
            raise ValueError(msg)
        return self


class NegateFilter(BaseCfgModel):
    """Represents a negated filter configuration in the Config schema.

    This allows for excluding documents that match the nested filter.
    """

    not_filter: FilterTypes = Field(..., validation_alias='not')
    """The filter to negate. Can be a phrase, phrases, or range filter."""


class AndFilter(BaseCfgModel):
    """Represents an 'and' filter configuration in the Config schema.

    This filter matches documents that satisfy all of the specified filters.
    """

    and_filters: list[FilterTypes] = Field(..., alias='and')
    """A list of filters. All filters must match for a document to be included."""


class OrFilter(BaseCfgModel):
    """Represents an 'or' filter configuration in the Config schema.

    This filter matches documents that satisfy at least one of the specified filters.
    """

    or_filters: list[FilterTypes] = Field(..., alias='or')
    """A list of filters. At least one filter must match for a document to be included."""
