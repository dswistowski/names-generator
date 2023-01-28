import os
import typing as t

from fastapi import FastAPI, Depends
from starlette.staticfiles import StaticFiles

from names_generator.domain import unique_word
from names_generator.model import Model, load, load_names

app = FastAPI(title="The Names Generator")

api_app = FastAPI(titl="The Names Generator API")

app.mount("/api", api_app)
app.mount("/", StaticFiles(directory="ui", html=True), name="ui")

MODEL_PATH = os.environ.get("MODEL_PATH", "./models/pokemons.pt")
NAMES_PATH = os.environ.get("NAMES_PATH", "./models/pokemons.txt")

MODEL = load(MODEL_PATH)
FORBIDDEN_NAMES = load_names(NAMES_PATH)


def get_model() -> Model:
    return MODEL


def get_forbidden_names() -> set[str]:
    return FORBIDDEN_NAMES


@api_app.get("/name")
def generate_name(
    model: Model = Depends(get_model),
    forbidden_names: t.FrozenSet[str] = Depends(get_forbidden_names),
):
    return {"name": unique_word(model.next_word, forbidden_names)}
