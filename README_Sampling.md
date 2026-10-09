# Bias in Bios — Sampling

This script creates smaller samples of the [LabHC/bias_in_bios dataset](https://huggingface.co/datasets/LabHC/bias_in_bios) for 8 professions: surgeon, physician, nurse, software engineer, architect, attorney, psychologist, and teacher.

- **Train (O):** 1,500 bios per profession, keeping each profession's original gender ratio as closely as integer rounding allows.
- **Dev and test:** gender-balanced within each profession (100 and 250 per gender per profession).

Sampling is performed without replacement, independently within the original `train`, `dev`, and `test` splits. The script does not move records between splits.

## Requirements

Install these packages inside your virtual environment:

Open Git Bash or terminal in the project folder and create a local virtual environment:

```bash
python -m venv .venv
```

If `python` is not recognized but the Windows Python launcher is available, use `py -m venv .venv` instead.

Activate it:

```bash
source .venv/Scripts/activate
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install datasets pandas numpy
```

Verify that the active Python belongs to your environment and the packages import successfully:

```bash
python -c "import sys; print(sys.executable)"
python -c "import datasets, pandas, numpy; print('Dependencies installed successfully')"
```

The interpreter path should point inside `.venv`.

For Linux or macOS, create the environment with `python3 -m venv .venv` and activate it with `source .venv/bin/activate`. The installation and run commands below are otherwise the same.

## Run

With the environment active, run from the project folder:

```bash
python sample_bias_in_bios.py
```

The script loads the dataset, samples each split, prints distribution comparisons, and saves the CSV files. Hugging Face manages its download cache separately from the output folder.

When opening a new Git Bash session, reactivate the existing environment before running the script:

```bash
source .venv/Scripts/activate
python sample_bias_in_bios.py
```

You only need to create the environment and install dependencies once per environment. To leave it:

```bash
deactivate
```

## Configuration

Edit the constants at the top of `sample_bias_in_bios.py`:

```python
SEED = 42
# ("natural", n): n bios per profession, keeping that profession's gender ratio.
# ("balanced", n): n bios per gender per profession.
SIZES = {"train": ("natural", 1_500), "dev": ("balanced", 100), "test": ("balanced", 250)}
KEEP = ["surgeon", "physician", "nurse", "software_engineer",
        "architect", "attorney", "psychologist", "teacher"]
OUTPUT = Path("bias_in_bios_sample")
```

| Split | Mode | Per profession | Total |
| --- | --- | ---: | ---: |
| Train | natural gender ratio | 1,500 | 12,000 |
| Dev | gender-balanced | 100 + 100 | 1,600 |
| Test | gender-balanced | 250 + 250 | 4,000 |

The balanced sizes are limited by the rarest group: the official dev and test splits contain only 110 and 273 female software engineers. If a size cannot be met, the script stops and lists the groups that are too small.

A fixed seed makes sampling reproducible for unchanged input data, row order, code, and dependency versions. The script uses seeds 42, 43, and 44 for train, dev, and test respectively with the default configuration.

In natural mode, each profession's gender split uses largest-remainder allocation: the profession total is exact, and each gender's count differs from its ideal proportional count by less than one row.

## Output

Files are written to `bias_in_bios_sample/`, relative to the directory from which you run the script. Running it again overwrites files with the same names.

| File | Contents |
| --- | --- |
| `train.csv` | Sampled training records |
| `dev.csv` | Sampled development records |
| `test.csv` | Sampled test records |
| `train_distribution.csv` | Original and sampled training distributions |
| `dev_distribution.csv` | Original and sampled development distributions |
| `test_distribution.csv` | Original and sampled test distributions |
| `O_train_ids.txt` | `source_row` of every train sample, one per line (input for the generation pipeline) |

Sample files retain the dataset columns (`hard_text`, `profession`, and `gender`) and add:

- `source_split`: the original split name.
- `source_row`: the zero-based row number within that source split.
- `profession_name`: the occupation name mapped from its numerical label.

The dataset uses `gender = 0` for men and `gender = 1` for women. Distribution reports include counts, totals, the percentage of women, and the men-to-women count ratio. CSV files use UTF-8 with a byte order mark (`utf-8-sig`).

## Git ignore rules

Place the accompanying `.gitignore` in the repository root if it's not already there. It excludes common virtual-environment directory names, generated samples, and Python bytecode. If your environment has a different name, add that directory too!

To create or append the rules using Git Bash:

```bash
cat >> .gitignore <<'IGNORE'
# Python virtual environments
.venv/
venv/
.env/
env/
ENV/

# Generated dataset samples
bias_in_bios_sample/

# Python bytecode
__pycache__/
*.py[cod]
IGNORE
```

Use this command once; `>>` preserves existing rules. `.gitignore` does not untrack files already committed. If necessary, remove only the affected tracked directories from Git's index, for example:

```bash
git rm -r --cached -- .venv bias_in_bios_sample
```

List only directories that Git currently tracks. `--cached` keeps the local files. Then stage the ignore file with `git add .gitignore` and commit your changes normally.

## References

- [Dataset and label mapping](https://huggingface.co/datasets/LabHC/bias_in_bios)
