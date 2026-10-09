"""Shared helpers: config, JSONL files, stable seeds, the profession table, gender detection."""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

import yaml


def _prof(id_, display, plural, article, title_terms, workplace):
    return {"id": id_, "display": display, "plural": plural, "article": article,
            "title_terms": title_terms, "workplace": workplace}


# Keys are config names; "id" is the Bias in Bios profession int. The HF dataset has plain int
# columns (no ClassLabel names), so the ids come from the dataset card. title_terms are banned
# whole words in generated bios (case-insensitive).
PROFESSIONS = {
    "surgeon": _prof(25, "surgeon", "surgeons", "a", ["surgeon", "surgeons"], "hospital"),
    "physician": _prof(19, "physician", "physicians", "a", ["physician", "physicians"],
                       "medical practice"),
    "nurse": _prof(13, "nurse", "nurses", "a", ["nurse", "nurses"], "hospital"),
    "software_engineer": _prof(24, "software engineer", "software engineers", "a",
                               ["software engineer", "software engineers",
                                "software developer", "software developers"], "tech company"),
    "architect": _prof(1, "architect", "architects", "an", ["architect", "architects"],
                       "architecture firm"),
    "attorney": _prof(2, "attorney", "attorneys", "an",
                      ["attorney", "attorneys", "lawyer", "lawyers"], "law firm"),
    "psychologist": _prof(22, "psychologist", "psychologists", "a",
                          ["psychologist", "psychologists"], "counseling practice"),
    "teacher": _prof(26, "teacher", "teachers", "a", ["teacher", "teachers"], "school"),
    # Spares, in case the profession list changes.
    "paralegal": _prof(15, "paralegal", "paralegals", "a", ["paralegal", "paralegals"], "law firm"),
    "dietitian": _prof(7, "dietitian", "dietitians", "a",
                       ["dietitian", "dietitians", "dietician", "dieticians",
                        "nutritionist", "nutritionists"], "nutrition clinic"),
    "journalist": _prof(11, "journalist", "journalists", "a",
                        ["journalist", "journalists", "reporter", "reporters"], "newsroom"),
    "professor": _prof(21, "professor", "professors", "a", ["professor", "professors"],
                       "university"),
    "dentist": _prof(6, "dentist", "dentists", "a", ["dentist", "dentists"], "dental clinic"),
    "painter": _prof(14, "painter", "painters", "a", ["painter", "painters"], "studio"),
}

# Bias in Bios gender ints: 0 = male, 1 = female.
GENDERS = {
    "male": {"id": 0, "pronouns": "he/him/his", "noun": "man"},
    "female": {"id": 1, "pronouns": "she/her/hers", "noun": "woman"},
}

PROMPT_TYPES = (0, 1, 4)
BACKENDS = ("openai_compat", "openai_batch", "mock")
VALIDATE_DEFAULTS = {"min_words": 50, "max_words": 180, "min_explanation_words": 8,
                     "shingle_n": 8, "max_shingle_overlap": 0.3, "opening_share_warn": 0.05}
COUNTS_DEFAULTS = {"gender_ratio": "balanced", "overgen": 1.2, "min_yield": 0.02,
                   "max_topup_calls": 5000}
GENERATOR_DEFAULTS = {"concurrency": 8, "retries": 5, "send_seed": True, "json_mode": True,
                      "timeout": 60, "backoff_base": 1.0}


def load_config(path):
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    required = ("run_name", "seed", "output_dir", "refs_file", "professions", "genders",
                "prompt", "counts", "sampling", "generators")
    missing = [k for k in required if k not in cfg]
    if missing:
        raise SystemExit(f"{path}: missing config keys {missing}")
    unknown = [p for p in cfg["professions"] if p not in PROFESSIONS]
    if unknown:
        raise SystemExit(f"Unknown professions {unknown}; add them to PROFESSIONS in gen/common.py")
    if sorted(cfg["genders"]) != ["female", "male"]:
        raise SystemExit("genders must be [male, female]")
    if cfg["prompt"]["type"] not in PROMPT_TYPES:
        raise SystemExit(f"prompt.type must be one of {PROMPT_TYPES}")
    cfg["counts"] = {**COUNTS_DEFAULTS, **cfg["counts"]}
    if cfg["counts"]["gender_ratio"] not in ("balanced", "refs"):
        raise SystemExit("counts.gender_ratio must be 'balanced' or 'refs'")
    cfg["validate"] = {**VALIDATE_DEFAULTS, **(cfg.get("validate") or {})}
    for name, gen in cfg["generators"].items():
        gen = cfg["generators"][name] = {**GENERATOR_DEFAULTS, **gen}
        if gen.get("backend") not in BACKENDS:
            raise SystemExit(f"generators.{name}.backend must be one of {BACKENDS}")
    cfg["config_path"] = str(path)
    return cfg


def run_path(cfg, name):
    out = Path(cfg["output_dir"])
    out.mkdir(parents=True, exist_ok=True)
    return out / name


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def setup_stdout():
    """Bios can contain characters a Windows console code page can't print."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except AttributeError:
            pass


# ---------------------------------------------------------------- files

def read_jsonl(path):
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
            if i == len(lines) - 1:  # half-written last line from an interrupted run
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
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


def write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def sha256_file(path):
    path = Path(path)
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------- seeds and counts

def stable_seed(*parts):
    """Seed that is the same on every machine and run (Python's hash() is salted per process)."""
    digest = hashlib.sha256("|".join(map(str, parts)).encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big") & 0x7FFFFFFF


def largest_remainder(weights, n):
    """Split n over the keys of weights (ints) proportionally; totals exactly n."""
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("weights must sum to a positive number")
    quotas = {k: n * w // total for k, w in weights.items()}
    order = list(weights)
    by_remainder = sorted(order, key=lambda k: (-(n * weights[k] % total), order.index(k)))
    for k in by_remainder[:n - sum(quotas.values())]:
        quotas[k] += 1
    return quotas


def load_refs(cfg):
    refs = read_jsonl(cfg["refs_file"])
    if not refs:
        raise SystemExit(f"No reference bios in {cfg['refs_file']}; run gen.prepare_refs first.")
    return refs


def cell_targets(cfg, refs):
    """Records to keep per (profession, gender) for each generator."""
    n = cfg["counts"]["per_profession"]
    targets = {}
    for prof in cfg["professions"]:
        if cfg["counts"]["gender_ratio"] == "balanced":
            weights = {g: 1 for g in cfg["genders"]}
        else:
            weights = {g: sum(r["profession"] == prof and r["gender"] == g for r in refs)
                       for g in cfg["genders"]}
            if not sum(weights.values()):
                raise SystemExit(f"No reference bios for {prof} in {cfg['refs_file']}")
        for g, k in largest_remainder(weights, n).items():
            targets[(prof, g)] = k
    return targets


# ---------------------------------------------------------------- text

def tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def word_count(text):
    return len(text.split())


MALE_PRONOUNS = {"he", "him", "his", "himself"}
FEMALE_PRONOUNS = {"she", "her", "hers", "herself"}


def detect_gender(text):
    """'male' / 'female' from pronouns, or None if there are none or both kinds are common.

    A bio about a man can mention his wife ("she"), so one gender has to clearly dominate (3:1).
    """
    toks = tokens(text)
    m = sum(t in MALE_PRONOUNS for t in toks)
    f = sum(t in FEMALE_PRONOUNS for t in toks)
    if m >= max(1, 3 * f):
        return "male"
    if f >= max(1, 3 * m):
        return "female"
    return None


@lru_cache(maxsize=None)
def title_pattern(profession):
    terms = sorted(PROFESSIONS[profession]["title_terms"], key=len, reverse=True)
    alternatives = [r"\s+".join(map(re.escape, t.split())) for t in terms]
    return re.compile(r"\b(?:" + "|".join(alternatives) + r")\b", re.IGNORECASE)


def has_title(text, profession):
    return bool(title_pattern(profession).search(text))
