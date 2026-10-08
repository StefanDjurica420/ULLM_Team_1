"""Filtering scored biographies and saving resulting datasets."""

from pathlib import Path
from filtering_scoring import custom_id_for, parse_score


def merge_scores(df, scores, scoring_mode, id_column):
    """Attach one valid score to each biography, in snapshot order."""
    # Check that the scores file has the expected columns and valid values, and that it matches the snapshot's IDs.
    required = {"custom_id", "bias_score", "model_response"}
    if not required.issubset(scores.columns):
        raise ValueError(f"Score file is missing columns: {sorted(required - set(scores.columns))}")
    if scores["custom_id"].isna().any() or scores["custom_id"].duplicated().any():
        raise ValueError("Score file contains missing or duplicate custom_id values.")

    expected_ids = []

    for bio_id in df[id_column]:
        request_id = custom_id_for(scoring_mode, bio_id)
        expected_ids.append(request_id)

    expected_id_set = set(expected_ids)
    actual_ids = set(scores["custom_id"])

    if actual_ids != expected_id_set:
        missing = expected_id_set - actual_ids
        extra = actual_ids - expected_id_set
        raise ValueError(
            f"Score IDs do not match the snapshot: "
            f"{len(missing)} missing, {len(extra)} extra."
        )

    # Here the scores are attached to the snapshot in the original order, and parsed to floats between 1.0 and 5.0.
    indexed = scores.set_index("custom_id")
    scored = df.copy()

    parsed_scores = []

    for request_id in expected_ids:
        score_value = indexed.at[request_id, "bias_score"]
        parsed_score = parse_score(str(score_value))
        parsed_scores.append(parsed_score)

    scored["bias_score"] = parsed_scores

    # Model responses are also attached to the scored dataframe, in the same order as the snapshot.
    model_responses = []

    for request_id in expected_ids:
        model_response = indexed.at[request_id, "model_response"]
        model_responses.append(model_response)

    scored["model_response"] = model_responses

    return scored


def filter_highest_scores(df, n_remove):
    """Remove highest scores. Ties are handled by removing them top down, so that the number of removed biographies is exactly n_remove."""
    if not 0 <= n_remove < len(df):
        raise ValueError(f"n_remove must be between 0 and {len(df) - 1}")

    sorted_df = df.sort_values("bias_score", ascending=False, kind="stable")
    removed = sorted_df.head(n_remove).copy()
    kept = df.drop(index=removed.index).copy()

    return kept, removed


def save_results(scored, kept, removed, output_dir):
    """Save separate CSVs without replacing existing experiment results."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    paths = [output_dir / name for name in ("scored.csv", "kept.csv", "removed.csv")]
    if any(path.exists() for path in paths):
        raise FileExistsError(f"Results already exist in {output_dir}. Use a new experiment ID.") # we do not want to overwrite existing results!
    for frame, path in zip((scored, kept, removed), paths):
        frame.to_csv(path, index=False, mode="x")
    return paths
