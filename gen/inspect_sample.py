"""Print a random sample of validated records and save it as review_sample.md for team review."""
from __future__ import annotations

import argparse
import random

from .common import load_config, read_jsonl, run_path, setup_stdout, stable_seed


def render(i, r):
    failed = [c for c, ok in r["checks"].items() if ok is False]
    order = f" · {r['contrastive_order']}" if r["contrastive_order"] else ""
    return "\n".join([
        f"## {i}. {r['id']}",
        f"{r['generator']} · {r['profession']} · asked: {r['target_gender'] or 'any'} · "
        f"pronouns: {r['gender'] or 'unclear'} · type {r['prompt_type']}{order} · "
        f"{r['word_count']} words",
        f"Failed checks: {', '.join(failed)}" if failed else "Passed all checks",
        "",
        f"**Bio:** {r['bio'] or '(none)'}",
        "",
        f"**Explanation:** {r['explanation'] or '(none)'}",
        "",
        "Adds information beyond the bio? [ ] yes [ ] partly [ ] no",
        "",
        "---",
        "",
    ])


def main(argv=None):
    setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", required=True)
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--generator")
    ap.add_argument("--profession")
    ap.add_argument("--failed", action="store_true", help="sample failed records instead")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args(argv)
    cfg = load_config(args.config)

    records = [r for r in read_jsonl(run_path(cfg, "validated.jsonl"))
               if r["passed"] != args.failed
               and args.generator in (None, r["generator"])
               and args.profession in (None, r["profession"])]
    if not records:
        raise SystemExit("No matching records; run gen.validate first or relax the filters.")
    rng = random.Random(stable_seed(cfg["seed"], "inspect", args.seed))
    sample = rng.sample(records, min(args.n, len(records)))

    filters = ", ".join(f"{k}={v}" for k, v in [("generator", args.generator),
                                               ("profession", args.profession),
                                               ("failed", args.failed)] if v)
    text = (f"# Review sample: {cfg['run_name']}\n\n{len(sample)} of {len(records)} "
            f"{'failed' if args.failed else 'passed'} records{' (' + filters + ')' if filters else ''}"
            "\n\n" + "".join(render(i, r) for i, r in enumerate(sample, 1)))
    path = run_path(cfg, "review_sample.md")
    path.write_text(text, encoding="utf-8")
    print(text)
    print(f"Saved to {path}")


if __name__ == "__main__":
    main()
