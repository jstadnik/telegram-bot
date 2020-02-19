import pytest

from bot.utils import (
    parse,
    get_answer,
    get_items,
    get_question,
    process_reply,
    get_possible_choices_for_question,
)


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


def test_get_items():
    expected = [
        "Hamster",
        "Fox",
        "Elephant",
        "Lizard",
        "Mouse",
        "Potato",
        "Pea",
        "Watermelon",
        "Orange",
    ]
    choices = get_items()
    for item in expected:
        assert item in choices
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
        (
            "no",
            {
                "question_category": "Size",
                "question_object": "Large",
                "known": {"Colour": "Green"},
                "partial": {"Colour": {"Green": True}},
            },
            {"Colour": "Green"},
            {"Colour": {"Green": True}, "Size": {"Large": False}},
        ),
        (
            "no",
            {
                "question_category": "Type",
                "question_object": "Animal",
                "known": {"Colour": "Green"},
                "partial": {"Colour": {"Green": True}, "Size": {"Large": False}},
            },
            {"Colour": "Green", "Type": "Vegetable", "Size": "Small"},
            {
                "Type": {"Animal": False},
                "Colour": {"Green": True},
                "Size": {"Large": False},
            },
        ),
    ],
)
def test_process_reply(reply, user_data, expected_known, expected_partial):
    known, partial = process_reply(reply, user_data)
    assert known == expected_known
    assert partial == expected_partial
