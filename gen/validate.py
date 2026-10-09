"""Parse raw responses, run the checks, and write validated.jsonl + validation_report.json.

Every response is kept; failed ones are marked with which checks failed. Records are processed
in id order so the near-duplicate check (which compares against previously accepted bios) is
deterministic.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict

from .common import (cell_targets, detect_gender, has_title, load_config, load_refs, read_jsonl,
                     run_path, setup_stdout, tokens, word_count, write_json, write_jsonl)

CHECKS = ("json_ok", "not_truncated", "bio_nonempty", "explanation_ok", "no_title", "length_ok",
          "gender_ok", "not_duplicate")


def parse_output(raw):
    """Return the {"bio", "explanation"} dict from a model response, or None."""
    if not raw:
        return None
    text = raw.strip()
    fenced = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, re.S)
    if fenced:
        text = fenced.group(1)
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start < 0 or end <= start:
            return None
        try:
            obj = json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            return None
    if not isinstance(obj, dict) or not isinstance(obj.get("bio"), str) \
            or not isinstance(obj.get("explanation"), str):
        return None
    return obj


def shingles(text, n):
    toks = tokens(text)
    return {" ".join(toks[i:i + n]) for i in range(len(toks) - n + 1)}


def opening(text):
    return " ".join(tokens(text)[:4])


def check_record(raw, row, cfg, seen):
    v = cfg["validate"]
    gen_cfg = cfg["generators"][row["generator"]]
    parsed = parse_output(raw.get("raw"))
    bio = (parsed or {}).get("bio", "").strip()
    explanation = (parsed or {}).get("explanation", "").strip()
    checks = dict.fromkeys(CHECKS)  # None = not run (the JSON didn't parse)
    checks["json_ok"] = parsed is not None
    checks["not_truncated"] = raw.get("finish_reason") != "length"
    detected, overlap, bio_shingles = None, None, set()
    if parsed is not None:
        detected = detect_gender(bio)
        bio_shingles = shingles(bio, v["shingle_n"])
        overlap = len(bio_shingles & seen) / len(bio_shingles) if bio_shingles else 0.0
        checks.update(
            bio_nonempty=bool(bio),
            explanation_ok=word_count(explanation) >= v["min_explanation_words"],
            no_title=not has_title(bio, row["profession"]),
            length_ok=v["min_words"] <= word_count(bio) <= v["max_words"],
            gender_ok=(detected == row["target_gender"] if row["target_gender"]
                       else detected is not None),
            not_duplicate=overlap <= v["max_shingle_overlap"])
    passed = all(checks.values())
    record = {
        "id": row["id"], "generator": row["generator"], "provider": gen_cfg.get("provider"),
        "model_id": gen_cfg.get("model"), "model_returned": raw.get("model_returned"),
        "profession": row["profession"], "target_gender": row["target_gender"],
        "gender": detected, "prompt_type": row["prompt_type"],
        "contrastive_order": row["contrastive_order"], "bio": bio, "explanation": explanation,
        "ref_ids": row["ref_ids"], "seed": row["seed"], "prompt_version": row["prompt_version"],
        "temperature": cfg["sampling"]["temperature"], "top_p": cfg["sampling"]["top_p"],
        "topup_round": row.get("topup_round", 0), "finish_reason": raw.get("finish_reason"),
        "usage": raw.get("usage"), "word_count": word_count(bio),
        "max_shingle_overlap": None if overlap is None else round(overlap, 4),
        "checks": checks, "passed": passed,
    }
    return record, (bio_shingles if passed else set())


def main(argv=None):
    setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", required=True)
    args = ap.parse_args(argv)
    cfg = load_config(args.config)
    v = cfg["validate"]

    plan = {r["id"]: r for r in read_jsonl(run_path(cfg, "plan.jsonl"))}
    raws, unknown = [], 0
    for gen in cfg["generators"]:
        seen_ids = set()
        for raw in read_jsonl(run_path(cfg, f"raw_{gen}.jsonl")):
            if raw["id"] in seen_ids:
                continue
            if raw["id"] not in plan:
                unknown += 1
                continue
            seen_ids.add(raw["id"])
            raws.append(raw)
    raws.sort(key=lambda r: r["id"])
    if unknown:
        print(f"warning: skipped {unknown} raw responses whose id is not in plan.jsonl")

    refs = load_refs(cfg)
    seen = set()
    for r in refs:
        seen |= shingles(r["text"], v["shingle_n"])
    records = []
    for raw in raws:
        record, accepted = check_record(raw, plan[raw["id"]], cfg, seen)
        seen |= accepted
        records.append(record)
    write_jsonl(run_path(cfg, "validated.jsonl"), records)

    # ------------------------------------------------------------ report
    targets = cell_targets(cfg, refs)
    report = {"n_records": len(records), "n_passed": sum(r["passed"] for r in records),
              "failures": {}, "passed_per_cell": {}, "short_cells": [], "gender_rates": {},
              "openings": {}, "avg_tokens": {}, "unresolved_errors": {}, "warnings": []}
    for gen in cfg["generators"]:
        recs = [r for r in records if r["generator"] == gen]
        report["failures"][gen] = {c: sum(r["checks"][c] is False for r in recs) for c in CHECKS}
        passed = Counter((r["profession"], r["gender"]) for r in recs if r["passed"])
        report["passed_per_cell"][gen] = {
            p: {g: {"passed": passed[(p, g)], "target": targets[(p, g)]} for g in cfg["genders"]}
            for p in cfg["professions"]}
        report["short_cells"] += [
            {"generator": gen, "profession": p, "gender": g, "passed": passed[(p, g)],
             "target": targets[(p, g)]}
            for p in cfg["professions"] for g in cfg["genders"] if passed[(p, g)] < targets[(p, g)]]
        # Which gender the generator wrote, among parsed bios (the key finding for types 0/4).
        rates = defaultdict(Counter)
        for r in recs:
            if r["checks"]["json_ok"] and r["bio"]:
                rates[r["profession"]][r["gender"] or "unclear"] += 1
        report["gender_rates"][gen] = {p: dict(rates[p]) for p in cfg["professions"]}
        openings = Counter(opening(r["bio"]) for r in recs if r["passed"])
        n_passed = sum(openings.values())
        report["openings"][gen] = [[o, round(c / n_passed, 4)] for o, c in openings.most_common(10)]
        for o, share in report["openings"][gen]:
            if share > v["opening_share_warn"]:
                report["warnings"].append(f"{gen}: {share:.1%} of passed bios open with '{o}...'")
        usage = [r["usage"] for r in recs if r["usage"] and r["usage"].get("prompt_tokens")]
        if usage:
            report["avg_tokens"][gen] = {
                k: round(sum(u[k] or 0 for u in usage) / len(usage), 1)
                for k in ("prompt_tokens", "completion_tokens")}
        done = {r["id"] for r in recs}
        report["unresolved_errors"][gen] = len(
            {e["id"] for e in read_jsonl(run_path(cfg, f"errors_{gen}.jsonl"))} - done)
    write_json(run_path(cfg, "validation_report.json"), report)

    print(f"Validated {report['n_records']} records, {report['n_passed']} passed.")
    for gen in cfg["generators"]:
        n = sum(r["generator"] == gen for r in records)
        fails = ", ".join(f"{c} {k}" for c, k in report["failures"][gen].items() if k)
        print(f"  {gen}: {n} records; failed checks: {fails or 'none'}")
        if report["unresolved_errors"][gen]:
            print(f"  {gen}: {report['unresolved_errors'][gen]} calls only in errors file "
                  "(rerun generate)")
    if cfg["prompt"]["type"] != 1:
        print("Gender the generators chose (parsed bios):")
        for gen, by_prof in report["gender_rates"].items():
            for p, c in by_prof.items():
                print(f"  {gen}/{p}: {c.get('male', 0)} M, {c.get('female', 0)} F, "
                      f"{c.get('unclear', 0)} unclear")
    for w in report["warnings"]:
        print(f"WARNING: {w}")
    if report["short_cells"]:
        print(f"{len(report['short_cells'])} cells below target "
              "(run gen.plan --topup, then generate again):")
        for c in report["short_cells"]:
            print(f"  {c['generator']}/{c['profession']}/{c['gender']}: "
                  f"{c['passed']}/{c['target']}")
    else:
        print("All cells reached their target.")


if __name__ == "__main__":
    main()
