import mlx.core as mx
import mlx.nn as mxnn
import mlx.utils
import pytest
import torch
from torch import Tensor

from openelm_pytorch.config import ModelConfig
from openelm_pytorch.openelm import (
    FeedForwardNetwork,
    MultiHeadAttention,
    OpenELM,
    RMSNorm,
    RoPE,
    TransformerDecoderLayer,
)
from openelm_pytorch.utils import get_torch_device
from tests.openelm_mlx import FeedForwardNetwork as MlxFeedForwardNetwork
from tests.openelm_mlx import GPTConfig
from tests.openelm_mlx import (
    MultiHeadCausalAttention as MlxMultiHeadCausalAttention,
)
from tests.openelm_mlx import OpenELM as MlxOpenELM
from tests.openelm_mlx import (
    TransformerDecoderLayer as MlxTransformerDecoderLayer,
)
from tests.utils import mlx_to_torch

# Make deterministic
mx.random.seed(42)
torch.manual_seed(42)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False


@torch.inference_mode()
@pytest.mark.parametrize("dims", (128, 4096))
@pytest.mark.parametrize("seq_len", (16, 2048))
def test_rmsnorm(dims: int, seq_len: int):
    rmsnorm_mlx = mxnn.RMSNorm(dims)
    rmsnorm = RMSNorm(dims)
    # Parameters should be the same already (weights = 1), but do this as a sanity check.
    rmsnorm.load_state_dict(
        {k: mlx_to_torch(v) for k, v in rmsnorm_mlx.parameters().items()}
    )

    x_mlx = mx.random.normal((2, seq_len, dims), dtype=mx.float32)
    y_mlx = rmsnorm_mlx(x_mlx)
    x = mlx_to_torch(x_mlx)
    y = rmsnorm(x)

    torch.testing.assert_close(y, mlx_to_torch(y_mlx), rtol=1e-4, atol=1e-4)


# NOTE: This test gets very slow on non-Apple devices, since all of the 'mlx'
# computations are forced to run on CPU.
@torch.inference_mode()
@pytest.mark.parametrize("model_name", ["OpenELM-270M"])
def test_feedforward(model_name: str):
    config = GPTConfig.from_name(model_name, vocab_size=32128, max_context_length=2048)
    device = get_torch_device()

    for layer_idx in range(config.num_transformer_layers):
        ffn_mlx = MlxFeedForwardNetwork(config, layer_idx=layer_idx)
        ffn = FeedForwardNetwork.from_config(
            config=config, layer_idx=layer_idx, device=device
        )
        ffn.load_state_dict(
            {
                k: mlx_to_torch(v, device=device)
                for k, v in mlx.utils.tree_flatten(ffn_mlx.parameters())
            }
        )

        x_mlx = mx.random.normal((2, 10, config.model_dim), dtype=mx.float32)
        y_mlx = ffn_mlx(x_mlx)
        x = mlx_to_torch(x_mlx, device=device)
        y = ffn(x)

        torch.testing.assert_close(
            y, mlx_to_torch(y_mlx, device=device), rtol=1e-5, atol=1e-5
        )


@torch.inference_mode()
@pytest.mark.parametrize("dim", (16, 128))
@pytest.mark.parametrize("seq_len", (16, 64))
def test_rope(dim: int, seq_len: int):
    rope_mlx = mxnn.RoPE(dim)
    rope = RoPE(dim)
    # NOTE: 'dim' is the only parameter for RoPE.  No need to load state_dict.

    x_mlx = mx.random.normal((2, seq_len, dim), dtype=mx.float32)
    y_mlx = rope_mlx(x_mlx)
    device = get_torch_device()
    x = mlx_to_torch(x_mlx, device=device)
    y = rope(x)

    # NOTE: There appears to be a significant amount of floating-point error in
    # either the 'torch' or 'mlx' trig functions.  Some elements have an absolute
    # difference of ~1e-5, which I think is acceptable.  Because the absolute value
    # is sometimes very close to zero, though, this makes the max relative difference
    # fairly large (~1e-3).  Set the relative tolerance to 1e-2 to account for this.
    # TODO: Check if we can resolve this discrepancy.
    torch.testing.assert_close(
        y, mlx_to_torch(y_mlx, device=device), rtol=1e-2, atol=1e-4
    )


@torch.inference_mode()
@pytest.mark.parametrize("model_name", ["OpenELM-270M"])
@pytest.mark.parametrize("seq_len", (16, 64))
def test_multihead_attention(model_name: str, seq_len: int):
    config = GPTConfig.from_name(model_name, vocab_size=32128, max_context_length=2048)
    device = get_torch_device()

    for layer_idx in range(config.num_transformer_layers):
        mha_mlx = MlxMultiHeadCausalAttention(config, layer_idx=layer_idx)
        mha = MultiHeadAttention.from_config(config, layer_idx=layer_idx, device=device)
        mha.load_state_dict(
            {
                k: mlx_to_torch(v, device=device)
                for k, v in mlx.utils.tree_flatten(mha_mlx.parameters())
            }
        )

        x_mlx = mx.random.normal((2, seq_len, config.model_dim), dtype=mx.float32)
        y_mlx, kv_mlx = mha_mlx(x_mlx)
        x = mlx_to_torch(x_mlx, device=device)
        y, kv = mha(x)

        assert kv_mlx is None
        assert kv is None
        torch.testing.assert_close(
            y, mlx_to_torch(y_mlx, device=device), rtol=1e-5, atol=1e-5
        )


@torch.inference_mode()
@pytest.mark.parametrize("model_name", ["OpenELM-270M"])
@pytest.mark.parametrize("seq_len", (16, 64))
def test_multihead_attention_kv_cache(model_name: str, seq_len: int):
    config = GPTConfig.from_name(model_name, vocab_size=32128, max_context_length=2048)
    device = get_torch_device()

    for layer_idx in range(config.num_transformer_layers):
        mha_mlx = MlxMultiHeadCausalAttention(config, layer_idx=layer_idx)
        mha = MultiHeadAttention.from_config(config, layer_idx=layer_idx, device=device)
        mha.load_state_dict(
            {
                k: mlx_to_torch(v, device=device)
                for k, v in mlx.utils.tree_flatten(mha_mlx.parameters())
            }
        )

        x_mlx = mx.random.normal((2, seq_len, config.model_dim), dtype=mx.float32)
        x = mlx_to_torch(x_mlx, device=device)
        kv_mlx: list[tuple[mx.array, mx.array]] | None = None
        kv: list[tuple[Tensor, Tensor]] | None = None

        for i in range(seq_len):
            y_mlx, kv_mlx = mha_mlx(
                x_mlx[:, i : i + 1], use_kv_cache=True, past_key_value=kv_mlx
            )
            y, kv = mha(x[:, i : i + 1], use_kv_cache=True, kv_cache=kv)

            assert kv_mlx is not None
            assert kv is not None
            # NOTE: A few elements had differences of ~2e-5.  I think this is
            # acceptable, but I'd prefer to set the tolerance to 1e-5.  Investigate
            # whether we can lower the threshold somehow.
            torch.testing.assert_close(
                kv[0], mlx_to_torch(kv_mlx[0], device=device), rtol=1e-4, atol=1e-4
            )
            torch.testing.assert_close(
                kv[1], mlx_to_torch(kv_mlx[1], device=device), rtol=1e-4, atol=1e-4
            )
            torch.testing.assert_close(
                y, mlx_to_torch(y_mlx, device=device), rtol=1e-5, atol=1e-5
            )


@torch.inference_mode()
@pytest.mark.parametrize("model_name", ["OpenELM-270M"])
@pytest.mark.parametrize("seq_len", (16, 64))
def test_transformer_decoder_layer(model_name: str, seq_len: int):
    config = GPTConfig.from_name(model_name, vocab_size=32128, max_context_length=2048)
    device = get_torch_device()

    for layer_idx in range(config.num_transformer_layers):
        tdl_mlx = MlxTransformerDecoderLayer(config, layer_idx=layer_idx)
        tdl = TransformerDecoderLayer.from_config(
            config, layer_idx=layer_idx, device=device
        )
        tdl.load_state_dict(
            {
                k: mlx_to_torch(v, device=device)
                for k, v in mlx.utils.tree_flatten(tdl_mlx.parameters())
            }
        )

        x_mlx = mx.random.normal((2, seq_len, config.model_dim), dtype=mx.float32)
        y_mlx, kv_mlx = tdl_mlx(x_mlx)
        x = mlx_to_torch(x_mlx, device=device)
        y, kv = tdl(x)

        assert kv_mlx is None
        assert kv is None
        torch.testing.assert_close(
            y, mlx_to_torch(y_mlx, device=device), rtol=1e-5, atol=1e-5
        )


@torch.inference_mode()
@pytest.mark.parametrize("model_name", ["OpenELM-270M"])
@pytest.mark.parametrize("seq_len", (16, 64))
def test_transformer_decoder_layer_kv_cache(model_name: str, seq_len: int):
    config = GPTConfig.from_name(model_name, vocab_size=32128, max_context_length=2048)
    device = get_torch_device()

    for layer_idx in range(config.num_transformer_layers):
        tdl_mlx = MlxTransformerDecoderLayer(config, layer_idx=layer_idx)
        tdl = TransformerDecoderLayer.from_config(
            config, layer_idx=layer_idx, device=device
        )
        tdl.load_state_dict(
            {
                k: mlx_to_torch(v, device=device)
                for k, v in mlx.utils.tree_flatten(tdl_mlx.parameters())
            }
        )

        x_mlx = mx.random.normal((1, seq_len, config.model_dim), dtype=mx.float32)
        x = mlx_to_torch(x_mlx, device=device)
        kv_mlx: list[tuple[mx.array, mx.array]] | None = None
        kv: list[tuple[Tensor, Tensor]] | None = None

        for i in range(seq_len):
            y_mlx, kv_mlx = tdl_mlx(
                x_mlx[:, i : i + 1], use_kv_cache=True, past_key_value=kv_mlx
            )
            y, kv = tdl(x[:, i : i + 1], use_kv_cache=True, kv_cache=kv)

            assert kv_mlx is not None
            assert kv is not None
            torch.testing.assert_close(
                kv[0], mlx_to_torch(kv_mlx[0], device=device), rtol=1e-2, atol=1e-5
            )
            torch.testing.assert_close(
                kv[1], mlx_to_torch(kv_mlx[1], device=device), rtol=1e-5, atol=1e-5
            )
            torch.testing.assert_close(
                y, mlx_to_torch(y_mlx, device=device), rtol=1e-5, atol=1e-5
            )


# NOTE: This test gets *extremely* slow for larger models, especially when running
# on CPU.  Only test 270M by default, but check the pretrained model outputs for all
# model types later on.
@torch.inference_mode()
@pytest.mark.parametrize("model_name", ["OpenELM-270M"])
@pytest.mark.parametrize("vocab_size", [32128])
@pytest.mark.parametrize("max_context_length", [2048])
@pytest.mark.parametrize("seq_len", (16, 64))
@pytest.mark.parametrize("is_causal", [True, False])
def test_openelm(
    model_name: str,
    vocab_size: int,
    max_context_length: int,
    seq_len: int,
    is_causal: bool,
):
    openelm_mlx = MlxOpenELM(
        model_name,
        vocab_size=vocab_size,
        max_context_length=max_context_length,
    )
    config = GPTConfig.from_name(
        model_name,
        vocab_size=vocab_size,
        max_context_length=max_context_length,
    )
    device = get_torch_device()
    openelm = OpenELM.from_config(config=config, device=device)
    openelm.load_state_dict(
        {
            k: mlx_to_torch(v, device=device)
            for k, v in mlx.utils.tree_flatten(openelm_mlx.parameters())
        }
    )

    x_mlx = mx.random.randint(low=0, high=config.vocab_size, shape=(2, seq_len))
    y_mlx = openelm_mlx(
        {
            "input_ids": x_mlx,
            "past_key_values": None,
            "use_kv_cache": False,
            "is_causal": is_causal,
        }
    )
    x = mlx_to_torch(x_mlx, device=device)
    y = openelm(x, is_causal=is_causal)

    torch.testing.assert_close(
        y, mlx_to_torch(y_mlx, device=device), rtol=1e-2, atol=1e-4
    )


@torch.inference_mode()
@pytest.mark.parametrize("model_name", ["OpenELM-270M"])
@pytest.mark.parametrize("vocab_size", [32128])
@pytest.mark.parametrize("max_context_length", [2048])
@pytest.mark.parametrize("seq_len", (16, 64))
@pytest.mark.parametrize("is_causal", [True, False])
def test_openelm_kv_cache(
    model_name: str,
    vocab_size: int,
    max_context_length: int,
    seq_len: int,
    is_causal: bool,
):
    openelm_mlx = MlxOpenELM(
        model_name,
        vocab_size=vocab_size,
        max_context_length=max_context_length,
    )
    config = GPTConfig.from_name(
        model_name,
        vocab_size=vocab_size,
        max_context_length=max_context_length,
    )
    device = get_torch_device()
    openelm = OpenELM.from_config(config=config, device=device)
    openelm.load_state_dict(
        {
            k: mlx_to_torch(v, device=device)
            for k, v in mlx.utils.tree_flatten(openelm_mlx.parameters())
        }
    )

    x_mlx = mx.random.randint(low=0, high=config.vocab_size, shape=(1, seq_len))
    x = mlx_to_torch(x_mlx, device=device)
    cache_mlx: list[tuple[mx.array, mx.array]] | None = None
    cache: list[tuple[Tensor, Tensor]] | None = None

    for i in range(seq_len):
        outputs_mlx = openelm_mlx(
            {
                "input_ids": x_mlx[:, i : i + 1],
                "past_key_values": cache_mlx,
                "use_kv_cache": True,
                "is_causal": is_causal,
            }
        )
        y_mlx = outputs_mlx["logits"]
        cache_mlx = outputs_mlx["past_key_values"]
        outputs = openelm.forward(
            x[:, i : i + 1], kv_cache=cache, use_kv_cache=True, is_causal=is_causal
        )
        y = outputs["logits"]
        cache = outputs["kv_cache"]

        assert cache_mlx is not None
        assert cache is not None
        for kv_mlx, kv in zip(cache_mlx, cache):
            torch.testing.assert_close(
                kv[0], mlx_to_torch(kv_mlx[0], device=device), rtol=1e-3, atol=1e-4
            )
            torch.testing.assert_close(
                kv[1], mlx_to_torch(kv_mlx[1], device=device), rtol=1e-3, atol=1e-4
            )
        torch.testing.assert_close(
            y, mlx_to_torch(y_mlx, device=device), rtol=1e-3, atol=1e-4
        )


@pytest.mark.parametrize("model_name", ["OpenELM-270M", "OpenELM-450M"])
def test_reset_parameters(model_name: str):
    config = ModelConfig.from_name(model_name)
    openelm = OpenELM.from_config(config=config)
    openelm.reset_parameters()


@pytest.mark.parametrize(
    "model_name",
    ["OpenELM-270M", "OpenELM-450M", "OpenELM-1_1B", "OpenELM-3B"],
)
def test_from_pretrained(model_name: str):
    device = get_torch_device()
    _ = OpenELM.from_pretrained(model_name, device=device)
