# Bias in Bios — constrained sampling

This script samples all 28 professions from `LabHC/bias_in_bios`, without replacement and independently within the official train, dev and test splits. It preserves each source split's within-profession gender ratios up to integer rounding while targeting 53.9% men overall. No records move between splits.

## Sampling proposal and its limits

The original authors selected the 28 most frequent occupations found in a small Common Crawl subset, merged some occupation titles (such as professor specializations), and collected matching biographies. Their resulting occupation proportions reflect web availability, extraction rules and deduplication; they were not set using population quotas. Calling the distribution purely random would be misleading.

The overall 53.9% male / 46.1% female ratio and within-profession ratios describe this dataset. They are not established estimates of workforce or general-population gender distributions. We retain them as experimental reference distributions, not as evidence of real-world representativeness.

A stepped minimum per profession (2.5% base, plus 2.5% for each complete 5% of original occupation share) is an experimental coverage requirement: it prevents extremely small occupation classes in our reduced dataset. It does not guarantee avoidance of overfitting, nor adequate numbers in every profession × gender subgroup. Overfitting must be assessed on held-out data; synthetic generation should additionally be checked for copying and low diversity.

References:
- https://www.microsoft.com/en-us/research/wp-content/uploads/2019/01/bios_bias.pdf (Section 3)
- https://huggingface.co/datasets/LabHC/bias_in_bios

## Defaults

| Split | Sample size | Base minimum per profession | Men | Women |
| --- | ---: | ---: | ---: | ---: |
| train | 12,000 | 300 | 6,468 | 5,532 |
| dev | 1,600 | 40 | 862 | 738 |
| test | 4,000 | 100 | 2,156 | 1,844 |

Sizes match the supplied old script. Unlike the old script, this version uses all 28 professions and does not balance genders within dev/test professions. The target male count is `floor(size * 0.539 + 0.5)`, so dev is 53.875% male. For each profession the minimum is `ceil(size * 0.025 * (1 + floor(original_share / 0.05)))` in each split. Original shares are calculated from exact source counts, not rounded displayed percentages. To use 12k/2k/6k instead, edit `SIZES`; feasibility will be checked again.

## Allocation method

For each profession i, let `p_i` be the proportion of women in its original source split and `n_i` its allocated sample size. The script solves an integer optimization problem with these constraints:

- All profession totals sum to the requested split size.
- Every profession receives its stepped minimum: 2.5% for source shares below 5%, 5% for shares from 5% to below 10%, 7.5% for shares from 10% to below 15%, etc. A profession at exactly 10% enters the 7.5% minimum band. In the current data these minimum shares sum to 95%; the remaining 5% is allocated by the optimizer.
- Female count `f_i` satisfies `abs(f_i - p_i * n_i) <= 0.5`. Thus the sampled count is a nearest-integer rounding of the original ratio. Exact half-integer ties may round either way to satisfy the global target.
- The total number of men equals the rounded target count.
- Neither gender quota exceeds the number of available source records.

Among feasible allocations it minimizes `sum(abs(n_i - size * original_profession_share_i))`. Thus profession proportions change only as needed under an absolute-deviation objective. Several equally optimal allocations may exist. The code does not pair professions manually and does not force equal profession sizes.

Ratios are computed from the corresponding source split only. The train allocation does not use dev/test statistics. The 53.9% overall target is a fixed design choice. Since quotas are allocated separately, profession proportions can differ across the three output splits; use the exact same saved held-out sets when comparing experimental methods.

If constraints cannot be met, or optimality is not established within the 60-second solver limit, the script raises an error. It never silently drops professions, samples with replacement, or relaxes constraints. All splits are validated before output writing starts.

## Install and run

Save the Python file as `sample_bias_in_bios.py`. Activate your existing virtual environment, then run:

```bash
python -m pip install datasets pandas numpy scipy
python sample_bias_in_bios.py
```

SciPy 1.9 or newer is required for `scipy.optimize.milp`. To create and activate a new environment in Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

In Windows Git Bash use `source .venv/Scripts/activate`; on Linux/macOS use `source .venv/bin/activate`.

Optional use of already-downloaded official Parquet files:

```bash
python sample_bias_in_bios.py --local-data path/to/parquet_folder --output bias_in_bios_sample
```

The folder must contain files named `train*.parquet`, `dev*.parquet`, and `test*.parquet`. Install `pyarrow` if needed for this optional mode. Source row IDs refer to the source rows in load order; use the default Hugging Face loader if downstream code expects that loader's row numbering.

## Configuration

At the top of the script:

```python
SEED = 42
SIZES = {"train": 12_000, "dev": 1_600, "test": 4_000}
MIN_SHARE = 0.025
TARGET_MALE_SHARE = 0.539
```

Reproducibility requires unchanged data, row order, configuration, and dependency/solver versions. The random seed controls record selection, not tie-breaking between equally optimal solver allocations. Archive output IDs and dependency versions for reproducible experiments.

## Outputs

The output directory defaults to `bias_in_bios_sample`. Existing files with the same names are overwritten.

- `train.csv`, `dev.csv`, `test.csv`: original columns plus `source_split`, `source_row` and `profession_name`.
- `train_distribution.csv`, `dev_distribution.csv`, `test_distribution.csv`: original and sampled counts, occupation shares, and within-profession percentages for men and women, including a TOTAL row.
- `O_train_ids.txt`: sorted zero-based source train row IDs, one per line, retained for the generation pipeline.

Gender labels are 0 for men and 1 for women. CSVs use `utf-8-sig`. Sampling preserves official split boundaries and avoids repeated source rows; it does not detect different source rows describing the same person or containing duplicate text across the original splits.

## Validation on the official Parquet files

The revised script was run successfully against all three official LabHC splits (257,478 train; 39,642 dev; 99,069 test). All requested totals, gender targets, profession minima, within-profession rounding constraints, and source-row uniqueness checks passed. Failure checks also confirmed rejection of impossible quotas, and fixed-seed record selection was verified.


The verified allocation under the stepped rule is shown below. Solver versions may select a different equally optimal allocation.

| Profession | Train | Dev | Test |
| --- | ---: | ---: | ---: |
| accountant | 300 | 40 | 100 |
| architect | 300 | 40 | 102 |
| attorney | 600 | 80 | 200 |
| chiropractor | 300 | 40 | 100 |
| comedian | 300 | 40 | 100 |
| composer | 300 | 40 | 100 |
| dentist | 300 | 40 | 147 |
| dietitian | 300 | 40 | 100 |
| dj | 300 | 40 | 100 |
| filmmaker | 300 | 40 | 100 |
| interior_designer | 300 | 40 | 100 |
| journalist | 600 | 80 | 201 |
| model | 300 | 40 | 100 |
| nurse | 549 | 75 | 191 |
| painter | 300 | 40 | 100 |
| paralegal | 300 | 40 | 100 |
| pastor | 300 | 40 | 100 |
| personal_trainer | 300 | 40 | 100 |
| photographer | 601 | 80 | 200 |
| physician | 900 | 152 | 300 |
| poet | 300 | 40 | 100 |
| professor | 2150 | 240 | 604 |
| psychologist | 300 | 40 | 100 |
| rapper | 300 | 40 | 100 |
| software_engineer | 300 | 40 | 100 |
| surgeon | 300 | 53 | 115 |
| teacher | 300 | 40 | 140 |
| yoga_teacher | 300 | 40 | 100 |
| TOTAL | 12000 | 1600 | 4000 |
