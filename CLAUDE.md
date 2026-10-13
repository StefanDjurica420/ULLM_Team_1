# ULLM project — synthetic data generation process

Team project (4 students, mentor-supervised, ~4–5 weeks). **I (Stefan) am in charge of generating
the synthetic data.** The generation code should also be reusable for the LLM filtering step.

Status tags: **[DECIDED]** agreed or required · **[PROPOSED]** suggested, not yet agreed ·
**[OPEN]** still to decide. Keep PROPOSED/OPEN items configurable and flag code that depends on them.

**Current status (2026-10-09):** professions and splits decided; `sample_bias_in_bios.py` produces
O and `bias_in_bios_sample/O_train_ids.txt`. Generation pipeline built (build-order steps 1, 2, 4
done; `pytest` passes, 24 tests on the mock backend and a fake OpenAI server). Refs prepared from
the real dataset (`data/refs_pilot.jsonl`, `data/refs_O.jsonl`) and the pilot plan rendered.
**[DECIDED 2026-10-09] Batch API dropped:** `gen/batch_openai.py` will not be built; GPT-4o-mini
runs live in the full run too (Batch would save only a few dollars and take hours to days).

**Pilot run 2026-10-09** (surgeon / nurse / software_engineer, both generators, 0 API errors, total
cost < $0.10; outputs in `data/runs/pilot_t1`, `data/runs/pilot_t4`, with `review_sample.md` in each
for the team review):
- Tokens per call ≈ 410–450 in, 175–210 out (lower than the 650/230 assumed in §6).
- Type 1: 270/288 passed. Type 4: 370/384 passed. Almost all failures are `no_title`, mostly
  organisation names ("American College of Surgeons", "nurse practitioner") → consider relaxing.
- **Type 4 gender choice is counter-stereotypical:** Llama picks the woman ~80% for all three
  professions; GPT-4o-mini picks female surgeons / software engineers (~85%) but male nurses
  (72%). Small word-order effect (Llama 85% F when the man is named first vs 77%), balanced by
  the randomised order. Consequence: with O's natural ratio (85% male surgeons) types 0/4 would
  need roughly 4–6× more calls for male-dominated jobs and discard most bios.
- **Explanations:** type 4 explanations justify the gender choice ("I chose the woman as the
  outstanding one because…") in 82–88% of bios; type 1 GPT-4o-mini explanations never mention
  gender (0/136), Llama in 31%. Otherwise they mostly restate the bio's content.
- Bios average 91–96 words vs real median 55 (see length note above).

**For the pilot review — length mismatch:** real `hard_text` is short (median 55 words, p5 26,
p95 ~110), but the prompt asks for 100 words (70–130, following Paper 1) and validate rejects
< 50. Synthetic bios will be about twice as long as real ones, which a classifier could pick up
on. Decide with the team whether to lower the target length. Build it step by step, testing each step
with a mock backend before touching paid APIs.

---

## 1. The project in one paragraph

Research question: does giving an LLM filter access to the generator's *explanations* help it pick
synthetic training examples that reduce downstream gender bias (without hurting task performance),
compared with a filter that sees only the content? Both filters keep the same number K of examples.

## 1a. The two reference papers

**Paper 1 — the one this project builds on:** Li et al., *Understanding and Mitigating Bias
Inheritance in LLM-based Data Augmentation on Downstream Tasks* (arXiv 2502.04419v3, May 2026;
code: github.com/MiaomiaoLi2/bias-inheritance). Gender-bias setup relevant to us:
- Generator **and** downstream model: **Llama-3.1-8B-Instruct** (main); **GPT-4o-mini** for the
  large-scale generalisation experiment; Qwen3 / DeepSeek-R1-Distill only in an appendix.
  The model is fine-tuned on data it generated itself.
- 6 professions: architect, dentist, nurse, painter, professor, software engineer, with workplaces
  {architecture firm, dental clinic, hospital, studio, university, tech company}.
- Real data: 600 Bias in Bios bios per profession, 300 M / 300 F → 3,600 total. Synthetic data
  replaces part of it at bias ratio γ = |D_a| / |D| ∈ {0, 5, 10, 20, 50}%.
- Test: 300 per profession, gender-balanced (1,800). Metric: accuracy computed separately for male
  and female bios.
- Downstream training: LoRA on Llama-3.1-8B-Instruct, lr 1e-5, 3 epochs. Classification is a
  prompt: "What is the profession of the person in the following text?" + bio → profession.
- GPT-4o-mini experiment: 7 professions, 6,400 per gender per profession (89,600), 50% replaced;
  evaluated on hiring/salary recommendation, not classification.
- **7 generation prompt types** (all "Write a 100 words biography …"):
  0 Neutral — "of a [profession]" (no gender cue; generator picks)
  1 Contextual Single Explicit — "of a [gender] [profession]"
  2 Contextual Intersectional Explicit — adds [age] and "influenced by [culture] culture"
  3 Contextual Implicit — "about a person whose name is [name]" (gendered names)
  4 Contrastive Single Explicit — "A [gender] and a [gender] are [profession]s in the same
    [workplace]. Write a 100 words biography of the outstanding one."
  5 Contrastive Intersectional Explicit — same with age + culture
  6 Contrastive Implicit — "[name] and [name] are [profession]s in the same [workplace]. …"
- Findings we rely on: contrastive explicit and contextual implicit bias have the most severe
  effects; with the Neutral prompt, Llama writes **more female bios for most professions** (even
  professor, software engineer), architect being the exception; GPT-4o-mini's alignment makes it
  react differently (more bias-sensitive) than Llama.

**Paper 2 — likely source of the explanation idea:** Kaneko, Bollegala & Baldwin, *A Multilingual
Social Bias Benchmark Incorporating Thinking Processes* (MBTP, ACL 2026; github.com/kanekomasahiro/MBTP).
Bias evaluation that considers the model's thinking process (TPAE) beats evaluating only the final
answer (SAE). Relevant points:
- Supports our premise that a rationale carries bias-relevant information beyond the output text.
- **Human-crafted thinking beat LLM-generated thinking** → generator explanations may be weaker
  than hoped; the pilot check on explanation informativeness is essential.
- Notes that LLMs assign higher likelihood to text resembling their own outputs → supports
  controlling filter self-preference (§7).
- Used `gpt-4o-mini-2024-07-18` (lowest bias scores of the models tested), Llama-3-70B-Instruct, OLMo 2.

## 2. Pipeline overview

```
Bias in Bios ──sample──► O (train) / dev / test
      │
      └─ O used as reference bios
                │
   [Llama 3.1-8B API] + [GPT-4o-mini API]   ← generation, ~30k records total
                │
            validate ──► synthetic pool (JSONL)
                │
   random K │ content-only filter │ explanation-aware filter   (each filter run with both LLMs)
                │
   teammates: train classifiers on O + subset ──► macro-F1, TPR gaps on test
```

## 3. Original data: Bias in Bios

- Hugging Face `LabHC/bias_in_bios`; official splits train ~257k, dev ~40k, test ~99k.
- Columns: `hard_text` (bio with the first sentence removed, since that sentence usually names the
  job), `profession` (int, 28 classes), `gender` (int, binary).
- The HF features are plain `int64`, **not ClassLabel**, so names can't be read from the dataset.
  Mapping (from the dataset card, used in `sample_bias_in_bios.py`): professions in alphabetical
  order 0 accountant … 28; `gender` 0 = male, 1 = female (checked: nurse is 91% `1`).
- **[DECIDED] 8 professions** (female share in the official data, identical across splits):
  surgeon 14.8% · software_engineer 15.8% · architect 23.7% · attorney 38.3% · physician 49.4% ·
  teacher 60.2% · psychologist 62.1% · nurse 90.8%. Chosen over the earlier candidates paralegal
  and dietitian, which have only 67 / 71 male bios in the official test split. The smallest
  minority group is female software engineers (273 in official test, 110 in official dev).
- **[DECIDED] Splits**, made by `sample_bias_in_bios.py` (seeds 42/43/44), each from its own
  official split:
  - **O (train): 1,500 per profession = 12,000**, natural gender ratio per profession.
    Row ids in `bias_in_bios_sample/O_train_ids.txt`. Identical in every training condition.
  - **dev: 100 M + 100 F per profession = 1,600**; **test: 250 M + 250 F per profession = 4,000**.
    (The earlier 2k/6k proposal can't be gender-balanced: too few female software engineers.)
- Synthetic data is never put in dev or test.

## 4. Generation

### Models — [DECIDED]
Both used through hosted APIs, matching the reference paper. The teacher requires multiple LLMs
for both generation and filtering, and these two cover both roles.

| Model | Access | Pin |
|---|---|---|
| Llama 3.1-8B-Instruct | **DeepInfra** [PROPOSED provider], OpenAI-compatible endpoint `https://api.deepinfra.com/v1/openai` | model `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo`: as of 2026-10-09 DeepInfra only serves this **FP8-quantized** variant (requests for the non-Turbo id are silently redirected to it). **[OPEN]** accept and report it as a deviation from Paper 1, or switch to a provider serving BF16 before the full run. Use ONE provider for every Llama call, generation and filtering |
| GPT-4o-mini | OpenAI API, live calls (Batch API dropped) | snapshot `gpt-4o-mini-2024-07-18` |

API keys come from env vars `DEEPINFRA_API_KEY` and `OPENAI_API_KEY`. Switching the Llama provider
only means changing `base_url`, `model`, `provider`, and `api_key_env` in the config.

Note: GPT-4o-mini is not the same as `o4-mini` (a different model, retired from the API on
2026-10-23). As of 2026-10-09 GPT-4o-mini has no announced shutdown date.

### Pool size — [DECIDED: ~30k total, natural gender ratio]
- **1,876 per profession per generator** (equal across professions, like O) → 2 × 8 × 1,876 =
  30,016 records. Within each profession the M/F split **follows O's gender ratio** (largest
  remainder), so synthetic data never changes gender representation; only content differs.
  Per generator (computed by `cell_targets` from `data/refs_O.jsonl`): surgeon 1,598 M / 278 F ·
  physician 949 / 927 · nurse 171 / 1,705 · software_engineer 1,580 / 296 · architect 1,432 / 444 ·
  attorney 1,158 / 718 · psychologist 712 / 1,164 · teacher 747 / 1,129.
- Over-generate ~15–20% per (generator, profession, gender) cell, validate, then randomly take
  exactly the target number per cell from records that pass. ≈ 36k calls total.
- Every record stores which generator produced it.

### Gender and prompt type — [OPEN]
Options, mapped to Paper 1's prompt types:
- **Type 1 (gender given):** controls counts, but the explanation can't explain a gender choice.
- **Type 0 Neutral (generator picks gender):** the explanation covers a real choice; counts are not
  controlled (Paper 1: Llama skews female for most professions), so over-generate per profession
  and check the per-cell supply.
- **Type 4 Contrastive Single Explicit (generator picks "the outstanding one"):** a real gendered
  choice, among the most damaging bias types in Paper 1 → most for the filters to catch, and the
  explanation has something substantive to justify.
- A mix of types, recording `prompt_type` per record.
Whichever is used, the pool must hit the natural-ratio target in every occupation × gender cell.
With types 0/4 that means over-generating and subsampling; minority cells (e.g. male nurse) may
need several `--topup` rounds. Log each generator's raw gender rates before subsampling (a finding
in itself). Decide after the pilot.

### Prompt
Start from the paper's prompt and add only what the design needs: the explanation, no job title
in the bio (to match `hard_text`), JSON output, and reference bios from O. Do **not** tell the
generator to avoid stereotypes, since that would remove what the filters are meant to catch.

Store templates as files in `prompts/` (Python `string.Template`, `$var` placeholders, so the
literal JSON braces need no escaping). Changing a template → bump its version (`_v2`).

`prompts/gen_type1_v1.txt` (gender given, Paper 1 type 1):
```text
Below are example biographies of people working as a $profession.
They are written in the third person and do not state the job title directly.

$refs

Write a 100 words biography of a $gender $profession.
- Write ONE new, realistic biography in the third person, using $pronouns pronouns, $min_words-$max_words words.
- Do not mention the job title "$profession" or obvious variants of it; the occupation should be clear from the content.
- Do not copy names, employers, or sentences from the examples.

Then explain your choices in 2-3 sentences: which details you included to make the occupation clear, and how you chose the person's background, attributes, and career path.

Return JSON only, in exactly this form: {"bio": "...", "explanation": "..."}
```

`prompts/gen_type0_v1.txt` (neutral, model picks gender, Paper 1 type 0): same as type 1 except
the task line is `Write a 100 words biography of a $profession.`, the first rule says
`... $min_words-$max_words words. Refer to the person with gendered pronouns (he or she).`, and the
explanation asks how the person's **gender**, background, attributes, and career path were chosen.

`prompts/gen_type4_v1.txt` (contrastive, Paper 1 type 4): same structure, task line
`$pair are $profession_plural in the same $workplace. Write a 100 words biography of the outstanding one.`,
first rule `... $min_words-$max_words words, about only the person you chose, using their gendered
pronouns (he or she).`, and the explanation asks **whom you chose as the outstanding one and why**,
plus the usual content choices. `$pair` is "A man and a woman" or "A woman and a man", randomised per
record (seeded) and stored as `contrastive_order`, so word order can't drive the choice.

Placeholders: `$refs` = "Example 1: <bio>\n\nExample 2: ...", `$profession` (display text, e.g.
"software engineer"), `$a_profession` ("an architect"; the templates use it wherever the spec
above says "a $profession", which would give "a architect"), `$profession_plural`, `$workplace`, `$gender` ("male"/"female"),
`$pronouns` ("he/him/his" / "she/her/hers"), `$pair`, `$min_words` (70), `$max_words` (130).

- Reference bios: drawn at random per call (seeded by record id), same profession, **only from O**
  in the final run; any official-train bios for the pilot.
- Sampling: temperature 0.9, top_p 0.95, max_tokens 500; `response_format={"type":"json_object"}`.

### Record schema (JSONL)
```json
{"id": "full_v1_llama_nurse_female_00417", "generator": "llama", "provider": "deepinfra",
 "model_id": "meta-llama/Meta-Llama-3.1-8B-Instruct", "profession": "nurse",
 "target_gender": "female", "gender": "female", "prompt_type": 1, "contrastive_order": null,
 "bio": "...", "explanation": "...", "ref_ids": [101, 2045, 377], "seed": 1944992947,
 "prompt_version": "v1", "temperature": 0.9, "top_p": 0.95}
```
`target_gender` is what the prompt asked for (null for types 0/4); `gender` is what the bio's
pronouns show, and it is the label used for matching and evaluation.
For training, `pool_training.jsonl` already has `hard_text` and Bias in Bios ints for
profession and gender (0 = male, 1 = female), so it can be concatenated with O directly.
Explanations are never training inputs. Gender stays in the files for matching and evaluation.

### Validation (log failure counts per check; report them)
- valid JSON; `bio` and `explanation` non-empty
- job title and obvious variants absent from the bio (`title_terms` per profession in
  `gen/common.py`). Note: real `hard_text` sometimes names the job later in the bio (only the first
  sentence is removed), so this check is stricter than the data; the team may relax it.
- pronouns match the gender label (detected gender needs a 3:1 majority of he/him/his vs
  she/her/hers, so "his wife … she" still counts as male; otherwise unclear → fail)
- length roughly within the `hard_text` length distribution
- no near-copies of reference bios or other pool bios (n-gram overlap)
- repeated openings ("With a passion for…"): flag if one opening covers more than a few % of bios

### Pilot (before the full run)
~30–50 bios per profession for 2–3 professions (e.g. surgeon / nurse), per generator, using
standard (non-batch) calls. Read them and check:
1. Do the bios look like real `hard_text`?
2. **Do the explanations add information not already visible in the bio?** If they mostly restate
   it, the main comparison will likely be null; revise the explanation instruction (e.g. ask what
   alternatives were considered and why they were rejected).
3. Real token usage per call, to update the cost estimate.

## 5. Code to build (spec)

Python ≥3.10, deps in `requirements.txt` (`openai`, `pyyaml`, `datasets`, `pandas`, `numpy`,
`pytest`); the `gen/` code itself uses only `openai`, `pyyaml`, `datasets` and the standard library. A package `gen/` with one module per
step, each runnable as `python -m gen.<step> --config <yaml>`. All outputs go to
`data/runs/<run_name>/` (gitignore `data/`, `.env`). Never delete records: failed ones stay in the
files, marked with which checks failed.

### Layout
```
configs/pilot.yaml               pilot, prompt type 1, 3 professions, 40 per profession split 50/50
configs/pilot_contrastive.yaml   same pilot with prompt type 4
configs/full.yaml                full run: 8 professions, 1,876 per profession at O's gender ratio, both generators live
configs/mock.yaml                both generators on the mock backend, for testing without keys
prompts/gen_type{0,1,4}_v1.txt   generation prompts (§4)
gen/common.py      config loading, JSONL read/append (tolerate a half-written last line), stable
                   seeds via sha256 (not Python hash()), PROFESSIONS table, pronoun detection
gen/prepare_refs.py  reference bios
gen/plan.py        render all prompts up front -> plan.jsonl; --topup
gen/generate.py    live calls via llm_api (+ mock backend)
llm_api/           shared API layer for generation AND filtering: ModelConfig/MODELS presets, LLMClient
                   (retries), MockClient, run_requests/run_prompts (concurrent, resumable JSONL),
                   parse_json(_fields), jsonl helpers, usage.py cost report. Documented in llm_api/README.md
gen/validate.py    parse + checks
gen/select_pool.py final pool
gen/inspect_sample.py  readable sample for the pilot review
gen/manifest.py    provenance
```

### Config (YAML) — example `configs/pilot.yaml`
```yaml
run_name: pilot_t1
seed: 42
output_dir: data/runs/pilot_t1
refs_file: data/refs_pilot.jsonl
professions: [surgeon, nurse, software_engineer]
genders: [male, female]
prompt: {type: 1, template: prompts/gen_type1_v1.txt, version: v1, n_refs: 3, min_words: 70, max_words: 130}
counts: {per_profession: 40, gender_ratio: balanced, overgen: 1.2}   # full.yaml: gender_ratio: refs
  # kept per (generator, profession); split M/F by the refs file's gender ratio (or `balanced`
  # for 50/50); per-cell target = largest-remainder share; calls = target*overgen
sampling: {temperature: 0.9, top_p: 0.95, max_tokens: 500}
generators:
  llama:
    backend: openai_compat              # openai_compat | openai_batch | mock
    provider: deepinfra
    base_url: https://api.deepinfra.com/v1/openai
    api_key_env: DEEPINFRA_API_KEY
    model: meta-llama/Meta-Llama-3.1-8B-Instruct
    concurrency: 16
    retries: 5
    send_seed: true                     # set false if the provider rejects `seed`
    json_mode: true                     # response_format json_object
  gpt4omini:
    backend: openai_compat
    provider: openai
    base_url: https://api.openai.com/v1
    api_key_env: OPENAI_API_KEY
    model: gpt-4o-mini-2024-07-18
    concurrency: 16
    retries: 5
    send_seed: true
    json_mode: true
validate:
  min_words: 50
  max_words: 180
  min_explanation_words: 8
  shingle_n: 8                 # word n-grams for near-duplicate detection
  max_shingle_overlap: 0.3     # fail if >30% of a bio's 8-grams already occur in refs or accepted bios
  opening_share_warn: 0.05     # warn if one 4-word opening covers >5% of a generator's bios
```
`full.yaml`: run_name `full_v1`, `refs_file: data/refs_O.jsonl`, all 8 professions, `per_profession: 1876`,
llama `concurrency: 32`, gpt4omini live (`openai_compat`). Raise `overgen` (~1.6) for prompt
types 0/4, where the model picks the gender and cells come out uneven.

### PROFESSIONS table (`gen/common.py`)
Per profession: display text, `title_terms` (banned whole words, case-insensitive), `workplace`
(for the contrastive prompt). Fail loudly if a config uses a profession missing from the table.
Also the Bias in Bios int id (for converting to training data). The 8 used:
- surgeon: [surgeon(s)], hospital · physician: [physician(s)], medical practice · nurse: [nurse(s)], hospital
- software_engineer: [software engineer(s), software developer(s)], tech company
- architect: [architect(s)], architecture firm · attorney: [attorney(s), lawyer(s)], law firm
- psychologist: [psychologist(s)], counseling practice · teacher: [teacher(s)], school
- Spares if the list changes: paralegal / law firm, dietitian / nutrition clinic, journalist /
  newsroom, professor / university, dentist / dental clinic, painter / studio

### Step specs
**prepare_refs** — `--source official_train --n-per-profession 300` (pilot) or `--ids-file
bias_in_bios_sample/O_train_ids.txt` (full; one official-train row index per line, written by
`sample_bias_in_bios.py`). Load `LabHC/bias_in_bios`; profession/gender names come from the ids in
the PROFESSIONS table (the dataset has no ClassLabel features); stop with a clear error if a
profession id is missing. Print the profession × gender counts and female share for every
official split (helps choose professions). Write `{ref_id, profession, gender, text}` JSONL plus
`<refs>.stats.json` with word-count percentiles of the reference bios.

**plan** — one row per API call: `id` (`{run}_{gen}_{prof}_{gender|any}_{k:05d}`), generator,
profession, `target_gender` (null for types 0/4), prompt_type, contrastive_order, ref_ids, `seed`
(stable hash of config seed + id), prompt_version, and the **fully rendered prompt**. Saving the
prompt makes the run auditable and lets live and batch backends send identical inputs. Refuse to
overwrite an existing plan if any existing id's prompt would change. `--topup`: after validate,
count passed records per (gen, prof, gender); for each short cell append
`ceil(short*overgen/yield)+2` calls (type 1) or `+4` (types 0/4, where calls are per profession and
the largest need over the two genders is used). `yield` = passed / calls made for that cell, i.e.
for types 0/4 it includes how often the model picks that gender, floored at `counts.min_yield`
(0.02); calls per cell capped at `counts.max_topup_calls` (5000). Ids are numbered after the existing
ones. Refuses while planned calls have no response (`--force` overrides) or validate is stale.

**generate** — `--generator NAME [--limit N]`. Async with a semaphore (`concurrency`), OpenAI
SDK `AsyncOpenAI(base_url, api_key, max_retries=0)`, own retry loop with exponential backoff
(rate limits, timeouts, 5xx). Skip ids already in `raw_<gen>.jsonl`; append each response
immediately: `{id, generator, raw, finish_reason, model_returned, usage{prompt_tokens,
completion_tokens}, ts}`. After all retries fail → `errors_<gen>.jsonl` (retried on next run).
Print progress and, at the end, average input/output tokens per call (needed for cost estimates).
`mock` backend: deterministic fake JSON from the record seed, with some deliberately broken
outputs (non-JSON, job title present) so every validation check gets exercised.

**batch_openai** — [DROPPED, not built; spec kept for reference] `submit [--chunk-size 4000] [--limit N]`: write `/v1/chat/completions` request
lines (`custom_id` = record id, same body as live incl. seed and response_format), upload with
`purpose="batch"`, create batches with `completion_window="24h"`; skip ids already done or in a
pending batch; save batch ids + member ids in `batches_<gen>.json`. `status`: print status and
request counts. `collect`: for finished batches, download the output file (and error file) and
append successes to `raw_<gen>.jsonl` in the same format as generate (match by `custom_id`, results
come back out of order), failures to `errors_<gen>.jsonl`; mark batches collected. Re-running
`submit` resends only what is still missing. Low usage tiers cap queued tokens: on a token-limit
failure, use smaller chunks and wait for earlier batches.

**validate** — parse JSON tolerantly (strip code fences, else extract the first `{...}`). Checks:
`json_ok`, `not_truncated` (finish_reason ≠ length), `bio_nonempty`, `explanation_ok` (≥
min_explanation_words), `no_title`, `length_ok`, `gender_ok` (detected pronoun gender == target;
for types 0/4 must be unambiguously male or female, which then becomes the record's gender),
`not_duplicate` (8-gram shingle overlap with all reference bios and previously **accepted** bios,
processed in id order for determinism). Write `validated.jsonl` (record schema from §4 plus
`word_count`, `max_shingle_overlap`, `checks{}`, `passed`) and `validation_report.json` (failures
per check per generator, passed per cell, top 4-word openings with shares). Print failures, warn on
repeated openings, list cells below their target.

**select_pool** — per (generator, profession, gender), shuffle passing records (seeded) and keep
exactly its target (from `per_profession` and `gender_ratio`); exit non-zero listing short cells unless `--allow-shortfall`. Write
`pool.jsonl` (full records, for the filters), `pool_training.jsonl` (`id, hard_text, profession,
gender` only, as dataset ints, **no explanations**), `pool_report.json`.

**inspect_sample** — `--n 20 [--generator] [--profession] [--failed]`: print and save
`review_sample.md` with bio, explanation, labels, failed checks, and a line
"Adds information beyond the bio? [ ] yes [ ] partly [ ] no" for the team review.

**manifest** — at the start of each generate/submit, append to `manifest.json`: time, generator
config (never the key), sampling, prompt config, sha256 of template, refs file and plan, config
path, Python version, platform, package versions.

### Build order (1, 2, 4 done; tests in `tests/`, run `python -m pytest`)
1. common + mock config with a small fake refs file → plan → generate (mock) → validate →
   select_pool → inspect_sample; check resume (kill mid-run, rerun) and `--topup`.
2. Test the live path against a tiny local fake OpenAI-compatible server that returns some 429s
   (`tests/fake_openai_server.py`: every 4th request 429, every 11th 500).
3. [DROPPED] Test batch_openai with a stubbed client (submit in chunks, collect, resubmit failures).
4. prepare_refs against the real dataset (needs internet) — check label names print correctly.
5. Real smoke test: `--limit 5` per generator, then the pilot.

### Commands once built
```bash
pip install -r requirements.txt
export DEEPINFRA_API_KEY=...  OPENAI_API_KEY=...

python -m pytest                                                                     # mock + fake-server tests
python -m gen.prepare_refs --config configs/pilot.yaml --source official_train --n-per-profession 300
python -m gen.plan     --config configs/pilot.yaml
python -m gen.generate --config configs/pilot.yaml --generator llama --limit 5      # smoke test
python -m gen.generate --config configs/pilot.yaml --generator llama
python -m gen.generate --config configs/pilot.yaml --generator gpt4omini
python -m gen.validate --config configs/pilot.yaml
python -m gen.inspect_sample --config configs/pilot.yaml --n 20
# repeat with configs/pilot_contrastive.yaml

# full run (after professions, prompt type and O are settled)
python -m gen.prepare_refs --config configs/full.yaml --ids-file bias_in_bios_sample/O_train_ids.txt
python -m gen.plan     --config configs/full.yaml
python -m gen.generate --config configs/full.yaml --generator llama
python -m gen.generate --config configs/full.yaml --generator gpt4omini
python -m gen.validate    --config configs/full.yaml
python -m gen.plan --config configs/full.yaml --topup   # if cells are short; then generate again
python -m gen.select_pool --config configs/full.yaml
```

## 6. Cost and time (prices checked 2026-10-09 — verify before running)

Token assumptions per generation call: ~650 input (instructions + 3 reference bios), ~230 output.
Replace with the real averages `gen.generate` prints after the pilot.

| Step | Llama 3.1-8B (DeepInfra, $0.02 / $0.05 per M) | GPT-4o-mini (Batch $0.075 / $0.30; live $0.15 / $0.60) |
|---|---|---|
| Pilot (2 configs, ~290 calls each per model) | < $0.05 | < $0.25 (live) |
| Full generation (~18k calls per model) | ~$0.45 | ~$2 batch / ~$4 live |
| Filtering, later (60k calls per model, ~500 in / 60 out) | ~$0.80 | ~$3.30 batch |

**Generation ≈ $3; whole project incl. filtering ≈ $7–10.** Other Llama hosts cost more (e.g.
Together $0.18/$0.18 → ~$3 for generation). Put ~$5 credit on each account and set spend limits.

Time:
- Building and testing the pipeline with Claude Code: a few hours.
- Setup (accounts, keys, `prepare_refs`, smoke test): ~1 hour.
- Pilot: each run takes minutes; reviewing outputs and iterating on the prompt: 1–2 days with the team.
- Full Llama run: ~18k calls at concurrency 32 → roughly 30–90 minutes, depending on rate limits.
- Full GPT-4o-mini batch: results within 24 h (often a few hours); longer if the queue limit
  forces several sequential chunks.
- Validate, top up short cells, select: under an hour.
Blocked on: prompt-type decision after pilot.

## 7. Filtering

On the same 30k pool, each strategy keeps K examples (size **[OPEN]**):
1. **Random.**
2. **Content-only:** LLM sees bio + occupation label.
3. **Explanation-aware:** same LLM, same criteria and prompt, plus the generator's explanation.

Criteria: stereotypical content / unsupported gender generalisations, relevance, consistency with
the label. A male software engineer bio is not biased by itself; representation is inspected
separately.

Both Llama 3.1-8B and GPT-4o-mini act as filters → 2 content-only + 2 explanation-aware subsets.
- **Self-preference:** a filter may favour bios from its own model. Take K/2 from each generator per
  subset and report whether each filter scores its own generator's bios higher.
- Per-record verdict, e.g. `{"id":..., "filter_model":..., "filter":"explanation_aware", "score":4, "keep":true}`;
  scoring scale **[OPEN]**.
- Before the full run, the team hand-labels ~100 bios and measures each filter's agreement.
- **Matched counts [PROPOSED]:** each filter keeps K split over occupation × gender cells in the
  pool's (= O's natural) proportions, so all subsets have identical representation and TPR-gap
  differences come from content. Minority cells get small (male nurse ≈ 58 at K = 10k).
- **Shuffled explanations [OPEN: from the start or if time allows]:** give the filter an
  explanation from another bio of the same occupation with similar length.

## 8. Downstream training and evaluation (teammates)

Conditions: O only · O + full pool · O + random K · O + content-only K (×2 filters) ·
O + explanation-aware K (×2 filters) → **7 conditions × 3 seeds = 21 runs**.
Downstream model **[OPEN]**. Paper 1 fine-tuned Llama-3.1-8B-Instruct with LoRA (lr 1e-5,
3 epochs) and classified by prompting; a small encoder (DistilBERT/RoBERTa) is much cheaper for
21 runs. If deviating from Paper 1, state it explicitly.

Metrics on one held-out test set: macro-F1; per-occupation TPR gap (female TPR − male TPR); a
predefined aggregate of **absolute** gaps; variation across seeds. Dev is for tuning prompts and
selection; test is never used for choices. Main comparison: explanation-aware vs content-only.

## 9. Open decisions
- Downstream model.
- Who sets gender in generation; K; filter scoring scale.
- Confirm matched-by-natural-ratio counts in filtered subsets.
- Shuffled-explanations experiment now or later.
- Which existing filtering method to add as a baseline; novelty vs prior work still to check.

## Working conventions
- Python, config-driven, small testable steps.
- Ask before spending money on paid APIs or launching full runs; pilot first.
