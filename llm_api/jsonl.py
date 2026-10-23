"""JSONL files (one JSON object per line) that survive interrupted runs."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def read_jsonl(path):
    """All rows of a JSONL file ([] if it doesn't exist). A half-written last line from an
    interrupted run is skipped with a warning; a broken line anywhere else is an error."""
    path = Path(path)
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    rows = []
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            if i == len(lines) - 1:
                print(f"warning: ignoring incomplete last line of {path}", file=sys.stderr)
                continue
            raise ValueError(f"{path}:{i + 1}: invalid JSON line") from None
    return rows


class JsonlAppender:
    """Appends one JSON object per line and flushes, so an interrupted run loses at most one line."""

    def __init__(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and path.stat().st_size:
            with open(path, "rb+") as f:
                f.seek(-1, os.SEEK_END)
                if f.read(1) != b"\n":  # drop a half-written last line before appending
                    f.seek(0)
                    f.truncate(f.read().rfind(b"\n") + 1)
        self.f = open(path, "a", encoding="utf-8")

    def write(self, row):
        self.f.write(json.dumps(row, ensure_ascii=False) + "\n")
        self.f.flush()

    def close(self):
        self.f.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


def write_jsonl(path, rows):
    """Write all rows at once (via a temp file, so a crash never leaves a half-written file)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    os.replace(tmp, path)
