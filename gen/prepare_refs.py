"""Write the reference bios that generation prompts draw their examples from.

  --source official_train --n-per-profession 300   random official-train bios (pilot)
  --ids-file bias_in_bios_sample/O_train_ids.txt   exactly the bios in O (full run)
  --source fake                                    random-word bios, no download (testing)
"""
from __future__ import annotations

import argparse
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path

from .common import (GENDERS, PROFESSIONS, load_config, setup_stdout, stable_seed, word_count,
                     write_json, write_jsonl)
from .mock import fake_refs

GENDER_NAMES = {g["id"]: name for name, g in GENDERS.items()}


def print_split_counts(dataset, professions):
    id_to_name = {PROFESSIONS[p]["id"]: p for p in professions}
    print(f"\n{'profession':<20}" + "".join(f"{s + ' M':>9}{s + ' F':>9}{'%F':>7}" for s in dataset))
    counts = {s: Counter(zip(dataset[s]["profession"], dataset[s]["gender"])) for s in dataset}
    for pid, name in id_to_name.items():
        line = f"{name:<20}"
        for s in dataset:
            m, f = counts[s][(pid, 0)], counts[s][(pid, 1)]
            line += f"{m:>9}{f:>9}{100 * f / max(1, m + f):>7.1f}"
        print(line)


def official_refs(cfg, n_per_profession, ids_file):
    from datasets import load_dataset

    dataset = load_dataset("LabHC/bias_in_bios")
    print_split_counts(dataset, cfg["professions"])
    train = dataset["train"]
    wanted = {PROFESSIONS[p]["id"]: p for p in cfg["professions"]}

    if ids_file:
        ids = sorted({int(line) for line in Path(ids_file).read_text().split() if line.strip()})
        if ids and not 0 <= ids[0] <= ids[-1] < len(train):
            raise SystemExit(f"{ids_file}: row ids outside the official train split")
    else:
        rng = random.Random(stable_seed(cfg["seed"], "prepare_refs"))
        by_prof = defaultdict(list)
        for i, pid in enumerate(train["profession"]):
            if pid in wanted:
                by_prof[pid].append(i)
        ids = sorted(i for pid in sorted(wanted)
                     for i in rng.sample(by_prof[pid], min(n_per_profession, len(by_prof[pid]))))

    rows = train.select(ids)
    refs, skipped = [], 0
    for ref_id, row in zip(ids, rows):
        if row["profession"] not in wanted:
            skipped += 1
            continue
        refs.append({"ref_id": ref_id, "profession": wanted[row["profession"]],
                     "gender": GENDER_NAMES[row["gender"]], "text": row["hard_text"]})
    if skipped:
        print(f"\nSkipped {skipped} ids whose profession is not in the config.")
    absent = set(cfg["professions"]) - {r["profession"] for r in refs}
    if absent:
        raise SystemExit(f"No reference bios for {sorted(absent)}")
    return refs


def word_stats(texts):
    counts = sorted(word_count(t) for t in texts)
    q = statistics.quantiles(counts, n=20) if len(counts) > 1 else counts * 19
    return {"n": len(counts), "mean": round(statistics.mean(counts), 1),
            "p5": q[0], "p25": q[4], "p50": q[9], "p75": q[14], "p95": q[18]}


def main(argv=None):
    setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--source", choices=["official_train", "fake"], default="official_train")
    ap.add_argument("--n-per-profession", type=int, default=300)
    ap.add_argument("--ids-file")
    args = ap.parse_args(argv)
    cfg = load_config(args.config)
    if args.ids_file and args.source != "official_train":
        raise SystemExit("--ids-file only works with --source official_train")

    if args.source == "fake":
        refs = fake_refs(cfg["professions"], args.n_per_profession, cfg["seed"])
    else:
        refs = official_refs(cfg, args.n_per_profession, args.ids_file)

    refs_file = Path(cfg["refs_file"])
    write_jsonl(refs_file, refs)
    stats = {"overall": word_stats([r["text"] for r in refs]),
             "per_profession": {p: word_stats([r["text"] for r in refs if r["profession"] == p])
                                for p in cfg["professions"]}}
    stats_file = refs_file.with_name(refs_file.stem + ".stats.json")
    write_json(stats_file, stats)

    print(f"\nWrote {len(refs)} reference bios to {refs_file}")
    for p in cfg["professions"]:
        g = Counter(r["gender"] for r in refs if r["profession"] == p)
        print(f"  {p:<20} {g['male']:>6} M {g['female']:>6} F")
    o = stats["overall"]
    v = cfg["validate"]
    print(f"Word counts: p5 {o['p5']:.0f}, median {o['p50']:.0f}, p95 {o['p95']:.0f} "
          f"(validate accepts {v['min_words']}-{v['max_words']}); details in {stats_file}")


if __name__ == "__main__":
    main()
