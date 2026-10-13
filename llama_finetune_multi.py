import gc
import inspect
import re
from importlib.metadata import version
from pathlib import Path

import fire
import torch
from datasets import load_dataset
from peft import LoraConfig, prepare_model_for_kbit_training
from transformers import (
    AutoTokenizer,
    BitsAndBytesConfig,
    LlamaForCausalLM,
    TrainingArguments,
)
from trl import SFTTrainer

try:
    from trl import SFTConfig
except ImportError:  # very old trl
    SFTConfig = None


def version_tuple(package: str) -> tuple[int, ...]:
    match = re.match(r"\d+(?:\.\d+)*", version(package))
    if not match:
        return (0,)
    return tuple(int(part) for part in match.group(0).split("."))


def check_training_dependencies() -> None:
    if version_tuple("accelerate") < (1, 3, 0):
        raise RuntimeError(
            "accelerate>=1.3.0 is required by the installed transformers Trainer. "
            "Upgrade it in the active environment: pip install -U 'accelerate>=1.3.0'"
        )


def train_one(
    base_model: str,
    data_file: Path,
    adapter_dir: Path,
    run_dir: Path,
    epochs: int,
    learning_rate: float,
    max_seq_length: int,
    batch_size: int,
    grad_accum: int,
    text_field: str,
) -> None:
    dataset = load_dataset("csv", data_files=str(data_file), split="train")
    if text_field not in dataset.column_names:
        raise ValueError(
            f"{data_file.name} has no '{text_field}' column; found {dataset.column_names}. "
            "Pass --text_field=<column> to pick the right one."
        )

    quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=False,
    )

    # Everything on GPU 0 (16 GB laptop GPU): no CPU offload, no max_memory cap needed.
    model = LlamaForCausalLM.from_pretrained(
        base_model,
        quantization_config=quant_config,
        device_map={"": 0},
        torch_dtype=torch.bfloat16,
    )
    model.config.use_cache = False
    model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=True)

    tokenizer = AutoTokenizer.from_pretrained(base_model)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    peft_params = LoraConfig(
        lora_alpha=32, lora_dropout=0.1, r=8, bias="none", task_type="CAUSAL_LM",
    )
    args_cls = SFTConfig if SFTConfig is not None else TrainingArguments
    arg_params = set(inspect.signature(args_cls.__init__).parameters)

    arg_kwargs = dict(
        output_dir=str(run_dir),
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=grad_accum,
        gradient_checkpointing=True,
        bf16=True,
        optim="paged_adamw_32bit",
        save_steps=100,
        logging_steps=25,
        learning_rate=learning_rate,
        weight_decay=0.001,
        max_grad_norm=0.3,
        max_steps=-1,
        group_by_length=True,
        lr_scheduler_type="constant",
        report_to="tensorboard",
    )
    # transformers >= 5 dropped warmup_ratio; a float < 1 in warmup_steps means a ratio.
    if "warmup_ratio" in arg_params:
        arg_kwargs["warmup_ratio"] = 0.03
    else:
        arg_kwargs["warmup_steps"] = 0.03

    # trl >= 0.9 keeps the SFT options in SFTConfig; older versions take them on the trainer.
    sft_options = {"dataset_text_field": text_field, "packing": False}
    length_key = "max_length" if "max_length" in arg_params else "max_seq_length"
    sft_options[length_key] = max_seq_length

    trainer_kwargs = {"model": model, "train_dataset": dataset, "peft_config": peft_params}
    if SFTConfig is not None and "dataset_text_field" in arg_params:
        arg_kwargs.update(sft_options)
    else:
        trainer_kwargs.update(sft_options)

    dropped = [k for k in arg_kwargs if k not in arg_params]
    if dropped:
        print(f"[warn] ignoring options not supported by this version: {dropped}")
    trainer_kwargs["args"] = args_cls(**{k: v for k, v in arg_kwargs.items() if k in arg_params})

    if "processing_class" in inspect.signature(SFTTrainer.__init__).parameters:
        trainer_kwargs["processing_class"] = tokenizer
    else:
        trainer_kwargs["tokenizer"] = tokenizer

    trainer = SFTTrainer(**trainer_kwargs)
    try:
        trainer.train()
        trainer.model.save_pretrained(str(adapter_dir))
        tokenizer.save_pretrained(str(adapter_dir))
    finally:
        # Free VRAM so the next dataset starts from a clean slate.
        del trainer, model
        gc.collect()
        torch.cuda.empty_cache()


def run(
    base_model: str = "meta-llama/Llama-3.1-8B-Instruct",
    data_dir: str = "train_data",
    output_root: str = "artifacts",
    pattern: str = "*.csv",
    epochs: int = 3,
    learning_rate: float = 2e-4,
    max_seq_length: int = 1024,
    batch_size: int = 2,
    grad_accum: int = 16,
    text_field: str = "hard_text",
    overwrite: bool = False,
) -> None:
    """Train one LoRA adapter per CSV file in data_dir, sequentially."""
    check_training_dependencies()

    files = sorted(Path(data_dir).glob(pattern))
    if not files:
        raise FileNotFoundError(f"No files matching {pattern!r} in {data_dir!r}")
    print(f"Found {len(files)} dataset(s): {[f.name for f in files]}")

    for data_file in files:
        name = data_file.stem
        adapter_dir = Path(output_root) / "models" / name
        run_dir = Path(output_root) / "runs" / name

        if (adapter_dir / "adapter_config.json").exists() and not overwrite:
            print(f"[skip] {name}: adapter already exists at {adapter_dir}")
            continue

        print(f"\n=== Training '{name}' on {data_file} ===")
        train_one(
            base_model=base_model,
            data_file=data_file,
            adapter_dir=adapter_dir,
            run_dir=run_dir,
            epochs=epochs,
            learning_rate=learning_rate,
            max_seq_length=max_seq_length,
            batch_size=batch_size,
            grad_accum=grad_accum,
            text_field=text_field,
        )
        print(f"[done] {name} -> {adapter_dir}")


if __name__ == "__main__":
    fire.Fire(run)
