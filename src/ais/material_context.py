"""Explicit material names and directed, qualified comparison links (M012).

Only pressure text is read. No case IDs, companies, response/outcome fields or
ranking exceptions occur here. Source words never gain an unreported input name.
Index expansions are comparison links; explanations retain the narrower evidence.
"""

from collections import Counter
from math import log
import re

from ais.context import read_pressure, COST, UP, DOWN, found
from ais.language_context import (
    query_profile as sentence_profile,
    describe_query as sentence_description,
    clarification as sentence_clarification,
    note as sentence_note,
)
from ais.reader_context import coverage as original_coverage
from ais.vocabulary import FAMILIES as PREVIOUS

REASONS = {
    "material_not_established": "We couldn't match that input name to the indexed pressure evidence.",
}

# Existing families remain unchanged except for the broad oil alias. Synthetic
# lexical tokens let the sentence grammar bind a multiword material as one noun.
MATERIALS = {
    "fuel": ("fuel", "fuel fuels"),
    "diesel": ("diesel fuel", "matdiesel"),
    "petrol": ("petrol / gasoline", "matpetrol"),
    "natural_oil": ("natural fats and oils (type unspecified)", "matnatural"),
    "edible_oil": ("edible / cooking oil", "matedible"),
    "vegetable_oil": ("vegetable oil", "matvegetable"),
    "rice_bran_oil": ("rice bran oil", "matricebran"),
    "copra": ("copra / dried coconut kernel", "matcopra"),
    "petrochemical": ("petrochemical inputs", "matpetrochemical"),
    "petrochemical_raw": ("petrochemical raw materials", "matpetroraw"),
    "petrochemical_packaging": ("petrochemical packaging", "matpetropack"),
    "oil_distribution": ("oil-related distribution costs", "matoildistribution"),
    "oil_packaging": ("oil-related packaging costs", "matoilpackaging"),
    "paper": ("paper", "paper papers"),
    "cardboard": ("cardboard", "cardboard"),
    "unclear_oil": ("oil (type unclear)", "matunclearoil"),
    "unlisted_oil": ("named oil not established", "matunlistedoil"),
}
FAMILIES = {k: v for k, v in PREVIOUS.items() if k != "oil"} | MATERIALS

# Direction is important: a source naming rice bran oil supports a broader
# vegetable-oil comparison. Generic natural fats do not establish edible use.
PARENTS = {
    "diesel": {"fuel"},
    "petrol": {"fuel"},
    "rice_bran_oil": {"vegetable_oil", "edible_oil", "natural_oil"},
    "vegetable_oil": {"natural_oil"},
    "edible_oil": {"natural_oil"},
    "petrochemical_raw": {"petrochemical"},
    "petrochemical_packaging": {"petrochemical", "packaging"},
    "oil_distribution": {"transport"},
    "oil_packaging": {"packaging"},
}
# These links yield related-only evidence, never named-input coverage. Sibling
# fuels are not aliases: a named petrol report cannot establish diesel.
BROADER_LINKS = {
    "fuel": {"diesel", "petrol"},
    "oil_distribution": {"fuel", "diesel", "petrol"},
}


def encode(text):
    """Recognize bounded material phrases, retaining their original surface words."""
    text = text.lower().replace("’", "'")
    surface = {}

    def substitute(pattern, replacements):
        nonlocal text

        def replace(match):
            values = replacements(match) if callable(replacements) else replacements
            for key in values:
                surface.setdefault(key, set()).add(match[0])
            cue = " costs" if re.search(r"\bcosts?\b", match[0]) else ""
            return " and ".join(MATERIALS[key][1].split()[0] for key in values) + cue

        text = re.sub(pattern, replace, text)

    use = r"(?:distribution|transport|freight|shipping|delivery)"
    linked = r"oil[ -](?:related|linked)\s+(?:costs?\s+(?:for|of|in)\s+)?(?:both\s+)?"
    substitute(rf"\b{linked}{use}\s+and\s+packaging\b", ["oil_distribution", "oil_packaging"])
    substitute(rf"\b{linked}{use}\b", ["oil_distribution"])
    substitute(rf"\b{linked}packaging\b", ["oil_packaging"])
    substitute(
        r"\bpetrochemical\s+raw[ -]materials?\s+and\s+packaging\b",
        ["petrochemical_raw", "petrochemical_packaging"],
    )
    substitute(r"\bpetrochemical\s+packaging(?:\s+materials?)?\b", ["petrochemical_packaging"])
    substitute(r"\bpetrochemical\s+(?:raw[ -])?materials?\b", ["petrochemical_raw"])
    substitute(r"\bpetrochemicals?\b", ["petrochemical"])
    substitute(r"\brice[ -]+bran[ -]+oils?\b", ["rice_bran_oil"])
    substitute(
        r"\b(?:natural[ -]+fats?[ -]+and[ -]+oils?|natural[ -]+oils?|natural[ -]+fats?)\b",
        ["natural_oil"],
    )
    substitute(r"\b(?:edible|cooking)[ -]+oils?\b", ["edible_oil"])
    substitute(r"\bvegetable[ -]+oils?\b", ["vegetable_oil"])
    substitute(
        r"\bcopra(?:\s*\(dried coconut kernels?\))?|\bdried[ -]+coconut[ -]+kernels?(?:\s*\(copra\))?",
        ["copra"],
    )
    substitute(r"\bdiesel(?:\s+fuels?)?\b", ["diesel"])
    substitute(r"\b(?:petrol|gasoline)(?:\s+fuels?)?\b", ["petrol"])

    # A named unlisted oil never falls back to a broad oil-family match. Avoid
    # swallowing grammatical words in "higher oil costs" or "and oil prices".
    generic = {
        "and",
        "or",
        "higher",
        "lower",
        "rising",
        "falling",
        "the",
        "our",
        "my",
        "an",
        "of",
        "for",
        "buy",
        "buying",
        "input",
        "no",
        "never",
        "without",
        "unknown",
        "unestablished",
        "whether",
        "uncertain",
        "unclear",
        "with",
        "not",
    }

    def unknown(match):
        prefix = match[1] or ""
        key = "unclear_oil" if not prefix or prefix in generic else "unlisted_oil"
        surface.setdefault(key, set()).add(match[0] if key == "unlisted_oil" else "oil")
        return (prefix + " " if prefix and key == "unclear_oil" else "") + MATERIALS[key][1]

    text = re.sub(r"\b(?:([a-z]+)\s+)?oils?\b", unknown, text)
    return text, surface


def profile(text, *, query=False):
    encoded, surface = encode(text)
    original_reading = None
    identity_replacements = []
    output_notes = []
    if query:
        # Naming a manufactured/sold product is not a purchase-cost request.
        # Retain other words so an outside reader business cannot disappear.
        aliases = {word for _, terms in FAMILIES.values() for word in terms.split()}
        parts = re.split(
            r"([.;!?]|\b(?:but|while|whereas)\b|\band(?=\s+we\b)|,(?=\s*(?:we|i|our)\b))", encoded
        )
        for i in range(0, len(parts), 2):
            part = parts[i]
            identity = re.match(r"\s*we\s+(sell|make|produce|manufacture|bottle|process)\b", part)
            if not identity or found(
                r"\b(?:buy\w*|purchas\w*|inputs?|costs?|bills?|expenses?)\b", part
            ):
                continue
            if identity[1] != "sell" and found(f"{COST}|{UP}|{DOWN}", part):
                continue
            pieces = re.split(r"\b(in|with|using|from|out of)\b", part, maxsplit=1)
            # A container/ingredient after a use preposition is an input;
            # a product before it ("cooking oil in India") is still output.
            has_inputs = len(pieces) == 3 and any(
                w in aliases for w in re.findall(r"\b\w+\b", pieces[2])
            )
            pieces[0] = re.sub(
                r"\b\w+\b",
                lambda m: ("product" if has_inputs else "output") if m[0] in aliases else m[0],
                pieces[0],
            )
            masked = "".join(pieces)
            if masked != part:
                identity_replacements.append((masked.strip(), part.strip()))
                parts[i] = masked if has_inputs else ""
                if not has_inputs:
                    output_notes.append(sentence_note(part, "output_context"))
        if identity_replacements:
            original_reading = sentence_profile(encoded, vocabulary=FAMILIES)
            encoded = "".join(parts)
    value = (
        sentence_profile(encoded, vocabulary=FAMILIES)
        if query
        else read_pressure(encoded, families=FAMILIES)
    )
    if original_reading and original_reading["blocked"] == "outside_scope":
        value["blocked"] = "outside_scope"
    value["ignored"].extend(output_notes)
    for key in value["words"]:
        if key in surface:
            value["words"][key] = surface[key]
    for item in value["ignored"]:
        for masked, original in identity_replacements:
            item["text"] = re.sub(
                r"\s+".join(re.escape(w) for w in masked.split()), lambda _: original, item["text"]
            )
        for key, (_, aliases) in MATERIALS.items():
            if key in surface:
                item["text"] = item["text"].replace(
                    aliases.split()[0], " / ".join(sorted(surface[key]))
                )
    if query:
        ambiguous = (
            sorted(surface.get("unclear_oil", [])) if "unclear_oil" in value["words"] else []
        )
        unlisted = (
            sorted(surface.get("unlisted_oil", [])) if "unlisted_oil" in value["words"] else []
        )
        value["material_uncertainty"] = ambiguous
        value["unresolved"].extend(f"{name} (type unclear)" for name in ambiguous)
        value["unrecognized"] = sorted(set(value["unrecognized"]) | set(unlisted))
    for key in ("unclear_oil", "unlisted_oil"):
        value["words"].pop(key, None)
        value["directions"].pop(key, None)
    value["concepts"] = [
        key for key in value["concepts"] if key not in {"unclear_oil", "unlisted_oil"}
    ]
    return value


def index_concepts(report):
    """Explicit source concepts plus declared, directed comparison links."""
    result = []
    for key in report["concepts"]:
        result.extend([key, *sorted(PARENTS.get(key, set()) | BROADER_LINKS.get(key, set()))])
    return result


def scores(query, reports):
    """BM25 with actual mention lengths, not the number of alias expansions.

    Material-name links have half the term frequency of direct named evidence.
    A generic non-material family (e.g. packaging) keeps its existing weight.
    The pool, formula, k1 and b remain shared; no post-ranking outcome feature.
    """
    if not reports:
        return []
    lengths = [len(r["concepts"]) for r in reports]
    average = sum(lengths) / len(lengths)
    if not average:
        return [0.0] * len(reports)
    documents = [Counter(index_concepts(r)) for r in reports]
    direct = [Counter(r["concepts"]) for r in reports]
    result = [0.0] * len(reports)
    for term in set(query["concepts"]):
        df = sum(term in doc for doc in documents)
        idf = log(1 + (len(reports) - df + 0.5) / (df + 0.5))
        for i, doc in enumerate(documents):
            tf = direct[i][term] + (0.5 if term in MATERIALS else 1.0) * (
                doc[term] - direct[i][term]
            )
            if tf:
                result[i] += idf * tf * 2.2 / (tf + 1.2 * (0.25 + 0.75 * lengths[i] / average))
    return result


def relationship(requested, reported):
    if requested == reported:
        return "named_input"
    if requested in PARENTS.get(reported, set()):
        return "more_specific_source"
    if requested in BROADER_LINKS.get(reported, set()):
        return "broader_source"
    return None


def compatible_matches(query, report):
    if query["blocked"] or report["blocked"]:
        return [], query["blocked"] or "unsupported_direction"
    accepted, reason = [], None
    for requested in sorted(query["words"]):
        choices = []
        for reported in sorted(report["words"]):
            relation = relationship(requested, reported)
            if not relation:
                continue
            q = query["directions"][requested] - {"unspecified"}
            r = report["directions"][reported] - {"unspecified"}
            if ("up" in q and "down" in r) or ("down" in q and "up" in r):
                return [], "opposite_direction"
            if not r or (q and q != r):
                reason = "unsupported_direction"
                continue
            qwords, rwords = query["words"][requested], report["words"][reported]
            exact = qwords & rwords
            named = relation != "broader_source" and (
                requested in MATERIALS
                or bool(exact)
                or any(
                    re.search(rf"\b{re.escape(qword)}\b", rword)
                    for qword in qwords
                    for rword in rwords
                )
            )
            kind = (
                relation
                if requested in MATERIALS or reported in MATERIALS
                else "shared_word"
                if exact
                else "related_words"
            )
            choices.append(
                {
                    "family": requested,
                    "label": FAMILIES[requested][0],
                    "query_terms": sorted(qwords),
                    "report_terms": sorted(rwords),
                    "relationship": "shared_word" if exact else "related_terms",
                    "shared_words": sorted(exact),
                    "query_direction": next(iter(q)) if q else "unspecified",
                    "report_direction": next(iter(r)),
                    "match_kind": kind,
                    "named_input_established": named,
                    "explanation": (
                        "The cited pressure passage reports oil-related distribution costs; it does not name the requested fuel or fuel type."
                        if reported == "oil_distribution" and relation == "broader_source"
                        else "The source names only a broader fuel category, not the requested fuel type."
                        if relation == "broader_source"
                        else "The source names a more specific input within the requested category; other varieties are not established."
                        if relation == "more_specific_source"
                        else "Both descriptions name this input; grade, purchase basis and scope can still differ."
                        if kind == "named_input"
                        else "These are matching or related input words, not proof of identical purchases."
                    ),
                }
            )
        if choices:
            accepted.append(
                min(
                    choices,
                    key=lambda m: (
                        not m["named_input_established"],
                        m["match_kind"] != "named_input",
                        m["report_terms"],
                    ),
                )
            )
    return accepted, None if accepted else reason


def coverage(query, matches):
    value = original_coverage(query, matches)
    related = sorted(m["family"] for m in matches if not m["named_input_established"])
    value["related_only"] = related
    value["related_notes"] = [m["explanation"] for m in matches if not m["named_input_established"]]
    value["supported"] = sorted(set(value["supported"]) - set(related))
    value["supported_count"] = len(value["supported"])
    value["related_count"] = len(related)
    value["partial"] = value["partial"] or bool(related)
    return value


def describe_query(value):
    result = sentence_description(value)
    if not value["blocked"] and not value["words"]:
        if value.get("material_uncertainty"):
            result["summary"] = (
                "The oil type is unclear; we have not assumed fuel, a petrochemical material or a natural oil."
            )
        elif value["unrecognized"]:
            result["summary"] = REASONS["material_not_established"]
    return result


def clarification(value):
    if not value["blocked"] and value.get("material_uncertainty"):
        return {
            "kind": "material_input",
            "title": "Which oil or material do you buy?",
            "message": "Do you mean fuel, a petrochemical input, cooking oil or another natural oil? Name the purchased material. We have not treated these as interchangeable; other clearly named pressures can still have partial matches.",
            "action": "Edit the material description",
        }
    if value["blocked"] == "outside_scope":
        return None
    return sentence_clarification(value)
