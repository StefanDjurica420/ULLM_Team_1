"""Score biographies with Llama through the shared llm_api code from the synthetic data generation."""

from pathlib import Path
import pandas as pd

from llm_api import get_model, read_jsonl, run_prompts # imports from the shared api code for synthetic data generation
from .filtering_scoring import build_prompt, custom_id_for, parse_score


def get_llama_scores_path(output_dir, experiment_id, scoring_mode):
    """Return the path of Llama's finished scores csv file."""
    return (
        Path(output_dir)
        / experiment_id
        / "scoring_results"
        / "llama"
        / f"llama_{scoring_mode}_scores.csv"
    )


def score_llama_biographies(
    df,
    scoring_mode,
    columns,
    experiment_id,
    output_dir,
    limit=None,
    mock=None,
):
    """Call Llama and save one valid score for every biography in a single csv file."""
    scores_path = get_llama_scores_path(output_dir, experiment_id, scoring_mode)
    raw_path = scores_path.parent / f"llama_{scoring_mode}_raw.jsonl"

    if scores_path.exists():
        print(f"Scores already saved: {scores_path}")
        return scores_path

    # add custom id to the data for each biography api call, so we can match the scored data with the original data
    requests = []
    expected_ids = [] # save expected ids to check that we get all the scores back from Llama

    for _, biography in df.iterrows():
        request_id = custom_id_for(scoring_mode, biography[columns["id"]])
        prompt = build_prompt(biography, scoring_mode, columns)

        requests.append({
            "id": request_id,
            "prompt": prompt,
        })
        expected_ids.append(request_id)


    llama = get_model("llama", json_mode=False, max_tokens=20) # We need a single number so json_mode is False and max_tokens is small.

    run_prompts(requests, llama, raw_path, limit=limit, mock=mock)

    # This part of the code reads the raw Llama output and validates it
    scores = {}
    expected_id_set = set(expected_ids)

    for answer in read_jsonl(raw_path):
        request_id = answer.get("id")

        if request_id not in expected_id_set:
            raise ValueError(f"Unexpected ID in Llama results: {request_id}")

        if request_id in scores:
            raise ValueError(f"Duplicate Llama result for {request_id}")

        if answer.get("finish_reason") != "stop":
            raise ValueError(f"Llama did not finish its answer for {request_id}")

        raw_response = answer.get("raw")

        if not isinstance(raw_response, str):
            raise ValueError(f"No answer text for {request_id}")

        try:
            score = parse_score(raw_response)
        except ValueError as error:
            raise ValueError(
                f"Invalid Llama score for {request_id}: {raw_response!r}"
            ) from error

        scores[request_id] = (score, raw_response)

    missing_ids = []

    for request_id in expected_ids:
        if request_id not in scores:
            missing_ids.append(request_id)

    if missing_ids:
        print(
            f"Saved {len(scores)} of {len(expected_ids)} scores. "
            f"{len(missing_ids)} still missing; run score again to continue."
        )
        return None

    # Save the validated scores to a CSV file
    score_rows = []

    for request_id in expected_ids:
        score, raw_response = scores[request_id]

        score_rows.append({
            "custom_id": request_id,
            "bias_score": score,
            "model_response": raw_response,
        })

    pd.DataFrame(score_rows).to_csv(scores_path, index=False, mode="x")
    print(f"Saved {len(score_rows)} validated scores: {scores_path}")

    return scores_path