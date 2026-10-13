"""Render every generation prompt up front into plan.jsonl (one row per API call).

Saving the rendered prompt makes the run auditable and lets the live and batch backends send
identical inputs. --topup appends calls for (generator, profession, gender) cells that are still
short after gen.validate.
"""
from __future__ import annotations

import argparse
import math
import random
import re
from collections import Counter
from pathlib import Path
from string import Template

from .common import (GENDERS, PROFESSIONS, cell_targets, load_config, load_refs, read_jsonl,
                     run_path, setup_stdout, stable_seed, write_jsonl)

PAIRS = {"man_first": "A man and a woman", "woman_first": "A woman and a man"}


def render_prompt(cfg, template, profession, gender, refs, order):
    p = PROFESSIONS[profession]
    examples = "\n\n".join(f"Example {i}: {' '.join(r['text'].split())}"
                           for i, r in enumerate(refs, 1))
    return template.substitute(
        refs=examples, profession=p["display"], a_profession=f"{p['article']} {p['display']}",
        profession_plural=p["plural"], workplace=p["workplace"], gender=gender or "",
        pronouns=GENDERS[gender]["pronouns"] if gender else "",
        pair=PAIRS[order] if order else "",
        min_words=cfg["prompt"]["min_words"], max_words=cfg["prompt"]["max_words"])


def make_row(cfg, template, refs_by_prof, generator, profession, gender, k, topup_round=0):
    row_id = f"{cfg['run_name']}_{generator}_{profession}_{gender or 'any'}_{k:05d}"
    rng = random.Random(stable_seed(cfg["seed"], row_id, "plan"))
    pool = refs_by_prof[profession]
    n_refs = cfg["prompt"]["n_refs"]
    if len(pool) < n_refs:
        raise SystemExit(f"Only {len(pool)} reference bios for {profession}; need {n_refs}.")
    chosen = rng.sample(pool, n_refs)
    order = rng.choice(sorted(PAIRS)) if cfg["prompt"]["type"] == 4 else None
    return {"id": row_id, "generator": generator, "profession": profession,
            "target_gender": gender, "prompt_type": cfg["prompt"]["type"],
            "contrastive_order": order, "ref_ids": [r["ref_id"] for r in chosen],
            "seed": stable_seed(cfg["seed"], row_id), "prompt_version": cfg["prompt"]["version"],
            "k": k, "topup_round": topup_round,
            "prompt": render_prompt(cfg, template, profession, gender, chosen, order)}


def initial_rows(cfg, template, refs_by_prof, targets):
    overgen = cfg["counts"]["overgen"]
    rows = []
    for gen in cfg["generators"]:
        for prof in cfg["professions"]:
            if cfg["prompt"]["type"] == 1:
                for g in cfg["genders"]:
                    rows += [make_row(cfg, template, refs_by_prof, gen, prof, g, k)
                             for k in range(math.ceil(targets[(prof, g)] * overgen))]
            else:
                n = math.ceil(sum(targets[(prof, g)] for g in cfg["genders"]) * overgen)
                rows += [make_row(cfg, template, refs_by_prof, gen, prof, None, k)
                         for k in range(n)]
    return rows


def topup_rows(cfg, template, refs_by_prof, targets, plan, force):
    """Extra calls for short cells, sized by each cell's observed yield (passed / calls)."""
    counts = cfg["counts"]
    raw_ids = {gen: {r["id"] for r in read_jsonl(run_path(cfg, f"raw_{gen}.jsonl"))}
               for gen in cfg["generators"]}
    pending = [r["id"] for r in plan if r["id"] not in raw_ids.get(r["generator"], set())]
    if pending and not force:
        raise SystemExit(f"{len(pending)} planned calls have no response yet (e.g. {pending[0]}); "
                         "run generate/collect first, or pass --force.")
    validated = read_jsonl(run_path(cfg, "validated.jsonl"))
    if {r["id"] for r in validated} != set().union(*raw_ids.values()):
        raise SystemExit("validated.jsonl is out of date; run gen.validate first.")

    calls = Counter((r["generator"], r["profession"], r["target_gender"]) for r in validated)
    passed = Counter((r["generator"], r["profession"], r["gender"]) for r in validated
                     if r["passed"])
    next_k = Counter()
    for r in plan:
        key = (r["generator"], r["profession"], r["target_gender"])
        next_k[key] = max(next_k[key], r["k"] + 1)
    topup_round = max((r.get("topup_round", 0) for r in plan), default=0) + 1

    rows = []
    for gen in cfg["generators"]:
        for prof in cfg["professions"]:
            needed = {}  # call-group gender (None for types 0/4) -> calls
            for g in cfg["genders"]:
                short = targets[(prof, g)] - passed[(gen, prof, g)]
                if short <= 0:
                    continue
                group = g if cfg["prompt"]["type"] == 1 else None
                made = calls[(gen, prof, group)]
                rate = max(passed[(gen, prof, g)] / made if made else 1.0, counts["min_yield"])
                n = math.ceil(short * counts["overgen"] / rate) + (2 if group else 4)
                if n > counts["max_topup_calls"]:
                    print(f"warning: {gen}/{prof}/{g} would need {n} calls at yield {rate:.3f}; "
                          f"capped at max_topup_calls={counts['max_topup_calls']}")
                    n = counts["max_topup_calls"]
                needed[group] = max(needed.get(group, 0), n)
                print(f"  {gen}/{prof}/{g}: {passed[(gen, prof, g)]}/{targets[(prof, g)]} passed, "
                      f"yield {rate:.2f} -> {n} calls")
            for group, n in needed.items():
                start = next_k[(gen, prof, group)]
                rows += [make_row(cfg, template, refs_by_prof, gen, prof, group, k, topup_round)
                         for k in range(start, start + n)]
    return rows


def main(argv=None):
    setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", required=True)
    ap.add_argument("--topup", action="store_true", help="add calls for short cells")
    ap.add_argument("--force", action="store_true",
                    help="with --topup: plan even though some calls have no response yet")
    args = ap.parse_args(argv)
    cfg = load_config(args.config)

    template_text = Path(cfg["prompt"]["template"]).read_text(encoding="utf-8")
    template = Template(template_text)
    used = {m.group(1) or m.group(2) for m in re.finditer(r"\$(?:(\w+)|\{(\w+)\})", template_text)}
    if cfg["prompt"]["type"] == 1 and "gender" not in used:
        raise SystemExit("prompt.type is 1 but the template has no $gender")
    if cfg["prompt"]["type"] == 4 and "pair" not in used:
        raise SystemExit("prompt.type is 4 but the template has no $pair")

    refs = load_refs(cfg)
    refs_by_prof = {p: sorted((r for r in refs if r["profession"] == p), key=lambda r: r["ref_id"])
                    for p in cfg["professions"]}
    targets = cell_targets(cfg, refs)
    plan_path = run_path(cfg, "plan.jsonl")
    plan = read_jsonl(plan_path)

    if args.topup:
        new = topup_rows(cfg, template, refs_by_prof, targets, plan, args.force)
    else:
        existing = {r["id"]: r for r in plan}
        desired = initial_rows(cfg, template, refs_by_prof, targets)
        changed = [r["id"] for r in desired
                   if r["id"] in existing and existing[r["id"]]["prompt"] != r["prompt"]]
        if changed:
            raise SystemExit(
                f"{len(changed)} existing plan rows would get a different prompt (e.g. "
                f"{changed[0]}). Use a new run_name or output_dir after changing the template, "
                "refs, or seed.")
        new = [r for r in desired if r["id"] not in existing]

    write_jsonl(plan_path, plan + new)
    print(f"Plan: {len(plan)} existing + {len(new)} new rows -> {plan_path}")
    for gen in cfg["generators"]:
        print(f"  {gen}: {sum(r['generator'] == gen for r in plan + new)} calls")
    if not args.topup:
        print("Targets kept per generator (profession: male/female): " + ", ".join(
            f"{p} {targets[(p, 'male')]}/{targets[(p, 'female')]}" for p in cfg["professions"]))


if __name__ == "__main__":
    main()
