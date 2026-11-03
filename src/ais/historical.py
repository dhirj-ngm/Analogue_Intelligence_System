"""Verify historical code against immutable Git blobs; data stays strictly current.

M009/M010/M011 change these explicit runtime/UI files. Older packets/results continue to
use the original method and renderer. No case or evidence hash is exempted.
"""

from hashlib import sha256
import subprocess

from ais.pilot import ROOT

M010_COMMIT = "13814c27e3f5efab6142ba3c4bbd1fededccd611"
M009_COMMIT = "d63b3c341fc72277abc235d292efe1ab721f36c8"
M008_COMMIT = "1e4e6d36fcfa95fc02c1d2a8f44f81be54129c61"
VERSIONED_FILES = {
    "scripts/check_collection_m007.py",
    "scripts/evaluate_m009.py",
    "scripts/evaluate_m010.py",
    "src/ais/collection.py",
    "src/ais/historical.py",
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
    for commit in (M010_COMMIT, M009_COMMIT, M008_COMMIT):
        original = subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)
        if sha256(original).hexdigest() == expected:
            return original
    raise ValueError(f"Historical code hash mismatch: {path}")
