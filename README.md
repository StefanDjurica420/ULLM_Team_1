# Does Access to Generator Explanations Improve Synthetic Data Filtering for Gender Bias Mitigation?

The first paper investigates how bias can be inherited through LLM-generated training data. Building on this setting, we propose to investigate whether access to the generator’s explanations helps an LLM filter select synthetic training examples that lead to lower downstream gender bias while preserving task performance.

## Research question

Does explanation-aware filtering reduce downstream gender bias more effectively than content-only filtering when both methods select the same number of synthetic training examples?

## Dataset and task

We plan to use Bias in Bios, which is also used in the paper Understanding and Mitigating Bias Inheritance in LLM-based Data Augmentation on Downstream Tasks. The downstream task will be occupation classification from biographies, and we will compare how well the model identifies each occupation for men and women.

We may restrict the experiment to a subset of occupations.

## Synthetic data generation

Using only the original data from the training split as a reference, an LLM will generate a shared pool of synthetic biographies, for example 10,000 examples, potentially more depending on the size of the training dataset.

Each generated record will contain:

- A synthetic biography.
- An occupation label, which can be specified in the generation prompt.
- A gender annotation for distribution analysis.
- A short explanation of the generator’s choices regarding the biography’s content and the person’s attributes.

We will use these explanations as extra information, without assuming they reflect how the model actually made its choices. We will first run a small pilot to check whether they provide useful details about each generated example.

## Filtering conditions

We will compare three selection strategies applied independently to the same synthetic pool:

1. **Random selection:** randomly select K examples.
2. **Content-only filtering:** an LLM evaluates the biography and occupation label.
3. **Explanation-aware filtering:** the same LLM evaluates the same information together with the generator’s explanation.

Both LLM filters will use the same evaluation criteria, covering stereotypical content, relevance, and consistency with the occupation label. Each strategy will retain the same number of examples, for example 2,000 out of 10,000.

We will record the occupation and gender distributions of the selected subsets. A comparison with matched occupation and gender counts will help distinguish the contribution of the explanations from changes in group representation alone.

## Downstream training

We will fine-tune separate copies of the same initial model under five conditions:

1. Original training data only.
2. Original data plus all synthetic examples.
3. Original data plus the randomly selected subset.
4. Original data plus the content-only filtered subset.
5. Original data plus the explanation-aware filtered subset.

The classification training examples will contain biographies and occupation labels. Generator explanations will be used only for selection and will not be included in downstream training.

The three K-example conditions will use matched training settings. The full synthetic-data condition will provide an additional reference, with its larger dataset size and training cost reported explicitly.

## Evaluation

All trained models will be evaluated on the same held-out test set. We will measure:

- Overall occupation-classification performance, such as macro-F1.
- Gender differences in true positive rates within occupations.
- Variation across repeated training runs.

Development data will be used to refine prompts and selection settings. The final test set will not be used to choose these settings.

The primary comparison is explanation-aware versus content-only filtering. Random selection tests whether filtering provides a benefit beyond selecting fewer examples, while the original-only and full-pool conditions establish the effects of augmentation.

## Shuffled explanations

If needed, we will add a condition in which the filter receives an explanation from a different synthetic example of the same occupation, with approximately matched length.

This tests whether any benefit depends on the explanation being associated with the specific example, rather than merely providing additional text. Results will be interpreted cautiously because mismatched explanations may also introduce contradictions.

## Potential contribution

The intended contribution is a controlled empirical study of whether generator explanations provide useful information for fairness-oriented synthetic data selection and whether that information translates into improved downstream behavior.

We do not assume that explanation-aware filtering will outperform the alternatives. A negative result could suggest that generator explanations are uninformative or misleading for this purpose under the tested conditions. The novelty of the specific comparison must be established against prior work on bias mitigation through data filtering and explanation-based data selection.

## GPT filtering pipeline

This pipeline uses GPT-4o-mini through the OpenAI Batch API to score biographies for gender bias. Each request asks GPT to score one biography; multiple requests are placed in a JSONL file and submitted as a batch job. After downloading and validating the scores, the pipeline removes the biographies with the highest scores. The dev_test_001 run used 10 biographies from dev.csv to test the full workflow. It is a pipeline test, not a result from the group’s synthetic dataset.

### Code files

- `filter_synthetic_data.py` contains the settings and runs one stage at a time.
- `filtering_dataset.py` loads the input, checks its columns and IDs, and saves a copy with biography IDs.
- `filtering_scoring.py` builds the GPT prompt and checks that each response is a score from 1.0 to 5.0.
- `filtering_openai.py` prepares and submits batches, checks their status, and downloads their results.
- `filtering_results.py` matches scores to biographies and saves the filtered datasets.

### Input and setup

The input CSV needs `hard_text`, `profession`, and `gender` columns. Explanation-aware scoring also needs an `explanation` column. A `bio_id` column is optional: the code adds IDs if they are missing.

1. Install Python 3.12 and the packages in `requirements.txt` with `python -m pip install -r requirements.txt`.
2. Put `OPENAI_API_KEY=your_key` in a local `.env` file. Do not commit this file.
3. Set `INPUT_PATH`, `EXPERIMENT_ID`, `SCORE_MODE`, `MAX_REQUESTS_PER_BATCH`, and `REMOVE_FRACTION` near the top of `filter_synthetic_data.py`. Use a new experiment ID for a new input dataset or a changed prompt, model, or batch size.

### Run the stages

Change `RUN_MODE` in `filter_synthetic_data.py`, then run `python filter_synthetic_data.py` for each stage:

1. **`prepare`** checks the data, saves `synthetic_with_ids.csv`, and creates JSONL batch input files. Run this once per experiment and scoring mode.
2. **`submit`** shows the number of batches and biography requests waiting to be submitted. With `DRY_RUN = True`, it only prints these counts. Set `DRY_RUN = False` to submit them to OpenAI; batches with saved submission IDs are skipped.
3. **`check`** shows the status of submitted batches.
4. **`download`** runs after all batches are complete. It saves the raw OpenAI responses and creates a scores CSV only if every biography has one valid score.
5. **`filter`** matches scores back to the input biographies and saves `scored.csv`, `kept.csv`, and `removed.csv`.

Files are saved under `filtering_outputs/<experiment>/`. The `batch_inputs/` folder contains requests, `batch_jobs/` contains submission IDs, `batch_results/` contains raw responses and scores, and `results/<model>/<mode>/` contains the final CSVs. This output folder is ignored by Git.

The number removed is `int(number_of_biographies * REMOVE_FRACTION)`, rounded down. If scores are tied, the original row order decides which biographies are removed. Existing batch inputs and final score files are not overwritten.
