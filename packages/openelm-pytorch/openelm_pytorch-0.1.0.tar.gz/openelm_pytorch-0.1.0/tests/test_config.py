import dataclasses

import pytest

from openelm_pytorch.config import ModelConfig
from tests.openelm_mlx import GPTConfig, gpt_configs


@pytest.mark.parametrize("model_name", list(gpt_configs.keys()))
def test_config_from_name(model_name: str):
    gpt_config = GPTConfig.from_name(
        model_name, vocab_size=32128, max_context_length=2048
    )
    assert isinstance(gpt_config, GPTConfig)
    openelm_config = ModelConfig.from_name(model_name)

    for key, value in dataclasses.asdict(openelm_config).items():
        assert getattr(gpt_config, key) == value
