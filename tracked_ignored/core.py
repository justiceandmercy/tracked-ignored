"""Core logic for tracked-ignored."""

import fnmatch
import os
import subprocess
from typing import List, Set


# Files that are almost never meant to be committed.
DANGEROUS_PATTERNS = [
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "*.p12",
    "*.pfx",
    "id_rsa",
    "id_ed25519",
    "id_ecdsa",
    "*.keystore",
    "*.jks",
]

ARTIFACT_PATTERNS = [
    "node_modules/*",
    "dist/*",
    "build/*",
    ".next/*",
    "__pycache__/*",
    "*.log",
    "*.pyc",
    ".DS_Store",
]


def _git(root: str, args: List[str], stdin: str = None) -> str:
    proc = subprocess.run(
        ["git", "-C", root] + args,
        input=stdin,
        capture_output=True,
        text=True,
    )
    return proc.stdout


def tracked_files(root: str) -> List[str]:
    out = _git(root, ["ls-files"])
    return [line for line in out.splitlines() if line.strip()]


def ignored_tracked(root: str, files: List[str]) -> Set[str]:
    if not files:
        return set()
    out = _git(root, ["check-ignore", "--stdin"], stdin="\n".join(files) + "\n")
    return set(line for line in out.splitlines() if line.strip())


def _matches(path: str, patterns: List[str]) -> bool:
    base = os.path.basename(path)
    for pat in patterns:
        if fnmatch.fnmatch(base, pat) or fnmatch.fnmatch(path, pat):
            return True
    return False


def dangerous_tracked(files: List[str]) -> List[str]:
    return sorted(f for f in files if _matches(f, DANGEROUS_PATTERNS))


def artifact_tracked(files: List[str]) -> List[str]:
    return sorted(f for f in files if _matches(f, ARTIFACT_PATTERNS))


def run(root: str) -> dict:
    files = tracked_files(root)
    ignored = ignored_tracked(root, files)
    dangerous = dangerous_tracked(files)
    artifacts = artifact_tracked(files)
    # de-dup: a file already reported as ignored-tracked need not be re-reported
    artifact_set = set(artifacts) - ignored
    dangerous_set = set(dangerous) - ignored
    return {
        "root": os.path.abspath(root),
        "total_tracked": len(files),
        "ignored_tracked": sorted(ignored),
        "dangerous": sorted(dangerous_set),
        "artifacts": sorted(artifact_set),
    }
