"""M010 local wording rules. No source-case changes or material synonyms.

Resolve explicit subjects/alternatives only. Ambiguous directions or reader roles
stop matching and ask for an edit; absence of a fall is never evidence of a rise.
"""

import re

from ais.context import UP, DOWN, COST, NEGATIVE, BUSINESS, fragments, found, describe
from ais.pilot import tokens
from ais.reader_context import (
    ROLE,
    LIVE,
    OUTSIDE_BUSINESS,
    query_profile as m009_profile,
    reader_pressure_text,
    clarification as m009_clarification,
)
from ais.vocabulary import FAMILIES

REASONS = {
    "ambiguous_cost_direction": "We cannot safely tell which input costs rose or fell.",
    "ambiguous_business_scope": "We cannot safely tell which business is yours and which is a supplier or customer.",
    "output_context": "Sales, selling prices and profit changes do not establish purchased-input cost pressure.",
    "third_party_cost": "Another business's own costs are not automatically your input costs.",
}
ALIASES = {word: family for family, (_, terms) in FAMILIES.items() for word in terms.split()}
OUTPUT = r"\b(?:sales|revenues?|profits?|margins?|selling|retail|output)\b"
CHANGE = f"(?:{UP}|{DOWN})"
COST_CONTEXT = rf"{COST}|\b(?:charges?|rates?|fees?)\b"


def inputs(text):
    text = re.sub(BUSINESS, " ", text, flags=re.I)
    return {ALIASES[w] for w in tokens(text) if w in ALIASES}


def note(text, reason):
    return {"text": text.strip(), "reason": reason, "message": REASONS[reason]}


def direction_words(text):
    text = text.lower().replace("’", "'")
    text = re.sub(r"\bnot only\b", "", text)
    text = re.sub(r"\bbut also\b", "and", text)
    text = re.sub(r"\b(?:raises?|raised|raising)\b", "increased", text)
    text = re.sub(r"\b(?:lowers?|lowered|lowering)\b", "decreased", text)
    text = re.sub(r"\bclimb(?:s|ed|ing)?\b", "increased", text)
    text = re.sub(r"\bdip(?:s|ped|ping)?\b", "decreased", text)
    return re.sub(r"\brisen\b", "rise", text)


def role_phrases(text):
    """Remove role descriptions, retaining predicates about charges to the reader."""
    text = text.replace("’", "'").lower().replace("we're", "we are")
    ambiguous = bool(
        re.search(r"\bwe\s+(?:may|might|could)\s+(?:be|operate)\b", text)
        and found(OUTSIDE_BUSINESS, text)
    )
    if (found(ROLE, text) or found(rf"\b(?:use\w*|hire\w*)\b.*{OUTSIDE_BUSINESS}", text)) and found(
        r"\b(?:its|their)\s+(?:own\s+)?(?:[\w-]+\s+){0,3}(?:costs?|prices?|bills?|expenses?)\b",
        text,
    ):
        ambiguous = True
    text = re.sub(
        rf"\bour\s+{ROLE}\s+(?:is|are)\s+(?:(?:an?|the)\s+)?{OUTSIDE_BUSINESS}",
        "our third party",
        text,
    )
    # Possessive client identity is not the supplied product/business itself.
    text = re.sub(rf"{OUTSIDE_BUSINESS}'s\s+", "", text)
    if re.search(
        r"\bwe (?:are|run|operate)\s+(?:an?\s+)?(?:airline|aircraft|bank|insurer)\s+(?:supplier|vendor)\b",
        text,
    ):
        ambiguous = True
    # "Our supplier, an airline, raised our charges" keeps the charge predicate.
    text = re.sub(
        rf"(\bour\s+(?:[\w-]+\s+){{0,3}}{ROLE}),\s*(?:an?|the)\s+{OUTSIDE_BUSINESS}(?:\s+(?:company|firm|business))?\s*,",
        r"\1 ",
        text,
    )
    # Reader uses a service provider; its clients do not identify our business.
    text = re.sub(
        r"\b(?:uses?|using|hires?|hiring|contracts? with|works? with)\s+(?:an?|the|our)\s+(?:logistics|shipping|transport)\s+(?:firm|company|provider|supplier|business)(?:\s+(?:whose\s+(?:customers|clients)\s+include|that\s+serves?)\s+[^.;!?]+)?",
        " uses a supplier ",
        text,
    )
    # Consumer goods can be supplied to customers in an outside industry.
    text = re.sub(
        rf"\b(?:for|to)\s+(?:(?:an?|the|our)\s+)?{OUTSIDE_BUSINESS}(?:\s+(?:customers?|clients?|companies))?",
        " ",
        text,
    )
    # These predicates explicitly assign the outside actor a third-party role.
    text = re.sub(
        rf"\b(?:an?|the)\s+{OUTSIDE_BUSINESS}(?:\s+(?:company|firm))?\s+(?:finances|funds|insures|buys|purchases)\s+our\s+[^.;!?]+",
        " ",
        text,
    )
    return text, ambiguous


def has_change(text):
    return found(CHANGE, text) or found(
        r"\b(?:pay|pays|paying|paid)\s+(?:more|less)\b|\bcharg\w*\b", text
    )


def comma_clauses(sentence):
    pieces = re.split(r",\s*", sentence)
    current = pieces[0]
    grouped = []
    for index, piece in enumerate(pieces[1:], 1):
        remainder = ", ".join(pieces[index:])
        if (
            has_change(current)
            and has_change(remainder)
            and (inputs(piece) or found(COST, piece) or found(OUTPUT, piece))
        ):
            grouped.append(current)
            current = piece
        else:
            current += ", " + piece
    grouped.append(current)
    for group in grouped:
        parts = re.split(r"\b(and|but|while|whereas)\b", group)
        current = parts[0]
        for separator, piece in zip(parts[1::2], parts[2::2], strict=True):
            if (
                has_change(current)
                and has_change(piece)
                and (inputs(piece) or found(COST, piece) or found(OUTPUT, piece))
            ):
                yield current
                current = piece
            else:
                current += " " + separator + " " + piece
        if current.strip():
            yield current


def positive_alternatives(text):
    """Only opposite, denied directional alternatives may be removed."""
    ambiguous = False
    pattern = re.compile(rf"\bnot\s+({CHANGE})\s+but\s+({CHANGE})")

    def positive(match):
        nonlocal ambiguous
        first_up, second_up = found(UP, match[1]), found(UP, match[2])
        if first_up == second_up:
            ambiguous = True
            return match[0]
        return match[2]

    text = pattern.sub(positive, text)
    # Work within explicit clauses, so a different subject after a comma/but
    # cannot have its direction transferred to a preceding input.
    result = []
    for part in fragments(text):
        denied = re.search(rf"(?:,\s*)?\b(?:not|rather than|instead of)\s+({CHANGE})\s*$", part)
        if denied:
            prefix = part[: denied.start()]
            actual = list(re.finditer(CHANGE, prefix))
            if actual and not found(NEGATIVE, prefix):
                if found(UP, actual[-1][0]) != found(UP, denied[1]):
                    part = prefix.strip()
                else:
                    ambiguous = True
        result.append(part)
    return result, ambiguous


def retained_cost_clause(text):
    """Separate the reader's purchase, a selling response and another actor's bill."""
    external = re.match(rf"\s*(?:our|the)\s+(?:[\w-]+\s+){{0,3}}{ROLE}(?:'s)?\b", text)
    transfer = bool(
        re.search(
            r"\bcharg\w*\s+(?:us|our)\b|\bour\s+(?:[\w-]+\s+){0,4}(?:prices?|rates?|charges?|fees?)\b",
            text,
        )
    )
    transfer = transfer or bool(
        external
        and found(r"\b(?:suppliers?|vendors?|carriers?|providers?)\b", external[0])
        and found(r"\b(?:prices?|rates?|fees?|charges?)\b", text)
        and found(CHANGE, text)
        and not found(r"\b(?:own|costs?|bills?|expenses?)\b", text)
    )
    if external and not transfer and (found(COST, text) or found(r"\bpay\w*\b", text)):
        return "", note(text, "third_party_cost")
    if found(rf"\bfor\s+our\s+{ROLE}\b", text) and found(COST, text):
        return "", note(text, "third_party_cost")
    if external and transfer:
        text = text[external.end() :]
    explicit_input = found(r"\b(?:input|purchase|purchasing|procurement|buying)\b", text)
    reader_sells = found(
        r"\bwe\s+(?:charge|charged|are charging|increased|decreased)\b", text
    ) and found(r"\b(?:prices?|more|less)\b", text)
    output_price = (
        found(r"\b(?:selling|retail|output|customer)\b", text)
        and found(r"\bprices?\b", text)
        and not found(r"\b(?:costs?|bills?|inputs?|purchases?)\b", text)
    )
    if not explicit_input and (
        reader_sells or output_price or (found(OUTPUT, text) and not found(COST, text))
    ):
        return "", note(text, "output_context")
    # Explicit buyer wording, not an alias from any sales/output word.
    buyer = re.compile(
        r"\b(we|i|(?:a|the|our)\s+(?:[\w-]+\s+){0,3}(?:company|business|maker))\s+(?:are\s+|is\s+)?(?:pay|pays|paying|paid)\s+(more|less)\s+for\s+(.+)$"
    )
    match = buyer.search(text)
    if match and inputs(match[3]):
        change = "rising" if match[2] == "more" else "falling"
        text = text[: match.start()] + f"{match[1]} buy {match[3]} with input costs {change}"
    return text, None


def query_profile(text):
    original = text
    text, scope_ambiguous = role_phrases(direction_words(text))
    notes, kept = [], []
    # A discarded third-party cost clause must never erase an explicit reader
    # identity later in that clause ("supplier costs rose but we run an airline").
    identities = re.finditer(
        r"\bwe\s+(?:are|run|operate|own)\s+(.+?)(?=\b(?:and|but|using|with|that|which|from)\b|[.;!?]|$)",
        text,
    )
    outside = any(found(OUTSIDE_BUSINESS, m[1]) and not found(NEGATIVE, m[1]) for m in identities)
    cost_ambiguous = False
    antecedent = None
    for sentence in re.split(r"[.;!?]", text):
        if not sentence.strip():
            continue
        if (
            found(UP, sentence)
            and found(DOWN, sentence)
            and found(r"\b(?:last year|previously|now|this year)\b", sentence)
        ):
            cost_ambiguous = True
        for comma_part in comma_clauses(sentence):
            # An explicit business identity is not an input purchase. Preserve
            # industry checks above; do not score the product in the identity.
            if (
                re.fullmatch(r"\s*we are an? [\w' -]+\s*", comma_part)
                and not found(COST_CONTEXT, comma_part)
                and not has_change(comma_part)
            ):
                antecedent = None
                continue
            raw, discarded = retained_cost_clause(comma_part.strip())
            if discarded:
                antecedent = None
                notes.append(discarded)
                continue
            cleaned, role_notes, is_outside = reader_pressure_text(raw)
            outside = outside or is_outside
            notes.extend(role_notes)
            parts, uncertain = positive_alternatives(cleaned)
            cost_ambiguous = cost_ambiguous or uncertain
            for part in parts:
                if found(OUTPUT, part) and not found(COST, part):
                    notes.append(note(part, "output_context"))
                    continue
                families = inputs(part)
                up, down = found(UP, part), found(DOWN, part)
                if up and down and not found(rf"{NEGATIVE}|\bneither\b", part):
                    cost_ambiguous = True
                if (
                    not families
                    and (up or down)
                    and not found(NEGATIVE, part)
                    and not found(OUTPUT, part)
                ):
                    if antecedent and found(r"\b(?:prices?|costs?|it|they|these|their)\b", part):
                        part = antecedent + " input " + part
                        families = inputs(part)
                    elif (
                        kept
                        and not found(LIVE, original)
                        and not m009_profile(part)["unrecognized"]
                    ):
                        cost_ambiguous = True
                if (
                    families
                    and (up or down)
                    and not found(COST_CONTEXT, part)
                    and not found(r"\b(?:cheaper|dearer|expensive)\b", part)
                ):
                    cost_ambiguous = True
                kept.append(part)
                if (
                    len(families) == 1
                    and not (up or down)
                    and found(r"\b(?:buy|buys|buying|purchase|costs?)\b", part)
                    and not found(NEGATIVE, part)
                ):
                    words = [w for w in tokens(re.sub(BUSINESS, " ", part)) if w in ALIASES]
                    antecedent = " ".join(words)
                else:
                    antecedent = None
    profile = m009_profile(". ".join(kept))
    profile["ignored"].extend(notes)
    if outside:
        profile["blocked"] = "outside_scope"
    if cost_ambiguous and not outside:
        profile["blocked"] = "ambiguous_cost_direction"
    if scope_ambiguous:
        profile["blocked"] = "ambiguous_business_scope"
    return profile


def describe_query(profile):
    blocked = profile["blocked"]
    value = (
        {"summary": REASONS[blocked], "ignored": profile["ignored"], "blocked": blocked}
        if blocked in REASONS
        else describe(profile)
    )
    value["pressure_directions"] = {key: sorted(v) for key, v in profile["directions"].items()}
    return value


def clarification(profile):
    if profile["blocked"] == "ambiguous_cost_direction":
        return {
            "kind": "cost_direction",
            "title": "Clarify which costs changed",
            "message": "Which input costs rose or fell, and over which period? Write one change per clause, for example: milk costs fell; energy costs rose. We have not assumed the missing direction.",
            "action": "Edit the cost description",
        }
    if profile["blocked"] == "ambiguous_business_scope":
        return {
            "kind": "business_scope",
            "title": "Clarify whose situation this is",
            "message": "What does your business do, and which business is the supplier or customer? State whose input costs changed so we do not assume another company's costs are yours.",
            "action": "Edit the business description",
        }
    return m009_clarification(profile)
