"""Prepare, submit, check, and download GPT scoring batches."""

import json
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

from filtering_scoring import build_prompt, custom_id_for, parse_score


def build_openai_batch_request(row, scoring_mode, model_id, columns):
    """Build one JSON request for a single biography, including a custom ID to match the response with the original data."""
    prompt = build_prompt(row, scoring_mode, columns)

    return {
        "custom_id": custom_id_for(scoring_mode, row[columns["id"]]),
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": model_id,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "max_completion_tokens": 20,
        },
    }


def get_openai_batch_path(output_dir, experiment_id, model_name, scoring_mode, batch_number=1):
    """Return the path for one batch input file."""
    filename = f"{model_name}_{scoring_mode}_batch_{batch_number:04d}.jsonl"
    return Path(output_dir) / experiment_id / "batch_inputs" / "openai" / filename



def write_openai_batch_file(df, scoring_mode, model_id, columns, output_path):
    """Write one JSONL request per biography in a batch input file"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "x", encoding="utf-8") as file:
        for _, row in df.iterrows():
            request = build_openai_batch_request(row, scoring_mode, model_id, columns)
            file.write(json.dumps(request) + "\n")

    return output_path


def prepare_openai_batches(
    df,
    scoring_mode,
    model_name,
    experiment_id,
    max_requests_per_batch,
    model_id,
    columns,
    output_dir,
):
    """Check if batches already exist, and if not split the data into batches of the specified size and write them to jsonl files for OpenAI scoring."""

    # Check if the first batch file already exists, and if so, raise an error to avoid overwriting existing files.
    first_batch_file_path = get_openai_batch_path(
        output_dir, experiment_id, model_name, scoring_mode, 1
    )
    batch_input_dir = first_batch_file_path.parent

    existing_batch_files = list(
        batch_input_dir.glob(f"{model_name}_{scoring_mode}_batch_*.jsonl")
    )

    if existing_batch_files:
        raise FileExistsError(
            f"Batch files already exist in {batch_input_dir}. "
            "If preparation completed, continue with submit. "
            "Otherwise, use a new experiment ID."
        )

    # Here we split the data into batches of the specified size and write them to jsonl files for OpenAI scoring.
    batch_file_paths = []

    for batch_number, start_row in enumerate(
        range(0, len(df), max_requests_per_batch), start=1
    ):
        batch_biographies = df.iloc[
            start_row:start_row + max_requests_per_batch
        ]
        batch_file_path = get_openai_batch_path(# This creates the path for the batch input file.
            output_dir, experiment_id, model_name, scoring_mode, batch_number
        )

        write_openai_batch_file(# This writes the batch input file with one JSON request per biography to the ealier created path.
            batch_biographies, scoring_mode, model_id, columns, batch_file_path
        )
        batch_file_paths.append(batch_file_path)

    return batch_file_paths


def create_openai_client(base_dir):
    """Load the API key from a .env file and initialize the OpenAI SDK client."""
    load_dotenv(Path(base_dir) / ".env")
    return OpenAI()


def get_batch_metadata_path(batch_path, experiment_id, output_dir):
    """Creates path to which the batch metadata JSON file should be written, based on the batch input file path."""
    batch_path = Path(batch_path)
    return Path(output_dir) / experiment_id / "batch_jobs" / f"{batch_path.stem}.json"


def save_batch_metadata(batch_path, experiment_id, uploaded_file_id, batch_id, output_dir):
    """Saves id's given to the batch by OpenAI in a JSON file and returns the file path."""
    metadata_path = get_batch_metadata_path(batch_path, experiment_id, output_dir)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)

    metadata = {
        "input_file": str(batch_path),
        "openai_file_id": uploaded_file_id,
        "openai_batch_id": batch_id,
        "status": "submitted",
    }

    with open(metadata_path, "x", encoding="utf-8") as file:
        json.dump(metadata, file, indent=4)

    return metadata_path


def submit_openai_batch(client, batch_path, experiment_id, output_dir):
    """Upload and submit a batch once, skipping already submitted batches."""
    batch_path = Path(batch_path)
    if not batch_path.is_file():
        raise FileNotFoundError(f"Batch file not found: {batch_path}")

    metadata_path = get_batch_metadata_path(batch_path, experiment_id, output_dir)
    # Check if the batch has already been submitted by looking for the metadata file.
    if metadata_path.exists():
        raise FileExistsError(f"Batch already has metadata: {metadata_path}")

    with open(batch_path, "rb") as file:
        uploaded_file = client.files.create(file=file, purpose="batch")

    batch = client.batches.create(
        input_file_id=uploaded_file.id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
    )
    # Print id immediatly in case the metadata save fails, so we can still check the batch status on OpenAI's website.
    print(f"OpenAI batch ID: {batch.id}")

    return save_batch_metadata(# Create the batch metadata file with the OpenAI file and batch IDs, and return the path to the metadata file.
        batch_path, experiment_id, uploaded_file.id, batch.id, output_dir
    )


def check_openai_batch_status(client, batch_id):
    """Retrieve and print the current processing status of one batch."""
    batch = client.batches.retrieve(batch_id)

    print(f"Batch ID: {batch.id}")
    print(f"Status: {batch.status}")
    print(f"Completed: {batch.request_counts.completed}")
    print(f"Failed: {batch.request_counts.failed}")
    print(f"Total: {batch.request_counts.total}")

    return batch


def find_prepared_batches(output_dir, experiment_id, model_name, scoring_mode, expected_ids):
    """Find the runs input batches and verify that the total custom ids in here match the IDs we would expect from the snapshot. Raises an error if they do not match."""
    input_dir = Path(output_dir) / experiment_id / "batch_inputs" / "openai"
    paths = sorted(input_dir.glob(f"{model_name}_{scoring_mode}_batch_*.jsonl"))

    if not paths:
        raise FileNotFoundError(f"No prepared batches found in {input_dir}. Run prepare first.")

    # This extracts the custom IDs from the prepared batch files
    found_ids = []
    for path in paths:
        with path.open("r", encoding="utf-8") as file:
            for line in file:
                found_ids.append(json.loads(line)["custom_id"])

    # Two similarity checks: 1) check for duplicates in the found IDs, and 2) check that the found IDs match the expected IDs from the snapshot. Raises an error if either check fails.
    if len(found_ids) != len(set(found_ids)):
        raise ValueError("Prepared batches contain duplicate custom_id values.")
    if set(found_ids) != set(expected_ids):
        raise ValueError("Prepared batches do not match the experiment snapshot. Run prepare with a new experiment ID.")
    return paths


def submit_prepared_batches(client, batch_paths, experiment_id, output_dir, dry_run=False):
    """Submit batches that do not have saved submission metadata (to avoid duplicates). When in dry_run mode, only print the number of batches to submit and do not actually submit them."""
    batches_to_submit = []

    for batch_path in batch_paths:
        metadata_path = get_batch_metadata_path(
            batch_path, experiment_id, output_dir
        )
        if not metadata_path.exists(): # If the batch has no metadata, it has not been submitted yet, so we add it to the list of batches to submit.
            batches_to_submit.append(batch_path)

    request_count = 0

    for batch_path in batches_to_submit:
        with batch_path.open("r", encoding="utf-8") as batch_file:
            for line in batch_file:
                request_count += 1

    # Checks diff between the number of batches already recorded and the number of batches to submit.
    recorded_count = len(batch_paths) - len(batches_to_submit)
    print(f"Already recorded: {recorded_count} batch(es)")
    print(f"To submit: {len(batches_to_submit)} batch(es), {request_count} request(s)")

    # only submit if not a dry run and there are batches to submit.
    if dry_run or not batches_to_submit:
        return

    if client is None:
        raise ValueError("An OpenAI client is required when dry_run is False.")

    for batch_path in batches_to_submit:
        metadata_path = submit_openai_batch( # This actually submits the batch to OpenAI via the api and saves the metadata to a JSON file.
            client, batch_path, experiment_id, output_dir
        )
        print(f"Saved: {metadata_path}")


def check_submitted_batches(client, batch_paths, experiment_id, output_dir):
    """Check every recorded batch and save its latest status and counts."""
    checked = 0
    for path in batch_paths:
        metadata_path = get_batch_metadata_path(path, experiment_id, output_dir)
        # Check if the batch has been submitted by looking for the metadata file.
        if not metadata_path.exists():
            print(f"Not submitted: {path.name}")
            continue
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        batch = check_openai_batch_status(client, metadata["openai_batch_id"]) # This prints the batch status
        metadata["status"] = batch.status
        metadata["request_counts"] = {
            "total": batch.request_counts.total,
            "completed": batch.request_counts.completed,
            "failed": batch.request_counts.failed,
        }
        metadata["output_file_id"] = batch.output_file_id
        metadata["error_file_id"] = batch.error_file_id
        metadata_path.write_text(json.dumps(metadata, indent=4), encoding="utf-8")
        checked += 1
    print(f"Checked {checked} submitted batch(es).")


def download_and_parse_results(
    client, batch_paths, experiment_id, output_dir, model_name, scoring_mode, expected_ids
):
    """Download batch results and save one valid score per biography."""
    result_dir = Path(output_dir) / experiment_id / "batch_results" / "openai"
    scores_path = result_dir / f"{model_name}_{scoring_mode}_scores.csv"

    if scores_path.exists():
        raise FileExistsError(f"Scores already saved: {scores_path}")

    result_dir.mkdir(parents=True, exist_ok=True)
    scores = {}

    # This iterates over all the prepared batch files, downloads the results from OpenAI, and parses the scores. It raises an error if any batch has not been submitted or is not completed, or if any score is invalid.
    for batch_path in batch_paths:
        metadata_path = get_batch_metadata_path(
            batch_path, experiment_id, output_dir
        )
        if not metadata_path.exists():
            raise FileNotFoundError(
                f"Batch has not been submitted: {batch_path.name}"
            )

        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        batch = client.batches.retrieve(metadata["openai_batch_id"])

        if batch.status != "completed":
            raise ValueError(
                f"Batch {batch.id} is {batch.status}; check it before downloading."
            )

        result_files = [
            ("output", batch.output_file_id),
            ("error", batch.error_file_id),
        ]

        for kind, file_id in result_files:
            if not file_id:
                continue

            raw_path = result_dir / f"{batch_path.stem}_{kind}.jsonl"

            if not raw_path.exists():
                with raw_path.open("x", encoding="utf-8") as raw_file:
                    raw_file.write(client.files.content(file_id).text)

            with raw_path.open("r", encoding="utf-8") as raw_file:
                for line_number, line in enumerate(raw_file, start=1):
                    item = json.loads(line)
                    custom_id = item.get("custom_id")

                    if not custom_id:
                        raise ValueError(
                            f"Missing custom_id in {raw_path.name}:{line_number}"
                        )

                    if kind == "error":
                        raise ValueError(
                            f"OpenAI reported an error for {custom_id}: "
                            f"{item.get('error')}"
                        )

                    if custom_id in scores:
                        raise ValueError(f"Duplicate response for {custom_id}")

                    try:
                        response = item["response"]

                        if item.get("error") or response["status_code"] != 200:
                            raise ValueError("request failed")

                        choice = response["body"]["choices"][0]

                        if choice["finish_reason"] != "stop":
                            raise ValueError(
                                f"finish_reason={choice['finish_reason']}"
                            )

                        raw_score = choice["message"]["content"]
                        if not isinstance(raw_score, str):
                            raise ValueError("missing score text")

                        score = parse_score(raw_score)

                    except (KeyError, IndexError, TypeError, ValueError) as error:
                        raise ValueError(
                            f"Invalid response for {custom_id} in "
                            f"{raw_path.name}:{line_number}: {error}"
                        ) from error

                    scores[custom_id] = (score, raw_score)

    # check that the scores we received match the expected IDs from the snapshot. Raises an error if they do not match.
    expected = set(expected_ids)
    received = set(scores)

    missing = expected - received
    unexpected = received - expected

    if missing or unexpected:
        raise ValueError(
            f"Scores do not match the dataset: "
            f"{len(missing)} missing, {len(unexpected)} unexpected. "
            f"Examples: missing {sorted(missing)[:5]}, "
            f"unexpected {sorted(unexpected)[:5]}"
        )

    # Create csv file with one row per biography, containing the custom ID, the parsed score, and the raw model response. The file is saved to the batch_results/openai directory.
    score_rows = []

    for custom_id in expected_ids:
        score, raw_score = scores[custom_id]
        score_rows.append({
            "custom_id": custom_id,
            "bias_score": score,
            "model_response": raw_score,
        })

    pd.DataFrame(score_rows).to_csv(scores_path, index=False, mode="x")
    print(f"Saved {len(score_rows)} validated scores: {scores_path}")
    return scores_path