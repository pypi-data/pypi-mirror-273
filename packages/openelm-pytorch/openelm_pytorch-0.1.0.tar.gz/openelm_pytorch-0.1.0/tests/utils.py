import mlx.core as mx
import numpy as np
import torch


def torch_to_mlx(x: torch.Tensor) -> mx.array:
    """Converts a PyTorch tensor to an MLX tensor with the same dtype.

    Args:
        x: PyTorch tensor to convert

    Returns:
        An MLX version with the same dtype and contents.
    """
    x = x.detach()
    torch_dtype = str(x.dtype).split(".")[-1]
    mlx_dtype = getattr(mx, torch_dtype)
    # MLX mentions that converting to bfloat16 under NumPy could result in
    # precision loss, so we first up-cast to fp32.
    if torch_dtype == "bfloat16":
        x = x.to(torch.float32)
    return mx.array(x.cpu().numpy(), dtype=mlx_dtype)


def mlx_to_torch(x: mx.array, device: torch.device | None = None) -> torch.Tensor:
    """Converts an MLX tensor to a PyTorch tensor with the same dtype.

    Args:
        x: MLX tensor to convert

    Returns:
        A PyTorch version with the same dtype and contents.
    """
    mlx_dtype = str(x.dtype).split(".")[-1]
    torch_dtype = getattr(torch, mlx_dtype)
    return torch.tensor(np.array(x), dtype=torch_dtype, device=device)
