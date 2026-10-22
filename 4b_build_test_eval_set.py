"""Build the evaluation sets (test and dev) for gender_evaluation.py / 6a_snellius_jobarray.py.

Reads  bias_in_bios_sample/test.csv  ->  writes testdata_hug/test.json   (final evaluation)
       bias_in_bios_sample/dev.csv   ->  writes testdata_hug/dev.json    (choosing settings,
                                                                          e.g. the learning rate)
Both are JSON Lines (one record per line), keeping only the biography, profession name
and gender:
    {"hard_text": "...", "profession": "nurse", "gender": "female"}

The profession name is stored under the key "profession" because that is the field
gender_evaluation.py reads. Gender is converted from the Bias in Bios codes
0 = male, 1 = female, so per-group results read e.g. "nurse_female".

Biographies that also appear in the original training data are removed from both sets,
and dev biographies that also appear in the test set are removed from dev, so the test
set stays fixed (see the paper note below).

PAPER NOTE (train/test overlap):
    The official LabHC/bias_in_bios splits contain a few identical biographies in both
    the train and the test split. After sampling (sample_bias_in_bios.py), 2 of the 4,000
    test biographies (0.05%) were identical to biographies in our 12,000-example original
    training set (one personal trainer, one dentist; same profession and gender labels in
    both). We removed them from the test set, leaving 3,998 test biographies. Overlap was
    checked by exact text match after lowercasing and trimming whitespace. The dev set had
    no overlap with the training data, but 2 of its 1,600 biographies (one comedian, one
    physician) also occurred in the test set; we removed them from dev, leaving 1,598 dev
    biographies.
    Suggested wording: "We removed two test biographies that also occurred verbatim in
    the training data and two development biographies that also occurred in the test set
    (duplicates across the official Bias in Bios splits), leaving 3,998 test and 1,598
    development examples."

Usage:
    python 4b_build_test_eval_set.py                  # builds test.json and dev.json
    python 4b_build_test_eval_set.py --splits dev     # only dev.json
    python 4b_build_test_eval_set.py --overwrite
"""
import argparse
import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
SOURCE_DIR = BASE_DIR / "bias_in_bios_sample"
OUTPUT_DIR = BASE_DIR / "testdata_hug"
TRAIN = SOURCE_DIR / "train.csv"  # original training data (= traindata_hug/train.csv)
SPLITS = ["test", "dev"]
GENDER_NAMES = {0: "male", 1: "female"}
REQUIRED = ["hard_text", "profession_name", "gender"]


def key(texts):
    """Text form used to detect duplicates: lowercased, surrounding whitespace removed."""
    return texts.str.strip().str.lower()


def read_split(path):
    df = pd.read_csv(path, encoding="utf-8-sig")
    missing = set(REQUIRED) - set(df.columns)
    if missing:
        raise ValueError(f"{path} is missing columns: {sorted(missing)}")
    if df[REQUIRED].isna().any().any():
        raise ValueError(f"{path} has empty values in {REQUIRED}")
    unknown = set(df["gender"]) - set(GENDER_NAMES)
    if unknown:
        raise ValueError(f"{path}: unexpected gender values {sorted(unknown)}")
    return df


def build(split, exclude, args):
    """exclude: {file name: set of texts} whose bios must not appear in this split."""
    source = SOURCE_DIR / f"{split}.csv"
    output = args.output_dir / f"{split}.json"
    df = read_split(source)

    # Drop bios that also occur in the excluded files (see PAPER NOTE above).
    print(f"\n{split}: {len(df)} bios in {source.name}")
    for name, texts in exclude.items():
        overlap = key(df["hard_text"]).isin(texts)
        if not overlap.any():
            print(f"  no overlap with {name}")
            continue
        print(f"  removed {overlap.sum()} that also appear in {name}:")
        for row in df[overlap].itertuples(index=False):
            print(f"    source_row={row.source_row}  {row.profession_name}  "
                  f"{GENDER_NAMES[row.gender]}  {row.hard_text[:60]!r}...")
        df = df[~overlap].reset_index(drop=True)

    if output.exists() and not args.overwrite:
        raise FileExistsError(f"{output} already exists. Use --overwrite to replace it.")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as f:
        for row in df.itertuples(index=False):
            record = {"hard_text": row.hard_text, "profession": row.profession_name,
                      "gender": GENDER_NAMES[row.gender]}
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    genders = df["gender"].map(GENDER_NAMES)
    counts = pd.crosstab(df["profession_name"], genders)
    print(f"  wrote {len(df)} records to {output.relative_to(BASE_DIR)}   "
          f"professions: {counts.shape[0]}   gender: {genders.value_counts().to_dict()}")
    small = counts[(counts < 10).any(axis=1)]
    if not small.empty:
        print(f"  groups with fewer than 10 people (noisy TPR):\n{small.to_string()}")
    return df


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--splits", nargs="+", choices=SPLITS, default=SPLITS)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--overwrite", action="store_true", help="Replace existing output files")
    args = parser.parse_args()

    train_texts = set(key(read_split(TRAIN)["hard_text"]))
    test_texts = set(key(read_split(SOURCE_DIR / "test.csv")["hard_text"]))
    exclude = {"test": {"train.csv": train_texts},
               "dev": {"train.csv": train_texts, "test.csv": test_texts}}  # test stays fixed
    built = {split: build(split, exclude[split], args) for split in args.splits}
    labels = sorted(next(iter(built.values()))["profession_name"].unique())
    print("\n--profession_labels " + ",".join(l.replace("_", " ") for l in labels))


if __name__ == "__main__":
    main()
