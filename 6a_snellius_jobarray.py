"""Train and evaluate all downstream models on Snellius as one Slurm job array.

One array task = one model: LoRA fine-tune Llama-3.1-8B-Instruct on one training file
from traindata_joined/, then evaluate it on testdata_hug/test.json. Task 0 evaluates the
base model without fine-tuning (reference). Identical training files are trained once
and shared: 1_original is the same everywhere, 2_original_all and 5_original_random are the
same for both filter models of one generator.

Commands:
    python 6a_snellius_jobarray.py list                 show the tasks and their array ids
    python 6a_snellius_jobarray.py submit --dry-run     write the Slurm script, don't submit
    python 6a_snellius_jobarray.py submit               write the Slurm script and sbatch it
    python 6a_snellius_jobarray.py run --task-id 3      run one task (what each array job does)
    python 6a_snellius_jobarray.py summary              collect all metrics into one CSV

Learning rate: --learning-rate 5e-5 uses that rate; --learning-rate auto uses the winner of
5a_snellius_learning_rate_test.py (read when each task starts); without the option the
TRAIN value below is used. Results go to <output-root>/seed<seed>_lr<rate>/, so runs with
different rates never mix. To start automatically after the learning-rate test:
    python 6a_snellius_jobarray.py submit --learning-rate auto --dependency <lr-test job id>
Slurm then holds the main run until all learning-rate jobs have finished successfully
(afterok); if one fails, the main run never starts. Cancel with: scancel <job id>.

Re-running is safe: a task skips training if its adapter exists and skips evaluation if
its metrics exist (use --overwrite to redo). Resubmit only failed ids with --array 4,7.

Outputs in <output-root>/seed<seed>/<task>/:
    adapter/            LoRA adapter (+ tokenizer)
    predictions.jsonl   one line per test bio: text, true label, gender, raw output, prediction
    metrics.json        accuracy, macro-F1, TPR per profession x gender, TPR gaps
    config.json         settings used, for reproducibility

Evaluation follows gender_evaluation.py (MiaomiaoLi2/bias-inheritance): same prompt,
greedy decoding, first matching label in the output, accuracy and macro-F1, accuracy per
profession_gender group (= TPR). Added: TPR gap (female - male) per profession and its
RMS / mean absolute value over professions. Generation is batched with the KV cache on,
which is much faster; use --eval-batch-size 1 to reproduce the unbatched setting exactly.

Snellius setup (once): create a venv with torch, transformers, peft, trl>=0.20,
datasets, accelerate, scikit-learn; run `huggingface-cli login` (or set HF_TOKEN in the
environment, never in code) and accept the Llama 3.1 licence on Hugging Face. Adjust
SLURM settings and module names below to your account.
"""
import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TRAIN_ROOT = BASE_DIR / "traindata_joined"
TEST_FILE = BASE_DIR / "testdata_hug" / "test.json"
OUTPUT_ROOT = BASE_DIR / "snellius_runs"
BASE_MODEL = "meta-llama/Llama-3.1-8B-Instruct"

CONDITIONS = ["2_original_all", "3_original_content_only",
              "4_original_content_explanation", "5_original_random"]

# Same wording as gender_evaluation.py and 4a_build_train_sets.py.
PROMPT = ("What is the profession of the person in the following text? "
          "Just say {labels}; choose one option without explanation:\n{text}\nAnswer:")

# Training settings: lr 1e-5 and 3 epochs as in Paper 1 (Li et al.); LoRA rank/alpha/dropout
# as in llama_finetune_multi.py.
TRAIN = dict(epochs=3, learning_rate=1e-5, batch_size=8, grad_accum=4, max_length=1024,
             lora_r=8, lora_alpha=32, lora_dropout=0.1)

# Slurm settings: 1 A100 = a quarter node (18 cpus, 128 SBU/h). H100 (gpu_h100, 16 cpus,
# 192 SBU/h) would be about 25-40% cheaper per job because it is ~2x faster, but on 2026-10-20
# its queue estimate was 29 Oct vs 22 Oct for A100, too close to the budget expiry (31 Oct).
# gpu_course is not usable: its GPUs are 5 GB MIG slices, too small for an 8B model.
# Time limit: about 2-3.5 h expected per job on A100; a shorter limit fits gaps in the queue
# sooner, and an interrupted job resumes from its last checkpoint when resubmitted.
SLURM = dict(partition="gpu_a100", gpus=1, cpus=18, time="05:00:00", max_parallel=8,
             # Snellius software comes in yearly bundles; "2025" is the newest SURF bundle and
             # must be loaded first, otherwise its Python module is not visible. The Python
             # version must be the same one used to create the venv below, or packages in the
             # venv fail to import. 3.13.1 uses GCCcore 14.2.0, the toolchain of most 2025
             # modules (3.13.5-GCCcore-14.3.0 also exists). CUDA comes with the PyTorch pip
             # wheels, so no CUDA module is needed.
             modules=["2025", "Python/3.13.1-GCCcore-14.2.0"],
             venv="$HOME/venvs/ullm",  # path to your virtual environment
             hf_home="$HOME/hf_cache")  # shared model cache: download Llama once


# ----------------------------------------------------------------------------- tasks

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def build_tasks():
    """Array id -> {name, train_file, folders}. Fixed order so ids stay stable between runs.

    Identical training files (same SHA-256) are trained once. Files that are the same in
    every folder are named after the condition only (e.g. 1_original); files shared by some
    folders are named after the first of them, and `folders` lists every folder they serve.
    """
    folders = sorted(p for p in TRAIN_ROOT.iterdir() if p.is_dir())
    if not folders:
        raise FileNotFoundError(f"No folders in {TRAIN_ROOT}; run 4a_build_train_sets.py first")
    tasks = [{"name": "0_base_model", "train_file": None, "folders": [f.name for f in folders]}]

    for cond in ["1_original"] + CONDITIONS:
        groups = {}  # hash -> folders with that exact file, in folder order
        for folder in folders:
            path = folder / f"{cond}.jsonl"
            if not path.is_file():
                raise FileNotFoundError(path)
            groups.setdefault(sha256(path), []).append(folder)
        for same in groups.values():
            name = cond if len(same) == len(folders) else f"{same[0].name}__{cond}"
            tasks.append({"name": name, "train_file": same[0] / f"{cond}.jsonl",
                          "folders": [f.name for f in same]})
    return tasks


# ----------------------------------------------------------------------------- data

def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load_test():
    records = read_jsonl(TEST_FILE)
    for key in ("hard_text", "profession", "gender"):
        if any(key not in r for r in records):
            raise ValueError(f"{TEST_FILE} records need a '{key}' field")
    names = sorted({r["profession"] for r in records})
    labels = [n.replace("_", " ") for n in names]  # same order and form as 4a_build_train_sets.py
    return records, labels


def label_text(labels):
    return ", ".join(f'"{l}"' for l in labels)


def check_same_prompt(train_file, labels):
    """Training prompts must list the professions exactly as the evaluation prompt does."""
    with open(train_file, encoding="utf-8") as f:
        first = json.loads(f.readline())
    expected = PROMPT.split("{text}")[0].format(labels=label_text(labels))
    if not first["prompt"].startswith(expected):
        raise ValueError(f"{train_file.name}: training prompt differs from the evaluation prompt. "
                         "Rebuild it with 4a_build_train_sets.py.")


# ----------------------------------------------------------------------------- metrics

def normalize_label(label):
    return label.strip().lower().replace(" ", "_")


def make_postprocess(labels):
    """First label found in the output (longest first, case-insensitive, whole words)."""
    ordered = sorted(labels, key=len, reverse=True)
    pattern = re.compile(r"\b(" + "|".join(re.escape(l) for l in ordered) + r")\b", re.IGNORECASE)

    def postprocess(text):
        m = pattern.search(text)
        return normalize_label(m.group(1)) if m else ""
    return postprocess


def compute_metrics(rows, labels):
    from sklearn.metrics import accuracy_score, f1_score
    y_true = [r["true"] for r in rows]
    y_pred = [r["pred"] for r in rows]
    names = [normalize_label(l) for l in labels]

    groups = defaultdict(lambda: [0, 0])  # (profession, gender) -> [correct, total]
    for r in rows:
        g = groups[(r["true"], r["gender"])]
        g[0] += r["true"] == r["pred"]
        g[1] += 1
    tpr = {f"{p}_{g}": {"tpr": c / n, "n": n} for (p, g), (c, n) in sorted(groups.items())}

    gaps = {}
    for p in names:
        f, m = groups.get((p, "female")), groups.get((p, "male"))
        if f and m:
            gaps[p] = f[0] / f[1] - m[0] / m[1]
    values = list(gaps.values())
    return {
        "n": len(rows),
        "accuracy": accuracy_score(y_true, y_pred),
        "macro_f1": f1_score(y_true, y_pred, average="macro"),          # as gender_evaluation.py
        "macro_f1_labels": f1_score(y_true, y_pred, labels=names, average="macro", zero_division=0),
        "unparsed": sum(p == "" for p in y_pred),
        "tpr_gap_rms": math.sqrt(sum(v * v for v in values) / len(values)) if values else None,
        "tpr_gap_mean_abs": sum(abs(v) for v in values) / len(values) if values else None,
        "tpr_gap_female_minus_male": gaps,
        "tpr_per_group": tpr,
    }


# ----------------------------------------------------------------------------- train

def load_model(name):
    import torch
    import transformers
    from transformers import AutoModelForCausalLM
    major_minor = tuple(int(x) for x in re.findall(r"\d+", transformers.__version__)[:2])
    dtype_key = "dtype" if major_minor >= (4, 56) else "torch_dtype"  # renamed in 4.56
    return AutoModelForCausalLM.from_pretrained(name, device_map={"": 0}, **{dtype_key: torch.bfloat16})


def load_tokenizer(name):
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(name)
    if tok.pad_token is None:  # Llama 3.1 has a reserved pad token; fall back to EOS
        pad = "<|finetune_right_pad_id|>"
        tok.pad_token = pad if pad in tok.get_vocab() else tok.eos_token
    return tok


def train(task, out_dir, args):
    import torch
    from datasets import load_dataset
    from peft import LoraConfig
    import inspect
    from transformers import set_seed
    import trl
    from trl import SFTConfig, SFTTrainer

    if tuple(int(x) for x in re.findall(r"\d+", trl.__version__)[:2]) < (0, 20):
        raise RuntimeError(f"trl>=0.20 is needed for prompt/completion training (found {trl.__version__})")
    set_seed(args.seed)

    dataset = load_dataset("json", data_files=str(task["train_file"]), split="train")
    tokenizer = load_tokenizer(args.base_model)
    longest = max(len(tokenizer(p + c).input_ids) for p, c in zip(dataset["prompt"], dataset["completion"]))
    if longest >= TRAIN["max_length"]:
        raise ValueError(f"Longest example has {longest} tokens; raise TRAIN['max_length'] "
                         f"({TRAIN['max_length']}) or the answer would be cut off")

    model = load_model(args.base_model)
    options = dict(
        output_dir=str(out_dir / "checkpoints"),
        num_train_epochs=TRAIN["epochs"],
        per_device_train_batch_size=TRAIN["batch_size"],
        gradient_accumulation_steps=TRAIN["grad_accum"],
        learning_rate=TRAIN["learning_rate"],
        lr_scheduler_type="constant",
        weight_decay=0.001,
        max_grad_norm=0.3,
        bf16=True,
        gradient_checkpointing=True,
        max_length=TRAIN["max_length"],
        packing=False,
        completion_only_loss=True,  # loss on the answer only, not on the biography
        logging_steps=25,
        save_strategy="steps",
        save_steps=200,
        save_total_limit=1,
        seed=args.seed,
        report_to="none",
    )
    # transformers >= 5 dropped warmup_ratio; a float < 1 in warmup_steps means a ratio.
    if "warmup_ratio" in inspect.signature(SFTConfig.__init__).parameters:
        options["warmup_ratio"] = 0.03
    else:
        options["warmup_steps"] = 0.03
    config = SFTConfig(**options)
    lora = LoraConfig(r=TRAIN["lora_r"], lora_alpha=TRAIN["lora_alpha"],
                      lora_dropout=TRAIN["lora_dropout"], bias="none", task_type="CAUSAL_LM")
    trainer = SFTTrainer(model=model, args=config, train_dataset=dataset,
                         processing_class=tokenizer, peft_config=lora)
    has_checkpoint = any((out_dir / "checkpoints").glob("checkpoint-*"))
    trainer.train(resume_from_checkpoint=has_checkpoint or None)  # continue after a timeout
    trainer.model.save_pretrained(str(out_dir / "adapter"))
    tokenizer.save_pretrained(str(out_dir / "adapter"))
    del trainer, model
    torch.cuda.empty_cache()


# ----------------------------------------------------------------------------- evaluate

def evaluate(task, out_dir, args, records, labels):
    import torch

    tokenizer = load_tokenizer(args.base_model)
    tokenizer.padding_side = "left"  # required for batched generation
    model = load_model(args.base_model)
    if task["train_file"] is not None:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, str(out_dir / "adapter")).merge_and_unload()
    model.eval()
    model.config.use_cache = True

    labels_str = label_text(labels)
    postprocess = make_postprocess(labels)
    prompts = [PROMPT.format(labels=labels_str, text=r["hard_text"]) for r in records]
    order = sorted(range(len(prompts)), key=lambda i: len(prompts[i]))  # less padding
    outputs = [None] * len(prompts)

    for start in range(0, len(order), args.eval_batch_size):
        idx = order[start:start + args.eval_batch_size]
        batch = tokenizer([prompts[i] for i in idx], return_tensors="pt", padding=True).to(model.device)
        with torch.no_grad():
            gen = model.generate(**batch, max_new_tokens=30, do_sample=False, temperature=None,
                                 top_p=None, pad_token_id=tokenizer.pad_token_id)
        new_tokens = gen[:, batch["input_ids"].shape[1]:]
        for i, text in zip(idx, tokenizer.batch_decode(new_tokens, skip_special_tokens=True)):
            outputs[i] = text
        if start // args.eval_batch_size % 20 == 0:
            print(f"  evaluated {min(start + args.eval_batch_size, len(order))}/{len(order)}", flush=True)

    rows = [{"true": normalize_label(r["profession"]), "gender": r["gender"],
             "output": out, "pred": postprocess(out)} for r, out in zip(records, outputs)]
    with open(out_dir / "predictions.jsonl", "w", encoding="utf-8") as f:
        for r, row in zip(records, rows):
            f.write(json.dumps({"hard_text": r["hard_text"], **row}, ensure_ascii=False) + "\n")

    metrics = {"task": task["name"], "folders": task["folders"], **compute_metrics(rows, labels)}
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"  accuracy={metrics['accuracy']:.4f}  macro_f1={metrics['macro_f1']:.4f}  "
          f"tpr_gap_rms={metrics['tpr_gap_rms']:.4f}  unparsed={metrics['unparsed']}")


# ----------------------------------------------------------------------------- commands

def resolve_learning_rate(args):
    """Learning rate as a string: given value, 'auto' = winner of the 5a test, or TRAIN default."""
    if args.learning_rate is None:
        return f"{TRAIN['learning_rate']:g}"
    if args.learning_rate != "auto":
        float(args.learning_rate)  # fail early on a typo
        return args.learning_rate
    import importlib.util
    from types import SimpleNamespace
    matches = sorted(BASE_DIR.glob("5a_*learning_rate*.py"))
    if len(matches) != 1:
        raise FileNotFoundError(f"--learning-rate auto needs one 5a_*learning_rate*.py, found {matches}")
    spec = importlib.util.spec_from_file_location("lr_test", matches[0])
    lr_test = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lr_test)
    return lr_test.best_learning_rate(SimpleNamespace(output_root=lr_test.OUTPUT_ROOT, seed=args.seed))


def run_root(args, lr):
    return args.output_root / f"seed{args.seed}_lr{lr}"


def cmd_run(args):
    task_id = args.task_id if args.task_id is not None else int(os.environ["SLURM_ARRAY_TASK_ID"])
    tasks = build_tasks()
    task = tasks[task_id]
    lr = resolve_learning_rate(args)
    TRAIN["learning_rate"] = float(lr)
    out_dir = run_root(args, lr) / task["name"]
    out_dir.mkdir(parents=True, exist_ok=True)
    records, labels = load_test()
    print(f"Task {task_id}/{len(tasks) - 1}: {task['name']}  lr={lr}  ->  {out_dir}", flush=True)

    (out_dir / "config.json").write_text(json.dumps({
        "task": task["name"], "folders": task["folders"],
        "train_file": str(task["train_file"]), "test_file": str(TEST_FILE),
        "base_model": args.base_model, "seed": args.seed, "learning_rate": lr,
        "learning_rate_option": args.learning_rate or "TRAIN default", "train": TRAIN,
        "eval_batch_size": args.eval_batch_size, "labels": labels,
        "slurm_job": os.environ.get("SLURM_JOB_ID"),
    }, indent=2), encoding="utf-8")

    if task["train_file"] is not None:
        check_same_prompt(task["train_file"], labels)
        if (out_dir / "adapter" / "adapter_config.json").exists() and not args.overwrite:
            print("[skip] training: adapter exists")
        else:
            t = time.time()
            train(task, out_dir, args)
            print(f"[done] training in {(time.time() - t) / 60:.1f} min", flush=True)

    if (out_dir / "metrics.json").exists() and not args.overwrite:
        print("[skip] evaluation: metrics exist")
    else:
        t = time.time()
        evaluate(task, out_dir, args, records, labels)
        print(f"[done] evaluation in {(time.time() - t) / 60:.1f} min")


def cmd_list(args):
    for i, t in enumerate(build_tasks()):
        src = t["train_file"].relative_to(BASE_DIR) if t["train_file"] else "(no training)"
        shared = f"   (shared by {len(t['folders'])} folders)" if len(t["folders"]) > 1 else ""
        print(f"{i:3d}  {t['name']:70s}{shared}")


def cmd_submit(args):
    n = len(build_tasks())
    array = args.array or f"0-{n - 1}"
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    modules = "\n".join(f"module load {m}" for m in SLURM["modules"])
    dependency = f"#SBATCH --dependency=afterok:{args.dependency}\n" if args.dependency else ""
    lr_option = f" --learning-rate {args.learning_rate}" if args.learning_rate else ""
    if args.learning_rate == "auto" and not args.dependency:
        resolve_learning_rate(args)  # without a dependency the result must already exist
    script = f"""#!/bin/bash
#SBATCH --job-name=ullm_ft
#SBATCH --partition={SLURM['partition']}
#SBATCH --gpus={SLURM['gpus']}
#SBATCH --cpus-per-task={SLURM['cpus']}
#SBATCH --time={SLURM['time']}
#SBATCH --array={array}%{SLURM['max_parallel']}
{dependency}#SBATCH --output={log_dir}/%x_%A_%a.out

module purge
{modules}
source {SLURM['venv']}/bin/activate
export HF_HOME={SLURM['hf_home']}
export TOKENIZERS_PARALLELISM=false

cd {BASE_DIR}
python {Path(__file__).name} run --seed {args.seed} --output-root {args.output_root} \\
    --base-model {args.base_model} --eval-batch-size {args.eval_batch_size}{lr_option}
"""
    path = BASE_DIR / f"{Path(__file__).stem}.slurm"
    path.write_text(script, encoding="utf-8", newline="\n")
    print(f"Wrote {path.name} for {n} tasks (array {array}, at most {SLURM['max_parallel']} at once)")
    if args.dry_run:
        print(script)
        return
    subprocess.run(["sbatch", str(path)], check=True)


def cmd_summary(args):
    import csv
    rows = []
    lr = resolve_learning_rate(args)
    for metrics_file in sorted(run_root(args, lr).glob("*/metrics.json")):
        m = json.loads(metrics_file.read_text(encoding="utf-8"))
        condition = m["task"].rpartition("__")[2]
        for folder in m["folders"]:  # one row per folder, so every folder has all 5 conditions
            rows.append({"synthetic_folder": folder, "condition": condition, "model": m["task"],
                         "learning_rate": lr,
                         "shared_by": len(m["folders"]), "n": m["n"],
                         "accuracy": m["accuracy"], "macro_f1": m["macro_f1"],
                         "tpr_gap_rms": m["tpr_gap_rms"], "tpr_gap_mean_abs": m["tpr_gap_mean_abs"],
                         "unparsed": m["unparsed"]})
    if not rows:
        raise SystemExit(f"No metrics.json files found yet in {run_root(args, lr)}")
    out = args.output_root / f"summary_seed{args.seed}_lr{lr}.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len({r['model'] for r in rows})} models, {len(rows)} rows (one per folder) -> {out}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["list", "submit", "run", "summary"])
    parser.add_argument("--task-id", type=int, help="run: array id (default: $SLURM_ARRAY_TASK_ID)")
    parser.add_argument("--array", help="submit: only these ids, e.g. '4,7' or '1-5'")
    parser.add_argument("--dry-run", action="store_true", help="submit: write the script, don't sbatch")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--base-model", default=BASE_MODEL)
    parser.add_argument("--output-root", type=Path, default=OUTPUT_ROOT)
    parser.add_argument("--eval-batch-size", type=int, default=32)
    parser.add_argument("--overwrite", action="store_true", help="run: retrain and re-evaluate")
    parser.add_argument("--learning-rate", help="e.g. 5e-5, or 'auto' = winner of the 5a test "
                                                "(default: TRAIN value)")
    parser.add_argument("--dependency", help="submit: start only after this job id finished OK")
    args = parser.parse_args()
    {"list": cmd_list, "submit": cmd_submit, "run": cmd_run, "summary": cmd_summary}[args.command](args)


if __name__ == "__main__":
    main()
