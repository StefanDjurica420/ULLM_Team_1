"""Getting a JSON object out of a model reply, even when the model wraps it in extra text."""
from __future__ import annotations

import json
import re


def parse_json(raw):
    """Return the JSON object in a reply, or None.

    Handles plain JSON, ```json fenced blocks, and JSON with chatter around it
    ("Sure! {...} Hope this helps").
    """
    if not raw:
        return None
    text = raw.strip()
    fenced = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, re.S)
    if fenced:
        text = fenced.group(1)
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start < 0 or end <= start:
            return None
        try:
            obj = json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            return None
    return obj if isinstance(obj, dict) else None


def parse_json_fields(raw, fields):
    """parse_json, but only if every field has the expected type, e.g.
    parse_json_fields(raw, {"score": int, "keep": bool}); otherwise None."""
    obj = parse_json(raw)
    if obj is None or not all(isinstance(obj.get(name), typ) for name, typ in fields.items()):
        return None
    return obj
