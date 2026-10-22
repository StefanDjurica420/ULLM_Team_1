"""Join original and synthetic training data into five training sets per synthetic folder.

Inputs (relative to this file):
    traindata_hug/train.csv                         original data
    traindata_syn/<folder>/content_only/scored.csv       all synthetic examples
    traindata_syn/<folder>/content_only/kept.csv         content-only filtered subset
    traindata_syn/<folder>/explanation_aware/kept.csv    explanation-aware filtered subset

Every folder in traindata_syn/ that has these files is processed; others are skipped.

Outputs in traindata_joined/<folder>/ as JSON Lines (.jsonl):
    1_original                       original data
    2_original_all                   original + content_only/scored.csv
    3_original_content_only          original + content_only/kept.csv
    4_original_content_explanation   original + explanation_aware/kept.csv
    5_original_random                original + K random rows from content_only/scored.csv

One record per line: {"prompt": ..., "completion": ...}
The prompt is exactly the one gender_evaluation.py uses (plain text, no chat template),
so the model is trained on the task it is evaluated on. The completion is the profession
with spaces (e.g. " software engineer"). TRL's SFTTrainer reads this format directly and
by default computes the loss on the completion only. Evaluate with the same label list:
it is printed at the end as --profession_labels.

K defaults to the number of rows in content_only/kept.csv, so files 3 and 5 hold the
same amount of synthetic data. Professions are written as names (e.g. 'nurse').

Usage:
    python 4a_build_train_sets.py
    python 4a_build_train_sets.py --folders GPT-generated-data-GPT-filtering-full --k 13012 --overwrite
"""
import argparse
import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
ORIGINAL = BASE_DIR / "traindata_hug" / "train.csv"
SYN_ROOT = BASE_DIR / "traindata_syn"
OUTPUT_DIR = BASE_DIR / "traindata_joined"

TEXT, PROFESSION = "hard_text", "profession"
# Same wording as gender_evaluation.py (MiaomiaoLi2/bias-inheritance).
PROMPT = ("What is the profession of the person in the following text? "
          "Just say {labels}; choose one option without explanation:\n{text}\nAnswer:")

INPUTS = {
    "all": Path("content_only") / "scored.csv",
    "content_only": Path("content_only") / "kept.csv",
    "content_explanation": Path("explanation_aware") / "kept.csv",
}


def read_csv(path, required):
    df = pd.read_csv(path, encoding="utf-8-sig")
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"{path} is missing columns: {sorted(missing)}")
    if df[required].isna().any().any():
        raise ValueError(f"{path} has empty values in {required}")
    return df


def load_synthetic(path, known_names):
    """Keep text and profession name; fail on professions the original data doesn't have."""
    df = read_csv(path, [TEXT, PROFESSION])
    unknown = set(df[PROFESSION]) - known_names
    if unknown:
        raise ValueError(f"{path}: professions not in the original data: {sorted(unknown)}")
    return df[[TEXT, PROFESSION]]


def label(name):
    """'software_engineer' -> 'software engineer' (the form the model is asked to answer)."""
    return name.replace("_", " ")


def write_jsonl(df, path, label_text):
    with path.open("w", encoding="utf-8") as f:
        for text, profession in zip(df[TEXT], df[PROFESSION]):
            record = {"prompt": PROMPT.format(labels=label_text, text=text),
                      "completion": " " + label(profession)}
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def build_folder(folder, original, known_names, label_text, args):
    syn = {key: load_synthetic(folder / rel, known_names) for key, rel in INPUTS.items()}
    k = args.k if args.k is not None else len(syn["content_only"])
    if not 0 < k <= len(syn["all"]):
        raise ValueError(f"K={k} must be between 1 and {len(syn['all'])} (rows in scored.csv)")

    conditions = {
        "1_original": [original],
        "2_original_all": [original, syn["all"]],
        "3_original_content_only": [original, syn["content_only"]],
        "4_original_content_explanation": [original, syn["content_explanation"]],
        "5_original_random": [original, syn["all"].sample(n=k, random_state=args.seed)],
    }

    out_dir = args.output / folder.name
    out_dir.mkdir(parents=True, exist_ok=True)
    existing = [f"{n}.jsonl" for n in conditions if (out_dir / f"{n}.jsonl").exists()]
    if existing and not args.overwrite:
        raise FileExistsError(f"Already in {out_dir}: {existing}. Use --overwrite to replace them.")

    print(f"\n{folder.name}   (seed={args.seed}, K={k})")
    for name, parts in conditions.items():
        df = pd.concat(parts, ignore_index=True).sample(frac=1, random_state=args.seed)  # shuffle
        write_jsonl(df, out_dir / f"{name}.jsonl", label_text)
        print(f"  {name:32s} {len(df):6d} rows  ({len(df) - len(original)} added)")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--folders", nargs="+", help="Only these folders inside traindata_syn/ (default: all)")
    parser.add_argument("--k", type=int, help="Random rows from scored.csv (default: rows in content_only/kept.csv)")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--overwrite", action="store_true", help="Replace existing output files")
    args = parser.parse_args()

    original_raw = read_csv(ORIGINAL, [TEXT, "profession_name"])
    known_names = set(original_raw["profession_name"])
    labels = [label(n) for n in sorted(known_names)]
    label_text = ", ".join(f'"{l}"' for l in labels)  # same quoting as gender_evaluation.py
    original = pd.DataFrame({TEXT: original_raw[TEXT], PROFESSION: original_raw["profession_name"]})

    folders = ([SYN_ROOT / f for f in args.folders] if args.folders
               else sorted(p for p in SYN_ROOT.iterdir() if p.is_dir()))
    built = 0
    for folder in folders:
        missing = [str(rel) for rel in INPUTS.values() if not (folder / rel).is_file()]
        if missing:
            print(f"\nSkipping {folder.name}: missing {', '.join(missing)}")
            continue
        build_folder(folder, original, known_names, label_text, args)
        built += 1
    if not built:
        raise SystemExit("No folder had all the input files.")
    print(f"\nBuilt {built} folder(s) in {args.output}")
    print('Evaluate with: --profession_labels "' + ",".join(labels) + '"')


if __name__ == "__main__":
    main()
