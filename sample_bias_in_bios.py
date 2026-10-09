from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
# ("natural", n): n bios per profession, keeping that profession's gender ratio.
# ("balanced", n): n bios per gender per profession.
SIZES = {"train": ("natural", 1_500), "dev": ("balanced", 100), "test": ("balanced", 250)}
KEEP = ["surgeon", "physician", "nurse", "software_engineer",
        "architect", "attorney", "psychologist", "teacher"]
OUTPUT = Path("bias_in_bios_sample")
PROFESSIONS = dict(enumerate([
    "accountant", "architect", "attorney", "chiropractor", "comedian",
    "composer", "dentist", "dietitian", "dj", "filmmaker",
    "interior_designer", "journalist", "model", "nurse", "painter",
    "paralegal", "pastor", "personal_trainer", "photographer", "physician",
    "poet", "professor", "psychologist", "rapper", "software_engineer",
    "surgeon", "teacher", "yoga_teacher",
]))
KEEP_IDS = [{name: i for i, name in PROFESSIONS.items()}[name] for name in KEEP]


def largest_remainder(counts, n):
    total = counts.sum()
    numerators = counts * n
    quotas = numerators // total
    remainder = numerators % total
    missing = int(n - quotas.sum())
    winners = remainder.sort_values(ascending=False, kind="stable").index[:missing]
    quotas.loc[winners] += 1
    return quotas


def group_quotas(df, mode, n):
    counts = df.groupby(["profession", "gender"], sort=True).size()
    if mode == "balanced":
        quotas = pd.Series(n, index=counts.index)
    elif mode == "natural":
        quotas = pd.concat([largest_remainder(group, n)
                            for _, group in counts.groupby(level="profession")])
    else:
        raise ValueError(f"Unknown sampling mode {mode!r}.")
    if len(counts) != 2 * len(KEEP_IDS):
        raise ValueError("Some profession x gender groups are empty.")
    short = quotas > counts
    if short.any():
        raise ValueError("Not enough rows for:\n"
                         + pd.DataFrame({"wanted": quotas[short],
                                         "available": counts[short]}).to_string())
    return quotas


def sample_groups(df, quotas, seed):
    rng = np.random.default_rng(seed)
    indices = []
    for key, group in df.groupby(["profession", "gender"], sort=True):
        indices.extend(rng.choice(group.index.to_numpy(), int(quotas.loc[key]),
                                  replace=False).tolist())
    rng.shuffle(indices)
    result = df.loc[indices].copy().reset_index(drop=True)
    assert len(result) == quotas.sum() and result["source_row"].is_unique
    return result


def gender_counts(df):
    counts = pd.crosstab(df["profession"], df["gender"]).reindex(
        index=KEEP_IDS, columns=[0, 1], fill_value=0)
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

    for offset, (split, (mode, n)) in enumerate(SIZES.items()):
        df = dataset[split].to_pandas().reset_index(drop=True)
        if not df["gender"].isin([0, 1]).all() or not df["profession"].isin(PROFESSIONS).all():
            raise ValueError("Unexpected gender/profession labels; check dataset mapping.")
        df["source_split"] = split
        df["source_row"] = np.arange(len(df))
        df = df[df["profession"].isin(KEEP_IDS)]
        sample = sample_groups(df, group_quotas(df, mode, n), SEED + offset)
        sample["profession_name"] = sample["profession"].map(PROFESSIONS)
        sample.to_csv(OUTPUT / f"{split}.csv", index=False, encoding="utf-8-sig")
        if split == "train":
            ids = "\n".join(map(str, sorted(sample["source_row"])))
            (OUTPUT / "O_train_ids.txt").write_text(ids + "\n", encoding="utf-8")

        comparison = gender_counts(df).add_prefix("original_").join(
            gender_counts(sample).add_prefix("sample_"))
        print(f"\n{split.upper()} ({mode}, n={n}): {len(df):,} -> {len(sample):,}")
        print(comparison.to_string(float_format=lambda x: f"{x:.2f}"))
        comparison.to_csv(OUTPUT / f"{split}_distribution.csv", encoding="utf-8-sig")

    print(f"\nSaved to: {OUTPUT.resolve()}")


if __name__ == "__main__":
    main()
