import pytest

from bot.utils import process_reply, get_answer

@pytest.mark.parametrize("reply,expected", [('yes', True), ('yeah', True), ('yup', True), ('Yes', True), ('Yeah', True), ('Yup', True), ('No', False), ('Nope', False), ('no', False), ('nah', False), ('something else', False)])
def test_process_reply(reply, expected):
    assert process_reply(reply) == expected

@pytest.mark.parametrize("data,expected", [({'animal': True, 'brown': True}, 'horse'), ({'animal': False, 'brown': True}, 'table')])
def test_get_answer(data, expected):
    assert get_answer(data) == expected
