"""Compare occupation and gender distributions before and after filtering reusing code from sample_bias_in_bios + creates table for tied score removal counts per occupation"""

from pathlib import Path
import pandas as pd
from sample_bias_in_bios import report, PROFESSIONS


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "final_filtered_data"
OUTPUT_DIR = BASE_DIR / "analysis" / "outputs"

# Dictionary to get correct synthetic data pool directory
INPUT_PATHS = {
    "GPT": BASE_DIR / "data" / "synthetic" / "gpt4omini" / "filtering_input.csv",
    "Llama": BASE_DIR / "data" / "synthetic" / "llama" / "filtering_input.csv",
}

# Results folder, generator, filtering model.
EXPERIMENTS = [
    ("GPT-generated-data-GPT-filtering-full", "GPT", "GPT"),
    ("GPT-generated-data-llama-filtering-full", "GPT", "Llama"),
    ("Llama-generated-data-filtering-GPT-full", "Llama", "GPT"),
    ("Llama-generated-data-llama-filtering-full", "Llama", "Llama"),
]

SCORING_MODES = ["content_only", "explanation_aware"]

# report() expects numerical labels, while final data has strings(for example: 'nurse') so we need a dict to convert back
PROFESSION_IDS = {}
for number, name in PROFESSIONS.items():
    PROFESSION_IDS[name] = number


def get_distribution(df):
    """Converts the profession strings to numbers and uses report() to get distribution"""
    data = df[["profession", "gender"]].copy()

    data["profession"] = data["profession"].map(PROFESSION_IDS)
    data["gender"] = data["gender"].map({"male": 0, "female": 1})

    if data.isna().any().any():
        raise ValueError("Unknown or missing profession or gender label.")

    return report(data)


def compare_distributions():
    """Compares occupation and gender distributions before and after filtering then saves the comparisons to CSV"""
    comparisons = []

    for folder, generator, filtering_model in EXPERIMENTS: # loop over 4 generator filter combinations
        full = pd.read_csv(
            INPUT_PATHS[generator], # get correct synthetic data pool
            usecols=["bio_id", "profession", "gender"],
        )

        if not full["bio_id"].is_unique:
            raise ValueError(f"Duplicate biography IDs in the {generator} pool.")

        full_distribution = get_distribution(full)

        for scoring_mode in SCORING_MODES: # loop over 2 scoring modes
            kept_path = DATA_DIR / folder / scoring_mode / "kept.csv"
            kept = pd.read_csv( # get correct kept file for current scoring mode
                kept_path,
                usecols=["bio_id", "profession", "gender"],
            )

            if not kept["bio_id"].is_unique:
                raise ValueError(f"Duplicate biography IDs in {kept_path}")

            if not kept["bio_id"].isin(full["bio_id"]).all():
                raise ValueError(f"Kept biographies do not match the pool: {kept_path}")

            kept_distribution = get_distribution(kept)

            # Put the full and kept distributions beside each other
            comparison = full_distribution.add_prefix("full_").join(
                kept_distribution.add_prefix("kept_")
            )

            # Calculate how many biographies are removed for each profession (absolute and percentage)
            comparison["removed_count"] = (
                comparison["full_total"] - comparison["kept_total"]
            )
            comparison["removed_pct"] = (
                100 * comparison["removed_count"] / comparison["full_total"]
            )

            # Calculate changes in occupation share and the female proportion within each occupation in percentage points
            comparison["profession_change_pp"] = (
                comparison["kept_profession_pct"]
                - comparison["full_profession_pct"]
            )
            comparison["women_change_pp"] = (
                comparison["kept_women_pct"]
                - comparison["full_women_pct"]
            )

            # make occupation names a normal column
            comparison = comparison.reset_index()

            # label every row by experiment
            comparison.insert(0, "scoring_mode", scoring_mode)
            comparison.insert(0, "filtering_model", filtering_model)
            comparison.insert(0, "generator", generator)

            comparisons.append(comparison)

            print(
                f"{generator} data, {filtering_model} filter, {scoring_mode}: "
                f"{len(full):,} full, {len(kept):,} kept"
            )

    results = pd.concat(comparisons, ignore_index=True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "filtering_distribution_comparison.csv"
    results.to_csv(output_path, index=False)

    print(f"\nSaved comparison: {output_path}")

def summarise_tied_removals():
    """Counts removed biographies at the cutoff score for each profession"""
    counts_by_run = {}

    for folder, generator, filtering_model in EXPERIMENTS: # loop over all 4 generator-filter model configurations
        for scoring_mode in SCORING_MODES:
            removed_path = DATA_DIR / folder / scoring_mode / "removed.csv"
            removed = pd.read_csv(
                removed_path,
                usecols=["profession", "bias_score"],
            )

            # The lowest removed score is the cutoff
            cutoff = removed["bias_score"].min()

            # Select all removed biographies at the cutoff
            tied_removed = removed[removed["bias_score"] == cutoff]

            # Create labels
            if scoring_mode == "content_only":
                mode_label = "CO"
            else:
                mode_label = "EA"

            run_label = f"{generator}/{filtering_model} {mode_label}"

            # Count per profession
            counts_by_run[run_label] = (
                tied_removed["profession"].value_counts()
            )

            print(f"{run_label}: {len(tied_removed)} boundary-tied removals")

    # Create single sorted dataframe
    results = pd.DataFrame(counts_by_run).fillna(0).astype(int)
    results = results.sort_index()
    results.index.name = "profession_name"

    # Add total counts
    results.loc["TOTAL"] = results.sum()

    # Keep profession names as a normal column
    results = results.reset_index()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "filtering_tied_removals_by_profession.csv"
    results.to_csv(output_path, index=False)

    print(f"\nSaved ties table: {output_path}")


compare_distributions()
summarise_tied_removals()