"""End-to-end tests on the mock backend and a local fake OpenAI server (no keys, no downloads)."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pytest
import yaml

from gen import generate, inspect_sample, plan, prepare_refs, select_pool, validate
from gen.common import (JsonlAppender, cell_targets, detect_gender, has_title, largest_remainder,
                        load_config, read_jsonl, stable_seed)
from gen.validate import parse_output
from tests.fake_openai_server import FakeOpenAIServer

ROOT = Path(__file__).resolve().parents[1]


def make_config(tmp_path, prompt=None, counts=None, generators=None):
    cfg = yaml.safe_load((ROOT / "configs/mock.yaml").read_text(encoding="utf-8"))
    cfg["output_dir"] = str(tmp_path / "run")
    cfg["refs_file"] = str(tmp_path / "refs.jsonl")
    cfg["prompt"]["template"] = str(ROOT / cfg["prompt"]["template"])
    cfg["prompt"].update(prompt or {})
    cfg["counts"].update(counts or {})
    if generators is not None:
        cfg["generators"] = generators
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    return str(path)


def run_pipeline(config, max_rounds=4):
    c = ["--config", config]
    prepare_refs.main(c + ["--source", "fake", "--n-per-profession", "40"])
    plan.main(c)
    cfg = load_config(config)
    for _ in range(max_rounds):
        for gen in cfg["generators"]:
            generate.main(c + ["--generator", gen])
        validate.main(c)
        if not read_report(cfg)["short_cells"]:
            break
        plan.main(c + ["--topup"])
    select_pool.main(c)
    return cfg


def read_report(cfg):
    return json.loads((Path(cfg["output_dir"]) / "validation_report.json").read_text("utf-8"))


def assert_pool_matches_targets(cfg):
    out = Path(cfg["output_dir"])
    pool = read_jsonl(out / "pool.jsonl")
    targets = cell_targets(cfg, read_jsonl(cfg["refs_file"]))
    counts = Counter((r["generator"], r["profession"], r["gender"]) for r in pool)
    for gen in cfg["generators"]:
        for (prof, g), n in targets.items():
            assert counts[(gen, prof, g)] == n
    assert all(r["passed"] for r in pool)
    training = read_jsonl(out / "pool_training.jsonl")
    assert len(training) == len(pool)
    assert set(training[0]) == {"id", "hard_text", "profession", "gender"}
    for gen in cfg["generators"]:  # one file pair per generator, together = the whole pool
        own = read_jsonl(out / f"pool_{gen}.jsonl")
        assert own and all(r["generator"] == gen for r in own)
        assert all(r["explanation"] for r in own)
        assert [r["id"] for r in read_jsonl(out / f"pool_training_{gen}.jsonl")] ==             [r["id"] for r in own]
    assert sum(len(read_jsonl(out / f"pool_{g}.jsonl")) for g in cfg["generators"]) == len(pool)


# ---------------------------------------------------------------- units

def test_stable_seed_is_deterministic():
    assert stable_seed(42, "x") == stable_seed(42, "x")
    assert stable_seed(42, "x") != stable_seed(42, "y")
    assert 0 <= stable_seed("anything") < 2 ** 31


def test_largest_remainder():
    assert largest_remainder({"male": 1, "female": 1}, 1876) == {"male": 938, "female": 938}
    # surgeon in O: 1278 M / 222 F; 1876 split keeps the ratio and sums exactly
    split = largest_remainder({"male": 1278, "female": 222}, 1876)
    assert split == {"male": 1598, "female": 278}
    assert sum(largest_remainder({"a": 1, "b": 1, "c": 1}, 10).values()) == 10


@pytest.mark.parametrize("text,expected", [
    ("He studied medicine. His patients trust him.", "male"),
    ("She joined in 2010 and her team grew.", "female"),
    ("He met his wife at college; she is a painter. He has two kids.", "male"),
    ("He and she founded it together; her and his roles differ.", None),
    ("The doctor works in Boston.", None),
])
def test_detect_gender(text, expected):
    assert detect_gender(text) == expected


def test_title_check_is_whole_word():
    assert has_title("A Software  Engineer at Google", "software_engineer")
    assert has_title("Lawyers love her.", "attorney")
    assert not has_title("She worked in nursing homes.", "nurse")
    assert not has_title("Surgeons' tools", "nurse")


@pytest.mark.parametrize("raw", [
    '{"bio": "b", "explanation": "e"}',
    '```json\n{"bio": "b", "explanation": "e"}\n```',
    'Here you go: {"bio": "b", "explanation": "e"} Hope it helps!',
])
def test_parse_output_tolerant(raw):
    assert parse_output(raw) == {"bio": "b", "explanation": "e"}


@pytest.mark.parametrize("raw", [None, "", "no json here", '{"bio": "b"}', '["bio"]',
                                 '{"bio": "b", "explanation": "e"'])
def test_parse_output_rejects(raw):
    assert parse_output(raw) is None


def test_jsonl_tolerates_half_written_line(tmp_path):
    path = tmp_path / "x.jsonl"
    path.write_text('{"id": 1}\n{"id": 2}\n{"id": 3, "ra', encoding="utf-8")
    assert [r["id"] for r in read_jsonl(path)] == [1, 2]
    with JsonlAppender(path) as out:  # drops the broken line before appending
        out.write({"id": 4})
    assert [r["id"] for r in read_jsonl(path)] == [1, 2, 4]


# ---------------------------------------------------------------- pipeline

def test_type1_pipeline(tmp_path):
    cfg = run_pipeline(make_config(tmp_path))
    assert_pool_matches_targets(cfg)
    report = read_report(cfg)
    for gen in cfg["generators"]:  # the mock plants a failure for every check
        assert all(n > 0 for n in report["failures"][gen].values()), report["failures"][gen]
    assert any("with a passion for" in w for w in report["warnings"])
    inspect_sample.main(["--config", str(tmp_path / "config.yaml"), "--n", "3"])
    assert (Path(cfg["output_dir"]) / "review_sample.md").exists()
    manifest = read_jsonl(Path(cfg["output_dir"]) / "manifest.jsonl")
    assert {m["generator"] for m in manifest} == set(cfg["generators"])


def test_type4_pipeline_reaches_natural_ratio(tmp_path):
    config = make_config(tmp_path, prompt={"type": 4,
                                           "template": str(ROOT / "prompts/gen_type4_v1.txt")},
                         counts={"overgen": 1.6})
    cfg = run_pipeline(config)
    assert_pool_matches_targets(cfg)
    plan_rows = read_jsonl(Path(cfg["output_dir"]) / "plan.jsonl")
    assert all(r["target_gender"] is None for r in plan_rows)
    assert {r["contrastive_order"] for r in plan_rows} == {"man_first", "woman_first"}
    assert "A woman and a man are nurses in the same hospital." in "".join(
        r["prompt"] for r in plan_rows)


def test_generate_resumes_without_duplicates(tmp_path):
    config = make_config(tmp_path)
    c = ["--config", config]
    prepare_refs.main(c + ["--source", "fake", "--n-per-profession", "40"])
    plan.main(c)
    generate.main(c + ["--generator", "llama", "--limit", "10"])
    raw_path = tmp_path / "run" / "raw_llama.jsonl"
    with open(raw_path, "a", encoding="utf-8") as f:
        f.write('{"id": "half-writ')  # simulate a crash mid-write
    generate.main(c + ["--generator", "llama"])
    ids = [r["id"] for r in read_jsonl(raw_path)]
    planned = [r["id"] for r in read_jsonl(tmp_path / "run" / "plan.jsonl")
               if r["generator"] == "llama"]
    assert len(ids) == len(set(ids)) == len(planned)


def test_plan_refuses_changed_prompts(tmp_path):
    config = make_config(tmp_path)
    c = ["--config", config]
    prepare_refs.main(c + ["--source", "fake", "--n-per-profession", "40"])
    plan.main(c)
    template = tmp_path / "template.txt"
    template.write_text((ROOT / "prompts/gen_type1_v1.txt").read_text("utf-8") + "\nBe concise.",
                        encoding="utf-8")
    with pytest.raises(SystemExit, match="different prompt"):
        plan.main(["--config", make_config(tmp_path, prompt={"template": str(template)})])


def test_topup_refuses_while_calls_pending(tmp_path):
    config = make_config(tmp_path)
    c = ["--config", config]
    prepare_refs.main(c + ["--source", "fake", "--n-per-profession", "40"])
    plan.main(c)
    generate.main(c + ["--generator", "llama", "--limit", "5"])
    with pytest.raises(SystemExit, match="no response yet"):
        plan.main(c + ["--topup"])


def test_live_path_with_rate_limits(tmp_path, monkeypatch):
    monkeypatch.setenv("FAKE_OPENAI_KEY", "test-key")
    with FakeOpenAIServer() as server:
        config = make_config(tmp_path, generators={"llama": {
            "backend": "openai_compat", "provider": "fake", "base_url": server.base_url,
            "api_key_env": "FAKE_OPENAI_KEY", "model": "fake-llama", "concurrency": 4,
            "retries": 8, "backoff_base": 0.01}})
        c = ["--config", config]
        prepare_refs.main(c + ["--source", "fake", "--n-per-profession", "40"])
        plan.main(c)
        generate.main(c + ["--generator", "llama"])
        validate.main(c)

    out = tmp_path / "run"
    planned = {r["id"] for r in read_jsonl(out / "plan.jsonl")}
    assert {r["id"] for r in read_jsonl(out / "raw_llama.jsonl")} == planned
    assert read_jsonl(out / "errors_llama.jsonl") == []
    assert server.status_counts.get(429, 0) > 0 and server.status_counts.get(500, 0) > 0
    body = server.bodies[0]
    assert body["response_format"] == {"type": "json_object"}
    assert isinstance(body["seed"], int) and body["temperature"] == 0.9
    assert sum(r["passed"] for r in read_jsonl(out / "validated.jsonl")) > 0


def test_total_counts_follow_refs_and_all_professions(tmp_path):
    from gen.common import ALL_PROFESSIONS

    config = make_config(tmp_path)
    cfg_dict = yaml.safe_load(open(config, encoding="utf-8"))
    cfg_dict["professions"] = "all"
    cfg_dict["counts"] = {"total": 1000, "overgen": 1.2}
    open(config, "w", encoding="utf-8").write(yaml.safe_dump(cfg_dict))
    cfg = load_config(config)
    assert cfg["professions"] == ALL_PROFESSIONS and len(ALL_PROFESSIONS) == 28
    refs = ([{"profession": "nurse", "gender": "female"}] * 9 + [{"profession": "nurse", "gender": "male"}]
            + [{"profession": p, "gender": "male"} for p in ALL_PROFESSIONS if p != "nurse"] * 3)
    targets = cell_targets(cfg, refs)
    assert sum(targets.values()) == 1000
    n_refs = len(refs)
    for (p, g), n in targets.items():  # every cell within one bio of its exact share of O
        exact = 1000 * sum(r["profession"] == p and r["gender"] == g for r in refs) / n_refs
        assert abs(n - exact) < 1
    assert targets[("surgeon", "female")] == 0


def test_select_pool_skips_excluded_ids(tmp_path):
    config = make_config(tmp_path)
    cfg = run_pipeline(config)
    first = read_jsonl(Path(cfg["output_dir"]) / "pool.jsonl")
    excluded = [r["id"] for r in first[:5]]
    ids_file = tmp_path / "exclude.txt"
    ids_file.write_text("\n".join(excluded) + "\n", encoding="utf-8")
    cfg_dict = yaml.safe_load(open(config, encoding="utf-8"))
    cfg_dict["exclude_ids_file"] = str(ids_file)
    open(config, "w", encoding="utf-8").write(yaml.safe_dump(cfg_dict))
    select_pool.main(["--config", config, "--allow-shortfall"])
    second = {r["id"] for r in read_jsonl(Path(cfg["output_dir"]) / "pool.jsonl")}
    assert not second & set(excluded)


def test_counts_needs_total_or_per_profession(tmp_path):
    config = make_config(tmp_path, counts={"total": 100})  # mock.yaml also has per_profession
    with pytest.raises(SystemExit, match="exactly one of"):
        load_config(config)
