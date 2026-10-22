"""Tests for the shared llm_api package (mock client and a local fake OpenAI server)."""
from __future__ import annotations

import asyncio
import json

import pytest

from llm_api import (FatalError, LLMClient, get_model, parse_json, parse_json_fields,
                     read_jsonl, run_prompts, run_requests)
from llm_api.usage import main as usage_main, usage_summary
from tests.fake_openai_server import FakeOpenAIServer


def judge(request):
    """Mock filter: keeps bios that mention 'patients'."""
    keep = "patients" in request["prompt"]
    return json.dumps({"score": 4 if keep else 2, "keep": keep})


REQUESTS = [{"id": f"bio_{i}", "prompt": f"Rate this bio: {text}", "seed": i}
            for i, text in enumerate(["She treats patients.", "He writes code.", "He sees patients."])]


def test_presets_and_overrides():
    llama = get_model("llama", concurrency=32)
    assert llama.model == "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
    assert llama.api_key_env == "DEEPINFRA_API_KEY" and llama.concurrency == 32
    assert get_model("gpt4omini").model == "gpt-4o-mini-2024-07-18"
    with pytest.raises(KeyError):
        get_model("gpt5")


def test_parse_json_fields():
    assert parse_json('```json\n{"keep": true}\n```') == {"keep": True}
    assert parse_json_fields('Sure: {"score": 3, "keep": false}', {"score": int, "keep": bool}) \
        == {"score": 3, "keep": False}
    assert parse_json_fields('{"score": "high"}', {"score": int}) is None
    assert parse_json("[1, 2]") is None


def test_run_prompts_with_mock_resumes_and_tags(tmp_path):
    out = tmp_path / "verdicts.jsonl"
    stats = run_prompts(REQUESTS, "llama", out, limit=2, mock=judge, tag={"filter": "content_only"})
    assert stats["ok"] == 2
    stats = run_prompts(REQUESTS, "llama", out, mock=judge, tag={"filter": "content_only"})
    assert stats["ok"] == 1  # only the one not done yet
    rows = read_jsonl(out)
    assert [r["id"] for r in rows] == ["bio_0", "bio_1", "bio_2"]
    assert all(r["filter"] == "content_only" for r in rows)
    assert [parse_json(r["raw"])["keep"] for r in rows] == [True, False, True]


def test_failing_requests_go_to_errors_file(tmp_path):
    def flaky(request):
        if request["id"] == "bio_1":
            raise RuntimeError("boom")
        return judge(request)

    out = tmp_path / "verdicts.jsonl"
    stats = run_prompts(REQUESTS, "gpt4omini", out, mock=flaky)
    assert stats["ok"] == 2 and stats["failed"] == 1
    assert [r["id"] for r in read_jsonl(tmp_path / "errors_verdicts.jsonl")] == ["bio_1"]
    run_prompts(REQUESTS, "gpt4omini", out, mock=judge)  # retried on the next run
    assert len(read_jsonl(out)) == 3


def test_duplicate_ids_rejected(tmp_path):
    with pytest.raises(ValueError, match="unique"):
        run_prompts(REQUESTS + REQUESTS[:1], "llama", tmp_path / "x.jsonl", mock=judge)


def test_live_client_retries_and_sends_settings(tmp_path, monkeypatch):
    monkeypatch.setenv("FAKE_KEY", "test-key")
    with FakeOpenAIServer(respond=lambda body: '{"score": 5, "keep": true}') as server:
        config = get_model("gpt4omini", base_url=server.base_url, api_key_env="FAKE_KEY",
                           backoff_base=0.01, retries=8, concurrency=4)
        requests = [{"id": f"r{i}", "prompt": f"bio {i}", "seed": i} for i in range(30)]
        stats = run_prompts(requests, config, tmp_path / "out.jsonl")
    assert stats["ok"] == 30 and stats["failed"] == 0
    assert server.status_counts.get(429, 0) > 0 and server.status_counts.get(500, 0) > 0
    body = server.bodies[0]
    assert body["model"] == "gpt-4o-mini-2024-07-18" and body["temperature"] == 0.0
    assert body["response_format"] == {"type": "json_object"} and "seed" in body


def test_messages_with_system_prompt(monkeypatch):
    monkeypatch.setenv("FAKE_KEY", "test-key")

    async def main(base_url):
        config = get_model("llama", base_url=base_url, api_key_env="FAKE_KEY", backoff_base=0.01)
        async with LLMClient(config) as client:
            return await client.complete(messages=[
                {"role": "system", "content": "You are a strict judge."},
                {"role": "user", "content": "Judge this."}])

    with FakeOpenAIServer(respond=lambda body: '{"keep": true}') as server:
        result = asyncio.run(main(server.base_url))
    assert parse_json(result["raw"]) == {"keep": True}
    assert server.bodies[0]["messages"][0]["role"] == "system"


def test_bad_key_stops_the_run(tmp_path, monkeypatch):
    monkeypatch.setenv("FAKE_KEY", "wrong-key")
    with FakeOpenAIServer() as server:
        config = get_model("llama", base_url=server.base_url, api_key_env="FAKE_KEY")
        with pytest.raises(FatalError, match="AuthenticationError"):
            run_prompts(REQUESTS, config, tmp_path / "out.jsonl")


def test_missing_key_is_fatal(monkeypatch):
    monkeypatch.delenv("DEEPINFRA_API_KEY", raising=False)
    with pytest.raises(FatalError, match="DEEPINFRA_API_KEY"):
        LLMClient(get_model("llama"))


def test_usage_summary(tmp_path, capsys):
    path = tmp_path / "raw.jsonl"
    path.write_text("\n".join(json.dumps(r) for r in [
        {"id": "a", "model_returned": "gpt-4o-mini-2024-07-18",
         "usage": {"prompt_tokens": 1_000_000, "completion_tokens": 1_000_000}},
        {"id": "b", "model_returned": "some-other-model",
         "usage": {"prompt_tokens": 10, "completion_tokens": 5}},
    ]) + "\n", encoding="utf-8")
    summary = usage_summary([path])
    assert summary["gpt-4o-mini-2024-07-18"]["cost_usd"] == 0.75
    assert summary["some-other-model"]["cost_usd"] is None
    usage_main([str(tmp_path / "*.jsonl")])
    assert "0.7500" in capsys.readouterr().out
