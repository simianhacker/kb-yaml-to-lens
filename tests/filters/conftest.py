

PHRASE_FILTER = {
    "meta": {
        "disabled": False,
        "negate": False,
        "alias": None,
        "key": "status",
        "field": "status",
        "params": {
            "query": "active"
        },
        "type": "phrase",
        "index": "logs-*"
    },
    "query": {
        "match_phrase": {
            "status": "active"
        }
    },
    "$state": {
        "store": "appState"
    }
}