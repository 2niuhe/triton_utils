"""
Utilities for examples.
"""

from typing import Tuple

import torch
from torch import autocast, nn
from triton.testing import do_bench


def benchmark_fw_and_bw(
    model: nn.Module,
    amp: bool = True,
    **input,
) -> Tuple[float, float, float]:
    """
    Benchmarks the forward and backward pass of a model.

    Args:
        model: Model to run.
        amp: Flag for running the forward pass using automatic mixed precision.
        **input: Input to the model.
    """
    with autocast("cuda", enabled=amp):
        fw = do_bench(lambda: model(**input))

    with autocast("cuda", enabled=amp):
        output = model(**input)
    output_grad = torch.randn_like(output)
    bw = do_bench(lambda: output.backward(output_grad, retain_graph=True))

    print(f"Forward pass mean execution time: {fw}")
    print(f"Backward pass mean execution time: {bw}")
    print(f"Forward plus backward pass mean execution time: {fw + bw}")
