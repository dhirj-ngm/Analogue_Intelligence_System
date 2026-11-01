"""M007 material names, separate from the frozen M005 vocabulary.

No company/query rules: both collection cohorts use these same input families.
Beef output prices are not automatically equated with live-cattle input costs.
"""

from ais.related import FAMILIES as PREVIOUS_FAMILIES

FAMILIES = {
    **PREVIOUS_FAMILIES,
    "coffee": ("coffee inputs", "coffee"),
    "cattle": ("cattle inputs", "cattle livestock"),
    "aluminum": ("aluminum inputs", "aluminum aluminium"),
}


def explain_context_matches(requested, reported, labels):
    matches = []
    for family in sorted(requested.keys() & reported.keys()):
        exact = requested[family] & reported[family]
        matches.append(
            {
                "family": family,
                "label": labels[family],
                "query_terms": sorted(requested[family]),
                "report_terms": sorted(reported[family]),
                "relationship": "shared_word" if exact else "related_terms",
                "shared_words": sorted(exact),
            }
        )
    return matches
