"""Build the five downstream training sets as CSV files in train_data/.

    1_original.csv                 original training data only
    2_original_all_synthetic.csv   original + every synthetic example
    3_original_random.csv          original + random subset of K synthetic examples
    4_original_content_only_<model>.csv   original + content-only filtered subset   (one per model)
    5_original_explanation_<model>.csv    original + explanation-aware filtered subset (one per model)

Inputs (relative to this file):
    bias_in_bios_sample/train.csv                                      original data
    filtering_outputs/<experiment>/synthetic_with_ids.csv              full synthetic pool
    filtering_outputs/<experiment>/results/<model>/content_only/kept.csv
    filtering_outputs/<experiment>/results/<model>/explanation_aware/kept.csv

Conditions 4 and 5 are built for every model folder in results/ (or only the ones
given with --model). K for the random subset defaults to the size of the content-only
kept set, so the K-example conditions are matched. Generator explanations are dropped: they are
used only for selection, never for downstream training.

Usage:
    python build_train_sets.py                       # auto-detects experiment and model
    python build_train_sets.py --experiment exp_001 --model gpt-4o-mini gpt-4o --seed 42
"""
import argparse
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
ORIGINAL_DIR = BASE_DIR / "bias_in_bios_sample"
FILTER_DIR = BASE_DIR / "filtering_outputs"
OUTPUT_DIR = BASE_DIR / "train_data"

TEXT, PROFESSION, GENDER, PROFESSION_NAME = "hard_text", "profession", "gender", "profession_name"
OUTPUT_COLUMNS = [TEXT, PROFESSION, GENDER, PROFESSION_NAME, "data_source", "source_id"]
MODES = ("content_only", "explanation_aware")


def read_csv(path):
    df = pd.read_csv(path, encoding="utf-8-sig")
    missing = {TEXT, PROFESSION, GENDER} - set(df.columns)
    if missing:
        raise ValueError(f"{path} is missing columns: {sorted(missing)}")
    if df[[TEXT, PROFESSION, GENDER]].isna().any().any():
        raise ValueError(f"{path} has empty values in {TEXT}/{PROFESSION}/{GENDER}")
    return df


def subdirs(parent, what):
    dirs = sorted(p.name for p in parent.iterdir() if p.is_dir()) if parent.is_dir() else []
    if not dirs:
        raise FileNotFoundError(f"No {what} folder found in {parent}")
    return dirs


def only_subdir(parent, what, flag):
    """Return the single subfolder of `parent`; ask for a flag when it is ambiguous."""
    dirs = subdirs(parent, what)
    if len(dirs) > 1:
        raise ValueError(f"Several {what} folders in {parent}: {dirs}. Choose one with {flag}.")
    return dirs[0]


def standardise(df, source, id_column, name_map):
    out = df.copy()
    if PROFESSION_NAME not in out.columns:
        out[PROFESSION_NAME] = pd.NA
    out[PROFESSION_NAME] = out[PROFESSION_NAME].where(out[PROFESSION_NAME].notna(), out[PROFESSION].map(name_map))
    out["data_source"] = source
    out["source_id"] = out[id_column] if id_column in out.columns else range(len(out))
    return out[OUTPUT_COLUMNS]


def kept_subset(pool, kept_path):
    """Rows of the pool whose bio_id appears in a filter's kept.csv."""
    kept = pd.read_csv(kept_path, encoding="utf-8-sig")
    if "bio_id" not in kept.columns:
        raise ValueError(f"{kept_path} has no bio_id column")
    unknown = set(kept["bio_id"]) - set(pool["bio_id"])
    if unknown:
        raise ValueError(f"{kept_path} has {len(unknown)} bio_ids not in the synthetic pool")
    return pool[pool["bio_id"].isin(kept["bio_id"])]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--original", type=Path, default=ORIGINAL_DIR / "train.csv")
    parser.add_argument("--experiment", help="Folder name inside filtering_outputs/")
    parser.add_argument("--model", nargs="+", help="Model folder(s) inside results/ (default: all)")
    parser.add_argument("--k", type=int, help="Random subset size (default: size of content-only kept set)")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--overwrite", action="store_true", help="Replace existing output files")
    args = parser.parse_args()

    original = read_csv(args.original)
    name_map = (original.dropna(subset=[PROFESSION_NAME]).drop_duplicates(PROFESSION)
                .set_index(PROFESSION)[PROFESSION_NAME].to_dict()
                if PROFESSION_NAME in original.columns else {})

    experiment = args.experiment or only_subdir(FILTER_DIR, "experiment", "--experiment")
    exp_dir = FILTER_DIR / experiment
    pool = read_csv(exp_dir / "synthetic_with_ids.csv")
    if "bio_id" not in pool.columns or pool["bio_id"].duplicated().any():
        raise ValueError("synthetic_with_ids.csv needs a unique bio_id column")
    models = args.model or subdirs(exp_dir / "results", "model")
    subsets = {model: {m: kept_subset(pool, exp_dir / "results" / model / m / "kept.csv") for m in MODES}
               for model in models}

    k = args.k if args.k is not None else len(subsets[models[0]]["content_only"])
    if not 0 < k <= len(pool):
        raise ValueError(f"K={k} must be between 1 and the pool size {len(pool)}")
    random_subset = pool.sample(n=k, random_state=args.seed)

    orig = standardise(original, "original", "source_row", name_map)
    syn = lambda df, label: standardise(df, label, "bio_id", name_map)
    conditions = {
        "1_original.csv": [orig],
        "2_original_all_synthetic.csv": [orig, syn(pool, "synthetic_all")],
        "3_original_random.csv": [orig, syn(random_subset, "synthetic_random")],
    }
    for model in models:
        safe = model.replace("/", "_").replace(" ", "_")
        conditions[f"4_original_content_only_{safe}.csv"] = [
            orig, syn(subsets[model]["content_only"], f"synthetic_content_only:{model}")]
        conditions[f"5_original_explanation_{safe}.csv"] = [
            orig, syn(subsets[model]["explanation_aware"], f"synthetic_explanation_aware:{model}")]

    args.output.mkdir(parents=True, exist_ok=True)
    existing = [n for n in conditions if (args.output / n).exists()]
    if existing and not args.overwrite:
        raise FileExistsError(f"Already in {args.output}: {existing}. Use --overwrite to replace them.")

    print(f"experiment={experiment}  models={models}  seed={args.seed}  K={k}")
    sizes = {f"{model}/{m}": len(s) for model, d in subsets.items() for m, s in d.items()}
    if len(set(sizes.values()) | {k}) > 1:
        print(f"WARNING: subset sizes differ {sizes}, random K={k}; the K-conditions are not matched.")
    for name, parts in conditions.items():
        df = pd.concat(parts, ignore_index=True).sample(frac=1, random_state=args.seed)  # shuffle
        df.to_csv(args.output / name, index=False, encoding="utf-8-sig")
        women = (df[GENDER] == 1).mean() * 100
        print(f"  {name:44s} {len(df):6d} rows  ({len(df) - len(orig)} synthetic, {women:.1f}% gender=1)")
    print(f"Saved to {args.output}")


if __name__ == "__main__":
    main()
