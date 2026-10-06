from pathlib import Path
import pandas as pd

# Constants for column names for easier reading 
TEXT_COLUMN = "hard_text"
PROFESSION_COLUMN = "profession"
GENDER_COLUMN = "gender"
EXPLANATION_COLUMN = "explanation"

# Experiment configuration
SCORE_MODE = "content_only"  # "content_only" or "explanation_aware"

# TODO: Define once synthetic data generation is finalized
INPUT_PATH = None
OUTPUT_DIR = None

# TODO: Decide filtering amount
N_REMOVE = None

def load_data(path):
    return pd.read_csv(path)

def validate_data(df, scoring_mode):
    """Validate that the input data has the correct columns and that the scoring mode is valid."""
    valid_modes = ["content_only", "explanation_aware"]

    if scoring_mode not in valid_modes:
        raise ValueError(
            f"Invalid scoring mode: {scoring_mode}. "
            f"Expected one of {valid_modes}."
        )

    required_columns = [
        TEXT_COLUMN,
        PROFESSION_COLUMN,
        GENDER_COLUMN,
    ]

    if scoring_mode == "explanation_aware":
        required_columns.append(EXPLANATION_COLUMN)

    missing_columns = []

    for column in required_columns:
        if column not in df.columns:
            missing_columns.append(column)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

def build_prompt(row, scoring_mode):
    """Build a prompt for the scorer model based on the scoring mode and the data in the row."""
    # TODO: Refine prompt using literature

    prompt = f"""
    Evaluate the following synthetic biography for gender bias.

    Biography:
    {row[TEXT_COLUMN]}

    Profession:
    {row[PROFESSION_COLUMN]}

    Gender:
    {row[GENDER_COLUMN]}
    """

    if scoring_mode == "explanation_aware":
        prompt += f"""

        Generator explanation:
        {row[EXPLANATION_COLUMN]}
        """

    prompt += """
    Give the biography a gender bias score from 1.0 to 5.0.

    Return only a single numerical score between 1.0 and 5.0.
    Do not include any explanation, labels, or additional text.

    Example output:
    3.7
    """

    return prompt

def run_scorer(prompt):
    """
    Send the prompt to the chosen LLM scorer and return its raw response.

    The implementation still needs to be decided:
    - load or access a local model,
    - call a locally running model server,
    - or call an external API.
    """

    # TODO: Implement once scorer model and access method are chosen
    raise NotImplementedError(
        "Scorer implementation has not been chosen yet."
    )

def parse_score(response):
    """Parse the raw response from the scorer model and return a float score between 1.0 and 5.0."""
    try:
        score = float(response.strip())
    except ValueError as e:
        raise ValueError(
            f"Could not convert model response to a number: {response}"
        ) from e

    if not 1.0 <= score <= 5.0:
        raise ValueError(
            f"Score must be between 1.0 and 5.0, got {score}"
        )

    return score

def score_biography(row, scoring_mode):
    """Score a single biography row from the dataset, using the specified scoring mode."""
    prompt = build_prompt(row, scoring_mode)
    response = run_scorer(prompt)
    score = parse_score(response)

    return score, response

def score_dataset(df, scoring_mode):
    """Score all biographies in the dataset and return a new DataFrame with scores and model responses."""
    df = df.copy()

    scores = []
    responses = []

    for _, row in df.iterrows():
        score, response = score_biography(
            row,
            scoring_mode
        )

        scores.append(score)
        responses.append(response)

    df["bias_score"] = scores
    df["model_response"] = responses

    return df

def filter_highest_scores(df, n_remove):
    """Remove the top n_remove highest scoring biographies from the dataset."""
    # TODO: Decide what to do with ties and class imbalance after the filtering. For now, we will just remove the top n_remove rows based on the bias_score.
    if not 0 <= n_remove < len(df):
        raise ValueError(
            f"n_remove must be between 0 and {len(df) - 1}"
        )

    sorted_df = df.sort_values(
        "bias_score",
        ascending=False
    )

    removed = sorted_df.head(n_remove).copy()
    kept = sorted_df.iloc[n_remove:].copy()

    return kept, removed

def save_results(scored, kept, removed, output_dir):
    """Save the scored, kept, and removed DataFrames to CSV files in the specified output directory."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    scored.to_csv(
        output_dir / "scored.csv",
        index=False
    )

    kept.to_csv(
        output_dir / "kept.csv",
        index=False
    )

    removed.to_csv(
        output_dir / "removed.csv",
        index=False
    )

def main():
    """Main function to run the scoring and filtering pipeline on synthetic data."""
    # Pipeline cannot run until these decisions are made
    if INPUT_PATH is None:
        return

    if OUTPUT_DIR is None:
        return

    if N_REMOVE is None:
        return

    # Load synthetic data
    df = load_data(INPUT_PATH)

    # Check expected columns
    validate_data(df, SCORE_MODE)

    # Score all biographies
    scored_df = score_dataset(
        df,
        SCORE_MODE
    )

    # Remove highest scoring biographies
    kept_df, removed_df = filter_highest_scores(
        scored_df,
        N_REMOVE
    )

    # Save results
    save_results(
        scored_df,
        kept_df,
        removed_df,
        OUTPUT_DIR
    )


if __name__ == "__main__":
    main()