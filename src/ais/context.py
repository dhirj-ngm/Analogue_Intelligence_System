"""Conservative clause rules for input role, direction and collection scope.

This is a small auditable grammar, not a general language/industry classifier.
Only pressure passages are read for cases. No company, response or result fields
are used. The unchanged M005 vocabulary/method remains available for comparison.
"""

import re

from ais.pilot import tokens
from ais.related import ALIASES, FAMILIES, explain_matches

UP = r"\b(?:ris(?:e|es|ing)|rose|increas\w*|higher|grew|grow\w*|inflation|more expensive|dearer|up)\b"
DOWN = (
    r"\b(?:fall\w*|fell|declin\w*|decreas\w*|dropp\w*|lower|cheaper|less expensive|reduc\w*|down)\b"
)
NEGATIVE = r"\b(?:no|not|never|without|unknown|unestablished)\b"
UNCERTAIN = r"\b(?:unclear|uncertain|whether|may|might|could|changed|changing|volatile|shifting|varies|vary)\b"
COST = r"\b(?:costs?|prices?|bills?|expenses?|inflation|expensive|cheaper|dearer|inputs?)\b"
NON_INPUT = r"\b(?:sales|revenues?|demand|orders?|consumption|volumes?)\b"
OUTSIDE = r"\b(?:airlines?|aircraft|aviation|airports?|aerospace|banks?|banking|insurance|insurers?|mining|smelting|steel|cement|semiconductors?|software|museums?|paintings?|artwork|marinas?|maritime|ferries)\b|\b(?:logistics provider|shipping company|transport company|data cent(?:er|re))\b"
BUSINESS = r"\b(?:(?:a|an|the)\s+)?(?:(?:food|chocolate|milk|dairy|consumer[ -]+goods|bottled[ -]+water|aviation|shipping|logistics|software)\s+){0,2}(?:maker|manufacturer|producer|retailer|provider|business|company|factory|plant)\b"

REASONS = {
    "outside_scope": "The description names a business outside this consumer-goods collection.",
    "sales_or_demand": "Sales or demand changes do not establish input-cost pressure.",
    "negated_or_unknown": "This part says the pressure was absent or unknown.",
    "unclear_direction": "The description does not establish which way these costs changed.",
    "conflicting_direction": "We couldn't separate the cost directions reliably enough for this comparison.",
    "ambiguous_sense": "The input word has no clear cost or energy meaning here.",
    "opposite_direction": "The matching reports describe costs moving in the opposite direction.",
    "unsupported_direction": "The report does not establish a compatible cost direction.",
}


def found(pattern, text):
    return bool(re.search(pattern, text, re.I))


def fragments(text):
    text = text.lower().replace("’", "'")
    text = re.sub(r"\b(?:can't|cannot|won't)\b", "not", text)
    text = re.sub(
        r"\b(is|are|was|were|did|does|do|could|would|should|has|have)n['’]t\b", r"\1 not", text
    )
    text = re.sub(r"\bnot only\b", "", text)
    text = re.sub(r"\bbut also\b", "and", text)
    # Contrast boundaries retain the positive side of "not X but Y". Commas
    # before a denied alternative retain "costs rise, not fall" without turning
    # "did not fall" into evidence of an increase.
    clauses = re.split(
        r"[;.!?]|\b(?:but|whereas|while|however|yet|as|because)\b|,\s*(?=(?:not|without)\b)", text
    )
    for clause in clauses:
        pieces = re.split(r"\band\b", clause)
        current = pieces[0]
        for piece in pieces[1:]:
            if found(f"{UP}|{DOWN}|{NEGATIVE}|{UNCERTAIN}", current) and found(
                f"{UP}|{DOWN}|{NEGATIVE}|{UNCERTAIN}", piece
            ):
                yield current.strip()
                current = piece
            else:
                current += " and " + piece
        if current.strip():
            yield current.strip()


def read_pressure(text):
    concepts, words, directions, ignored = [], {}, {}, []
    blocked = None
    for fragment in fragments(text):
        negative = found(NEGATIVE, fragment)
        if not negative and found(OUTSIDE, fragment):
            blocked = "outside_scope"
        # Business product identity is context, not an input being purchased.
        pressure = re.sub(BUSINESS, " ", fragment, flags=re.I)
        recognized = [(term, ALIASES[term]) for term in tokens(pressure) if term in ALIASES]
        if not recognized:
            continue
        families = {family for _, family in recognized}
        reason = None
        if negative:
            reason = "negated_or_unknown"
        elif found(UNCERTAIN, pressure):
            reason = "unclear_direction"
        elif (
            "cyberattack" not in families
            and found(NON_INPUT, pressure)
            and not found(COST, pressure)
        ):
            reason = "sales_or_demand"
        elif any(term == "power" for term, _ in recognized) and not found(
            r"\b(?:costs?|prices?|bills?|energy|electric\w*|utility|grid)\b", pressure
        ):
            reason = "ambiguous_sense"
        up, down = found(UP, pressure), found(DOWN, pressure)
        if not reason and up and down:
            reason = "conflicting_direction"
        if reason:
            ignored.append({"text": fragment, "reason": reason, "message": REASONS[reason]})
            continue
        direction = (
            "up"
            if up
            else "down"
            if down
            else "disruption"
            if "cyberattack" in families
            else "unspecified"
        )
        for term, family in recognized:
            concepts.append(family)
            words.setdefault(family, set()).add(term)
            directions.setdefault(family, set()).add(direction)
    for family, values in directions.items():
        if {"up", "down"} <= values:
            blocked = "conflicting_direction"
    if any(item["reason"] == "conflicting_direction" for item in ignored):
        blocked = "conflicting_direction"
    # An explicit change statement must not be reinterpreted as a topic-only
    # query. Topic lists such as "milk flour electricity" remain useful searches.
    return {
        "concepts": concepts,
        "words": words,
        "directions": directions,
        "ignored": ignored,
        "blocked": blocked,
    }


def compatible_matches(query, report):
    if query["blocked"]:
        return [], query["blocked"]
    if report["blocked"]:
        return [], "unsupported_direction"
    matches = explain_matches(query["words"], report["words"])
    accepted = []
    reason = None
    for match in matches:
        family = match["family"]
        q = query["directions"][family] - {"unspecified"}
        r = report["directions"][family] - {"unspecified"}
        # A shared input moving the opposite way vetoes a partial match on
        # another input. An unknown direction is never flipped or filled in.
        if ("up" in q and "down" in r) or ("down" in q and "up" in r):
            return [], "opposite_direction"
        if not r or (q and q != r):
            reason = "unsupported_direction"
            continue
        match["query_direction"] = next(iter(q)) if q else "unspecified"
        match["report_direction"] = next(iter(r))
        accepted.append(match)
    return accepted, None if accepted else reason


def describe(profile):
    if profile["blocked"]:
        summary = REASONS[profile["blocked"]]
    elif profile["words"]:
        parts = []
        for family, values in sorted(profile["directions"].items()):
            direction = (
                "rising costs"
                if "up" in values
                else "falling costs"
                if "down" in values
                else "disruption"
                if "disruption" in values
                else "direction not specified"
            )
            parts.append(f"{FAMILIES[family][0]} ({direction})")
        summary = "Searching for: " + "; ".join(parts) + "."
    elif profile["ignored"]:
        summary = profile["ignored"][0]["message"]
    else:
        summary = "No specific input or disruption could be read from this description."
    return {"summary": summary, "ignored": profile["ignored"], "blocked": profile["blocked"]}
