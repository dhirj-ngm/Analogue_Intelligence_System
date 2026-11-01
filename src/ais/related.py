"""Small, explicit input families; related terms are not new source facts.

These relationships apply to every query and every eligible pressure passage.
They contain no companies, case IDs, responses, dates or outcome labels.
"""

import re

from ais.pilot import tokens

FAMILIES = {
    "dairy": ("dairy inputs", "dairy milk"),
    "grain": ("grain inputs", "grain grains wheat flour corn maize oats oat cereal cereals"),
    "energy": ("energy", "energy electricity electric power gas"),
    "cocoa": ("cocoa and chocolate inputs", "cocoa cacao chocolate"),
    "oil": ("oil and fuel", "oil petroleum fuel fuels diesel petrol gasoline"),
    "transport": (
        "transport",
        "transport transportation freight shipping delivery distribution logistics",
    ),
    "resin": ("resin and plastic materials", "resin resins plastic plastics polymer polymers"),
    "fibre": ("fibre inputs", "fiber fibers fibre fibres pulp"),
    "packaging": ("packaging", "packaging"),
    "currency": ("currency transactions", "currency currencies forex exchange"),
    "production": ("production", "production manufacturing"),
    "cyberattack": ("cyberattack disruption", "cyberattack cyberattacks"),
}
ALIASES = {term: family for family, (_, terms) in FAMILIES.items() for term in terms.split()}


def analyze(text):
    """Return supported concept occurrences and the original words behind them.

    Explicit negation/unknown clauses are discarded before normalizing terms.
    Generic ingredient/commodity words and unlisted vocabulary supply no match.
    This is deliberately not an understanding of industry, intent or direction.
    """
    clauses = re.split(r"[;.]", text)
    positive = " ".join(
        clause
        for clause in clauses
        if not re.search(r"\b(no|not|unknown|unestablished)\b", clause, re.I)
    )
    concepts, original = [], {}
    for term in tokens(positive):
        family = ALIASES.get(term)
        if family:
            concepts.append(family)
            original.setdefault(family, set()).add(term)
    return concepts, original


def explain_matches(requested, reported):
    matches = []
    for family in sorted(requested.keys() & reported.keys()):
        exact = requested[family] & reported[family]
        matches.append(
            {
                "family": family,
                "label": FAMILIES[family][0],
                "query_terms": sorted(requested[family]),
                "report_terms": sorted(reported[family]),
                "relationship": "shared_word" if exact else "related_terms",
                "shared_words": sorted(exact),
            }
        )
    return matches
