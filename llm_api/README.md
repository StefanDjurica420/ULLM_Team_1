# llm_api

Python helpers for sending prompts to our two language models and saving their answers:

| Name in code | Model | Provider | Key needed |
|---|---|---|---|
| `"llama"` | Llama 3.1-8B Instruct (`meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo`) | DeepInfra | `DEEPINFRA_API_KEY` |
| `"gpt4omini"` | GPT-4o-mini (`gpt-4o-mini-2024-07-18`) | OpenAI | `OPENAI_API_KEY` |

The synthetic data generation uses this package, and the filtering step can use it in the same way. You give it a list of prompts; it sends them to the model and saves every answer to a file. Along the way it:

- sends many prompts at once, so thousands of prompts take minutes rather than hours;
- waits and retries automatically when the provider is busy or has a temporary error;
- saves each answer as soon as it arrives, so an interrupted run can simply be restarted;
- reports how many tokens were used and what they cost.

It does not know anything about bios or filtering. You write the prompts and decide what to do with the answers.

**Contents**
1. [Setup](#1-setup)
2. [API key or token](#2-api-key-or-token)
3. [Quick start](#3-quick-start)
4. [Reading the results](#4-reading-the-results)
5. [Method reference](#5-method-reference)
6. [Settings](#6-settings)
7. [When something goes wrong](#7-when-something-goes-wrong)
8. [Costs](#8-costs)
9. [Managing access tokens](#9-managing-access-tokens)

---

## 1. Setup

Do this once, in PowerShell, from the project folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

In Git Bash, activate with `source .venv/Scripts/activate` instead.

To check the installation (no key needed, nothing is sent anywhere):

```powershell
python -m pytest tests/test_llm_api.py
```

Always run your scripts from the project folder with the environment activated, otherwise Python cannot find `llm_api`.

## 2. API key or token

The code reads the key from an **environment variable**, never from a file. This keeps keys out of code and out of git. You only need the variable for the model you use.

**Llama:** you receive a DeepInfra token (a long string that starts with `jwt:`). Save it once in PowerShell:

```powershell
setx DEEPINFRA_API_KEY "jwt:..."
```

**GPT-4o-mini** (only if you use it):

```powershell
setx OPENAI_API_KEY "sk-..."
```

`setx` stores the value permanently for your Windows user, but only **new** windows see it. Close PowerShell, open a new one, and activate the environment again.

To set a key for the current window only, use `$env:DEEPINFRA_API_KEY = "..."` (PowerShell) or `export DEEPINFRA_API_KEY="..."` (Git Bash).

### Test it

This sends one tiny prompt to Llama and costs a fraction of a cent:

```powershell
python -c "from llm_api import run_prompts; print(run_prompts([{'id': 't1', 'prompt': 'Reply with JSON: {\"ok\": true}'}], 'llama', 'data/filtering/token_test.jsonl'))"
```

If the output shows `'ok': 1`, everything works. If not, see [section 7](#7-when-something-goes-wrong).

### Keeping keys safe

- Never put a key or token in code, a config file, a commit, a screenshot or a chat.
- If one is exposed anyway, report it so it can be switched off and replaced.

## 3. Quick start

### Try it for free first

Pass `mock=` with a function that pretends to be the model. Nothing is sent and nothing is charged, but the output file looks exactly like a real one. This lets you build and test all your code first.

```python
from llm_api import run_prompts

def fake_model(request):
    return '{"score": 3, "keep": true}'

prompts = [
    {"id": "bio_1", "prompt": "Rate this bio. Answer in JSON: She treats patients at a clinic."},
    {"id": "bio_2", "prompt": "Rate this bio. Answer in JSON: He writes backend code."},
]

run_prompts(prompts, "llama", "data/filtering/test.jsonl", mock=fake_model)
```

### A real run

Example: a filter that judges every bio in the synthetic pool with Llama.

```python
from string import Template
from llm_api import read_jsonl, run_prompts

pool = read_jsonl("data/runs/full_v1/pool.jsonl")       # the synthetic bios

# Prompt stored in a file, with $profession and $bio where the values go.
template = Template(open("prompts/filter_content_only_v1.txt", encoding="utf-8").read())

requests = [
    {"id": bio["id"],                                    # reuse the bio's id
     "prompt": template.substitute(profession=bio["profession"], bio=bio["bio"])}
    for bio in pool
]

out = "data/filtering/content_only_llama.jsonl"
run_prompts(requests, "llama", out, limit=5)             # first 5 only: check the answers
run_prompts(requests, "llama", out)                      # then the rest (the 5 are skipped)
```

Good to know:
- **Each request needs a unique `id`.** Use the bio's own id, so answers can be matched back to bios.
- **The prompt must ask for JSON.** The API is set to return JSON, and the provider rejects prompts that don't mention it.
- **Use `string.Template` (`$name`) for prompt files, not `.format()` or f-strings.** Prompts contain curly braces for the JSON example, which break `.format()`.
- **Use a separate output file for each filter and model**, e.g. `content_only_llama.jsonl` and `explanation_aware_llama.jsonl`.
- **Running the same command again is safe.** Requests that already have an answer are skipped.

## 4. Reading the results

The output file has one line per answer:

```json
{"id": "full_v1_llama_nurse_female_00417",
 "raw": "{\"score\": 4, \"keep\": true}",
 "finish_reason": "stop",
 "model_returned": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
 "usage": {"prompt_tokens": 312, "completion_tokens": 14},
 "ts": "2026-10-13T10:00:00+00:00"}
```

| Field | Meaning |
|---|---|
| `id` | The id from your request |
| `raw` | The model's reply, exactly as received |
| `finish_reason` | `"stop"` = finished normally; `"length"` = cut off by `max_tokens` |
| `model_returned` | The model that actually answered (report this one) |
| `usage` | Tokens sent and received, used for the cost report |
| `ts` | Time of the answer (UTC) |
| *(your `tag` fields)* | Anything passed as `tag=` is added to every line |

To turn the replies into values:

```python
from llm_api import read_jsonl, parse_json_fields

for row in read_jsonl("data/filtering/content_only_llama.jsonl"):
    verdict = parse_json_fields(row["raw"], {"score": int, "keep": bool})
    if verdict is None:
        print("unusable answer:", row["id"])
    else:
        print(row["id"], verdict["score"], verdict["keep"])
```

Because the raw reply is kept, you can change how you parse it later without new API calls.

## 5. Method reference

Everything below is imported with `from llm_api import ...`, except the cost report, which is in `llm_api.usage`.

### Sending prompts

**`run_prompts(requests, model, out_path, *, errors_path=None, limit=None, tag=None, mock=None)`**
Sends all requests and appends the answers to `out_path`. This is the method to use in normal scripts.
- `requests`: list of dicts, each with a unique `"id"` and either a `"prompt"` (text) or `"messages"` (chat format, see [System prompt](#system-prompt)). An optional `"seed"` (int) makes answers more reproducible.
- `model`: `"llama"`, `"gpt4omini"`, or a configuration from `get_model(...)`.
- `out_path`: the JSONL file for the answers. Folders are created if needed.
- `errors_path`: where failed requests are logged. Default: `errors_<output file name>` in the same folder.
- `limit`: send at most this many new requests (useful for a first test).
- `tag`: dict of extra fields copied into every output line, e.g. `{"filter": "content_only"}`.
- `mock`: function `request -> reply text`. Uses a fake model instead of the API.
- Returns a dict: `requested`, `ok`, `failed`, `prompt_tokens`, `completion_tokens`, `seconds`.
- Does not work inside Jupyter; use `run_requests` there.

**`run_requests(requests, client, out_path, *, errors_path=None, concurrency=8, limit=None, tag=None, label="llm")`**
The async version of `run_prompts`, for Jupyter notebooks or your own async code. You pass a client instead of a model name:

```python
from llm_api import LLMClient, get_model, run_requests

async with LLMClient(get_model("llama")) as client:
    stats = await run_requests(requests, client, "data/filtering/out.jsonl", concurrency=16)
```

### Models and clients

**`get_model(name, **changes)`**
Returns the settings for `"llama"` or `"gpt4omini"`, optionally with some values changed, e.g. `get_model("llama", max_tokens=100)`. See [section 6](#6-settings) for all settings. `MODELS` holds the two unchanged presets.

**`ModelConfig`**
The settings object that `get_model` returns. You normally don't create one yourself.

**`LLMClient(config, api_key=None)`**
Connection to one model, with automatic retries. Reads the key from the environment variable unless `api_key` is given. Use it with `async with`:
- `await client.complete(prompt, seed=None)`: sends one prompt and returns `{"raw", "finish_reason", "model_returned", "usage"}`.
- `await client.complete(messages=[...])`: the same, with a chat-format message list.

```python
async with LLMClient(get_model("llama")) as client:
    result = await client.complete("Answer in JSON: is the sky blue?")
```

**`MockClient(respond)`**
A fake client for testing. `respond(request)` returns the reply text. It can be used wherever an `LLMClient` is expected; `run_prompts(..., mock=...)` uses it for you.

**`FatalError`**
Raised when the whole run must stop: a missing or invalid key, or a model the provider doesn't recognise.

**`CallFailed`**
A single request that failed for good. You don't normally see it, because the runner writes it to the errors file and continues.

### Parsing replies

**`parse_json(raw)`**
Returns the JSON object in a reply as a dict, or `None`. It also handles replies wrapped in a code block or surrounded by text ("Sure! Here it is: {...}").

**`parse_json_fields(raw, fields)`**
Like `parse_json`, but also checks that each field exists and has the right type, e.g. `{"score": int, "keep": bool}`. Returns `None` if anything is missing or wrong.

### Files

**`read_jsonl(path)`**
Reads a JSONL file (one JSON object per line) into a list of dicts. Returns `[]` if the file doesn't exist. A half-written last line, left by an interrupted run, is skipped with a warning.

**`write_jsonl(path, rows)`**
Writes a list of dicts to a JSONL file in one go. It writes to a temporary file first, so a crash never leaves a half-written file.

**`JsonlAppender(path)`**
Adds lines to a JSONL file one at a time, saving each immediately. Use it with `with JsonlAppender(path) as out: out.write(row)`.

### Costs

**`python -m llm_api.usage <files...>`**
Prints calls, tokens and estimated cost per model for the given output files (wildcards allowed). See [section 8](#8-costs).

**`usage_summary(paths)`** (from `llm_api.usage`)
The same numbers as a dict, for use in your own code.

## 6. Settings

The defaults are chosen for judging/filtering, so usually nothing needs changing. To change settings, create a configuration with `get_model` and pass it instead of the name:

```python
from llm_api import get_model, run_prompts

llama = get_model("llama", max_tokens=100, concurrency=16)
run_prompts(requests, llama, "data/filtering/content_only_llama.jsonl")
```

| Setting | Default | What it does |
|---|---|---|
| `temperature` | 0.0 | Randomness of the answers. 0 gives the most consistent judgements |
| `top_p` | 1.0 | Another randomness setting; leave as is |
| `max_tokens` | 500 | Maximum answer length. A short verdict needs far fewer, and lowering this saves a little money |
| `json_mode` | True | Asks the provider for JSON output |
| `send_seed` | True | Sends the request's `"seed"`, if it has one, for more reproducible answers |
| `concurrency` | 8 | How many requests are in flight at once. 16–32 works well |
| `retries` | 5 | How often a busy or failed request is retried |
| `timeout` | 60 | Seconds to wait for one answer |
| `backoff_base` | 1.0 | First wait between retries in seconds; it doubles each time |

### System prompt

To give the model a separate instruction, use `"messages"` instead of `"prompt"`:

```python
{"id": "bio_1",
 "messages": [{"role": "system", "content": "You are a strict reviewer. Answer in JSON."},
              {"role": "user", "content": "Rate this bio: ..."}]}
```

## 7. When something goes wrong

| What you see | What it means / what to do |
|---|---|
| `Set the DEEPINFRA_API_KEY environment variable` | The key isn't set in this window. After `setx`, open a **new** PowerShell window |
| `FatalError ... AuthenticationError` | The key or token is wrong or incomplete. A token starts with `jwt:`; copy the whole string |
| `FatalError ... PermissionDenied` or `NotFound` | The key or token doesn't allow this model, or the model name is wrong |
| Every request suddenly fails (`errors_<file>.jsonl` fills up) | Read the error message in that file. Mentions of payment, quota or limits usually mean the token has expired or reached its spending limit; a new token is needed |
| `ModuleNotFoundError: llm_api` | Run your script from the project folder, with the environment activated |
| Error mentioning an "event loop" | You're in Jupyter: use `run_requests` with `await` |
| A few lines in `errors_<file>.jsonl` | Those requests failed even after retrying. Run the same command again to retry only those |
| Script stopped halfway | Nothing is lost. Run it again and it continues where it stopped |
| `parse_json_fields` returns `None` | The model didn't answer in the requested format. Make the prompt's JSON instructions clearer |

Busy servers, rate limits and temporary errors are retried automatically (after about 1, 2, 4… seconds). You only notice them as a slightly slower run.

## 8. Costs

```powershell
python -m llm_api.usage "data/filtering/*.jsonl"
```

```
model                                            calls   tokens in  tokens out    cost $
meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo        336      145123       68475    0.0063
total (known prices)                                                              0.0063
```

Costs are estimated from the prices in `llm_api/usage.py` (checked 2026-10-09: Llama $0.02 per million input tokens and $0.05 per million output tokens; GPT-4o-mini $0.15 / $0.60). The provider's billing page has the exact numbers.

Before a large run, test with `limit=20`, check the cost, and multiply.

## 9. Managing access tokens

This section is for whoever manages the DeepInfra account.

Rather than sharing the account's own key, each user gets a **scoped token**. A scoped token:
- works only for the models listed in it;
- expires on a set date;
- stops at a spending limit;
- is charged to the key that created it, so usage can be tracked separately.

### Create a token

1. In the DeepInfra dashboard (deepinfra.com/dash/api_keys), create an API key used only for signing tokens, e.g. named `filtering`. Keep this key private.
2. In Git Bash, store that key without displaying it:
   ```bash
   read -s -p "Signing key: " DI_KEY; echo
   ```
   Paste with Shift+Insert or right-click; nothing appears on screen. `echo ${#DI_KEY}` should print a number above 0.
3. Request the token. `api_key_name` must be the exact name of the signing key in the dashboard:
   ```bash
   curl -s -X POST https://api.deepinfra.com/v1/scoped-jwt \
     -H "Authorization: Bearer $DI_KEY" \
     -H "Content-Type: application/json" \
     -d '{"api_key_name": "filtering",
          "models": ["meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"],
          "expires_delta": 3628800,
          "spending_limit": 5.0}'
   ```
   - `expires_delta`: lifetime in seconds (3628800 = 6 weeks; maximum one year).
   - `spending_limit`: maximum spend in US dollars.
   - The reply is `{"token": "jwt:..."}`. The token is the whole string between the quotes, including `jwt:`.
   - The error `no tokens named ...` means `api_key_name` doesn't match a key name in the dashboard.
4. Hand the token over privately: on a call, with Signal disappearing messages, or with a one-time share link from a password manager (e.g. Bitwarden Send). Never use a group chat, email, the repo or a screenshot.
5. Close Git Bash, which clears the stored key.

### Check a token

```bash
curl -s "https://api.deepinfra.com/v1/scoped-jwt?jwtoken=<token>" -H "Authorization: Bearer $DI_KEY"
```

This shows `expires_at` (Unix time), the allowed `models`, `spending_limit`, and `spending_current` (the amount used so far).

### Revoke access

Delete the signing key in the dashboard. As far as the DeepInfra docs indicate, tokens created with that key then stop working too. Create a new signing key and new tokens if access is still needed.

### GPT-4o-mini access

OpenAI works differently. The account owner invites the person to the organization (platform.openai.com → Settings → Members) and adds them to a separate project with its own budget limit (Settings → Projects → Limits). The person then creates their own key inside that project, and OpenAI's usage page shows each project's costs separately. Make sure they aren't also a member of the Default project, which the project budget doesn't cover.
