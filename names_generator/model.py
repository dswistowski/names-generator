import typing as t
from dataclasses import dataclass

import torch


@dataclass
class Model:
    C: torch.FloatTensor
    W1: torch.FloatTensor
    b1: torch.FloatTensor
    W2: torch.FloatTensor
    b2: torch.FloatTensor
    itos: t.Mapping[int, str]


def load(path: str) -> Model:
    with open(path, "rb") as f:
        ((C, W1, b1, W2, b2), itos) = torch.load(f)
    return Model(C, W1, b1, W2, b2, itos)


def load_names(path: str) -> t.FrozenSet[str]:
    with open(path) as f:
        return set(filter(None, f.read().split("\n")))
