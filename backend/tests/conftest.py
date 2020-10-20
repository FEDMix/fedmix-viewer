import pytest

from fedmix_backend import get_schema


@pytest.fixture
def schema():
    return get_schema()
