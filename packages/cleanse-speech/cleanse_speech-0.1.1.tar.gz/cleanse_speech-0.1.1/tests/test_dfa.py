import io

import pytest

from cleanse_speech import DLFA


@pytest.fixture
def test_censor():
    dfa = DLFA(words_resource=[
        ['你好'],
        io.BytesIO(b'sensitive'),
    ])
    assert dfa.censor_text('This is a 你好 word.', 10) == 'This is a ** word.'
    assert dfa.censor_text('This is a sensitive word.', 10) == 'This is a ********* word.'


def test_contains_illegal():
    dfa = DLFA(words_resource=[
        ['你好'],
        io.BytesIO(b'sensitive'),
    ])
    assert dfa.contains_illegal('This is a 你好 word.')
    assert dfa.contains_illegal('This is a sensitive word.')
    assert not dfa.contains_illegal('This is a normal word.')
