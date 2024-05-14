import time
from typing import Iterator

import torch
from torch import Tensor

from openelm_pytorch.openelm import OpenELM
from openelm_pytorch.tokenizer import Tokenizer
from openelm_pytorch.utils import get_torch_device

MODEL_NAME = "OpenELM-450M"
DEVICE = get_torch_device()
# From "The Treasure Island" by R.L.Stevenson, public domain.
PROMPT = (
    "Squire Trelawney, Dr. Livesey, and the rest of these gentlemen having "
    "asked me to write down the whole particulars about Treasure Island, "
    "from the"
)


def generate(
    model: OpenELM,
    tokenizer: Tokenizer,
    prompt: str = PROMPT,
    max_tokens: int = 1024,
    top_k: int = 10,
    temperature: float = 1.0,
    print_stats: bool = False,
) -> Iterator[str]:
    device = next(iter(model.parameters())).device
    temperature = max(temperature, 1e-8)
    is_training = model.training
    model.eval()

    input_ids = tokenizer([prompt]).to(device)
    tokens = input_ids[0].tolist()  # For decoding text later.

    with torch.inference_mode():
        prompt_start = time.perf_counter()
        outputs = model.forward(input_ids, use_kv_cache=True)
        token = outputs["logits"][0, -1].argmax().item()
        cache = outputs["kv_cache"]
        tokens.append(token)
        prompt_end = time.perf_counter()

        generation_start = time.perf_counter()
        for i in range(max_tokens):
            outputs = model.forward(
                input_ids=torch.tensor([[token]], device=device),
                kv_cache=cache,
                use_kv_cache=True,
            )
            logits, cache = outputs["logits"], outputs["kv_cache"]
            probs = torch.softmax(logits[0, -1] / temperature, dim=-1)
            # Get top-k tokens, renormalize their probabilities, and weighted sample.
            token_ids: Tensor  # for mypy
            probs, token_ids = probs.topk(k=top_k, dim=-1)
            probs /= probs.sum()
            # Take weighted random sample from the top-k tokens.
            sampled_idx: int = torch.multinomial(probs, num_samples=1).item()  # type: ignore
            token: int = token_ids[sampled_idx].item()  # type: ignore

            tokens.append(token)
            if i % 5 == 0:
                yield tokenizer.decode(tokens)

        if tokens:
            yield tokenizer.decode(tokens)
        generation_end = time.perf_counter()

        if print_stats:
            prompt_speed = input_ids.shape[-1] / (prompt_end - prompt_start)
            generation_speed = max_tokens / (generation_end - generation_start)
            print(f"\nTotal time: {generation_end - generation_start:.2f} seconds")
            print(f"Prompt:     {prompt_speed:.2f} tokens/sec")
            print(f"Generation: {generation_speed:.2f} tokens/sec")

    # Restore the model's original training state.
    model.train(mode=is_training)


def main(
    model_name: str = MODEL_NAME,
    prompt: str = PROMPT,
    max_tokens: int = 1024,
    temperature: float = 1.0,
    top_k: int = 10,
    device: str | torch.device = DEVICE,
) -> None:
    print(f"Using device: {device}")
    tokenizer = Tokenizer.from_file("tokenizer.model")
    model = OpenELM.from_pretrained(
        model_name=model_name,
        device=device,
        dtype=torch.float16,
    )

    print("Generating text...")
    model = model.to(get_torch_device())
    prev_output = ""
    for output in generate(
        model,
        tokenizer=tokenizer,
        prompt=prompt,
        max_tokens=max_tokens,
        top_k=top_k,
        temperature=temperature,
        print_stats=True,
    ):
        # Return to the start of the line and print the output (no newline)
        print(output[len(prev_output) :], end="", flush=True)
        prev_output = output
    print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model-name", type=str, default=MODEL_NAME)
    parser.add_argument("--prompt", type=str, default=PROMPT)
    parser.add_argument("--max-tokens", type=int, default=1024)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--device", type=str, default=DEVICE)
    args = parser.parse_args()

    main(**vars(args))
