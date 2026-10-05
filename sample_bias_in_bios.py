from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
SIZES = {"train": 12_000, "dev": 2_000, "test": 6_000}
OUTPUT = Path("bias_in_bios_sample")
PROFESSIONS = dict(enumerate([
    "accountant", "architect", "attorney", "chiropractor", "comedian",
    "composer", "dentist", "dietitian", "dj", "filmmaker",
    "interior_designer", "journalist", "model", "nurse", "painter",
    "paralegal", "pastor", "personal_trainer", "photographer", "physician",
    "poet", "professor", "psychologist", "rapper", "software_engineer",
    "surgeon", "teacher", "yoga_teacher",
]))


def stratified_sample(df, n, seed):
    if not 0 < n <= len(df):
        raise ValueError(f"Cannot select {n} rows from {len(df)}.")
    groups = df.groupby(["profession", "gender"], sort=True)
    counts = groups.size()

    numerators = counts * n
    quotas = numerators // len(df)
    remainder = numerators % len(df)
    missing = int(n - quotas.sum())
    winners = remainder.sort_values(ascending=False, kind="stable").index[:missing]
    quotas.loc[winners] += 1

    rng = np.random.default_rng(seed)
    indices = []
    for key, group in groups:
        indices.extend(rng.choice(group.index.to_numpy(), int(quotas.loc[key]),
                                  replace=False).tolist())
    rng.shuffle(indices)
    result = df.loc[indices].copy().reset_index(drop=True)
    assert len(result) == n and result["source_row"].is_unique
    return result


def gender_counts(df):
    counts = pd.crosstab(df["profession"], df["gender"]).reindex(
        index=list(PROFESSIONS), columns=[0, 1], fill_value=0)
    counts.columns = ["men", "women"]
    counts.index = [PROFESSIONS[i] for i in counts.index]
    counts.loc["TOTAL"] = counts.sum()
    counts["total"] = counts["men"] + counts["women"]
    counts["women_pct"] = 100 * counts["women"] / counts["total"].replace(0, np.nan)
    counts["M:F"] = counts["men"].astype(str) + ":" + counts["women"].astype(str)
    counts.index.name = "profession_name"
    return counts


def main():
    from datasets import load_dataset

    dataset = load_dataset("LabHC/bias_in_bios")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    originals, samples = [], []

    for offset, (split, n) in enumerate(SIZES.items()):
        df = dataset[split].to_pandas().reset_index(drop=True)
        if not df["gender"].isin([0, 1]).all() or not df["profession"].isin(PROFESSIONS).all():
            raise ValueError("Unexpected gender/profession labels; check dataset mapping.")
        df["source_split"] = split
        df["source_row"] = np.arange(len(df))
        sample = stratified_sample(df, n, SEED + offset)
        sample["profession_name"] = sample["profession"].map(PROFESSIONS)
        sample.to_csv(OUTPUT / f"{split}.csv", index=False, encoding="utf-8-sig")

        comparison = gender_counts(df).add_prefix("original_").join(
            gender_counts(sample).add_prefix("sample_"))
        print(f"\n{split.upper()}: {len(df):,} -> {len(sample):,}")
        print(comparison.to_string(float_format=lambda x: f"{x:.2f}"))
        comparison.to_csv(OUTPUT / f"{split}_distribution.csv", encoding="utf-8-sig")

        if split == "test":
            small = gender_counts(sample).drop(index="TOTAL")
            small = small[(small["men"] < 50) | (small["women"] < 50)]
            if not small.empty:
                print("\nSmall test groups (<50 for either gender):")
                print(small[["men", "women"]].to_string())
                print("TPR gaps here may be noisy; 50 is a flag, not a sufficiency guarantee.")
        originals.append(df[["profession", "gender"]])
        samples.append(sample[["profession", "gender"]])

    combined = gender_counts(pd.concat(originals, ignore_index=True)).add_prefix("original_").join(
        gender_counts(pd.concat(samples, ignore_index=True)).add_prefix("sample_"))
    print("\nALL SPLITS COMBINED:")
    print(combined.to_string(float_format=lambda x: f"{x:.2f}"))
    combined.to_csv(OUTPUT / "combined_distribution.csv", encoding="utf-8-sig")
    print(f"\nSaved to: {OUTPUT.resolve()}")


if __name__ == "__main__":
    main()
