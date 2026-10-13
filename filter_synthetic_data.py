"""Set RUN_MODE here, then run this file for one GPT filtering stage."""

from pathlib import Path
import pandas as pd

from filtering.filtering_dataset import (
    load_data,
    add_biography_ids,
    validate_data,
    save_dataset_snapshot,
)
from filtering.filtering_openai import (
    create_openai_client,
    find_prepared_batches,
    prepare_openai_batches,
    submit_prepared_batches,
    check_submitted_batches,
    download_and_parse_results,
)
from filtering.filtering_results import merge_scores, filter_highest_scores, save_results
from filtering.filtering_scoring import custom_id_for


# Constants for column names for easier reading
TEXT_COLUMN = "hard_text"
PROFESSION_COLUMN = "profession"
GENDER_COLUMN = "gender"
EXPLANATION_COLUMN = "explanation"
ID_COLUMN = "bio_id"

# Pass column names to helper functions in a dictionary for easier reading and to avoid hardcoding column names in multiple places.
COLUMNS = {
    "text": TEXT_COLUMN,
    "profession": PROFESSION_COLUMN,
    "gender": GENDER_COLUMN,
    "explanation": EXPLANATION_COLUMN,
    "id": ID_COLUMN,
}

# Experiment settings
EXPERIMENT_ID = "dev_test_001"
SCORE_MODE = "content_only"  # "content_only" or "explanation_aware" to use the explanation column in scoring
MODEL_NAME = "gpt_4o_mini" # for now only supports gpt_4o_mini
GPT_MODELS = {"gpt_4o_mini": "gpt-4o-mini"}
RUN_MODE = "filter"  # "prepare", "submit", "check", "download", "filter"
DRY_RUN = False  # Applies to submit only. Set to False to actually send a paid api request.

REMOVE_FRACTION = 0.20  # Fraction of highest scored biographies to remove
MAX_REQUESTS_PER_BATCH = 1000  # Number of biographies per batch input file

# Paths
BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR / "bias_in_bios_sample" / "dev.csv"  # Testing only, we will use synthetic data later
OUTPUT_DIR = BASE_DIR / "filtering_outputs"


def main():
    """Runs a single filtering stage, either preparing, submitting, checking, downloading or filtering.

        prepare: Loads and validates input data, adds unique IDs if needed, saves a snapshot of the dataset, and prepares batch json files for OpenAI scoring.
        submit: If it is a dry run it will only print the number of batches and requests to be submitted. Otherwise, it will submit the prepared batches to OpenAI for scoring.
        check: Checks the status of submitted batches.
        download: Downloads and parses the results of submitted batches.
        filter: Filters the dataset based on the downloaded scores and saves the results.
    """
    if RUN_MODE not in {"prepare", "submit", "check", "download", "filter"}:
        raise ValueError(f"The run mode ({RUN_MODE}) you chose does not exist...")


    model_id = GPT_MODELS[MODEL_NAME]
    snapshot_path = OUTPUT_DIR / EXPERIMENT_ID / "synthetic_with_ids.csv"

    if snapshot_path.exists(): # load snapshot if it exists, otherwise load input and add IDs
        df = load_data(snapshot_path, ID_COLUMN)
        print(f"Loaded existing dataset: {snapshot_path}")

    else: # snapshot does not exist, so we load the data and add IDs
        if RUN_MODE != "prepare":
            raise FileNotFoundError(f"No dataset snapshot: {snapshot_path}. Run prepare first.") # prepare mode always needs to run first to create the snapshot.

        if INPUT_PATH is None:
            raise ValueError("INPUT_PATH has not been configured.")

        df = load_data(INPUT_PATH, ID_COLUMN)
        df = add_biography_ids(df, ID_COLUMN)

    validate_data(df, SCORE_MODE, COLUMNS) # we always validate data

    if RUN_MODE == "prepare":
        if not snapshot_path.exists():
            save_dataset_snapshot(df, EXPERIMENT_ID, OUTPUT_DIR)
            print(f"Saved dataset snapshot to {snapshot_path}")

        batch_paths = prepare_openai_batches( # Split the data into batches of the specified size and write them to jsonl files for OpenAI scoring.
            df, SCORE_MODE, MODEL_NAME, EXPERIMENT_ID,
            MAX_REQUESTS_PER_BATCH, model_id, COLUMNS, OUTPUT_DIR,
        )
        print(f"{len(batch_paths)} batch file(s) ready.")
        return

     # This creates a list of all the expected custom IDs for the prepared batches, based on the data used.
    expected_ids = []
    for bio_id in df[ID_COLUMN]:
        request_id = custom_id_for(SCORE_MODE, bio_id)
        expected_ids.append(request_id)

    batch_paths = find_prepared_batches( # This finds the actual custom ids from the prepared batch files, and checks that they match the expected IDs. Raises an error if they do not match.
        OUTPUT_DIR, EXPERIMENT_ID, MODEL_NAME, SCORE_MODE, expected_ids
    )

    if RUN_MODE == "submit":
        client = None if DRY_RUN else create_openai_client(BASE_DIR) # If it is a dry run, we do not create the client, otherwise we create it to really submit the batches.
        submit_prepared_batches(client, batch_paths, EXPERIMENT_ID, OUTPUT_DIR, DRY_RUN) # Actual submission of the batches

    elif RUN_MODE == "check": # Checks the status of the submitted batches, and prints the status of each batch.
        check_submitted_batches(
            create_openai_client(BASE_DIR), batch_paths, EXPERIMENT_ID, OUTPUT_DIR
        )
    elif RUN_MODE == "download": # Downloads the raw results from OpenAI and saves them and also parses them to a csv file only the scores per custom ID.
        download_and_parse_results(
            create_openai_client(BASE_DIR), batch_paths, EXPERIMENT_ID,
            OUTPUT_DIR, MODEL_NAME, SCORE_MODE, expected_ids,
        )
    elif RUN_MODE == "filter": # Filters the dataset based on the downloaded scores, removes the highest scored biographies, and saves the results to a new directory.
        scores_path = (
            OUTPUT_DIR / EXPERIMENT_ID / "batch_results" / "openai"
            / f"{MODEL_NAME}_{SCORE_MODE}_scores.csv"
        )
        if not scores_path.exists():
            raise FileNotFoundError(f"No validated scores: {scores_path}. Run download first.")
        scores = pd.read_csv(scores_path, dtype={"custom_id": "string"})
        scored = merge_scores(df, scores, SCORE_MODE, ID_COLUMN)
        n_remove = int(len(scored) * REMOVE_FRACTION)  # Round down.
        kept, removed = filter_highest_scores(scored, n_remove)
        result_dir = OUTPUT_DIR / EXPERIMENT_ID / "results" / MODEL_NAME / SCORE_MODE
        save_results(scored, kept, removed, result_dir)
        print(f"Kept {len(kept)} biographies; removed {len(removed)}. Saved in {result_dir}")


if __name__ == "__main__":
    main()
