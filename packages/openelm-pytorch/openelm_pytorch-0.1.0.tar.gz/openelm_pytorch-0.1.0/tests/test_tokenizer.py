import os
from tempfile import TemporaryDirectory
from typing import Generator, Sequence

import pytest
import torch

from openelm_pytorch.tokenizer import Tokenizer

TOKENIZER_URL = "https://drive.google.com/uc?id=1HaSMrw27lJKfMVvxFzYhpJWqrlH3qwXm"


@pytest.fixture(scope="module")
def tokenizer() -> Generator[Tokenizer, None, None]:
    with TemporaryDirectory() as tempdir:
        tokenizer_path = os.path.join(tempdir, "tokenizer.model")
        torch.hub.download_url_to_file(TOKENIZER_URL, tokenizer_path)
        yield Tokenizer.from_file(tokenizer_path)


@pytest.mark.parametrize(
    "text",
    [
        "Hello, world!",
        "A test string for the tokenizer.",
    ],
)
def test_encode_decode(text: str, tokenizer: Tokenizer) -> None:
    encoded = tokenizer(text)
    decoded = tokenizer.decode(encoded)
    assert text == decoded


@pytest.mark.parametrize(
    "texts",
    [
        ("Hello, world!", "A test string for the tokenizer."),
    ],
)
def test_batch_encode_decode(texts: Sequence[str], tokenizer: Tokenizer) -> None:
    texts = ["Hello, world!", "A test string for the tokenizer."]
    encoded = tokenizer(texts)
    decoded = tokenizer.batch_decode(encoded)
    assert texts == decoded
