"""Tiny local OpenAI-compatible chat completions server for testing the live path.

Every 4th request gets a 429 and every 11th a 500, so retries are exercised. Responses come from
the mock model.
"""
from __future__ import annotations

import json
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from gen.mock import mock_response


class FakeOpenAIServer(ThreadingHTTPServer):
    def __init__(self):
        super().__init__(("127.0.0.1", 0), Handler)
        self.lock = threading.Lock()
        self.n_requests = 0
        self.status_counts = {}
        self.bodies = []

    @property
    def base_url(self):
        return f"http://127.0.0.1:{self.server_address[1]}/v1"

    def __enter__(self):
        threading.Thread(target=self.serve_forever, daemon=True).start()
        return self

    def __exit__(self, *exc):
        self.shutdown()
        self.server_close()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, status, payload):
        data = json.dumps(payload).encode()
        with self.server.lock:
            self.server.status_counts[status] = self.server.status_counts.get(status, 0) + 1
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        with self.server.lock:
            self.server.n_requests += 1
            n = self.server.n_requests
            self.server.bodies.append(body)
        if n % 4 == 0:
            return self.send(429, {"error": {"message": "Rate limit reached", "type": "requests"}})
        if n % 11 == 0:
            return self.send(500, {"error": {"message": "Internal error", "type": "server_error"}})

        prompt = body["messages"][0]["content"]
        gender = re.search(r"biography of a (male|female) ", prompt)
        profession = re.search(r"working as an? (.+?)\.\n", prompt)
        result = mock_response({"seed": body.get("seed", 0), "prompt": prompt,
                                "target_gender": gender.group(1) if gender else None,
                                "profession": profession.group(1).replace(" ", "_")})
        self.send(200, {
            "id": f"chatcmpl-{n}", "object": "chat.completion", "created": 0,
            "model": body["model"],
            "choices": [{"index": 0, "finish_reason": result["finish_reason"], "logprobs": None,
                         "message": {"role": "assistant", "content": result["raw"]}}],
            "usage": {**result["usage"],
                      "total_tokens": sum(result["usage"].values())}})
