import os
from dataclasses import dataclass
from functools import partial
from typing import Any, Callable, Literal, Sequence

import torch
from lightning import Fabric, seed_everything
from lightning.fabric.loggers import TensorBoardLogger
from lightning.fabric.strategies import DDPStrategy
from lora_pytorch import LoRA
from torch import Tensor
from torch.nn.utils import clip_grad_value_
from torch.optim.lr_scheduler import LambdaLR, LRScheduler
from torch.utils.data import DataLoader
from tqdm import tqdm

from openelm_pytorch.openelm import OpenELM
from openelm_pytorch.tokenizer import Tokenizer
from openelm_pytorch.utils import get_torch_device

from ..generate_text import PROMPT, generate
from .gutenberg import GutenbergEBookDataset

torch.set_float32_matmul_precision("medium")


def collate_fn(
    batch: Sequence[str],
    tokenizer: Tokenizer,
    max_length: int = 1024,
    device: torch.device | str | None = None,
) -> tuple[Tensor, Tensor]:
    token_ids = tokenizer(batch, device=device)[:, : max_length + 1]
    x = token_ids[:, :-1]
    y = token_ids[:, 1:]
    return x, y


def loss_fn(logits: Tensor, target_ids: Tensor) -> Tensor:
    return torch.nn.functional.cross_entropy(
        logits.view(-1, logits.size(-1)), target_ids.view(-1)
    )


@dataclass
class TrainingState:
    fabric: Fabric
    model: LoRA[OpenELM]
    optimizer: torch.optim.Optimizer
    lr_scheduler: LRScheduler
    callbacks: Sequence[Callable[["TrainingState", float], None]] = ()

    current_step: int = 0
    current_epoch: int = 0
    accumulate_grad_batches: int = 1
    monitor: str = "val_loss"
    monitor_mode: Literal["min", "max"] = "min"


@dataclass
class ModelCheckpoint:
    state_dict: dict[str, Tensor]
    optimizer_state: dict[str, Tensor]
    current_step: int
    current_epoch: int

    @classmethod
    def from_training_state(cls, state: TrainingState) -> "ModelCheckpoint":
        return cls(
            state_dict=state.model.state_dict(),
            optimizer_state=state.optimizer.state_dict(),
            current_step=state.current_step,
            current_epoch=state.current_epoch,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "state_dict": self.state_dict,
            "optimizer_state": self.optimizer_state,
            "current_step": self.current_step,
            "current_epoch": self.current_epoch,
        }

    def save(self, path: str) -> None:
        torch.save(self.to_dict(), path)

    @classmethod
    def load(cls, path: str) -> "ModelCheckpoint":
        checkpoint_dict = torch.load(path)
        return cls(**checkpoint_dict)


class CheckpointCallback:
    def __init__(
        self, save_dir: str, name: str = "checkpoint_epoch-{epoch:03d}.pt"
    ) -> None:
        self.save_dir = save_dir
        self.name = name
        self.best_path: str | None = None
        self.best_loss: float | None = None

    def __call__(self, state: TrainingState, loss: float) -> None:
        if self.best_loss is None:
            self.best_loss = loss

        fabric = state.fabric
        # 'local_rank == 0' means this only happens for the main process
        if fabric.local_rank == 0 and loss <= self.best_loss:
            checkpoint = ModelCheckpoint.from_training_state(state)
            self.best_loss = loss
            if self.best_path is not None:
                os.remove(self.best_path)
            self.best_path = os.path.join(
                self.save_dir, self.name.format(epoch=state.current_epoch)
            )
            torch.save(checkpoint, self.best_path)

        # All processes wait for main to finish saving the checkpoint.
        fabric.barrier()


def train_one_epoch(
    state: TrainingState,
    train_dataloader: DataLoader,
    val_dataloader: DataLoader,
    log_frequency: int = 25,
) -> None:
    state.current_epoch += 1
    fabric, model, optimizer, scheduler = (
        state.fabric,
        state.model,
        state.optimizer,
        state.lr_scheduler,
    )
    is_main_process = fabric.local_rank == 0
    is_training = model.training
    model.train()

    with tqdm(
        desc=f"Ep: {state.current_epoch}", disable=(not is_main_process)
    ) as progbar:
        train_loss, val_loss = 0.0, 0.0
        for input_ids, target_ids in train_dataloader:
            state.current_step += 1
            accumulating = state.current_step % state.accumulate_grad_batches != 0
            with fabric.no_backward_sync(model, enabled=accumulating):  # type: ignore
                logits = model.forward(input_ids)
                loss = loss_fn(logits, target_ids)
                fabric.backward(loss)

            if not accumulating:
                clip_grad_value_(model.parameters(), 1.0)
                optimizer.step()
                optimizer.zero_grad()
                scheduler.step()

            if state.current_step % log_frequency == 0:
                fabric.log("loss", loss, step=state.current_step)
                train_loss = loss.item()
                progbar.set_postfix_str(f"loss={train_loss:.4f}", refresh=False)
            progbar.update(1)

        model.eval()
        val_progbar = tqdm(desc="val", position=1, leave=False)
        for i, (input_ids, target_ids) in enumerate(val_dataloader):
            with torch.inference_mode():
                logits = model.forward(inputs=input_ids, labels=target_ids)
            loss = loss_fn(logits, target_ids)
            val_loss = (val_loss * i + loss.item()) / (i + 1)

            if i % log_frequency == 0:
                val_progbar.set_postfix_str(f"val_loss={val_loss:.4f}", refresh=False)
            val_progbar.update(1)
            progbar.update(1)

        fabric.log("val_loss", val_loss, step=state.current_step)
        val_progbar.close()
        progbar.set_postfix_str(
            f"loss={train_loss:.4f}, val_loss={val_loss:.4f}", refresh=False
        )

        for callback in state.callbacks:
            callback(state, val_loss)

        # Return model to its original training state
        model.train(mode=is_training)


def train(
    model: LoRA[OpenELM],
    train_dataloader: DataLoader,
    val_dataloader: DataLoader,
    accelerator: str = "auto",
    precision: str | None = None,
    epochs: int = 10,
    lr: float = 1e-4,
    lr_warmup_steps: int = 250,
    accumulate_grad_batches: int = 1,
    log_frequency: int = 25,
):
    if precision is None:
        if torch.cuda.is_available():
            # use bfloat16 if supported
            version, _ = torch.cuda.get_device_capability()
            precision = "bf16-mixed" if version >= 8 else "16-mixed"
        else:
            precision = "32-true"

    logger = TensorBoardLogger(root_dir="./")
    fabric = Fabric(
        accelerator=accelerator,
        strategy=DDPStrategy(find_unused_parameters=True),
        precision=precision,  # type: ignore
        loggers=[logger],
    )
    fabric.launch()
    print(f"Experiment version: {logger.version}")
    print("-" * 40)

    # Setup with fabric.
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, eps=1e-6)
    model, optimizer = fabric.setup(model, optimizer)
    lr_scheduler = LambdaLR(
        optimizer, lambda step: min(1.0, step / lr_warmup_steps + 1e-8)
    )
    train_dataloader, val_dataloader = fabric.setup_dataloaders(
        train_dataloader, val_dataloader
    )
    # Construct a training state and run the training loop.
    state = TrainingState(
        fabric=fabric,
        model=model,
        optimizer=optimizer,
        lr_scheduler=lr_scheduler,
        accumulate_grad_batches=accumulate_grad_batches,
        callbacks=[CheckpointCallback(save_dir=logger.log_dir)],
    )
    for _ in range(epochs):
        train_one_epoch(
            state=state,
            train_dataloader=train_dataloader,
            val_dataloader=val_dataloader,
            log_frequency=log_frequency,
        )


def main(
    model_name: str,
    tokenizer_path: str,
    model_checkpoint: str | None = None,
    accelerator: str = "auto",
    precision: str | None = None,
    epochs: int = 3,
    lr: float = 1e-5,
    lr_warmup_steps: int = 100,
    batch_size: int = 64,
    accumulate_grad_batches: int = 1,
    log_frequency: int = 25,
    seed: int = 42,
    eval_only: bool = False,
    eval_prompt: str = PROMPT,
    eval_max_tokens: int = 1024,
):
    seed_everything(seed)
    # config = ModelConfig.from_name(model_name)
    # model = OpenELM.from_config(config)
    # model = OpenELM.from_pretrained(model_name)
    # model = LoRA.from_module(OpenELM.from_config(config), rank=5)
    model = OpenELM.from_pretrained(model_name)
    tokenizer = Tokenizer.from_file(tokenizer_path)

    if not eval_only:
        # NOTE: Only initialize the LoRA model if training has been requested.
        lora_model = LoRA.from_module(model, rank=5)
        if model_checkpoint is not None:
            lora_model.load_state_dict(
                ModelCheckpoint.load(model_checkpoint).state_dict
            )

        num_devices = torch.cuda.device_count()
        if num_devices > 0:
            # Lightning Fabric does not scale the batch size for distributed training.
            # In order to keep batch size the same, divide by the number of devices.
            if batch_size % num_devices != 0:
                raise ValueError(f"{batch_size=} must be divisible by {num_devices=}.")
            batch_size = batch_size // num_devices

        train_dataloader = DataLoader(
            GutenbergEBookDataset(
                split="train",
                chunk_size=4096,
                drop_last=True,
            ),
            batch_size=batch_size,
            collate_fn=partial(collate_fn, tokenizer=tokenizer),
            drop_last=True,
        )
        val_dataloader = DataLoader(
            GutenbergEBookDataset(split="val", chunk_size=4096),
            batch_size=batch_size,
            collate_fn=partial(collate_fn, tokenizer=tokenizer),
        )

        train(
            model=model,
            train_dataloader=train_dataloader,
            val_dataloader=val_dataloader,
            accelerator=accelerator,
            precision=precision,
            epochs=epochs,
            lr=lr,
            lr_warmup_steps=lr_warmup_steps,
            accumulate_grad_batches=accumulate_grad_batches,
            log_frequency=log_frequency,
        )
        model = lora_model.merge_lora(inplace=True)

    # Generate some text
    model = model.to(get_torch_device())
    prev_output = ""
    for output in generate(
        model,
        tokenizer=tokenizer,
        prompt=eval_prompt,
        max_new_tokens=eval_max_tokens,
        print_stats=True,
    ):
        # Return to the start of the line and print the output (no newline)
        print(output[len(prev_output) :], end="", flush=True)
        prev_output = output
    print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model-name", type=str, required=True)
    parser.add_argument("--tokenizer-path", type=str, required=True)
    parser.add_argument("--model-checkpoint", type=str, default=None)
    parser.add_argument("--accelerator", type=str, default="auto")
    parser.add_argument("--precision", type=str, default=None)
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--lr", type=float, default=1e-5)
    parser.add_argument("--lr-warmup-steps", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--accumulate-grad-batches", type=int, default=1)
    parser.add_argument("--log-frequency", type=int, default=25)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--eval-only", action="store_true")
    parser.add_argument("--eval-prompt", type=str, default=PROMPT)
    parser.add_argument("--eval-max-tokens", type=int, default=1024)
    args = parser.parse_args()

    main(**vars(args))
