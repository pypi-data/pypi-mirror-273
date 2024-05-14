import os

import torch


def get_torch_device() -> torch.device:
    """Returns the device PyTorch tensors should be created on."""
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif (
        hasattr(torch.backends, "mps")
        and torch.backends.mps.is_available()
        and os.environ.get("PYTORCH_DISABLE_MPS", "0").lower() not in ("1", "true")
    ):
        return torch.device("mps")
    else:
        return torch.device("cpu")


def make_divisible(val: int | float, divisor: int) -> int:
    """Make val divisible by divisor, rounding down no more than 10%, otherwise
    rounding up. If val is less than divisor, returns divisor."""
    assert val >= 0.0, val
    assert divisor > 0, divisor
    assert isinstance(divisor, int)

    if val < divisor:
        return divisor

    # First round down to a whole multiple of divisor and see if it's within 10%
    # of val. If it is, return it, if not, add another `divisor` to get the
    # upper rounding.
    round_down = int(val + divisor / 2) // divisor * divisor

    if round_down <= 0.9 * val:
        return round_down + divisor
    else:
        return round_down


def linspace(start: float, end: float, num: int) -> list[float]:
    if num == 1:
        return [start]
    step = (end - start) / (num - 1)
    return [round(start + i * step, 2) for i in range(num)]
