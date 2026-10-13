"""Provenance: one manifest.json entry per generate / batch submit."""
from __future__ import annotations

import json
import platform
import sys
from importlib import metadata

from .common import now, run_path, sha256_file, write_json

PACKAGES = ("openai", "PyYAML", "datasets", "numpy", "pandas")


def _version(package):
    try:
        return metadata.version(package)
    except metadata.PackageNotFoundError:
        return None


def append_manifest(cfg, step, generator):
    path = run_path(cfg, "manifest.json")
    entries = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    entries.append({
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
    })
    write_json(path, entries)
