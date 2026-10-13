# Calling Llama and GPT-4o-mini from Python

This folder contains the code we use to talk to our two language models:

- **Llama 3.1-8B**, which runs on DeepInfra;
- **GPT-4o-mini**, which runs on OpenAI.

The synthetic data generation already uses this code; it made all 672 calls of the pilot without a single failure. The filtering step needs the same thing, so you don't have to write your own API code: just import this.

In short: **you give it a list of prompts, it sends them to the model and saves every answer to a file.** It deals with the annoying parts for you:

- It sends many prompts at the same time, so thousands of prompts take minutes, not hours.
- If the provider says "too many requests" or has a hiccup, it waits and tries again.
- Every answer is saved the moment it arrives. If your laptop crashes halfway, run the script again and it continues where it stopped.
- It can tell you how much your runs cost.

It knows nothing about bios or filtering. You write the prompts and decide what to do with the answers.

---

## Step 1: Set up (once)

Open a terminal in the project folder, activate the project's Python environment (see `README_Generation.md`), and install the requirements:

```bash
python -m pip install -r requirements.txt
```

To check that everything works (this needs no API key and costs nothing):

```bash
python -m pytest tests/test_llm_api.py
```

Always run your own scripts from the project folder, otherwise Python won't find `llm_api`.

## Step 2: Set your API key

The code reads your key from an *environment variable*: a setting that lives in your terminal session, not in a file. Set it every time you open a new terminal.

Git Bash:
```bash
export OPENAI_API_KEY="sk-..."
export DEEPINFRA_API_KEY="..."
```

PowerShell:
```powershell
$env:OPENAI_API_KEY = "sk-..."
$env:DEEPINFRA_API_KEY = "..."
```

**Never put a key in your code, in a config file, or in a chat.** See [API keys](#api-keys-who-gets-what) at the bottom for how to get your own.

## Step 3: Try it without spending money

Before using the real models, try everything with a fake one. You write a small function that pretends to be the model:

```python
from llm_api import run_prompts

def fake_model(request):
    return '{"score": 3, "keep": true}'     # always gives the same answer

prompts = [
    {"id": "bio_1", "prompt": "Rate this bio as JSON: She treats patients at a clinic."},
    {"id": "bio_2", "prompt": "Rate this bio as JSON: He writes backend code."},
]

run_prompts(prompts, "llama", "data/filtering/test.jsonl", mock=fake_model)
```

The output file looks exactly like a real run's, so you can build and test your whole filtering and analysis code first, and only switch to the real model at the end by removing `mock=fake_model`.

## Step 4: Run a real filter

Here is a full example: a content-only filter with GPT-4o-mini over the synthetic pool.

```python
from string import Template
from llm_api import read_jsonl, run_prompts

# 1. Load the synthetic bios.
pool = read_jsonl("data/runs/full_v1/pool.jsonl")

# 2. Load your prompt from a file. It contains $profession and $bio where the values go.
template = Template(open("prompts/filter_content_only_v1.txt", encoding="utf-8").read())

# 3. Make one request per bio. Use the bio's own id, so you can match answers to bios later.
requests = [
    {"id": bio["id"],
     "prompt": template.substitute(profession=bio["profession"], bio=bio["bio"])}
    for bio in pool
]

# 4. Send them. Start with limit=5 to check that the answers look right.
run_prompts(requests, "gpt4omini", "data/filtering/content_only_gpt4omini.jsonl",
            tag={"filter": "content_only"}, limit=5)
```

When the first 5 answers look good, run the same code again without `limit=5`. It skips the 5 that are already done and sends the rest.

A few things to know:

- **Which model:** write `"gpt4omini"` or `"llama"`. These are the exact same models that generated the bios, which matters for the comparison in the paper.
- **The prompt must mention JSON** (e.g. "Answer in JSON: {"score": ..., "keep": ...}"). We ask the API for JSON output, and OpenAI refuses requests whose prompt doesn't say "JSON".
- **Why `Template` and not an f-string or `.format()`:** your prompt will contain curly braces for the JSON example, and those confuse `.format()`. `Template` uses `$name` instead, so braces are fine.
- **One output file per filter and model**, e.g. `content_only_llama.jsonl`, `explanation_aware_gpt4omini.jsonl`. For the explanation-aware filter, also put `bio["explanation"]` into the prompt.
- **`tag`** is optional. Whatever you put in it is copied into every line of the output file, which is handy for knowing what produced a file.

## Step 5: Read the answers

Each line of the output file is one answer:

```json
{"id": "full_v1_llama_nurse_female_00417", "filter": "content_only",
 "raw": "{\"score\": 4, \"keep\": true}", "finish_reason": "stop",
 "model_returned": "gpt-4o-mini-2024-07-18",
 "usage": {"prompt_tokens": 312, "completion_tokens": 14}, "ts": "2026-10-13T10:00:00+00:00"}
```

`raw` is the model's reply, exactly as received. To turn it into usable values:

```python
from llm_api import read_jsonl, parse_json_fields

for row in read_jsonl("data/filtering/content_only_gpt4omini.jsonl"):
    verdict = parse_json_fields(row["raw"], {"score": int, "keep": bool})
    if verdict is None:
        print("unusable answer for", row["id"])     # the model didn't follow the format
    else:
        print(row["id"], verdict["score"], verdict["keep"])
```

`parse_json_fields` also copes with replies like "Sure! Here you go: {...}" or JSON inside a code block, and returns `None` when the answer is unusable. Because the raw reply is kept, you can change how you parse it later without paying for new API calls.

## If something goes wrong

- **"Too many requests", timeouts, or server errors:** these are handled for you. It waits a moment (1, 2, 4 seconds, and so on) and tries again, up to 5 times.
- **A prompt still fails after that:** it is written to a separate errors file next to your output (e.g. `errors_content_only_gpt4omini.jsonl`), and the other prompts keep going. Run the script again later to retry only the failed ones.
- **Missing or wrong API key, or a model the provider doesn't know:** everything stops immediately with a `FatalError` that says what's wrong, so you don't get thousands of failed requests. (A typo in the short name, like `"lama"`, gives an error listing the valid names.)
- **The script stops halfway** (crash, Ctrl+C, laptop goes to sleep): nothing is lost. Run it again and it continues.

## Changing settings

The defaults suit filtering, so you usually don't need to change anything. If you do, use `get_model`:

```python
from llm_api import get_model, run_prompts

llama = get_model("llama", max_tokens=100, concurrency=16)
run_prompts(requests, llama, "data/filtering/content_only_llama.jsonl")
```

The settings you might care about:

- **`temperature`** (default 0): how random the answers are. 0 gives the most consistent judgements. Generation used 0.9 because we wanted varied bios.
- **`max_tokens`** (default 500): the maximum answer length. A short verdict needs much less, and lowering it saves a little money.
- **`concurrency`** (default 8): how many prompts are sent at the same time. 16–32 worked fine in the pilot.

Others, rarely needed:
- `top_p` (1.0): another randomness setting.
- `json_mode` (on): asks for JSON output.
- `send_seed` (on): if your request has a `"seed"`, it is sent for more reproducible answers.
- `retries` (5): how often to retry.
- `timeout` (60 seconds): how long to wait for one answer.

**System prompt:** to give the model a separate instruction ("You are a strict reviewer"), use `messages` instead of `prompt` in a request:

```python
{"id": "bio_1", "messages": [
    {"role": "system", "content": "You are a strict reviewer. Answer in JSON."},
    {"role": "user", "content": "Rate this bio: ..."}]}
```

## Using a Jupyter notebook

`run_prompts` doesn't work inside Jupyter: you'll get an error about an "event loop". In a notebook, use this version instead (note the `await`):

```python
from llm_api import LLMClient, get_model, run_requests

async with LLMClient(get_model("llama")) as client:
    await run_requests(requests, client, "data/filtering/out.jsonl", concurrency=16)
```

## How much did it cost?

```bash
python -m llm_api.usage "data/filtering/*.jsonl"
```

This counts the tokens in your output files and estimates the cost per model. For example, here is the generation pilot:

```
model                                            calls   tokens in  tokens out    cost $
gpt-4o-mini-2024-07-18                             336      144048       61645    0.0586
meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo        336      145123       68475    0.0063
total (known prices)                                                              0.0649
```

The prices come from `llm_api/usage.py` and were checked on 2026-10-09. The providers' billing pages show the real numbers. Before a big run, do a small one (`limit=20`), check its cost, and multiply.

## API keys: who gets what

We share the same accounts and credit, but each person gets **their own key**. Then nobody has to send keys around, a key can be switched off without affecting anyone else, and we can see who spent what.

- **OpenAI:** Andrei invites you to the organization (platform.openai.com → Settings → Members) and creates a project called "filtering" with its own spending limit. You make your own key inside that project. OpenAI's usage page then shows generation and filtering costs separately.
- **DeepInfra:** Andrei creates a separate key named "filtering" and gives it to you in person or by private message, never in a group chat or the repo. To see what filtering cost, use the cost report above on your output files.

Rules:
- Never put a key in code, a config file, a commit or a chat.
- If a key ends up somewhere public anyway, switch it off in the provider's dashboard straight away and make a new one.
- Check with Andrei before runs that would cost more than a few dollars.

---

## Reference: what's in this folder

| File | What it does |
|---|---|
| `client.py` | The two models (`get_model("llama")`, `get_model("gpt4omini")`) and the client that makes one API call with retries (`LLMClient`). Also `MockClient`, the fake model used by `mock=` |
| `runner.py` | `run_prompts` (normal scripts) and `run_requests` (notebooks): send many prompts and save the answers |
| `parsing.py` | `parse_json` and `parse_json_fields`: get the JSON out of a reply |
| `jsonl.py` | `read_jsonl` and `write_jsonl`: read and write files with one JSON object per line |
| `usage.py` | The cost report (`python -m llm_api.usage`) |

| Model name | Provider | Exact model |
|---|---|---|
| `"llama"` | DeepInfra (key: `DEEPINFRA_API_KEY`) | `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo`, the 8-bit "Turbo" version, the only one DeepInfra offers |
| `"gpt4omini"` | OpenAI (key: `OPENAI_API_KEY`) | `gpt-4o-mini-2024-07-18` |

More examples, including a fake server that imitates OpenAI's errors, are in `tests/test_llm_api.py`.
