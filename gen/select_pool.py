"""Pick exactly the target number of passing records per (generator, profession, gender).

pool.jsonl           full records incl. explanations, for the filters (both generators)
pool_training.jsonl  id, hard_text, profession, gender only, with Bias in Bios ints
                     (gender 0 = male, 1 = female); no explanations (both generators)
pool_<gen>.jsonl, pool_training_<gen>.jsonl
                     the same, one file per generator (e.g. pool_llama.jsonl)

Records listed in the config's optional exclude_ids_file (one id per line, e.g. bios used as
few-shot examples for the filters) are never selected.
"""
from __future__ import annotations

import argparse
import random
from collections import defaultdict
from pathlib import Path

from .common import (GENDERS, PROFESSIONS, cell_targets, load_config, load_refs, read_jsonl,
                     run_path, setup_stdout, stable_seed, write_json, write_jsonl)


def main(argv=None):
    setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--allow-shortfall", action="store_true",
                    help="write the pool even if some cells are below target")
    args = ap.parse_args(argv)
    cfg = load_config(args.config)
    targets = cell_targets(cfg, load_refs(cfg))

    excluded = set()
    if cfg.get("exclude_ids_file"):
        excluded = set(Path(cfg["exclude_ids_file"]).read_text(encoding="utf-8").split())
        print(f"Excluding {len(excluded)} ids listed in {cfg['exclude_ids_file']}")

    by_cell = defaultdict(list)
    for r in read_jsonl(run_path(cfg, "validated.jsonl")):
        if r["passed"] and r["id"] not in excluded:
            by_cell[(r["generator"], r["profession"], r["gender"])].append(r)

    pool, cells, short = [], [], []
    for gen in cfg["generators"]:
        for prof in cfg["professions"]:
            for g in cfg["genders"]:
                candidates = sorted(by_cell[(gen, prof, g)], key=lambda r: r["id"])
                random.Random(stable_seed(cfg["seed"], "select", gen, prof, g)).shuffle(candidates)
                target = targets[(prof, g)]
                kept = candidates[:target]
                pool += kept
                cell = {"generator": gen, "profession": prof, "gender": g, "target": target,
                        "available": len(candidates), "kept": len(kept)}
                cells.append(cell)
                if len(kept) < target:
                    short.append(cell)

    for c in short:
        print(f"short: {c['generator']}/{c['profession']}/{c['gender']} "
              f"{c['available']}/{c['target']}")
    if short and not args.allow_shortfall:
        raise SystemExit(f"{len(short)} cells are below target; run gen.plan --topup and "
                         "generate again, or pass --allow-shortfall.")

    pool.sort(key=lambda r: r["id"])

    def training_rows(records):
        return [{"id": r["id"], "hard_text": r["bio"],
                 "profession": PROFESSIONS[r["profession"]]["id"],
                 "gender": GENDERS[r["gender"]]["id"]} for r in records]

    write_jsonl(run_path(cfg, "pool.jsonl"), pool)
    write_jsonl(run_path(cfg, "pool_training.jsonl"), training_rows(pool))
    for gen in cfg["generators"]:
        own = [r for r in pool if r["generator"] == gen]
        write_jsonl(run_path(cfg, f"pool_{gen}.jsonl"), own)
        write_jsonl(run_path(cfg, f"pool_training_{gen}.jsonl"), training_rows(own))
    write_json(run_path(cfg, "pool_report.json"),
               {"n_records": len(pool), "short_cells": short, "cells": cells})
    print(f"Pool: {len(pool)} records -> {run_path(cfg, 'pool.jsonl')}")
    for gen in cfg["generators"]:
        print(f"  {gen}: {sum(r['generator'] == gen for r in pool)} -> pool_{gen}.jsonl, "
              f"pool_training_{gen}.jsonl")


if __name__ == "__main__":
    main()
