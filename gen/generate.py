"""Send planned prompts to one generator and append raw responses to raw_<gen>.jsonl.

Resumable: ids already in raw_<gen>.jsonl are skipped, so rerunning after a crash or with a
larger --limit continues where it stopped. Calls that fail after all retries go to
errors_<gen>.jsonl and are retried on the next run. The API calls themselves are done by the
shared llm_api package (also used for filtering).
"""
from __future__ import annotations

import argparse
import asyncio

from llm_api import FatalError, LLMClient, MockClient, ModelConfig, run_requests

from .common import load_config, read_jsonl, run_path, setup_stdout
from .manifest import append_manifest
from .mock import mock_response


def make_client(cfg, gen_name):
    gen_cfg = cfg["generators"][gen_name]
    if gen_cfg["backend"] == "mock":
        return MockClient(mock_response)
    return LLMClient(ModelConfig.from_dict(gen_name, {**gen_cfg, **cfg["sampling"]}))


async def run(cfg, gen_name, limit):
    raw_path = run_path(cfg, f"raw_{gen_name}.jsonl")
    plan = [r for r in read_jsonl(run_path(cfg, "plan.jsonl")) if r["generator"] == gen_name]
    if not plan:
        raise SystemExit(f"No plan rows for {gen_name}; run gen.plan first.")
    done = {r["id"] for r in read_jsonl(raw_path)}
    if all(r["id"] in done for r in plan):
        print(f"[{gen_name}] all {len(plan)} planned calls are done")
        return

    client = make_client(cfg, gen_name)
    append_manifest(cfg, "generate", gen_name)
    async with client:
        await run_requests(plan, client, raw_path,
                           errors_path=run_path(cfg, f"errors_{gen_name}.jsonl"),
                           concurrency=cfg["generators"][gen_name]["concurrency"], limit=limit,
                           tag={"generator": gen_name}, label=gen_name)


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
        raise SystemExit(f"{args.generator}: the Batch API is not supported; "
                         "set backend: openai_compat for live calls.")
    try:
        asyncio.run(run(cfg, args.generator, args.limit))
    except FatalError as e:
        raise SystemExit(f"[{args.generator}] stopped: {e}") from None


if __name__ == "__main__":
    main()
