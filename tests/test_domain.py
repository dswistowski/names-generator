from names_generator.domain import unique_word


def test_unique_word_should_return_first_unique_word():
    def next_word():
        return "foo"

    assert unique_word(next_word, frozenset()) == "foo"


def test_unique_word_should_ship_non_unique_word():
    def word_generator():
        yield "foo"
        yield "bar"

    generator = word_generator()

    def next_word():
        return next(generator)

    assert unique_word(next_word, frozenset(["foo"])) == "bar"
