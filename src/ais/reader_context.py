"""M009 query roles and evidence coverage, without new material synonyms.

Case scoring still reads only the frozen pressure passages with the old grammar.
These limited rules distinguish explicit reader/supplier roles, not every sentence.
"""

import re

from ais.context import OUTSIDE, NEGATIVE, COST, fragments, found, read_pressure
from ais.pilot import tokens
from ais.vocabulary import FAMILIES

OUTSIDE_BUSINESS = f"(?:{OUTSIDE}|\\blogistics (?:company|business|supplier)\\b)"
ROLE = r"(?:suppliers?|vendors?|carriers?|providers?|customers?|clients?)"
LIVE = r"\blive[ -]+animals?\b"
EXTRA_REASONS = {
    "supplier_context": "A supplier or customer reference alone does not establish your input-cost pressure."
}


def reader_pressure_text(text):
    """Set aside explicit third-party descriptions; retain reader cost clauses."""
    retained, notes = [], []
    own_outside = False
    for sentence in re.split(r"[.!?;]", text.lower().replace("’", "'")):
        if not sentence.strip():
            continue
        # Bound an explicit reader business before a relationship such as
        # "using a logistics provider". A food supplier cannot excuse an airline.
        own = re.search(
            r"\bwe\s+(?:are|run|operate|own)\s+(.+?)(?=\b(?:and|using|with|that|which|from)\b|$)",
            sentence,
        )
        ours = re.search(
            rf"\bour\s+((?:(?!(?:{ROLE}|is|are|serves|supplies)\b)[\w-]+\s+){{0,3}}(?:business|company|firm|operation))\b",
            sentence,
        )
        if any(
            m and not found(NEGATIVE, m.group(1)) and found(OUTSIDE_BUSINESS, m.group(1))
            for m in (own, ours)
        ):
            own_outside = True
        if not found(OUTSIDE_BUSINESS, sentence):
            retained.append(sentence)
            continue
        removed = []
        changed = False
        reverse = re.search(
            rf"\b(?:are|is)\s+our\s+{ROLE}\b|\b(?:us|our\b[^.!?;]{{0,60}})\s+as\s+(?:an?|their)\s+{ROLE}\b",
            sentence,
        )
        external = re.search(rf"\b(?:our|the|an?|their)\s+(?:[\w-]+\s+){{0,4}}{ROLE}\b", sentence)
        if reverse:
            removed.append(sentence.strip())
            sentence = ""
            changed = True
        elif external and (
            re.search(r"\bcharg\w*\s+(?:us|our)\b", sentence)
            or (
                sentence[external.start() :].startswith("our ")
                and found(r"\b(?:prices?|rates?|fees?|charges?)\b", sentence)
                and found(r"\b(?:rais\w*|increas\w*|higher|lower)\b", sentence)
            )
        ):
            removed.append(sentence[external.start() : external.end()])
            sentence = sentence[: external.start()] + sentence[external.end() :]
            changed = True
        elif external and not re.search(r"\bcharg\w*\s+(?:us|our)\b", sentence):
            # A third party's own fuel bill is not automatically our input cost.
            prefix = sentence[: external.start()]
            if not prefix.strip() or prefix.strip() in {"and", "but"}:
                removed.append(sentence.strip())
                sentence = ""
                changed = True
            elif re.search(r"\band\s*$", prefix):
                removed.append(sentence[external.start() :].strip())
                sentence = prefix.rsplit("and", 1)[0]
                changed = True
        # Explicit relational phrases leave the purchased input/cost statement.
        relation = re.compile(
            rf"\b(?:from|using|use|via|through|charged by|by)\s+"
            rf"(?:(?:a|an|our|its|their|the)\s+)?(?:[\w-]+\s+){{0,3}}?"
            rf"{OUTSIDE_BUSINESS}(?:\s+{ROLE})?(?:\s+(?:that|which)\s+[^.!?;]+)?",
            re.I,
        )
        removed.extend(m.group(0) for m in relation.finditer(sentence))
        sentence, count = relation.subn(" ", sentence)
        active = re.compile(
            rf"\b(?:an?|the)?\s*{OUTSIDE_BUSINESS}(?:\s+{ROLE})?\s+(?:supplies|delivers to|serves)\s+(?:us|our)\b",
            re.I,
        )
        removed.extend(m.group(0) for m in active.finditer(sentence))
        sentence, active_count = active.subn(" ", sentence)
        count += active_count
        changed = changed or bool(count)
        if changed:
            notes.extend(
                {
                    "text": part,
                    "reason": "supplier_context",
                    "message": "A supplier's or customer's industry does not set your business type or establish your own costs.",
                }
                for part in removed
            )
        retained.append(sentence)
    cleaned = ". ".join(retained)
    # Unassigned outside-industry mentions remain conservative, including roles
    # these simple patterns could not separate.
    remaining_outside = any(
        not found(NEGATIVE, part) and found(OUTSIDE_BUSINESS, part) for part in fragments(cleaned)
    )
    return cleaned, notes, own_outside or remaining_outside


GENERIC = set(
    "a an the our your their my its we i they is are was were have has had "
    "and or for from of in on at to by with as after before compared last year "
    "higher lower rising falling increased decreased purchasing purchase road "
    "input inputs raw material materials raw-material production business company "
    "consumer goods all total overall actual own prices price cost costs bill bills "
    "expenses more less sharply significantly".split()
)


def query_profile(text, *, vocabulary=FAMILIES):
    cleaned, notes, outside = reader_pressure_text(text)
    profile = read_pressure(cleaned, families=vocabulary)
    if outside:
        profile["blocked"] = "outside_scope"
    profile["ignored"].extend(notes)
    live = []
    unknown = set()
    aliases = {word for _, terms in vocabulary.values() for word in terms.split()}
    for clause in fragments(cleaned):
        if found(NEGATIVE, clause):
            continue
        if found(LIVE, clause) and (
            found(COST, clause) or found(r"\b(?:buy|buys|buying|bought|purchase\w*)\b", clause)
        ):
            live.append("live-animal purchases")
        # Unknown names in explicit cost requests are display-only, never aliases
        # or terms added to BM25. Business/product identity without costs is not
        # treated as another requested pressure.
        for match in re.finditer(
            r"((?:\b[a-z][a-z-]*\b[\s,/-]+){0,10})\b(?:costs?|prices?|bills?|expenses?)\b", clause
        ):
            prefix = match.group(1)
            if found(LIVE, prefix):
                continue
            # Read a local noun/list phrase, not instructional or business
            # context preceding it. Related adjectives do not create additional
            # pressures ("plastic bottle" is one named material phrase).
            prefix = re.split(
                r"\b(?:faces?|facing|paying|want|example|that|separates?|company|business|maker|manufacturer)\b",
                prefix,
            )[-1]
            for part in re.split(r",|\band\b|\bor\b", prefix):
                words = [word for word in tokens(part) if word not in GENERIC]
                if not words or any(word in aliases for word in words):
                    continue
                if live and set(words) <= {"beef"}:
                    continue
                unknown.add(words[-1])
    profile["unresolved"] = sorted(set(live)) if not outside else []
    profile["unrecognized"] = sorted(unknown)
    return profile


def clarification(profile):
    if not profile["unresolved"]:
        return None
    return {
        "kind": "live_animal_input",
        "message": "Do you mean buying cattle, or a different live animal? Name the input you buy and say whether its costs rose or fell. Beef selling prices and sales are different from cattle purchase costs.",
        "action": "Edit the input description",
    }


def coverage(profile, matches):
    supported = sorted(m["family"] for m in matches)
    missing = sorted(set(profile["words"]) - set(supported))
    names = {key: " / ".join(sorted(words)) for key, words in profile["words"].items()}
    unknown = profile["unrecognized"]
    unresolved = profile["unresolved"]
    return {
        "supported": supported,
        "missing": missing,
        "names": names,
        "unrecognized": unknown,
        "unresolved": unresolved,
        "supported_count": len(supported),
        "identified_count": len(profile["words"]) + len(unknown) + len(unresolved),
        "partial": bool(missing or unknown or unresolved),
    }
