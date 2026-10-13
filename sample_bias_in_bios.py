"""Constrained, split-preserving sampling of LabHC/bias_in_bios."""
from pathlib import Path
import argparse
import math
import numpy as np
import pandas as pd
from scipy.optimize import Bounds, LinearConstraint, milp

SEED = 42
SIZES = {"train": 12_000, "dev": 1_600, "test": 4_000}
MIN_SHARE = 0.025
TARGET_MALE_SHARE = 0.539
OUTPUT = Path("bias_in_bios_sample")
PROFESSIONS = dict(enumerate([
    "accountant", "architect", "attorney", "chiropractor", "comedian",
    "composer", "dentist", "dietitian", "dj", "filmmaker",
    "interior_designer", "journalist", "model", "nurse", "painter",
    "paralegal", "pastor", "personal_trainer", "photographer", "physician",
    "poet", "professor", "psychologist", "rapper", "software_engineer",
    "surgeon", "teacher", "yoga_teacher",
]))

def allocate(counts, n, min_share=MIN_SHARE, male_share=TARGET_MALE_SHARE):
    """Minimize L1 change from source occupation proportions subject to quotas.

    Variables: total, female count, absolute deviation for each profession.
    Female quotas are within 0.5 rows of the source-split proportional ideal.
    Half-integer ties may go either way to meet the overall gender target.
    Each full 5% of source occupation share adds MIN_SHARE to its minimum.
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Sample size must be a positive integer.")
    if not 0 < min_share <= 1 or not 0 <= male_share <= 1:
        raise ValueError("Invalid minimum share or gender target.")
    counts = counts.reindex(index=list(PROFESSIONS), columns=[0, 1], fill_value=0)
    a = counts.to_numpy(dtype=int)
    k = len(a)
    totals = a.sum(axis=1)
    if (totals == 0).any():
        raise ValueError("Every profession must be present in the source split.")
    # Integer division counts complete 5% blocks, avoiding floating boundary errors.
    blocks = (20 * totals) // totals.sum()
    floor = np.array([math.ceil(n * min_share * (1 + int(b)) - 1e-10)
                      for b in blocks], dtype=int)
    if floor.sum() > n or (totals < floor).any() or n > totals.sum():
        raise ValueError(f"Infeasible size/minimum: n={n}, minimum={floor} per profession. "
                         "Reduce the minimum or sample size, or revise the profession selection.")
    ratios = a[:, 1] / totals
    ideal = n * totals / totals.sum()
    target_men = int(math.floor(n * male_share + 0.5))
    rows, lower, upper = [], [], []
    def add(entries, lo, hi):
        row = np.zeros(3 * k)
        for j, value in entries.items():
            row[j] = value
        rows.append(row); lower.append(lo); upper.append(hi)
    add({i: 1 for i in range(k)}, n, n)
    add({k+i: 1 for i in range(k)}, n-target_men, n-target_men)
    for i in range(k):
        add({i: 1, k+i: -1}, 0, a[i, 0])  # available men
        add({i: -ratios[i], k+i: 1}, -0.5, 0.5)
        add({i: 1, 2*k+i: -1}, -np.inf, ideal[i])
        add({i: -1, 2*k+i: -1}, -np.inf, -ideal[i])
    result = milp(
        c=np.r_[np.zeros(2*k), np.ones(k)],
        integrality=np.r_[np.ones(2*k), np.zeros(k)],
        bounds=Bounds(np.r_[floor, np.zeros(2*k)],
                      np.r_[totals, a[:, 1], np.full(k, np.inf)]),
        constraints=LinearConstraint(np.array(rows), lower, upper),
        options={"time_limit": 60, "mip_rel_gap": 0.0},
    )
    if not result.success:
        raise ValueError("No proven optimal allocation found; no constraints relaxed. "
                         f"Solver: {result.message}")
    sizes = np.rint(result.x[:k]).astype(int)
    women = np.rint(result.x[k:2*k]).astype(int)
    q = pd.DataFrame({0: sizes-women, 1: women}, index=list(PROFESSIONS))
    if (q.to_numpy() < 0).any() or (q.to_numpy() > a).any():
        raise RuntimeError("Invalid group quotas.")
    if sizes.sum() != n or (sizes < floor).any() or q[0].sum() != target_men:
        raise RuntimeError("Allocation violates size, minimum or gender target.")
    if (np.abs(women - ratios * sizes) > 0.50001).any():
        raise RuntimeError("Allocation violates within-profession gender ratios.")
    return q


def prepare(df, split):
    df = df.reset_index(drop=True).copy()
    if not df["gender"].isin([0, 1]).all() or not df["profession"].isin(PROFESSIONS).all():
        raise ValueError("Unexpected gender/profession labels.")
    df["source_split"] = split
    df["source_row"] = np.arange(len(df))
    return df


def gender_counts(df):
    return pd.crosstab(df["profession"], df["gender"]).reindex(
        index=list(PROFESSIONS), columns=[0, 1], fill_value=0)


def sample_groups(df, quotas, seed):
    rng = np.random.default_rng(seed)
    indices = []
    for profession in PROFESSIONS:
        for gender in (0, 1):
            available = df.index[(df.profession == profession) & (df.gender == gender)]
            indices.extend(rng.choice(available, int(quotas.loc[profession, gender]),
                                      replace=False).tolist())
    rng.shuffle(indices)
    sample = df.loc[indices].copy().reset_index(drop=True)
    sample["profession_name"] = sample["profession"].map(PROFESSIONS)
    if not sample.source_row.is_unique or not gender_counts(sample).equals(quotas):
        raise RuntimeError("Sample does not match allocation or contains repeated row IDs.")
    return sample


def report(df):
    c = gender_counts(df)
    c.index = [PROFESSIONS[i] for i in c.index]
    c.columns = ["men", "women"]
    c.loc["TOTAL"] = c.sum()
    c["total"] = c.men + c.women
    c["profession_pct"] = 100 * c.total / len(df)
    c["men_pct"] = 100 * c.men / c.total
    c["women_pct"] = 100 * c.women / c.total
    c.index.name = "profession_name"
    return c


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local-data", type=Path,
                        help="Optional directory containing official train/dev/test Parquet files.")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    if args.local_data is None:
        from datasets import load_dataset
        dataset = load_dataset("LabHC/bias_in_bios")
    prepared = []
    # Validate all splits before writing any output files.
    for offset, (split, n) in enumerate(SIZES.items()):
        if args.local_data is None:
            raw = dataset[split].to_pandas()
        else:
            paths = sorted(args.local_data.glob(f"{split}*.parquet"))
            if not paths:
                raise ValueError(f"No {split} Parquet files found.")
            raw = pd.concat([pd.read_parquet(p) for p in paths], ignore_index=True)
        df = prepare(raw, split)
        quotas = allocate(gender_counts(df), n)
        sample = sample_groups(df, quotas, SEED + offset)
        comparison = report(df).add_prefix("original_").join(report(sample).add_prefix("sample_"))
        prepared.append((split, sample, comparison))
        print(f"\n{split.upper()}: {len(sample):,} rows; "
              f"men {(sample.gender == 0).mean():.2%}; "
              f"minimum profession {sample.profession.value_counts().min()} rows")
        print(comparison.to_string(float_format=lambda x: f"{x:.2f}"))
    args.output.mkdir(parents=True, exist_ok=True)
    for split, sample, comparison in prepared:
        sample.to_csv(args.output / f"{split}.csv", index=False, encoding="utf-8-sig")
        comparison.to_csv(args.output / f"{split}_distribution.csv", encoding="utf-8-sig")
        if split == "train":
            ids = "\n".join(map(str, sorted(sample.source_row)))
            (args.output / "O_train_ids.txt").write_text(ids + "\n", encoding="utf-8")
    print(f"\nSaved to: {args.output.resolve()}")


if __name__ == "__main__":
    main()
