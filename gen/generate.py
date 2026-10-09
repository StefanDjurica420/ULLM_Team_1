"""Send planned prompts to one generator and append raw responses to raw_<gen>.jsonl.

Resumable: ids already in raw_<gen>.jsonl are skipped, so rerunning after a crash or with a
larger --limit continues where it stopped. Calls that fail after all retries go to
errors_<gen>.jsonl and are retried on the next run.
"""
from __future__ import annotations

import argparse
import asyncio
import os
import random
import time

from .common import JsonlAppender, load_config, now, read_jsonl, run_path, setup_stdout
from .manifest import append_manifest
from .mock import mock_response


class CallFailed(Exception):
    def __init__(self, message, attempts):
        super().__init__(message)
        self.attempts = attempts


class FatalError(Exception):
    """An error that will hit every call (bad key, unknown model): stop the run."""


class MockCaller:
    async def call(self, row):
        return mock_response(row)

    async def close(self):
        pass


class OpenAICaller:
    def __init__(self, cfg, gen_cfg):
        import openai

        self.openai = openai
        key = os.environ.get(gen_cfg["api_key_env"])
        if not key:
            raise SystemExit(f"Set the {gen_cfg['api_key_env']} environment variable.")
        self.gen = gen_cfg
        self.sampling = cfg["sampling"]
        self.client = openai.AsyncOpenAI(base_url=gen_cfg["base_url"], api_key=key,
                                         max_retries=0, timeout=gen_cfg["timeout"])

    def request(self, row):
        kwargs = {"model": self.gen["model"],
                  "messages": [{"role": "user", "content": row["prompt"]}],
                  "temperature": self.sampling["temperature"], "top_p": self.sampling["top_p"],
                  "max_tokens": self.sampling["max_tokens"]}
        if self.gen["send_seed"]:
            kwargs["seed"] = row["seed"]
        if self.gen["json_mode"]:
            kwargs["response_format"] = {"type": "json_object"}
        return kwargs

    async def call(self, row):
        openai = self.openai
        kwargs = self.request(row)
        last = None
        for attempt in range(self.gen["retries"] + 1):
            if attempt:
                delay = min(60.0, self.gen["backoff_base"] * 2 ** (attempt - 1))
                await asyncio.sleep(delay * random.uniform(0.5, 1.5))
            try:
                resp = await self.client.chat.completions.create(**kwargs)
            except (openai.RateLimitError, openai.APIConnectionError,
                    openai.InternalServerError) as e:
                last = e
                continue
            except (openai.AuthenticationError, openai.PermissionDeniedError,
                    openai.NotFoundError) as e:
                raise FatalError(f"{type(e).__name__}: {e}") from e
            except openai.APIStatusError as e:
                if e.status_code >= 500:
                    last = e
                    continue
                raise CallFailed(f"{type(e).__name__}: {e}", attempt + 1) from e
            choice, usage = resp.choices[0], resp.usage
            return {"raw": choice.message.content, "finish_reason": choice.finish_reason,
                    "model_returned": resp.model,
                    "usage": {"prompt_tokens": usage.prompt_tokens if usage else None,
                              "completion_tokens": usage.completion_tokens if usage else None}}
        raise CallFailed(f"{type(last).__name__}: {last}", self.gen["retries"] + 1)

    async def close(self):
        await self.client.close()


async def run(cfg, gen_name, limit):
    gen_cfg = cfg["generators"][gen_name]
    raw_path = run_path(cfg, f"raw_{gen_name}.jsonl")
    plan = [r for r in read_jsonl(run_path(cfg, "plan.jsonl")) if r["generator"] == gen_name]
    if not plan:
        raise SystemExit(f"No plan rows for {gen_name}; run gen.plan first.")
    done = {r["id"] for r in read_jsonl(raw_path)}
    todo = [r for r in plan if r["id"] not in done]
    if limit is not None:
        todo = todo[:limit]
    print(f"[{gen_name}] {len(plan)} planned, {len(done)} done, {len(todo)} to call now")
    if not todo:
        return

    caller = MockCaller() if gen_cfg["backend"] == "mock" else OpenAICaller(cfg, gen_cfg)
    append_manifest(cfg, "generate", gen_name)
    semaphore = asyncio.Semaphore(gen_cfg["concurrency"])
    stats = {"ok": 0, "failed": 0, "prompt_tokens": 0, "completion_tokens": 0}
    every = max(10, len(todo) // 20)
    start = time.monotonic()

    with JsonlAppender(raw_path) as raw_out, \
            JsonlAppender(run_path(cfg, f"errors_{gen_name}.jsonl")) as err_out:

        async def worker(row):
            async with semaphore:
                try:
                    result = await caller.call(row)
                except CallFailed as e:
                    err_out.write({"id": row["id"], "generator": gen_name, "error": str(e),
                                   "attempts": e.attempts, "ts": now()})
                    stats["failed"] += 1
                else:
                    raw_out.write({"id": row["id"], "generator": gen_name, **result, "ts": now()})
                    stats["ok"] += 1
                    stats["prompt_tokens"] += result["usage"]["prompt_tokens"] or 0
                    stats["completion_tokens"] += result["usage"]["completion_tokens"] or 0
            n = stats["ok"] + stats["failed"]
            if n % every == 0 or n == len(todo):
                print(f"[{gen_name}] {n}/{len(todo)}  ok {stats['ok']}  failed {stats['failed']}"
                      f"  {time.monotonic() - start:.0f}s", flush=True)

        tasks = [asyncio.create_task(worker(r)) for r in todo]
        try:
            await asyncio.gather(*tasks)
        except FatalError as e:
            for t in tasks:
                t.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            raise SystemExit(f"[{gen_name}] stopped: {e}") from None
        finally:
            await caller.close()

    if stats["ok"]:
        print(f"[{gen_name}] average tokens per call: "
              f"{stats['prompt_tokens'] / stats['ok']:.0f} in, "
              f"{stats['completion_tokens'] / stats['ok']:.0f} out")
    if stats["failed"]:
        print(f"[{gen_name}] {stats['failed']} calls failed; see errors_{gen_name}.jsonl. "
              "Rerun to retry them.")


def main(argv=None):
    setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", required=True)
    ap.add_argument("--generator", required=True)
    ap.add_argument("--limit", type=int, help="call at most N not-yet-done rows (smoke test)")
    args = ap.parse_args(argv)
    cfg = load_config(args.config)
    if args.generator not in cfg["generators"]:
        raise SystemExit(f"Unknown generator {args.generator!r}; "
                         f"config has {list(cfg['generators'])}")
    if cfg["generators"][args.generator]["backend"] == "openai_batch":
        raise SystemExit(f"{args.generator} uses the Batch API: use gen.batch_openai, or set "
                         "backend: openai_compat for live calls.")
    asyncio.run(run(cfg, args.generator, args.limit))


if __name__ == "__main__":
    main()
