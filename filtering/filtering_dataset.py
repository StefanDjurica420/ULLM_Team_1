"""Dataset loading, ID assignment, validation, and reproducible snapshots."""
from pathlib import Path
import pandas as pd


def load_data(path, id_column="bio_id"):
    """Read a csv file into a dataframe"""
    return pd.read_csv(path, dtype={id_column: "string"})


def add_biography_ids(df, id_column):
    """Adds an unique id column to the dataframe if it does not exist yet."""
    df = df.copy()

    if id_column not in df.columns:
        df[id_column] = range(len(df))

    return df


def validate_data(df, scoring_mode, columns):
    """Checks for required columns, non-empty values and unique IDs."""
    valid_modes = ["content_only", "explanation_aware"]

    if scoring_mode not in valid_modes:
        raise ValueError(
            f"Invalid scoring mode: {scoring_mode}. "
            f"Expected one of {valid_modes}."
        )

    required_columns = [
        columns["text"],
        columns["profession"],
        columns["gender"],
        columns["id"],
    ]

    if scoring_mode == "explanation_aware": # Need explanation column only for explanation aware mode
        required_columns.append(columns["explanation"])

    missing_columns = [name for name in required_columns if name not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if df.empty:
        raise ValueError("The dataset has no biographies.")

    for column in required_columns:
        if df[column].isna().any() or (df[column].astype(str).str.strip() == "").any():
            raise ValueError(f"Column {column!r} contains missing or empty values.")

    id_column = columns["id"]
    if not df[id_column].astype(str).is_unique:
        raise ValueError("Biography IDs must be unique.")


def save_dataset_snapshot(df, experiment_id, output_dir):
    """Save the input dataset with IDs to a reproducible snapshot file, which is later used for submit, download and filter modes."""
    output_path = Path(output_dir) / experiment_id / "synthetic_with_ids.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, mode="x")
    return output_path
