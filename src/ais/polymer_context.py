"""M013: specific polymer names, using the unchanged M012 grammar and scoring.

Sibling polymers never match one another. A specific source can support a
generic plastic request; generic plastic cannot establish a specific polymer.
No case, company, response or outcome rules.
"""

import re

from ais import material_context as previous

POLYMERS = {
    "hdpe": ("HDPE (high-density polyethylene)", "mathdpe"),
    "pet": ("PET (polyethylene terephthalate)", "matpet"),
    "ldpe": ("LDPE (low-density polyethylene)", "matldpe"),
    "pvc": ("PVC (polyvinyl chloride)", "matpvc"),
    "polypropylene": ("polypropylene", "matpolypropylene"),
}
MATERIALS = previous.MATERIALS | POLYMERS
FAMILIES = previous.FAMILIES | POLYMERS
PARENTS = previous.PARENTS | {key: {"resin"} for key in POLYMERS}


def encode(text):
    # Consume an adjacent generic label/definition once. Otherwise a query for
    # "PVC plastic" would fall back to generic plastic despite missing PVC.
    patterns = {
        "hdpe": r"(?:high[ -]+density[ -]+polyethylene(?:\s*\(hdpe\))?|hdpe(?:\s*\(high[ -]+density[ -]+polyethylene\))?)",
        "pet": r"(?:polyethylene[ -]+terephthalate(?:\s*\(pet\))?|pet(?:\s+resin)?(?:\s*\(polyethylene[ -]+terephthalate\))?)",
        "ldpe": r"(?:low[ -]+density[ -]+polyethylene(?:\s*\(ldpe\))?|ldpe)",
        "pvc": r"(?:polyvinyl[ -]+chloride(?:\s*\(pvc\))?|pvc)",
        "polypropylene": r"polypropylene",
    }
    surface = {}
    for key, pattern in patterns.items():

        def replace(match, key=key):
            surface.setdefault(key, set()).add(match[0].lower())
            return POLYMERS[key][1]

        # PET food/care and PET scans are different senses, not material inputs.
        sense = r"(?!\s+(?:food|foods|care|owner\w*|scan\w*|imaging)\b)" if key == "pet" else ""
        text = re.sub(
            rf"\b{pattern}(?!\w){sense}(?:\s+(?:resins?|plastics?|polymers?))?",
            replace,
            text,
            flags=re.I,
        )
    encoded, other = previous.encode(text)
    return encoded, other | surface


def profile(text, *, query=False):
    return previous.profile(
        text, query=query, encoder=encode, vocabulary=FAMILIES, material_types=MATERIALS
    )


def scores(query, reports):
    return previous.scores(query, reports, parents=PARENTS, material_types=MATERIALS)


def compatible_matches(query, report):
    matches, reason = previous.compatible_matches(
        query, report, parents=PARENTS, vocabulary=FAMILIES, material_types=MATERIALS
    )
    for match in matches:
        if match["family"] in POLYMERS:
            match["display_label"] = POLYMERS[match["family"]][0]
        if match["family"] == "resin" and match["match_kind"] == "more_specific_source":
            # A named polymer establishes the broad plastic category, while
            # never establishing another specific polymer in that category.
            match["named_input_established"] = True
    return matches, reason


def coverage(query, matches):
    result = previous.coverage(query, matches)
    for key in POLYMERS.keys() & result["names"].keys():
        result["names"][key] = POLYMERS[key][0]
    return result


describe_query = previous.describe_query
clarification = previous.clarification
