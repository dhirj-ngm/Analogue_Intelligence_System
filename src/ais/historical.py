"""Verify historical code against immutable Git blobs; data stays strictly current.

M009 changes these explicit runtime/UI files. Older packets/results continue to
use the original method and renderer. No case or evidence hash is exempted.
"""

from hashlib import sha256
import subprocess

from ais.pilot import ROOT

M008_COMMIT = "1e4e6d36fcfa95fc02c1d2a8f44f81be54129c61"
VERSIONED_FILES = {
    "scripts/check_collection_m007.py",
    "src/ais/search.py",
    "src/ais/relevance.py",
    "assets/app/reader.mjs",
    "assets/app/app.js",
    "assets/app/index.html",
    "assets/app/app.css",
}


def frozen_bytes(path, expected):
    current = (ROOT / path).read_bytes()
    if sha256(current).hexdigest() == expected:
        return current
    if path not in VERSIONED_FILES:
        raise ValueError(f"Frozen input changed: {path}")
    original = subprocess.check_output(["git", "show", f"{M008_COMMIT}:{path}"], cwd=ROOT)
    if sha256(original).hexdigest() != expected:
        raise ValueError(f"Historical code hash mismatch: {path}")
    return original
