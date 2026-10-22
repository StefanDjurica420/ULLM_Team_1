# ULLM team one: results of the Snellius runs

Results from Snellius "ullm_results_2026-10-22.tgz" 
size:8.6 MB
md5sum : 03176367a39d38aa2cdc035fefd1f1bf
unpacked in: `snellius_runs/` 
Contains:
- the learning-rate test
- the evaluation results of all trained models. ( )
( The trained models themselves (LoRA adapters) are not included.)

## What was run
### TEST TO DETERMINE LEARNING RATE
- Learning-rate test: 4 learning rates, original data only, evaluated on the dev set
  (1,598 biographies).
### ANALYSIS using determined learning rate
- Model: Llama-3.1-8B-Instruct, fine-tuned with LoRA to classify the profession in a
  biography (28 professions), 3 epochs, learning rate 2e-4, seed 42.
- Test set: 3,998 real Bias in Bios biographies (`testdata_hug/test.json` in the repo).
- 14 models: the base model without fine-tuning, the model trained on the original data
  only, and 12 models trained on original + synthetic data (see "Model names" below).

## Folder structure

```
snellius_runs/
├── summary_seed42_lr2e-4.csv        overview: one row per model and synthetic folder
├── seed42_lr2e-4/                   the 14 models (training seed 42, learning rate 2e-4)
│   └── <model name>/
│       ├── metrics.json             all scores of this model on the test set
│       ├── config.json              settings used for training and evaluation
│       └── predictions.jsonl        the model's answer for every test biography
└── lr_sweep/seed42/                 learning-rate test (dev set)
    └── lr1e-5 | lr5e-5 | lr1e-4 | lr2e-4/
        ├── metrics.json
        └── config.json
```

## Model names

`<synthetic folder>__<condition>`, for example
`GPT-generated-data-llama-filtering-full__4_original_content_explanation`.

- Synthetic folder = which model **generated** the synthetic biographies and which model
  **filtered** them: GPT-generated / Llama-generated, GPT-filtering / llama-filtering.
- Conditions (training data):
  - `0_base_model`: no fine-tuning (added as extra reference)
  - `1_original`: original training data only (12,000 bios)
  - `2_original_all`: original + all synthetic bios (15,008)
  - `3_original_content_only`: original + bios kept by the content-only filter (13,008)
  - `4_original_content_explanation`: original + bios kept by the explanation-aware filter (13,008)
  - `5_original_random`: original + 13,008 randomly chosen synthetic bios
(Models whose training data were identical were trained only once, due to budget limitations.
results are reused 14 models are therfore mapped on 6 contitions x 4 test sets = 24 )

## Files

**summary_seed42_lr2e-4.csv**: one row per synthetic folder and condition.
`accuracy`, `macro_f1`, `tpr_gap_rms`, `tpr_gap_mean_abs`, `unparsed` as in metrics.json
below; `shared_by` = number of folders that use the same model.

**metrics.json** (per model)
- `n`: number of test biographies (3,998)
- `accuracy`: share of biographies with the correct profession
- `macro_f1`: macro-F1 as computed by gender_evaluation.py (Li et al.);
  `macro_f1_labels`: macro-F1 over the 28 professions only
- `unparsed`: answers in which no profession could be found (counted as wrong)
- `tpr_per_group`: per profession and gender, the true positive rate (share recognised
  correctly) and the number of biographies `n`, e.g. `nurse_female`
- `tpr_gap_female_minus_male`: per profession, TPR women − TPR men
  (positive = women recognised better, negative = men recognised better)
- `tpr_gap_rms`: gender-bias measure, root mean square of those gaps over the professions
  (0 = no gap; larger = more bias). `tpr_gap_mean_abs`: mean absolute gap.

**config.json** (per model): training data file, test file, base model, seed, learning
rate, all training settings (`train`), the list of professions (`labels`) and the Slurm job id.

**predictions.jsonl** (per model): one line per test biography:
`hard_text` (the biography), `true` (correct profession), `gender`, `output` (the model's
raw answer) and `pred` (the profession read from that answer; empty if none was found).

**lr_sweep/.../metrics.json**: the same scores on the dev set, used to choose the learning
rate (2e-4, highest macro-F1).
