# llm_api: calling Llama and GPT-4o-mini

The generation pipeline (`gen/`) and the filtering step both send many prompts to the same two models and need JSON answers back. This package holds the part they share, so filtering can reuse code that already ran the pilot (672 calls, no failures) instead of writing its own API code.

It contains:
- the model settings for the two models;
- an API client that retries on errors;
- a runner that sends many prompts in parallel and can resume after an interruption;
- tolerant JSON parsing of replies;
- a report of tokens used and their cost.

It knows nothing about bios or filters. You write the prompts; it sends them and saves the answers.

| Module | What it gives you |
|---|---|
| `client.py` | `MODELS` / `get_model()`: the two models with the exact ids used for generation. `LLMClient`: one API call with retries. `MockClient`: a fake model for testing |
| `runner.py` | `run_prompts()` / `run_requests()`: send a list of prompts concurrently and save every answer to a JSONL file, resumably |
| `parsing.py` | `parse_json()` / `parse_json_fields()`: get the JSON object out of a reply, even if the model wraps it in text or a code block |
| `jsonl.py` | `read_jsonl()`, `write_jsonl()`, `JsonlAppender`: JSONL files that survive crashes |
| `usage.py` | `python -m llm_api.usage <files>`: calls, tokens and estimated cost per model |

## Setup

From the repo root, in the project environment (see `README_Generation.md`):

```bash
python -m pip install -r requirements.txt
python -m pytest tests/test_llm_api.py      # no keys needed
```

Set the API keys as environment variables, never in code (see [API keys](#api-keys-and-sharing-the-accounts) below):

```bash
export OPENAI_API_KEY="sk-..."          # Git Bash; PowerShell: $env:OPENAI_API_KEY = "sk-..."
export DEEPINFRA_API_KEY="..."
```

Run your scripts from the repo root (`python -m filtering.something` or `python my_script.py`) so `import llm_api` works.

## Quick start

A request is a dict with a unique `id` and a `prompt`. Use the pool record's id, so each verdict can be joined back to its bio:

```python
from string import Template
from llm_api import read_jsonl, run_prompts, parse_json_fields

pool = read_jsonl("data/runs/full_v1/pool.jsonl")   # bio + explanation + labels per record
# Your prompt, with $profession and $bio placeholders. string.Template (not str.format) lets the
# prompt contain literal JSON braces like {"score": 1-5, "keep": true/false}.
TEMPLATE = Template(open("prompts/filter_content_only_v1.txt", encoding="utf-8").read())

requests = [{"id": r["id"],
             "prompt": TEMPLATE.substitute(profession=r["profession"], bio=r["bio"]),
             "seed": 0}
            for r in pool]

stats = run_prompts(requests, "gpt4omini", "data/filtering/content_only_gpt4omini.jsonl",
                    tag={"filter": "content_only"}, limit=5)   # limit=5: smoke test first
print(stats)   # {'requested': 5, 'ok': 5, 'failed': 0, 'prompt_tokens': ..., ...}

for row in read_jsonl("data/filtering/content_only_gpt4omini.jsonl"):
    verdict = parse_json_fields(row["raw"], {"score": int, "keep": bool})  # None if malformed
```

Run the same line again without `limit` and it only sends the requests that aren't done yet. For the explanation-aware filter, use a template that also includes `r["explanation"]` and write to a different output file. Use `"llama"` instead of `"gpt4omini"` for the other filter model.

### Output file

One line per answered request:

```json
{"id": "full_v1_llama_nurse_female_00417", "filter": "content_only",
 "raw": "{\"score\": 4, \"keep\": true}", "finish_reason": "stop",
 "model_returned": "gpt-4o-mini-2024-07-18",
 "usage": {"prompt_tokens": 312, "completion_tokens": 14}, "ts": "2026-10-13T10:00:00+00:00"}
```

- `raw` is the reply exactly as received. Parse it afterwards with `parse_json_fields`, so a parsing change never needs new API calls.
- Fields passed in `tag` are copied into every line.
- `model_returned` is the model that actually answered. Report it in the paper.

### What happens when things go wrong

| Situation | Behaviour |
|---|---|
| Rate limit (429), timeout, connection error, server error (5xx) | Retried automatically, waiting about 1, 2, 4, … seconds (up to `retries` times) |
| A request still fails, or is rejected (e.g. 400) | Written to `errors_<output file name>`; the other requests continue. Rerun to retry |
| Wrong or missing API key, unknown model | `FatalError`: the whole run stops at once |
| Script killed halfway (Ctrl+C, crash, laptop sleep) | Everything already answered is saved. Rerun and it continues |

## Models and settings

```python
from llm_api import get_model
cfg = get_model("llama", concurrency=32, max_tokens=100)   # preset with some settings changed
```

| Preset | Provider | Model id |
|---|---|---|
| `"llama"` | DeepInfra (`DEEPINFRA_API_KEY`) | `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo` |
| `"gpt4omini"` | OpenAI (`OPENAI_API_KEY`) | `gpt-4o-mini-2024-07-18` |

These are the same model ids and providers used to generate the pool. Keep it that way, so "Llama as generator" and "Llama as filter" are the same model. DeepInfra only serves the 8-bit (FP8) "Turbo" version of Llama 3.1-8B.

| Setting | Default | Notes |
|---|---|---|
| `temperature` | 0.0 | Deterministic-ish judging. Generation used 0.9 |
| `top_p` | 1.0 | |
| `max_tokens` | 500 | A short verdict needs far fewer; lowering it saves a little money |
| `json_mode` | True | Asks the API for a JSON object. The prompt must mention JSON, or OpenAI rejects the request |
| `send_seed` | True | Sends each request's `seed` (if given) for more reproducible answers |
| `concurrency` | 8 | Requests in flight at once. 16–32 worked fine in the pilot |
| `retries` | 5 | Extra attempts after rate limits and server errors |
| `timeout` | 60 | Seconds per request |

Pass `get_model(...)`'s result instead of a name to use changed settings: `run_prompts(requests, cfg, ...)`.

### System prompts

Use `messages` instead of `prompt` in a request:

```python
{"id": "...", "messages": [{"role": "system", "content": "You are a strict reviewer."},
                           {"role": "user", "content": "..."}]}
```

### In Jupyter, or with your own async code

`run_prompts` starts its own event loop, which Jupyter doesn't allow. In a notebook, use the async version:

```python
from llm_api import LLMClient, get_model, run_requests

async with LLMClient(get_model("llama")) as client:
    stats = await run_requests(requests, client, "data/filtering/out.jsonl", concurrency=16)
    one = await client.complete("Return {\"ok\": true} as JSON")   # a single call
```

## Testing without keys or money

Pass `mock=`, a function that receives the request dict and returns the reply text:

```python
def fake_judge(request):
    return '{"score": 3, "keep": true}'

run_prompts(requests, "llama", "data/filtering/test.jsonl", mock=fake_judge)
```

The output file has the same format as a real run, so you can build and test the whole filtering and analysis code before spending anything. `tests/test_llm_api.py` has more examples, including a local fake OpenAI server that returns rate-limit errors.

## Usage and cost

```bash
python -m llm_api.usage "data/runs/*/raw_*.jsonl" "data/filtering/*.jsonl"
```
```
4 files
model                                            calls   tokens in  tokens out    cost $
gpt-4o-mini-2024-07-18                             336      144048       61645    0.0586
meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo        336      145123       68475    0.0063
total (known prices)                                                              0.0649
```

That example is the actual pilot. The cost is an estimate from the prices in `llm_api/usage.py` (checked 2026-10-09); the providers' billing pages are the real numbers. Before a big run, do a `limit=20` run and multiply its cost up.

## API keys and sharing the accounts

Both accounts are paid from shared credit, so each of us uses our own key on the same account. That way nobody has to pass keys around, each key can be revoked separately, and we can see who used what.

- **OpenAI:** Andrei invites you to the organization (platform.openai.com → Settings → Members). Use a separate **project** for filtering (Settings → Projects, e.g. "filtering"), with its own budget limit. Create your own key inside that project. The usage dashboard then shows generation and filtering costs separately.
- **DeepInfra:** ask Andrei for a separate API key named e.g. "filtering". Share it in person or by direct message, never in a group chat or the repo. It can be revoked when the project ends. To see filtering costs separately, use `python -m llm_api.usage` on the filtering output files.

Rules for keys:
- Never commit a key, paste it into code, or put it in a config file.
- If a key ends up somewhere public (a chat, a commit, a screenshot), revoke it right away and make a new one.
- Stop and check with Andrei before runs that would cost more than a few dollars.
