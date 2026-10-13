# Filtering the biographies

The filtering scripts ask a model to give each biography a gender bias score from 1.0 to 5.0. The biographies with the highest scores are then removed. `content_only` gives the model the biography, profession and gender. `explanation_aware` also includes the explanation written by the model that generated the biography.

This README describes the code we have now. The `dev_test_001` GPT run used 10 rows from `dev.csv` to check the full process. Llama has also been tested on four real API calls. These are code checks, not results from the final synthetic dataset.

## Files

- `filter_synthetic_data_openai.py` runs the GPT-4o-mini filtering stages through the OpenAI Batch API.
- `filter_synthetic_data_llama.py` runs the Llama stages through the shared `llm_api` code.
- `filtering/filtering_dataset.py` loads the CSV, checks its columns and IDs, and saves a copy with biography IDs.
- `filtering/filtering_scoring.py` builds the prompt and checks that an answer is a number from 1.0 to 5.0.
- `filtering/filtering_openai.py` prepares, submits, checks and downloads the GPT batches.
- `filtering/filtering_llama.py` calls Llama and saves its scores.
- `filtering/filtering_results.py` matches scores to biographies and saves the filtered CSVs.

## Input and setup

The input must be a CSV with `hard_text`, `profession` and `gender` columns. `explanation_aware` also needs an `explanation` column. `bio_id` is optional; the code adds IDs if they are missing.

Both scripts currently point to the local `bias_in_bios_sample/dev.csv` file. That sample has numerical profession and gender labels, and the prompt uses those values exactly as they appear in the CSV. For the synthetic data, the filtering CSV will need to be made from `pool.jsonl`: use its `id` as `bio_id`, its `bio` as `hard_text`, and keep the profession, gender and explanation. `pool_training.jsonl` has numerical labels and no explanations, so it is not the input for explanation-aware scoring. This conversion is not part of the filtering scripts yet.

Install the packages with `python -m pip install -r requirements.txt`. The GPT script reads `OPENAI_API_KEY` from a local `.env` file. The Llama script uses `DEEPINFRA_API_KEY` from the environment; see [llm_api/README.md](llm_api/README.md) for the token setup. Do not commit API keys.

In either script, set `INPUT_PATH`, `EXPERIMENT_ID`, `SCORE_MODE` and `NUMBER_TO_REMOVE` before running. `NUMBER_TO_REMOVE` is the number removed, not the number kept, and it must be smaller than the number of biographies. The `prepare` stage saves `filtering_outputs/<experiment>/synthetic_with_ids.csv`. Later stages load this saved CSV, so changing `INPUT_PATH` with the same experiment ID will not change the data being scored. Use a new experiment ID for a different input dataset or prompt.

## GPT-4o-mini

Set `RUN_MODE` in `filter_synthetic_data_openai.py`, then run `python filter_synthetic_data_openai.py` for each stage:

1. `prepare` saves the dataset with IDs and makes JSONL batch input files. Each line is one request for one biography. `MAX_REQUESTS_PER_BATCH` controls how many requests go in each file. Existing batch input files are not overwritten.
2. `submit` prints how many batches and requests are waiting. With `DRY_RUN = True`, it only prints the counts. Set `DRY_RUN = False` to submit paid batch jobs. Batches that already have saved submission IDs are skipped.
3. `check` prints the status of the submitted batches.
4. `download` saves the raw responses and creates a scores CSV after every biography has one valid score.
5. `filter` matches the scores to the saved dataset and writes `scored.csv`, `kept.csv` and `removed.csv`.

## Llama

Set `RUN_MODE` in `filter_synthetic_data_llama.py`, then run `python filter_synthetic_data_llama.py` for each stage:

1. `prepare` saves the dataset with IDs. It does not make batch files.
2. `score` sends one request per biography using `llm_api` and saves the raw answers. Set `CALL_LIMIT` to a small number to try a few calls first; set it back to `None` to continue with the remaining biographies. A scores CSV is written only when every biography has a valid score.
3. `filter` matches the scores to the saved dataset and writes `scored.csv`, `kept.csv` and `removed.csv`.

The current Llama code stops if a saved answer is not a valid score. It does not automatically retry that answer.

## Output

Everything is saved under `filtering_outputs/<experiment>/`, which Git ignores. GPT batch inputs are in `batch_inputs/openai/`, submitted job IDs in `batch_jobs/`, and downloaded responses and scores in `batch_results/openai/`. Llama raw answers and scores are in `scoring_results/llama/`. The final CSVs are in `results/<model>/<mode>/`.

`scored.csv` contains all biographies with their scores. `kept.csv` contains the biographies left after filtering, and `removed.csv` contains the highest-scoring biographies. If scores are tied, the original row order decides which biographies are removed. Existing final result files are not overwritten.
