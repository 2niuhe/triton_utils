from dataclasses import dataclass
from typing import Callable, List

import torch


@dataclass
class OperatorImpl:
    key: str
    impl: Callable
    way: str  # 'cuda'


class use_gems:
    def __init__(self, bindings: List[OperatorImpl]):
        self.lib = torch.library.Library("aten", "IMPL")
        self.bindings = bindings

    def __enter__(self):
        for b in self.bindings:
            self.lib.impl(b.key, b.impl, b.way)

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.lib
