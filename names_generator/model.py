import typing as t
from dataclasses import dataclass

import torch


@dataclass(frozen=True)
class Model:
    C: torch.FloatTensor
    W1: torch.FloatTensor
    b1: torch.FloatTensor
    W2: torch.FloatTensor
    b2: torch.FloatTensor
    itos: t.Mapping[int, str]

    def next_letter(
        self, context: list[int], generator: torch.Generator
    ) -> t.Tuple[str | None, list[int]]:
        emb = self.C[torch.tensor(context)]
        h = torch.tanh(emb.view(1, -1) @ self.W1 + self.b1)
        logits = h @ self.W2 + self.b2
        prob = logits.softmax(dim=1)
        ix = t.cast(int, torch.multinomial(prob, 1, generator=generator).item())
        context = context[1:] + [ix]
        if self.itos[ix] == ".":
            return None, context
        return self.itos[ix], context

    def next_word(self, generator: torch.Generator | None = None) -> str:
        if generator is None:
            generator = torch.Generator()
            generator.seed()

        out = []
        context = [0] * 3
        while True:
            letter, context = self.next_letter(context, generator)
            if letter is None:
                break
            out.append(letter)

        return "".join(out).strip()


def load(path: str) -> Model:
    with open(path, "rb") as f:
        ((C, W1, b1, W2, b2), itos) = torch.load(f)
    return Model(C, W1, b1, W2, b2, itos)


def load_names(path: str) -> set[str]:
    with open(path) as f:
        return set(filter(None, f.read().split("\n")))
