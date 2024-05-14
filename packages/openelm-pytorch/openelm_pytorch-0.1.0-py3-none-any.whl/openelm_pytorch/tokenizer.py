"""
A tokenizer for OpenELM models with an interface similar to Huggingface 'transformers'.
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import sentencepiece
import torch
from torch import Tensor


class Tokenizer:
    """A tokenizer for OpenELM with an interface similar to Huggingface."""

    def __init__(self, model: sentencepiece.SentencePieceProcessor):
        self.model = model

    @classmethod
    def from_file(cls, model_path: str | Path) -> Tokenizer:
        """NOTE: We can't automatically download the tokenizer, because OpenELM uses
        the Llama2 tokenizer, which requires a license agreement or API token.
        Instead, users can download the tokenizer from 'meta-llama/Llama-2-7b' on
        Huggingface and pass the path to this method.
        TODO: Add a note about this in the README.

        >>> tokenizer = Tokenizer.from_file("tokenizer.model")
        """
        model = sentencepiece.SentencePieceProcessor(model_file=str(model_path))
        return cls(model=model)

    def __call__(
        self,
        text: str | Sequence[str],
        device: torch.device | None = None,
        max_length: int | None = None,
        add_bos: bool = True,
        add_eos: bool = False,
    ) -> Tensor:
        # NOTE: The default 'pad_id' is -1, but this causes problems with the
        # tokenizer.  Token ID 1 appears to be the same as 'pad_id'.
        PAD_ID = 1

        if isinstance(text, str):
            return torch.as_tensor(
                self.model.Encode(text, add_bos=add_bos, add_eos=add_eos),
                device=device,
                dtype=torch.long,
            )
        else:  # isinstance(text, list)
            encoded: list[list[int]] = [
                self.model.Encode(t, add_bos=add_bos, add_eos=add_eos) for t in text
            ]
            pad_length = max(len(e) for e in encoded)
            if max_length is not None:
                pad_length = min(pad_length, max_length)

            out = torch.empty(
                (len(encoded), pad_length), device=device, dtype=torch.long
            ).fill_(PAD_ID)
            for i, e in enumerate(encoded):
                out[i, : len(e)] = torch.as_tensor(e, device=device, dtype=torch.long)

            return out

    def decode(self, ids: Tensor | Sequence[int]) -> str:
        if isinstance(ids, Tensor):
            ids = ids.tolist()
        return self.model.Decode([i for i in ids if i != self.model.pad_id()])

    def batch_decode(self, ids: Tensor | Sequence[Sequence[int]]) -> list[str]:
        if isinstance(ids, Tensor):
            ids = ids.tolist()
        return [self.decode(ids[i]) for i in range(len(ids))]


if __name__ == "__main__":
    tokenizer = Tokenizer.from_file("tokenizer.model")
    tokenized = tokenizer(["Hello, world!", "Hello, it's me."])
    print(tokenized)
