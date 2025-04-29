from typing import Literal

from pydantic import BaseModel, Field


class Sort(BaseModel):
    """
    Represents the sort configuration used in various parts of the YAML schema,
    such as sorting options in controls or terms in Lens charts.
    """

    by: str = Field(
        ..., description="The field name to sort the data by."
    )
    direction: Literal["asc", "desc"] = Field(
        ..., description="The sort direction. Must be either 'asc' for ascending or 'desc' for descending."
    )


class BaseFilter(BaseModel):
    """
    Base class for defining filter configurations in the YAML schema.

    Specific filter types (e.g., exists, phrase, range) inherit from this base class.
    """

    field: str = Field(
        ..., description="The name of the field to apply the filter to."
    )


class ExistsFilter(BaseFilter):
    """
    Represents an 'exists' filter configuration in the YAML schema.

    This filter checks for the existence or non-existence of a specific field.
    """

    exists: bool = Field(
        ..., description="If `true`, the field must exist. If `false`, the field must not exist."
    )


class PhraseFilter(BaseFilter):
    """
    Represents a 'phrase' filter configuration in the YAML schema.

    This filter matches documents where a specific field contains an exact phrase.
    """

    equals: str = Field(
        ..., description="The exact phrase value that the field must match."
    )


class PhrasesFilter(BaseFilter):
    """
    Represents a 'phrases' filter configuration in the YAML schema.

    This filter matches documents where a specific field contains one or more
    of the specified phrases.
    """

    in_list: list[str] = Field(
        ..., alias="in", description="A list of phrases. Documents must match at least one of these phrases in the specified field."
    )


class RangeFilter(BaseFilter):
    """
    Represents a 'range' filter configuration in the YAML schema.

    This filter matches documents where a numeric or date field falls within a specified range.
    """

    gte: str | None = Field(
        None, description="Greater than or equal to value for the range filter."
    )
    lte: str | None = Field(
        None, description="Less than or equal to value for the range filter."
    )
    lt: str | None = Field(
        None, description="Less than value for the range filter."
    )
    gt: str | None = Field(
        None, description="Greater than value for the range filter."
    )


class NegationFilter(BaseModel):
    """
    Represents a negated filter configuration in the YAML schema.

    This allows for excluding documents that match the nested filter.
    """

    not_filter: ExistsFilter | PhraseFilter | PhrasesFilter | RangeFilter = Field(
        ..., alias="not", description="The filter to negate. Can be a phrase, phrases, or range filter."
    )


class BaseQuery(BaseModel):
    """
    Base class for defining query configurations in the YAML schema.

    Specific query types (e.g., KQL, Lucene) inherit from this base class.
    """
    # No common fields needed at this level currently.
    pass


class KqlQuery(BaseQuery):
    """
    Represents a KQL (Kibana Query Language) query configuration.

    KQL is the default query language in Kibana and provides a simplified syntax
    for filtering data.
    """

    kql: str = Field(
        default="", description="The KQL query string to filter data."
    )


class LuceneQuery(BaseQuery):
    """
    Represents a Lucene query configuration.

    Lucene provides a more powerful and flexible syntax for querying data
    compared to KQL.
    """

    lucene: str = Field(
        default="", description="The Lucene query string to filter data."
    )
