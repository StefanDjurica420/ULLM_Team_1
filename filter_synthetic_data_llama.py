"""Set RUN_MODE here, then run one Llama filtering stage."""

from pathlib import Path

import pandas as pd

from filtering.filtering_dataset import (
    load_data,
    add_biography_ids,
    validate_data,
    save_dataset_snapshot,
)
from filtering.filtering_llama import (
    get_llama_scores_path,
    score_llama_biographies,
)
from filtering.filtering_results import (
    merge_scores,
    filter_highest_scores,
    save_results,
)


# Column names in the input CSV
COLUMNS = {
    "text": "hard_text",
    "profession": "profession",
    "gender": "gender",
    "explanation": "explanation",
    "id": "bio_id",
}

# Experiment settings
EXPERIMENT_ID = "llama_dev_full_001"
SCORE_MODE = "content_only"  # Or "explanation_aware"
RUN_MODE = "prepare"         # "prepare", "score", or "filter" # so no submit/check/download stages for Llama like with openai, we dont use a batching api for llama.
NUMBER_TO_REMOVE = 2000

# Set to 4 to score only four biographies in the first real run.
# Set back to None to score the remaining biographies.
CALL_LIMIT = None

# Paths
BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR / "bias_in_bios_sample" / "dev.csv"
OUTPUT_DIR = BASE_DIR / "filtering_outputs"


def main():
    """Prepare the dataset, score it with Llama, or filter it."""

    if RUN_MODE not in {"prepare", "score", "filter"}:
        raise ValueError(f"Unknown RUN_MODE: {RUN_MODE}")


    id_column = COLUMNS["id"]
    saved_dataset_path = OUTPUT_DIR / EXPERIMENT_ID / "synthetic_with_ids.csv"

    # Check if run was already prepared and saved, or if we need to prepare it now.
    if saved_dataset_path.exists():
        df = load_data(saved_dataset_path, id_column)
        print(f"Loaded existing dataset: {saved_dataset_path}")
    else:
        if RUN_MODE != "prepare":# check that we are not trying to score or filter without a prepared dataset
            raise FileNotFoundError(
                f"No saved dataset: {saved_dataset_path}. Run prepare first."
            )

        df = load_data(INPUT_PATH, id_column)
        df = add_biography_ids(df, id_column)

    validate_data(df, SCORE_MODE, COLUMNS)

    if RUN_MODE == "prepare":
        if saved_dataset_path.exists():
            print(f"Dataset already prepared: {saved_dataset_path}")
        else:
            save_dataset_snapshot(df, EXPERIMENT_ID, OUTPUT_DIR)
            print(f"Saved dataset: {saved_dataset_path}")

        return

    if RUN_MODE == "score":
        scores_path = score_llama_biographies(
            df,
            SCORE_MODE,
            COLUMNS,
            EXPERIMENT_ID,
            OUTPUT_DIR,
            limit=CALL_LIMIT,
        )

        if scores_path is None:
            print("Some biographies still need scores. Run score again.")

        return

    # RUN_MODE is "filter" from this point onward.
    scores_path = get_llama_scores_path(
        OUTPUT_DIR,
        EXPERIMENT_ID,
        SCORE_MODE,
    )

    if not scores_path.exists():
        raise FileNotFoundError(
            f"No validated Llama scores: {scores_path}. Run score first."
        )

    scores = pd.read_csv(scores_path, dtype={"custom_id": "string"})
    scored = merge_scores(df, scores, SCORE_MODE, id_column)

    kept, removed = filter_highest_scores(scored, NUMBER_TO_REMOVE)

    results_dir = (
        OUTPUT_DIR
        / EXPERIMENT_ID
        / "results"
        / "llama"
        / SCORE_MODE
    )

    save_results(scored, kept, removed, results_dir)

    print(
        f"Kept {len(kept)} biographies; removed {len(removed)}. "
        f"Saved in {results_dir}"
    )


if __name__ == "__main__":
    main()