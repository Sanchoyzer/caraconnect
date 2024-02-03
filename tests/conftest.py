import pytest
from faker import Faker


@pytest.fixture(scope='session')
def faker():
    return Faker()


@pytest.fixture
def count_items(faker):
    return faker.pyint(min_value=2, max_value=9)
