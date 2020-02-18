import pytest

from bot.utils import (
    parse,
    get_answer,
    get_choices,
    get_question,
    process_reply,
    get_column_values,
    get_possible_choices_for_question,
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
        ({"Type": "Animal", "Colour": "Brown", "Size": "Small"}, "Hamster"),
        ({"Type": "Vegetable", "Colour": "Orange", "Size": "Medium"}, "Orange"),
        ({"Type": "Vegetable", "Colour": "Grey", "Size": "Large"}, None),
        ({"Type": "Animal", "Colour": "Orange"}, "Fox"),
        ({"Size": "Medium", "Colour": "Orange"}, None),
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
    "user_data,expected",
    [
        (
            {"known": {}, "partial": {}},
            [
                "Animal",
                "Vegetable",
                "Orange",
                "Grey",
                "Green",
                "Brown",
                "Small",
                "Medium",
                "Large",
            ],
        ),
        ({"known": {"Colour": "Grey"}, "partial": {}}, ["Small", "Large"]),
    ],
)
def test_get_question(user_data, expected):
    _, question = get_question(user_data)
    assert question in expected


@pytest.mark.parametrize(
    "user_data,expected",
    [
        (
            {"known": {}, "partial": {}},
            {
                "Type": {"Animal", "Vegetable"},
                "Colour": {"Orange", "Grey", "Green", "Brown"},
                "Size": {"Small", "Medium", "Large"},
            },
        ),
        ({"known": {"Colour": "Grey"}, "partial": {}}, {"Size": {"Small", "Large"}}),
        ({"known": {"Type": "Animal", "Colour": "Brown"}, "partial": {"Colour": {"Green": False, "Grey": False, "Brown": True}, "Type": {"Animal": True}, "Size": {"Medium": False}}}, {}),
    ],
)
def test_get_possible_choices_for_question(user_data, expected):
    all_options = get_possible_choices_for_question(user_data)
    for key, item in expected.items():
        assert all_options[key] == item


@pytest.mark.parametrize(
    "reply,user_data,expected_known,expected_partial",
    [
        (
            "yes",
            {
                "question_category": "Type",
                "question_object": "Animal",
                "partial": {},
                "known": {},
            },
            {"Type": "Animal"},
            {"Type": {"Animal": True}},
        ),
        (
            "no",
            {
                "question_category": "Type",
                "question_object": "Vegetable",
                "partial": {},
                "known": {},
            },
            {"Type": "Animal"},
            {"Type": {"Vegetable": False}},
        ),
        (
            "no",
            {
                "question_category": "Type",
                "question_object": "Animal",
                "partial": {},
                "known": {},
            },
            {"Type": "Vegetable"},
            {"Type": {"Animal": False}},
        ),
    ],
)
def test_process_reply(reply, user_data, expected_known, expected_partial):
    known, partial = process_reply(reply, user_data)
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
