# Filtering the biographies
In the filtering scripts the synthetic biographies are given a gender bias score from 1.0 to 5.0 by either GPT-4o-mini or Meta Llama 3.1 8B Instruct Turbo.
The k highest scoring biographies are then removed.

There are two scoring modes:
- `content_only`: the model receives the biography, profession and gender.
- `explanation_aware`: the model receives biography, profession, gender and an explanation.

This explanation is created by the model which creates the synthetic data. It is asked to explain why it generated the biography the way it did.

## Experiments

The synthetic data created by both models is also scored and filtered by the same models.

- GPT-4o-mini is used for filtering through the OpenAI Batch API.
- Llama 3.1 8B Instruct Turbo through DeepInfra, using the shared `llm_api` code from the data generation.

Each combination of synthetic data source LLM and filtering LLM was run in both scoring modes, resulting in eight total filtering runs. Each run scored 15,008 biographies, and removed 2,000, resulting in a filtered dataset of 13,008.

## Scoring prompt

All runs used the same prompt structure. Each prompt contained five example biographies, including a score and a short reason to guide the model. The prompt is defined in `filtering/filtering_scoring.py`.

## Files

- `filter_synthetic_data_openai.py`: configuration of experiment settings, and runs the experiment stages for the GPT-4o-mini filtering.

- `filter_synthetic_data_llama.py`: configuration of experiment settings, and runs the experiment stages for the Llama 3.1 8B filtering.

- `filtering/filtering_dataset.py`: loads, adds IDs, validates, and saves synthetic data.

- `filtering/filtering_scoring.py`: builds prompt and parses scorer model reply.

- `filtering/filtering_openai.py`: builds OpenAI batch requests in the correct format, submits them, checks them, and downloads/parses results.

- `filtering/filtering_llama.py`: calls Llama API and saves valid scores.

- `filtering/filtering_results.py` matches scores to biographies, filters for highest scores, and saves results.

## Input and setup

Use `python -m pip install -r requirements.txt` to install the required packages.

The GPT script reads `OPENAI_API_KEY` from a `.env` file.

The Llama script uses `DEEPINFRA_API_KEY` from the environment, see llm_api/README.md for detailed instructions.

The synthetic data is generated in JSONL format, which was converted to CSV format. The `INPUT_PATH` was then set to the correct CSV for
the GPT-4o-mini and Llama 3.1 8B generated biographies, separately.

The input synthetic data files need a `hard_text`, `profession` and `gender` column. For explanation-aware filtering also an `explanation` column is required.

Before running either script, configure:

- `INPUT_PATH`: the path to the CSV for the generated synthetic data you want to filter.
- `EXPERIMENT_ID`: a unique ID for the experiment to make the results identifiable
- `SCORE_MODE`: `content_only` or `explanation_aware`.
- `NUMBER_TO_REMOVE`: the number of biographies that will be removed.
- `MAX_REQUESTS_PER_BATCH`: number of biographies per batch.

## GPT-4o-mini
Run `python filter_synthetic_data_openai.py`, through the following stages by setting the `RUN_MODE` to:

1. `prepare`: to save the dataset with IDs and create JSONL formatted batch input files.
2. `submit`: with `DRY_RUN = True` to print the number of created batches. Set `DRY_RUN = False` to actually submit the batches
3. `check`: to print the status of the submitted batches.
4. `download`: to save the raw responses and create a CSV with valid scores.
5. `filter` matches the scores to the saved dataset of step 1 and creates `scored.csv`, `kept.csv` and `removed.csv`, by filtering it.

The experiment runs used a batch size of 1,000, resulting in 16 batch files for each run.

## Llama
Run `python filter_synthetic_data_llama.py`, through the following stages by setting the `RUN_MODE` to:

1. `prepare`: to save the dataset with IDs
2. `score` : Sends one request per biography and saves the raw results.
3. `filter` matches the scores to the saved dataset and creates `scored.csv`, `kept.csv` and `removed.csv`, by filtering it.

Llama uses individual API calls rather than the OpenAI Batch API. This means there were 15,008 calls per run.

## Output

Everything is saved under `filtering_outputs/<experiment>/`:

- `synthetic_with_ids.csv`: the saved input dataset.
- `batch_inputs/openai/`: GPT batch request files.
- `batch_jobs/`: saved OpenAI batch IDs.
- `batch_results/openai/`: downloaded GPT-4o-mini responses and validated scores.
- `scoring_results/llama/`: raw Llama 3.1 8B answers and validated scores.
- `results/<model>/<mode>/`: the final three CSV files:

    - `scored.csv`: all biographies with their scores and model responses.
    - `kept.csv`: the biographies remaining after filtering.
    - `removed.csv`: the highest scoring biographies that were removed.

Scores are matched to the original biographies using their request IDs. If scores are tied, the  row order in the original dataset decides which biographies are removed and kept.
