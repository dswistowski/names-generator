import typing as t


def unique_word(
    next_word: t.Callable[[], str], forbitten_names: t.FrozenSet[str]
) -> str:
    while True:
        word = next_word()

        if word and word not in forbitten_names:
            return word
