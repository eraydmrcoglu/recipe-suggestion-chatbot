from unittest import mock

import pytest


@pytest.fixture(scope="function", autouse=True)
def openai_mock():
    with mock.patch("openai.ChatCompletion.create") as _fixture:
        yield _fixture
