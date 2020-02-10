import pytest

from bot.utils import (
    parse,
    get_answer,
    get_choices,
    get_question,
    process_reply,
    get_column_values,
)
from bot.constants import Category


@pytest.mark.parametrize(
    "reply,expected",
    [
        ("yes", True),
        ("yeah", True),
        ("yup", True),
        ("Yes", True),
        ("Yeah", True),
        ("Yup", True),
        ("No", False),
        ("Nope", False),
        ("no", False),
        ("nah", False),
        ("something else", False),
    ],
)
def test_parse(reply, expected):
    assert parse(reply) == expected


@pytest.mark.parametrize(
    "data,expected",
    [
        ({"Type": "Animal", "Colour": "Brown"}, "Hamster"),
        ({"Type": "Vegetable", "Colour": "Orange"}, "Orange"),
        ({"Type": "Vegetable", "Colour": "Grey"}, -1),
    ],
)
def test_get_answer(data, expected):
    assert get_answer(data) == expected


@pytest.mark.parametrize(
    "category,expected",
    [
        (
            Category.ITEM,
            [
                "Hamster",
                "Fox",
                "Elephant",
                "Lizard",
                "Mouse",
                "Potato",
                "Pea",
                "Watermelon",
                "Orange",
            ],
        ),
        (Category.TYPE, ["Animal", "Vegetable"]),
    ],
)
def test_get_choices(category, expected):
    choices = get_choices(category)
    for item in expected:
        assert item in expected
        choices.remove(item)
    assert len(choices) == 0


@pytest.mark.parametrize(
    "category,partial,expected",
    [
        (Category.TYPE, {"Type": {"Vegetable": False}}, ["Animal"]),
        (Category.TYPE, {}, ["Animal", "Vegetable"]),
        (Category.COLOR, {"Colour": {"Brown": False}}, ["Orange", "Grey", "Green"]),
    ],
)
def test_get_question(category, partial, expected):
    question = get_question(category, partial)
    assert question in expected


@pytest.mark.parametrize(
    "reply,user_data,category,expected_known,expected_partial",
    [
        (
            "yes",
            {"question_object": "Animal", "partial": {}, "known": {}},
            Category.TYPE,
            {"Type": "Animal"},
            {"Animal": True},
        ),
        (
            "no",
            {"question_object": "Vegetable", "partial": {}, "known": {}},
            Category.TYPE,
            {"Type": "Animal"},
            {"Vegetable": False},
        ),
        (
            "no",
            {"question_object": "Animal", "partial": {}, "known": {}},
            Category.TYPE,
            {"Type": "Vegetable"},
            {"Animal": False},
        ),
    ],
)
def test_process_reply(reply, user_data, category, expected_known, expected_partial):
    known, partial = process_reply(reply, user_data, category)
    assert known == expected_known
    assert partial == expected_partial


@pytest.mark.parametrize(
    "col,expected",
    [
        (
            0,
            [
                "Hamster",
                "Fox",
                "Elephant",
                "Lizard",
                "Mouse",
                "Potato",
                "Pea",
                "Watermelon",
                "Orange",
            ],
        ),
        (1, ["Animal", "Vegetable"]),
    ],
)
def test_get_column_values(col, expected):
    result = get_column_values(col)
    for item in expected:
        assert item in expected
        result.remove(item)
    assert len(result) == 0
