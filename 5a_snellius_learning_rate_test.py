"""Choose the learning rate on the dev set before the main Snellius run.

Trains the original-data-only model (1_original) once per candidate learning rate,
evaluates each on testdata_hug/dev.json (never on the test set), and returns the best
learning rate as a string. Training and evaluation code is reused from the 6a job-array
script, so the settings are identical to the main run apart from the learning rate.

Commands:
    python 5a_snellius_learning_rate_test.py list               candidates and array ids
    python 5a_snellius_learning_rate_test.py submit --dry-run   write the Slurm script only
    python 5a_snellius_learning_rate_test.py submit             write it and sbatch it
    python 5a_snellius_learning_rate_test.py run --task-id 2    one candidate (array job)
    python 5a_snellius_learning_rate_test.py best               print the best rate, e.g. 1e-4
    python 5a_snellius_learning_rate_test.py table              show all results

`best` prints only the learning rate, so it can be used directly:
    LR=$(python 5a_snellius_learning_rate_test.py best)

Selection rule: highest macro-F1 over the 28 professions on dev. Rates within TIE_MARGIN
of the best count as a tie, and the lowest of those wins. The gender gap is NOT used to
choose: tuning towards low bias would influence the outcome the study measures.

Outputs in snellius_runs/lr_sweep/seed<seed>/lr<rate>/ (adapter, predictions, metrics,
config), separate from the main runs.

PAPER NOTE: "The learning rate was selected from {1e-5, 5e-5, 1e-4, 2e-4} by macro-F1 on
the development set (1,598 biographies), using the model trained on the original data
only, and kept fixed for all conditions."
"""
import argparse
import importlib.util
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

BASE_DIR = Path(__file__).resolve().parent
DEV_FILE = BASE_DIR / "testdata_hug" / "dev.json"
OUTPUT_ROOT = BASE_DIR / "snellius_runs" / "lr_sweep"
LEARNING_RATES = ["1e-5", "5e-5", "1e-4", "2e-4"]  # strings: also used as folder names
TIE_MARGIN = 0.005  # macro-F1 difference treated as a tie
SLURM_TIME = "02:30:00"  # 1_original only (12,000 examples, ~1-1.5 h on A100); short = starts sooner


def load_jobarray():
    """Import the 6a job-array script (its name starts with a digit, so not via import)."""
    matches = sorted(BASE_DIR.glob("6a_*jobarray*.py"))
    if len(matches) != 1:
        raise FileNotFoundError(f"Expected one 6a_*jobarray*.py next to this file, found {matches}")
    spec = importlib.util.spec_from_file_location("jobarray", matches[0])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, matches[0].name


def run_dir(args, lr):
    return args.output_root / f"seed{args.seed}" / f"lr{lr}"


def load_dev(ja):
    """Dev records and the label list; the labels must match the training prompts."""
    records = ja.read_jsonl(DEV_FILE)
    for k in ("hard_text", "profession", "gender"):
        if any(k not in r for r in records):
            raise ValueError(f"{DEV_FILE} records need a '{k}' field; run 4b_build_test_eval_set.py")
    _, labels = ja.load_test()  # labels from the test set = labels in the training prompts
    dev_labels = sorted({r["profession"].replace("_", " ") for r in records})
    if dev_labels != sorted(labels):
        raise ValueError("dev.json has different professions than test.json")
    return records, labels


def original_task(ja):
    task = next(t for t in ja.build_tasks() if t["name"] == "1_original")
    return task


# ----------------------------------------------------------------------------- commands

def cmd_list(args):
    for i, lr in enumerate(LEARNING_RATES):
        print(f"{i:3d}  lr={lr:6s} -> {run_dir(args, lr).relative_to(BASE_DIR)}")


def cmd_run(args):
    ja, _ = load_jobarray()
    task_id = args.task_id if args.task_id is not None else int(os.environ["SLURM_ARRAY_TASK_ID"])
    lr = LEARNING_RATES[task_id]
    out_dir = run_dir(args, lr)
    out_dir.mkdir(parents=True, exist_ok=True)

    ja.TRAIN = {**ja.TRAIN, "learning_rate": float(lr)}  # the only setting that differs
    task = {**original_task(ja), "name": f"1_original_lr{lr}"}
    records, labels = load_dev(ja)
    ja.check_same_prompt(task["train_file"], labels)
    print(f"Task {task_id}: learning rate {lr}  ->  {out_dir}", flush=True)

    (out_dir / "config.json").write_text(json.dumps({
        "task": task["name"], "learning_rate": lr, "train_file": str(task["train_file"]),
        "eval_file": str(DEV_FILE), "base_model": args.base_model, "seed": args.seed,
        "train": ja.TRAIN, "eval_batch_size": args.eval_batch_size,
        "slurm_job": os.environ.get("SLURM_JOB_ID"),
    }, indent=2), encoding="utf-8")

    if (out_dir / "adapter" / "adapter_config.json").exists() and not args.overwrite:
        print("[skip] training: adapter exists")
    else:
        t = time.time()
        ja.train(task, out_dir, args)
        print(f"[done] training in {(time.time() - t) / 60:.1f} min", flush=True)

    if (out_dir / "metrics.json").exists() and not args.overwrite:
        print("[skip] evaluation: metrics exist")
    else:
        t = time.time()
        ja.evaluate(task, out_dir, args, records, labels)
        print(f"[done] evaluation on dev in {(time.time() - t) / 60:.1f} min")


def cmd_submit(args):
    ja, ja_name = load_jobarray()
    original_task(ja)  # fail early if the training data is missing
    if not DEV_FILE.is_file():
        raise FileNotFoundError(f"{DEV_FILE} missing; run 4b_build_test_eval_set.py first")
    s = ja.SLURM
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    modules = "\n".join(f"module load {m}" for m in s["modules"])
    script = f"""#!/bin/bash
#SBATCH --job-name=ullm_lr
#SBATCH --partition={s['partition']}
#SBATCH --gpus={s['gpus']}
#SBATCH --cpus-per-task={s['cpus']}
#SBATCH --time={SLURM_TIME}
#SBATCH --array=0-{len(LEARNING_RATES) - 1}
#SBATCH --output={log_dir}/%x_%A_%a.out

module purge
{modules}
source {s['venv']}/bin/activate
export HF_HOME={s['hf_home']}
export TOKENIZERS_PARALLELISM=false

cd {BASE_DIR}
python {Path(__file__).name} run --seed {args.seed} --output-root {args.output_root} \\
    --base-model {args.base_model} --eval-batch-size {args.eval_batch_size}
"""
    path = BASE_DIR / "5a_snellius_learning_rate_test.slurm"
    path.write_text(script, encoding="utf-8", newline="\n")
    print(f"Wrote {path.name}: {len(LEARNING_RATES)} learning rates {LEARNING_RATES} "
          f"(training code from {ja_name})")
    if args.dry_run:
        print(script)
        return
    subprocess.run(["sbatch", str(path)], check=True)


def collect(args):
    results, missing = [], []
    for lr in LEARNING_RATES:
        f = run_dir(args, lr) / "metrics.json"
        if not f.is_file():
            missing.append(lr)
            continue
        m = json.loads(f.read_text(encoding="utf-8"))
        results.append({"lr": lr, "macro_f1": m["macro_f1_labels"], "accuracy": m["accuracy"],
                        "unparsed": m["unparsed"], "n": m["n"], "tpr_gap_rms": m["tpr_gap_rms"]})
    return results, missing


def best_learning_rate(args):
    """Return the best learning rate as a string, e.g. '1e-4'."""
    results, missing = collect(args)
    if missing:
        raise RuntimeError(f"No dev results yet for learning rate(s) {missing}; "
                           f"run (or resubmit) those tasks first")
    top = max(r["macro_f1"] for r in results)
    tied = [r for r in results if top - r["macro_f1"] <= TIE_MARGIN]
    return min(tied, key=lambda r: float(r["lr"]))["lr"]


def cmd_best(args):
    try:
        print(best_learning_rate(args))
    except RuntimeError as e:
        sys.exit(str(e))


def cmd_table(args):
    results, missing = collect(args)
    print(f"{'lr':>6}  {'macro_f1':>8}  {'accuracy':>8}  {'unparsed':>8}  {'tpr_gap_rms':>11}")
    for r in results:
        print(f"{r['lr']:>6}  {r['macro_f1']:8.4f}  {r['accuracy']:8.4f}  {r['unparsed']:8d}  "
              f"{r['tpr_gap_rms']:11.4f}")
    if missing:
        print(f"missing: {missing}")
    else:
        print(f"best (macro-F1, ties within {TIE_MARGIN} -> lower rate): {best_learning_rate(args)}")
    print("Note: tpr_gap_rms is shown for information only and is not used to choose.")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["list", "submit", "run", "best", "table"])
    parser.add_argument("--task-id", type=int, help="run: array id (default: $SLURM_ARRAY_TASK_ID)")
    parser.add_argument("--dry-run", action="store_true", help="submit: write the script, don't sbatch")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--base-model", default="meta-llama/Llama-3.1-8B-Instruct")
    parser.add_argument("--output-root", type=Path, default=OUTPUT_ROOT)
    parser.add_argument("--eval-batch-size", type=int, default=32)
    parser.add_argument("--overwrite", action="store_true", help="run: retrain and re-evaluate")
    args = parser.parse_args()
    {"list": cmd_list, "submit": cmd_submit, "run": cmd_run,
     "best": cmd_best, "table": cmd_table}[args.command](args)


if __name__ == "__main__":
    main()
