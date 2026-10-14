"""Provenance: one manifest.jsonl line per generate run.

Each entry is appended as one complete line in a single write (no rewrite, no crash cleanup), so
two generators started at the same moment can't clash over the file or cut off each other's line.
"""
from __future__ import annotations

import json
import platform
import sys
from importlib import metadata

from .common import now, run_path, sha256_file

PACKAGES = ("openai", "PyYAML", "datasets", "numpy", "pandas")


def _version(package):
    try:
        return metadata.version(package)
    except metadata.PackageNotFoundError:
        return None


def append_manifest(cfg, step, generator, note=None):
    entry = {
        "time": now(), "step": step, "generator": generator,
        # The config only holds the *name* of the API key's env var, never the key.
        "generator_config": cfg["generators"][generator],
        "sampling": cfg["sampling"], "prompt": cfg["prompt"], "counts": cfg["counts"],
        "config_path": cfg["config_path"],
        "sha256": {"config": sha256_file(cfg["config_path"]),
                   "template": sha256_file(cfg["prompt"]["template"]),
                   "refs": sha256_file(cfg["refs_file"]),
                   "plan": sha256_file(run_path(cfg, "plan.jsonl"))},
        "python": sys.version, "platform": platform.platform(),
        "packages": {p: _version(p) for p in PACKAGES},
    }
    if note:
        entry["note"] = note
    with open(run_path(cfg, "manifest.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
