"""Fake data for testing without API keys: reference bios and a deterministic mock model.

The mock text is random words, not realistic bios. Some outputs are deliberately broken so that
every validation check gets exercised.
"""
from __future__ import annotations

import json
import random
import re

from .common import PROFESSIONS

VOCAB = """
able account advanced annual applied award based board broad career center chief clinical
community complex conference continued core county current daily degree department design
developed diverse early education effective experience expert family field focus former founded
global group growing guided health high honors improved independent industry initial joined
junior key known lead learned local long major managed member methods modern national network
new northern novel office original outreach part partner people practice private program
project public quality recent regional research rural senior served service skills small
southern special staff state strong student studied support system team technical training
trusted united urban various volunteer western wide work years young annual practical careful
creative steady thoughtful patient calm curious driven focused generous honest humble kind
loyal sharp warm bright quiet active open city river valley coast island mountain harbor
bridge garden market station library museum theater college school village forest summer
winter spring autumn morning evening weekend holiday travel music reading hiking cooking
running cycling painting writing chess soccer tennis swimming climbing fishing sailing dancing
""".split()

HINTS = {
    "surgeon": ["the operating room", "a surgical residency", "complex trauma cases",
                "minimally invasive procedures"],
    "physician": ["internal medicine", "primary care patients", "a busy clinic",
                  "preventive medicine"],
    "nurse": ["patient care", "the intensive care unit", "night shifts", "bedside monitoring"],
    "software_engineer": ["distributed systems", "open-source code", "backend services",
                          "data pipelines"],
    "architect": ["building design", "urban housing", "sustainable structures", "site plans"],
    "attorney": ["litigation", "corporate law", "clients in court", "the bar exam"],
    "psychologist": ["therapy sessions", "cognitive behavioral methods", "counseling",
                     "mental health research"],
    "teacher": ["the classroom", "middle school students", "the curriculum", "lesson plans"],
}

PRONOUNS = {"male": ("He", "his"), "female": ("She", "her")}


def _filler(rng, n):
    return " ".join(rng.choice(VOCAB) for _ in range(n))


def fake_bio(rng, profession, gender, n_words):
    subject, possessive = PRONOUNS[gender]
    hints = HINTS.get(profession, ["daily work"])
    words = []
    while len(words) < n_words:
        words += (f"{subject} {_filler(rng, rng.randint(4, 8))} {rng.choice(hints)} with "
                  f"{possessive} {_filler(rng, rng.randint(3, 7))}.").split()
    return " ".join(words[:n_words]).rstrip(".") + "."


def fake_refs(professions, n_per_profession, seed):
    rng = random.Random(seed)
    refs = []
    for prof in professions:
        female_share = rng.uniform(0.15, 0.9)
        for _ in range(n_per_profession):
            gender = "female" if rng.random() < female_share else "male"
            refs.append({"ref_id": len(refs), "profession": prof, "gender": gender,
                         "text": fake_bio(rng, prof, gender, rng.randint(60, 120))})
    return refs


def mock_response(row):
    """Deterministic fake completion for a plan row, in the same shape as a real API result."""
    rng = random.Random(row["seed"])
    prof = row["profession"]
    gender = row.get("target_gender") or ("female" if rng.random() < 0.65 else "male")
    bio = fake_bio(rng, prof, gender, rng.randint(70, 130))
    explanation = f"I chose a {gender} person {_filler(rng, 5)} because {_filler(rng, 9)}."
    finish_reason = "stop"
    fault = rng.random()

    if fault < 0.04:
        raw = f"Sure! Here is the biography:\n{bio}"
    else:
        if fault < 0.08:
            display = PROFESSIONS[prof]["display"] if prof in PROFESSIONS else prof
            bio = f"As a {display}, {bio[0].lower()}{bio[1:]}"
        elif fault < 0.11:  # mixed pronouns: wrong for type 1, ambiguous for types 0/4
            other = "male" if gender == "female" else "female"
            bio = fake_bio(rng, prof, gender, 45) + " " + fake_bio(rng, prof, other, 45)
        elif fault < 0.13:
            bio = " ".join(bio.split()[:20])
        elif fault < 0.15:
            match = re.search(r"Example 1: (.*?)(?:\n\n|$)", row.get("prompt", ""), re.S)
            bio = match.group(1) if match else bio
        elif fault < 0.17:
            explanation = "Chosen at random."
        elif fault < 0.25:
            bio = f"With a passion for {bio[0].lower()}{bio[1:]}"
        elif 0.29 <= fault < 0.30:
            bio = ""
        raw = json.dumps({"bio": bio, "explanation": explanation})
        if 0.25 <= fault < 0.27:
            raw = f"```json\n{raw}\n```"  # valid, but needs tolerant parsing
        elif 0.27 <= fault < 0.29:
            raw, finish_reason = raw[:len(raw) // 2], "length"

    return {"raw": raw, "finish_reason": finish_reason, "model_returned": "mock",
            "usage": {"prompt_tokens": len(row.get("prompt", "")) // 4,
                      "completion_tokens": len(raw) // 4}}
