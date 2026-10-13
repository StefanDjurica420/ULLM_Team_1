"""Token usage and estimated cost of API calls, read from the output files.

    python -m llm_api.usage data/runs/*/raw_*.jsonl
"""
from __future__ import annotations

import argparse
import glob
from collections import defaultdict

from .jsonl import read_jsonl

# USD per 1M tokens (input, output), keyed by the model id the API returns.
# Checked 2026-10-09; check the providers' pricing pages before relying on them.
PRICES = {
    "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo": (0.02, 0.05),
    "gpt-4o-mini-2024-07-18": (0.15, 0.60),
}


def usage_summary(paths):
    """Per returned model id: calls, prompt/completion tokens and estimated cost (None if the
    model is not in PRICES)."""
    totals = defaultdict(lambda: {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0})
    for path in paths:
        for row in read_jsonl(path):
            if "usage" not in row:
                continue
            t = totals[row.get("model_returned") or "unknown"]
            t["calls"] += 1
            t["prompt_tokens"] += (row["usage"] or {}).get("prompt_tokens") or 0
            t["completion_tokens"] += (row["usage"] or {}).get("completion_tokens") or 0
    for model, t in totals.items():
        price = PRICES.get(model)
        t["cost_usd"] = (round((t["prompt_tokens"] * price[0] + t["completion_tokens"] * price[1])
                               / 1e6, 4) if price else None)
    return dict(totals)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("paths", nargs="+", help="output JSONL files (glob patterns allowed)")
    args = ap.parse_args(argv)
    paths = sorted({p for pattern in args.paths for p in (glob.glob(pattern) or [pattern])})
    summary = usage_summary(paths)
    print(f"{len(paths)} files")
    print(f"{'model':<46}{'calls':>8}{'tokens in':>12}{'tokens out':>12}{'cost $':>10}")
    total = 0.0
    for model, t in sorted(summary.items()):
        cost = "?" if t["cost_usd"] is None else f"{t['cost_usd']:.4f}"
        print(f"{model:<46}{t['calls']:>8}{t['prompt_tokens']:>12}{t['completion_tokens']:>12}"
              f"{cost:>10}")
        total += t["cost_usd"] or 0
    print(f"{'total (known prices)':<78}{total:>10.4f}")


if __name__ == "__main__":
    main()
