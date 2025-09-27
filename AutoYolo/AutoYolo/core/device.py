"""Runtime device resolution utilities.

This module centralises logic to pick an optimal inference backend for
AutoYolo while gracefully handling brand-new GPUs such as the RTX 5060.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class DeviceInfo:
    """Runtime device metadata."""

    type: str
    torch_device: str
    description: str
    backend: str


def _try_torch_cuda() -> Optional[DeviceInfo]:
    try:
        import torch
    except Exception:  # pragma: no cover - torch optional for docs build
        return None

    if not torch.cuda.is_available():
        return None

    index = torch.cuda.current_device()
    name = torch.cuda.get_device_name(index)
    capability = torch.cuda.get_device_capability(index)

    try:
        torch.zeros(1, device=f"cuda:{index}")
    except RuntimeError as exc:
        message = str(exc)
        if "no kernel image" in message or "sm_" in message:
            return None
        raise

    major, minor = capability
    arch = f"sm_{major}{minor}"
    desc = f"CUDA GPU · {name} ({arch})"
    return DeviceInfo("cuda", f"cuda:{index}", desc, backend="torch")


def _try_torch_directml() -> Optional[DeviceInfo]:
    try:
        import torch_directml  # type: ignore
    except Exception:
        return None

    device = torch_directml.device()
    desc = "DirectML GPU · torch-directml"
    return DeviceInfo("dml", "dml", desc, backend="torch-directml")

def resolve_device(preferred: str | None = None) -> DeviceInfo:
    """Resolve the best available device.

    Parameters
    ----------
    preferred:
        Optional manual override ("cuda", "dml", or "cpu").
    """

    if preferred in {"cuda", "gpu"}:
        device = _try_torch_cuda()
        if device:
            return device
    elif preferred == "dml":
        device = _try_torch_directml()
        if device:
            return device
        return DeviceInfo("cpu", "cpu", "CPU · DirectML unavailable", backend="cpu")
    elif preferred == "cpu":
        return DeviceInfo("cpu", "cpu", "CPU", backend="cpu")

    cuda_device = _try_torch_cuda()
    if cuda_device:
        return cuda_device

    dml_device = _try_torch_directml()
    if dml_device:
        return dml_device

    return DeviceInfo("cpu", "cpu", "CPU", backend="cpu")
