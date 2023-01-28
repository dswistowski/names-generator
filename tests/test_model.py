from unittest.mock import patch, mock_open

import torch

from names_generator.model import load_names, load


def test_load_names_should_return_list_of_names():
    with patch("builtins.open", mock_open(read_data="foo\nbar")) as m:
        assert load_names("foo") == set(["foo", "bar"])
        m.assert_called_once_with("foo")


def test_load_names_should_ignore_empty_lines():
    with patch("builtins.open", mock_open(read_data="foo\n\nbar")) as m:
        assert load_names("foo") == set(["foo", "bar"])
        m.assert_called_once_with("foo")


def test_model_can_be_executed():
    model = load("./models/names.pt")
    g = torch.Generator().manual_seed(42)

    assert model.next_word(g) == "Anastantynandra"
