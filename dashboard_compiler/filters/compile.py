"""Compile Dashboard filter objects into their Kibana view model representations."""

from dashboard_compiler.filters.config import AndFilter, ExistsFilter, FilterJunctionTypes, FilterTypes, NegateFilter, OrFilter, PhraseFilter, PhrasesFilter, RangeFilter
from dashboard_compiler.filters.view import KbnFilter, KbnFilterMeta, KbnFilterState


def compile_exists_filter(filter: ExistsFilter, negate: bool = False) -> KbnFilter:  # noqa: A002, FBT001, FBT002
    """Compile an ExistsFilter object into its Kibana view model representation.

    Args:
        filter (ExistsFilter): The ExistsFilter object to compile.
        negate (bool): Whether to negate the filter. Defaults to False.

    Returns:
        KbnFilter: The compiled Kibana filter view model.

    """
    meta = KbnFilterMeta(
        type='exists',
        key=filter.exists,
        field=filter.exists,
        disabled=filter.disabled or False,
        negate=negate,
    )

    return KbnFilter(
        meta=meta,
        state=KbnFilterState(),
        query={'exists': {'field': filter.exists}},
    )


def compile_phrase_filter(filter: PhraseFilter, negate: bool = False) -> KbnFilter:  # noqa: A002, FBT001, FBT002
    """Compile a PhraseFilter object into its Kibana view model representation.

    Args:
        filter (PhraseFilter): The PhraseFilter object to compile.
        negate (bool): Whether to negate the filter. Defaults to False.

    Returns:
        KbnFilter: The compiled Kibana filter view model.

    """
    meta = KbnFilterMeta(
        type='phrase',
        params={'query': filter.equals},
        disabled=filter.disabled or False,
        key=filter.field,
        field=filter.field,
        negate=negate,
    )

    return KbnFilter(
        meta=meta,
        state=KbnFilterState(),
        query={'match_phrase': {filter.field: filter.equals}},
    )


def compile_phrases_filter(filter: PhrasesFilter, negate: bool = False) -> KbnFilter:  # noqa: A002, FBT001, FBT002
    """Compile a PhrasesFilter object into its Kibana view model representation.

    Args:
        filter (PhrasesFilter): The PhrasesFilter object to compile.
        negate (bool): Whether to negate the filter. Defaults to False.

    Returns:
        KbnFilter: The compiled Kibana filter view model.

    """
    meta = KbnFilterMeta(
        type='phrases',
        params=list(filter.in_list),
        disabled=filter.disabled or False,
        key=filter.field,
        field=filter.field,
        negate=negate,
    )

    return KbnFilter(
        meta=meta,
        state=KbnFilterState(),
        query={
            'bool': {
                'minimum_should_match': 1,
                'should': [{'match_phrase': {filter.field: value}} for value in filter.in_list],
            },
        },
    )


def compile_range_filter(filter: RangeFilter, negate: bool = False) -> KbnFilter:  # noqa: A002, FBT001, FBT002
    """Compile a RangeFilter object into its Kibana view model representation.

    Args:
        filter (FilterTypes): The Filter object to compile.
        negate (bool): Whether to negate the filter. Defaults to False.

    Returns:
        KbnFilter: The compiled Kibana filter view model.

    """
    range_query = {}

    if filter.gte is not None:
        range_query['gte'] = filter.gte
    if filter.lte is not None:
        range_query['lte'] = filter.lte
    if filter.gt is not None:
        range_query['gt'] = filter.gt
    if filter.lt is not None:
        range_query['lt'] = filter.lt

    return KbnFilter(
        meta=KbnFilterMeta(
            type='range',
            params=range_query,
            disabled=filter.disabled or False,
            key=filter.field,
            field=filter.field,
            negate=negate,
        ),
        state=KbnFilterState(),
        query={'range': {filter.field: range_query}},
    )

def compile_junction_filter(filter: FilterJunctionTypes) -> KbnFilter:

    if isinstance(filter, NegateFilter):
        nested_filter = filter.not_filter
        return compile_filter(filter=nested_filter, negate=True)

    msg = f'Unimplemented filter junction type: {type(filter)}'
    raise NotImplementedError(msg)




def compile_filter(filter: FilterTypes, negate: bool = False) -> KbnFilter:  # noqa: A002, FBT001, FBT002
    """Compile a single Filter object into its Kibana view model representation.

    Args:
        filter (Filter): The Filter object to compile.
        negate (bool): Whether to negate the filter. Defaults to False.

    Returns:
        KbnFilter: The compiled Kibana filter view model.

    """
    if isinstance(filter, ExistsFilter):
        return compile_exists_filter(filter, negate)

    if isinstance(filter, PhraseFilter):
        return compile_phrase_filter(filter, negate)

    if isinstance(filter, PhrasesFilter):
        return compile_phrases_filter(filter, negate)

    if isinstance(filter, RangeFilter):
        return compile_range_filter(filter, negate)

    msg = f'Unimplemented filter type: {type(filter)}'
    raise NotImplementedError(msg)


def compile_filters(filters: list[FilterJunctionTypes | FilterTypes]) -> list[KbnFilter]:
    """Compile the filters of a Dashboard object into its Kibana view model representation.

    Args:
        filters (list[BaseFilter]): The list of filter objects to compile.

    Returns:
        list[KbnFilter]: The compiled list of Kibana filter view models.

    """
    kbn_filters = []

    for dashboard_filter in filters:
        if isinstance(dashboard_filter, NegateFilter | AndFilter | OrFilter):
            kbn_filters.append(compile_junction_filter(dashboard_filter))
        if isinstance(dashboard_filter, ExistsFilter | PhraseFilter | PhrasesFilter | RangeFilter):
            kbn_filters.append(compile_filter(dashboard_filter))

    return kbn_filters
