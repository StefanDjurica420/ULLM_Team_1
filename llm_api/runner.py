"""Run many requests concurrently and save every answer to a JSONL file, resumably.

Each request is a dict with a unique "id" and a "prompt" (or "messages"), optionally a "seed".
Answers are appended to out_path the moment they arrive; ids already in out_path are skipped, so
rerunning after a crash or with a bigger limit continues where it stopped. Requests that still
fail after all retries go to errors_path and are retried on the next run.
"""
from __future__ import annotations

import asyncio
import time
from datetime import datetime, timezone
from pathlib import Path

from .client import FatalError, LLMClient, MockClient, get_model
from .jsonl import JsonlAppender, read_jsonl


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


async def run_requests(requests, client, out_path, *, errors_path=None, concurrency=8,
                       limit=None, tag=None, label="llm"):
    """Send requests through client (LLMClient or MockClient) and append the answers.

    Each output line is {"id", **tag, "raw", "finish_reason", "model_returned", "usage", "ts"}.
    tag adds fixed fields to every line, e.g. {"filter": "content_only"}. Returns a stats dict.
    Raises FatalError (after stopping the remaining requests) on errors like a bad API key.
    """
    out_path = Path(out_path)
    errors_path = Path(errors_path) if errors_path else out_path.with_name(f"errors_{out_path.name}")
    requests = list(requests)
    ids = [r["id"] for r in requests]
    if len(set(ids)) != len(ids):
        raise ValueError("request ids must be unique")
    done = {r["id"] for r in read_jsonl(out_path)}
    todo = [r for r in requests if r["id"] not in done]
    if limit is not None:
        todo = todo[:limit]
    print(f"[{label}] {len(requests)} requests, {len(done & set(ids))} already done, "
          f"{len(todo)} to call now")
    stats = {"requested": len(todo), "ok": 0, "failed": 0, "prompt_tokens": 0,
             "completion_tokens": 0, "seconds": 0.0}
    if not todo:
        return stats

    tag = tag or {}
    semaphore = asyncio.Semaphore(concurrency)
    every = max(10, len(todo) // 20)
    start = time.monotonic()

    with JsonlAppender(out_path) as out, JsonlAppender(errors_path) as err_out:

        async def worker(request):
            async with semaphore:
                try:
                    result = await client.call(request)
                except Exception as e:  # CallFailed, or a bug in a mock: record and go on
                    if isinstance(e, FatalError):
                        raise
                    err_out.write({"id": request["id"], **tag, "error": f"{type(e).__name__}: {e}",
                                   "attempts": getattr(e, "attempts", 1), "ts": _now()})
                    stats["failed"] += 1
                else:
                    out.write({"id": request["id"], **tag, **result, "ts": _now()})
                    stats["ok"] += 1
                    stats["prompt_tokens"] += result["usage"]["prompt_tokens"] or 0
                    stats["completion_tokens"] += result["usage"]["completion_tokens"] or 0
            n = stats["ok"] + stats["failed"]
            if n % every == 0 or n == len(todo):
                print(f"[{label}] {n}/{len(todo)}  ok {stats['ok']}  failed {stats['failed']}"
                      f"  {time.monotonic() - start:.0f}s", flush=True)

        tasks = [asyncio.create_task(worker(r)) for r in todo]
        try:
            await asyncio.gather(*tasks)
        except FatalError:
            for t in tasks:
                t.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            raise

    stats["seconds"] = round(time.monotonic() - start, 1)
    if stats["ok"]:
        print(f"[{label}] average tokens per call: "
              f"{stats['prompt_tokens'] / stats['ok']:.0f} in, "
              f"{stats['completion_tokens'] / stats['ok']:.0f} out")
    if stats["failed"]:
        print(f"[{label}] {stats['failed']} requests failed; see {errors_path}. "
              "Rerun to retry them.")
    return stats


def run_prompts(requests, model, out_path, *, errors_path=None, limit=None, tag=None, mock=None):
    """Synchronous wrapper: run_requests with a client made for you.

    model is "llama", "gpt4omini" or a ModelConfig. Pass mock=<function(request) -> reply> to
    use a MockClient instead of the real API. Not usable inside Jupyter (which already runs an
    event loop): there, use `await run_requests(...)` with an LLMClient.
    """
    config = get_model(model) if isinstance(model, str) else model

    async def main():
        client = MockClient(mock) if mock else LLMClient(config)
        async with client:
            return await run_requests(requests, client, out_path, errors_path=errors_path,
                                      concurrency=config.concurrency, limit=limit, tag=tag,
                                      label=config.name)

    return asyncio.run(main())
