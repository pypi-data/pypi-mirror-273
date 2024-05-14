from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from enum import Enum

from openelm_pytorch.utils import linspace, make_divisible


class ModelName(str, Enum):
    OpenELM_270M = "OpenELM-270M"
    OpenELM_450M = "OpenELM-450M"
    OpenELM_1_1B = "OpenELM-1_1B"
    OpenELM_3B = "OpenELM-3B"


def compute_heads(model_dim: int, head_dim: int) -> int:
    if model_dim % head_dim == 0:
        return model_dim // head_dim
    raise ValueError(
        "Model dimension should be divisible by head dimension. Got: "
        f"{model_dim} and {head_dim}."
    )


@dataclass
class ModelConfig:
    vocab_size: int = 32128
    max_context_length: int = 2048

    num_transformer_layers: int = 12
    model_dim: int = 2048
    ffn_dim_divisor: int = 256

    head_dim: int = 128
    qkv_multipliers: tuple[float, float] = (0.5, 1.0)
    # This variable allows to switch between multi-head attention, group query
    # attention, and multi-query attention.
    # When num_gqa_groups == 1, then it is multi-head attention.
    # When 1 < num_gqa_groups < num_heads and num_heads is divisible by
    # num_gqa_groups, then it is group query attention
    # When num_gqa_groups == num_heads, then it is multi-query attention
    num_gqa_groups: int = 4

    # These are to be initialized in __post_init__ below!
    num_query_heads: list[int] = field(default_factory=lambda: [])
    num_kv_heads: list[int] = field(default_factory=lambda: [])
    ffn_multipliers: list[float] = field(default_factory=lambda: [0.5, 4.0])

    rope_freq_constant: int = 10000
    # Note that rope_max_length is set to twice of max_context_length.
    # This allows flexibility in token lengths during training or fine-tuning.
    rope_max_length: int = 4096

    def __post_init__(self) -> None:
        # Each attention layer have different latent dimensions assuming
        # qkv_multipliers[0] != qkv_multipliers[1].
        # This results in variable allocation of parameters in attention layer.
        # This scaling is known as layer-wise or block-wise scaling:
        # https://arxiv.org/abs/2008.00623
        qkv_multipliers = [
            round(v, 2)
            for v in linspace(
                self.qkv_multipliers[0],
                self.qkv_multipliers[1],
                num=self.num_transformer_layers,
            )
        ]
        query_dims = [
            make_divisible(
                self.model_dim * mult, divisor=self.head_dim * self.num_gqa_groups
            )
            for mult in qkv_multipliers
        ]

        # compute the number of query, key, and value heads
        # For multi-head and multi-query attention, the number of heads for
        # query, key, and value are the same.
        # For group query attention, the number of key and value heads are the same.
        self.num_query_heads = [
            compute_heads(q_dim, self.head_dim) for q_dim in query_dims
        ]
        self.num_kv_heads = [
            q_heads // self.num_gqa_groups for q_heads in self.num_query_heads
        ]

        # Each FFN layer have different latent dimensions assuming
        # ffn_multipliers[0] != ffn_multipliers[1].
        # This results in variable allocation of parameters in FFN layer.
        # This scaling is known as layer-wise or block-wise scaling:
        # https://arxiv.org/abs/2008.00623
        self.ffn_multipliers = [
            round(v, 2)
            for v in linspace(
                self.ffn_multipliers[0],
                self.ffn_multipliers[1],
                num=self.num_transformer_layers,
            )
        ]

    @classmethod
    def from_name(
        cls,
        model_name: str | ModelName,
        num_transformer_layers: int | None = None,
        model_dim: int | None = None,
        head_dim: int | None = None,
        **kwargs,
    ) -> ModelConfig:
        # NOTE: Use 'kwargs' to override any other (optional) arguments to ModelConfig.
        if model_name == ModelName.OpenELM_270M:
            return cls(
                num_transformer_layers=(num_transformer_layers or 16),
                model_dim=(model_dim or 1280),
                head_dim=(head_dim or 64),
                **kwargs,
            )
        elif model_name == ModelName.OpenELM_450M:
            return cls(
                num_transformer_layers=(num_transformer_layers or 20),
                model_dim=(model_dim or 1536),
                head_dim=(head_dim or 64),
                **kwargs,
            )
        elif model_name == ModelName.OpenELM_1_1B:
            return cls(
                num_transformer_layers=(num_transformer_layers or 28),
                model_dim=(model_dim or 2048),
                head_dim=(head_dim or 64),
                **kwargs,
            )
        elif model_name == ModelName.OpenELM_3B:
            return cls(
                num_transformer_layers=(num_transformer_layers or 36),
                model_dim=(model_dim or 3072),
                head_dim=(head_dim or 128),
                **kwargs,
            )
        else:
            raise ValueError(f"Unknown model name: {model_name}")


class PretrainedModelName(str, Enum):
    OpenELM_270M = "OpenELM-270M"
    OpenELM_270M_INSTRUCT = "OpenELM-270M-Instruct"
    OpenELM_450M = "OpenELM-450M"
    OpenELM_450M_INSTRUCT = "OpenELM-450M-Instruct"
    OpenELM_1_1B = "OpenELM-1_1B"
    OpenELM_1_1B_INSTRUCT = "OpenELM-1_1B-Instruct"
    OpenELM_3B = "OpenELM-3B"
    OpenELM_3B_INSTRUCT = "OpenELM-3B-Instruct"


@dataclasses.dataclass
class PretrainedModelConfig:
    config: ModelConfig
    weights_uri: str | list[str]
    # TODO: Optional backup URIs, in case the original weights are moved or unaccessible
    # weights_backup_uri: str | list[str] | None = None

    @classmethod
    def from_name(cls, model_name: str | PretrainedModelName) -> PretrainedModelConfig:
        # TODO: Convert to using 'safetensors' checkpoints for security reasons.

        if model_name == PretrainedModelName.OpenELM_270M:
            return cls(
                config=ModelConfig.from_name(ModelName.OpenELM_270M),
                weights_uri="https://docs-assets.developer.apple.com/ml-research/models/corenet/v0.1.0/openelm/mlx/270M/weights.safetensors",
            )
        elif model_name == PretrainedModelName.OpenELM_450M:
            return cls(
                config=ModelConfig.from_name(ModelName.OpenELM_450M),
                weights_uri="https://docs-assets.developer.apple.com/ml-research/models/corenet/v0.1.0/openelm/mlx/450M/weights.safetensors",
            )
        elif model_name == PretrainedModelName.OpenELM_1_1B:
            return cls(
                config=ModelConfig.from_name(ModelName.OpenELM_1_1B),
                weights_uri="https://docs-assets.developer.apple.com/ml-research/models/corenet/v0.1.0/openelm/mlx/1.1B/weights.safetensors",
            )
        elif model_name == PretrainedModelName.OpenELM_3B:
            return cls(
                config=ModelConfig.from_name(ModelName.OpenELM_3B),
                weights_uri="https://docs-assets.developer.apple.com/ml-research/models/corenet/v0.1.0/openelm/mlx/3B/weights.safetensors",
            )
        else:
            raise ValueError(f"Unknown pretrained model name: {model_name}")
