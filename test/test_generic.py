import os

import pytest


@pytest.fixture
def doodad():
    return "You should write some tests"


# @pytest.mark.skipif(
#     os.getenv("IGNORE_FAILING_TEST", False) == "true",
#     reason="Explicitly ignoring failing test",
# )
# def test_write_some_tests(doodad):
#     assert "write some tests!" == doodad
