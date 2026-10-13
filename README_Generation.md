# Synthetic Data Generation Pipeline

This pipeline generates the synthetic biographies for our experiment. It sends prompts to two LLMs through their APIs (Llama 3.1-8B via DeepInfra, GPT-4o-mini via OpenAI), checks every generated bio, and produces a pool of synthetic bios with:

- an occupation label and a gender label, in the same format as Bias in Bios;
- the generator's **explanation** of its choices, used later by the explanation-aware filter.

Everything is run from a terminal in this folder, one step at a time. Each step reads a config file, writes its results to `data/runs/<run_name>/`, and can be rerun safely.

## How it works

```
Bias in Bios ──sample_bias_in_bios.py──► O (12k train bios), dev, test
                                           │
                        gen.prepare_refs   │  real bios used as examples in the prompts
                                           ▼
                        gen.plan           write every prompt to plan.jsonl (one line per API call)
                                           ▼
                        gen.generate       send the prompts to Llama / GPT-4o-mini, save raw answers
                                           ▼
                        gen.validate       parse and check every bio
                                           │
                        gen.plan --topup   if some profession × gender cells are short,
                        gen.generate       add calls for them and generate again
                                           ▼
                        gen.select_pool    keep exactly the target number per cell
                                           ▼
                             pool.jsonl            full records incl. explanations (for the filters)
                             pool_training.jsonl   bio + labels only (for downstream training)
```

Each API call asks the model for **one bio plus a 2–3 sentence explanation**, returned as JSON. The prompt shows three real bios of the same profession from our training sample O as examples. It tells the model to write in the same style without naming the job title, which matches Bias in Bios' `hard_text`, where the first sentence (which usually names the job) is removed.

### Design decisions already made

- **8 professions:** surgeon, physician, nurse, software engineer, architect, attorney, psychologist, teacher. This mixes male- and female-dominated jobs, and each has enough minority-gender bios in the official test split.
- **Splits** (made by `sample_bias_in_bios.py`, see `README_Sampling.md`):
  - **O (train):** 1,500 bios per profession, keeping each profession's natural gender ratio.
  - **dev:** 100 men + 100 women per profession.
  - **test:** 250 men + 250 women per profession.
- **Synthetic pool:** about 30k bios, 1,876 per profession per generator. Within each profession, the male/female split follows O's ratio (e.g. surgeon 1,598 M / 278 F). The synthetic data therefore never changes gender representation; only the content of the bios differs.
- **Two generators,** each producing half the pool, so we can compare the models and control for a filter preferring its own model's text.

### Prompt types

The configs support three prompt types from the reference paper (Li et al.):

| Type | Prompt | Who chooses the gender |
|---|---|---|
| 1 | "Write a 100 words biography of a *female* nurse." | the prompt |
| 0 | "Write a 100 words biography of a nurse." | the model |
| 4 | "*A man and a woman* are nurses in the same hospital. Write a 100 words biography of the outstanding one." | the model |

With types 0 and 4 the model picks the gender, so the pipeline over-generates and then subsamples to hit the target ratio.

## Setup (once)

You need Python 3.10 or newer. Run these in Git Bash from the project folder:

```bash
python -m venv .venv
source .venv/Scripts/activate        # PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest                     # should end with "24 passed"
```

The tests run the whole pipeline on a fake model, so they need no API keys and cost nothing.

### API keys

Generation needs an API key with credit for each provider:

- **OpenAI** (GPT-4o-mini): platform.openai.com → Billing (prepaid credit; a ChatGPT subscription does not cover the API) → API keys. Set a monthly budget limit.
- **DeepInfra** (Llama): deepinfra.com → Billing → API keys.

The code reads the keys from environment variables. Set them in each new terminal:

```bash
export OPENAI_API_KEY="sk-..."           # Git Bash
export DEEPINFRA_API_KEY="..."
```
```powershell
$env:OPENAI_API_KEY = "sk-..."           # PowerShell
$env:DEEPINFRA_API_KEY = "..."
```

**Never put keys in a config file, in the code, or in a chat.** If a key leaks, revoke it in the provider's dashboard and create a new one.

## Running it

### 1. Make the data sample (once)

```bash
python sample_bias_in_bios.py
```

This downloads Bias in Bios and writes `bias_in_bios_sample/`: train/dev/test CSVs and `O_train_ids.txt`, the row ids of O.

### 2. Reference bios

These are the real bios that appear as examples in the prompts.

```bash
# pilot: 300 random official-train bios per profession
python -m gen.prepare_refs --config configs/pilot.yaml --n-per-profession 300
# full run: exactly the bios in O
python -m gen.prepare_refs --config configs/full.yaml --ids-file bias_in_bios_sample/O_train_ids.txt
```

### 3. Plan, generate, validate

```bash
C=configs/pilot.yaml
python -m gen.plan     --config $C
python -m gen.generate --config $C --generator llama --limit 5      # smoke test: 5 calls
python -m gen.generate --config $C --generator llama
python -m gen.generate --config $C --generator gpt4omini
python -m gen.validate --config $C
```

`validate` prints how many bios failed each check and lists any profession × gender cells that are below target. If cells are short, top up and repeat:

```bash
python -m gen.plan     --config $C --topup
python -m gen.generate --config $C --generator llama
python -m gen.generate --config $C --generator gpt4omini
python -m gen.validate --config $C
```

### 4. Build the pool and review

```bash
python -m gen.select_pool    --config $C
python -m gen.inspect_sample --config $C --n 20          # writes review_sample.md
python -m gen.inspect_sample --config $C --n 20 --failed # look at rejected bios
```

`review_sample.md` shows each bio with its explanation and a checkbox: *"Adds information beyond the bio? yes / partly / no"*. This is what the team fills in when judging whether explanations are useful.

### Full run

The same steps with `configs/full.yaml`, once the open decisions below are settled (the prompt type is set in the config):

```bash
C=configs/full.yaml
python -m gen.prepare_refs --config $C --ids-file bias_in_bios_sample/O_train_ids.txt
python -m gen.plan     --config $C
python -m gen.generate --config $C --generator llama --limit 5        # smoke test first
python -m gen.generate --config $C --generator gpt4omini --limit 5
python -m gen.generate --config $C --generator llama                  # about 1.5-3 hours
python -m gen.generate --config $C --generator gpt4omini              # about 1 hour
python -m gen.validate --config $C
python -m gen.plan     --config $C --topup                            # repeat these four lines
python -m gen.generate --config $C --generator llama                  # until validate reports
python -m gen.generate --config $C --generator gpt4omini              # "All cells reached
python -m gen.validate --config $C                                    #  their target."
python -m gen.select_pool --config $C
```

The two `generate` commands can run at the same time in two terminals (each needs the keys set).

## Configs

| File | Purpose |
|---|---|
| `configs/mock.yaml` | Fake model, no keys needed. For trying out the pipeline. Make fake refs with `python -m gen.prepare_refs --config configs/mock.yaml --source fake --n-per-profession 40` |
| `configs/pilot.yaml` | Pilot, type 1, 3 professions, 40 bios per profession per generator, 50/50 gender |
| `configs/pilot_contrastive.yaml` | The same pilot with type 4 |
| `configs/full.yaml` | Full run: 8 professions, 1,876 per profession per generator, O's gender ratio |

The settings you are most likely to change:

- **`prompt`:** the prompt type, template file, and length range in words.
- **`counts.per_profession`:** bios to keep per profession per generator.
- **`counts.gender_ratio`:** `balanced` (50/50) or `refs` (same ratio as the reference bios, i.e. O).
- **`counts.overgen`:** how many extra calls to make up front (1.2 = 20% extra; use about 1.6 for types 0/4).
- **`validate`:** limits for the checks.
- **`generators`:** model, provider URL, concurrency, and `send_seed` / `json_mode`. Set these to `false` if a provider rejects them.

Prompt templates are in `prompts/`. If you change a template, save it as a new version (`_v2`) and use a new `run_name`. `gen.plan` refuses to change prompts in an existing run, so results stay traceable.

## Output files (`data/runs/<run_name>/`)

| File | Contents |
|---|---|
| `plan.jsonl` | Every planned call: id, profession, target gender, example bio ids, seed, and the full prompt text |
| `raw_<generator>.jsonl` | The model's raw answers, token usage, and timestamps |
| `errors_<generator>.jsonl` | Calls that failed after all retries; they are retried on the next `generate` run |
| `validated.jsonl` | Every record with parsed bio and explanation, detected gender, results of each check, and `passed` |
| `validation_report.json` | Failures per check, counts per cell, the genders the models chose, and repeated openings |
| `pool.jsonl` | The final pool with full records, **including explanations** (input for the filters) |
| `pool_training.jsonl` | `id, hard_text, profession, gender` only, with the same integer labels as Bias in Bios (gender 0 = male, 1 = female). **No explanations.** Can be appended to O directly |
| `review_sample.md` | Sample for manual review |
| `manifest.json` | What was run: config, model, prompt and data checksums, package versions |

`data/` is not committed to git (it's in `.gitignore`), so share runs with the team some other way, e.g. a shared drive.

### The checks in `validate`

A bio passes only if all of these hold:

| Check | Meaning |
|---|---|
| `json_ok` | The answer could be parsed into a bio and an explanation |
| `not_truncated` | The model didn't stop because it ran out of tokens |
| `bio_nonempty` | The bio is not empty |
| `explanation_ok` | The explanation is at least 8 words |
| `no_title` | The bio doesn't contain the job title (e.g. "surgeon", "lawyer") |
| `length_ok` | The bio is 50–180 words |
| `gender_ok` | The pronouns (he/she) match the intended gender; for types 0/4 they must clearly be one gender |
| `not_duplicate` | The bio doesn't copy text from the example bios or from other bios in the pool |

Failed bios are never deleted. They stay in `validated.jsonl`, marked with the checks they failed.

## Good to know

- **Interrupting is safe.** Every answer is saved the moment it arrives. Rerunning `generate` skips calls that are already done.
- **Rate limits and server errors** are retried automatically with increasing waits. Calls that still fail go to the errors file and are retried on the next run.
- **Everything is seeded.** The same config gives the same prompts and example bios. The model outputs themselves vary slightly between runs.
- **Cost:** a call is about 430 input and 190 output tokens. The whole pilot (both prompt types, both models, 672 calls) cost $0.065. Check spending any time with `python -m llm_api.usage "data/runs/*/raw_*.jsonl"`. The full run (about 18k calls per model) costs roughly $0.35 for Llama and $3.20 for GPT-4o-mini, with prompt type 1. Types 0/4 need several times more calls (see below).
- **Speed:** with the default concurrency, Llama does about 2 calls per second and GPT-4o-mini about 6.
- **Llama variant:** DeepInfra only serves the 8-bit quantized "Turbo" version of Llama 3.1-8B, so the configs name it explicitly.

## Pilot results (2026-10-09)

Professions: surgeon, nurse, software engineer, with both models and both prompt types 1 and 4.

- The pipeline ran without API errors. 270 of 288 (type 1) and 370 of 384 (type 4) bios passed. Almost all rejections were the job-title check catching organisation names like "American College of Surgeons".
- **Explanations:** with type 4, 82–88% of explanations justify the gender choice ("I chose the woman as the outstanding one because…"), which is information not in the bio. With type 1, explanations mostly restate the bio, and GPT-4o-mini never mentions gender.
- **Type 4 choices are counter-stereotypical:** Llama picks the woman about 80% of the time for all three professions; GPT-4o-mini picks female surgeons and software engineers but male nurses. Matching O's ratio (about 85% male surgeons) therefore needs several times more calls for male-dominated jobs.
- Generated bios average about 93 words; real Bias in Bios bios have a median of 55.

## Open decisions (before the full run)

1. **Prompt type:** type 4 gives explanations with real content but needs more over-generation (estimated $10–15 in total instead of about $5).
2. **Bio length:** ask for shorter bios to match the real data?
3. **Llama variant:** accept the FP8 Turbo model and report it, or switch to a provider serving full precision.
4. **Job-title check:** relax it for organisation names?

## Where to find the pilot results

On the machine that ran the pilot, in `data/runs/`:

| Folder | Run |
|---|---|
| `data/runs/pilot_t1/` | type 1 (gender given), 288 calls |
| `data/runs/pilot_t4/` | type 4 (contrastive), 384 calls |

In each folder, start with:
- `review_sample.md`: 20 random passed bios with explanations and the review checkboxes;
- `validation_report.json`: failure counts, genders the models chose, and token usage;
- `validated.jsonl`: every bio with its explanation and check results.

To make a new review sheet, e.g. 20 Llama surgeon bios: `python -m gen.inspect_sample --config configs/pilot_contrastive.yaml --n 20 --generator llama --profession surgeon`.

## Not built: OpenAI Batch API

The Batch API would halve GPT-4o-mini's price, but results take hours to a day and the saving is only a few dollars, so we run all calls live.
