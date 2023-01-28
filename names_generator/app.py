import os
import typing as t

import torch
from fastapi import FastAPI, Depends
from starlette.staticfiles import StaticFiles

from names_generator.model import Model, load, load_names

app = FastAPI(title="The Names Generator")

api_app = FastAPI(titl="The Names Generator API")

app.mount("/api", api_app)
app.mount("/", StaticFiles(directory="ui", html=True), name="ui")

MODEL_PATH = os.environ.get("MODEL_PATH", "./models/names.pt")
NAMES_PATH = os.environ.get("NAMES_PATH", "./models/names.txt")

MODEL = load(MODEL_PATH)
FORBITTEN_NAMES = load_names(NAMES_PATH)


def get_model() -> Model:
    return MODEL


def get_forbitten_names() -> t.FrozenSet[str]:
    return FORBITTEN_NAMES


@api_app.get("/name")
def generate_name(
    seed: int = -1,
    model: Model = Depends(get_model),
    forbitten_names: t.FrozenSet[str] = Depends(get_forbitten_names),
):
    g = torch.Generator()
    if seed == -1:
        g.seed()
    else:
        g.manual_seed(seed)

    C = model.C
    W1 = model.W1
    b1 = model.b1
    W2 = model.W2
    b2 = model.b2
    itos = model.itos

    while True:
        out = []
        context = [0] * 3
        while True:
            emb = C[torch.tensor(context)]
            h = torch.tanh(emb.view(1, -1) @ W1 + b1)
            logits = h @ W2 + b2
            prob = logits.softmax(dim=1)
            ix = torch.multinomial(prob, 1, generator=g).item()
            context = context[1:] + [ix]
            if itos[ix] == '.':
                break
            out.append(itos[ix])
        word = "".join(out).strip()
        if word and word not in forbitten_names:
            return {"name": word}