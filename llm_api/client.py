"""One chat-completion call to Llama 3.1-8B (DeepInfra) or GPT-4o-mini (OpenAI), with retries.

Both providers speak the OpenAI chat API, so one client class covers both; only the base URL,
model id and API key differ (see MODELS).
"""
from __future__ import annotations

import asyncio
import os
import random
from dataclasses import dataclass, fields, replace


@dataclass(frozen=True)
class ModelConfig:
    """Everything needed to call one model.

    The defaults suit judging/filtering (temperature 0, JSON output). For generation the
    pipeline passes temperature 0.9 and top_p 0.95.
    """
    name: str             # short name used in file names and logs, e.g. "llama"
    model: str            # provider's model id
    base_url: str
    api_key_env: str      # name of the environment variable holding the key (never the key)
    provider: str = ""
    temperature: float = 0.0
    top_p: float = 1.0
    max_tokens: int = 500
    json_mode: bool = True      # response_format={"type": "json_object"}
    send_seed: bool = True      # send a per-request seed (set False if a provider rejects it)
    concurrency: int = 8        # requests in flight at once
    retries: int = 5            # extra attempts after rate limits, timeouts and 5xx errors
    timeout: float = 60.0       # seconds per request
    backoff_base: float = 1.0   # first retry waits ~1 s, then 2, 4, ... (max 60)

    @classmethod
    def from_dict(cls, name, values):
        """Build from a config dict; keys that are not ModelConfig fields are ignored."""
        known = {f.name for f in fields(cls)} - {"name"}
        return cls(name=name, **{k: v for k, v in values.items() if k in known})


# The two models used in the project. Use the same ids for generation and filtering.
MODELS = {
    # DeepInfra only serves the FP8-quantized "Turbo" variant of Llama 3.1-8B (checked
    # 2026-10-09); requests for the non-Turbo id are silently redirected to it.
    "llama": ModelConfig(name="llama", provider="deepinfra",
                         base_url="https://api.deepinfra.com/v1/openai",
                         api_key_env="DEEPINFRA_API_KEY",
                         model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"),
    "gpt4omini": ModelConfig(name="gpt4omini", provider="openai",
                             base_url="https://api.openai.com/v1",
                             api_key_env="OPENAI_API_KEY",
                             model="gpt-4o-mini-2024-07-18"),
}


def get_model(name, **overrides):
    """A preset from MODELS with some settings changed, e.g. get_model("llama", concurrency=32)."""
    if name not in MODELS:
        raise KeyError(f"Unknown model {name!r}; choose from {list(MODELS)}")
    return replace(MODELS[name], **overrides)


class CallFailed(Exception):
    """One request failed for good (after retries, or a bad request). Other requests go on."""

    def __init__(self, message, attempts):
        super().__init__(message)
        self.attempts = attempts


class FatalError(Exception):
    """An error that would hit every request (missing or bad key, unknown model): stop the run."""


class LLMClient:
    """Async client for one model.

        async with LLMClient(get_model("gpt4omini")) as client:
            result = await client.complete("Say hi as JSON", seed=1)

    complete() returns {"raw": reply text, "finish_reason", "model_returned",
    "usage": {"prompt_tokens", "completion_tokens"}}.
    """

    def __init__(self, config, api_key=None):
        import openai

        self.openai = openai
        self.config = config
        key = api_key or os.environ.get(config.api_key_env)
        if not key:
            raise FatalError(f"Set the {config.api_key_env} environment variable.")
        self.client = openai.AsyncOpenAI(base_url=config.base_url, api_key=key,
                                         max_retries=0, timeout=config.timeout)

    def build_request(self, prompt=None, messages=None, seed=None):
        if (prompt is None) == (messages is None):
            raise ValueError("pass exactly one of prompt or messages")
        c = self.config
        kwargs = {"model": c.model,
                  "messages": messages or [{"role": "user", "content": prompt}],
                  "temperature": c.temperature, "top_p": c.top_p, "max_tokens": c.max_tokens}
        if c.send_seed and seed is not None:
            kwargs["seed"] = seed
        if c.json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        return kwargs

    async def complete(self, prompt=None, *, messages=None, seed=None):
        """Send one prompt (or a full messages list) and return the reply, retrying on
        rate limits, timeouts, connection errors and 5xx with exponential backoff."""
        openai = self.openai
        kwargs = self.build_request(prompt, messages, seed)
        last = None
        for attempt in range(self.config.retries + 1):
            if attempt:
                delay = min(60.0, self.config.backoff_base * 2 ** (attempt - 1))
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
        raise CallFailed(f"{type(last).__name__}: {last}", self.config.retries + 1)

    async def call(self, request):
        """complete() for a request dict with "prompt" or "messages" and optionally "seed"."""
        return await self.complete(request.get("prompt"), messages=request.get("messages"),
                                   seed=request.get("seed"))

    async def close(self):
        await self.client.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.close()


class MockClient:
    """Stand-in for LLMClient for tests and dry runs, no key or money needed.

    respond(request) gets the whole request dict and returns the reply text, or a complete
    result dict in the same shape as LLMClient.complete().
    """

    def __init__(self, respond):
        self.respond = respond

    async def call(self, request):
        out = self.respond(request)
        if isinstance(out, str):
            out = {"raw": out, "finish_reason": "stop", "model_returned": "mock",
                   "usage": {"prompt_tokens": len(request.get("prompt") or "") // 4,
                             "completion_tokens": len(out) // 4}}
        return out

    async def close(self):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        pass
