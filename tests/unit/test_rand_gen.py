from collections import Counter

import pytest

from app.services.helpers import is_float_equal
from app.services.rand_gen import RandomGen


@pytest.fixture
def count_items(faker):
    return faker.pyint(min_value=2, max_value=9)


@pytest.fixture
def values(faker, count_items):
    result = [faker.unique.pyint(min_value=-10, max_value=10) for _ in range(count_items)]
    faker.unique.clear()
    return result


@pytest.fixture
def probabilities(faker, count_items):
    tmp = [faker.pyint(min_value=1, max_value=10**4) for _ in range(count_items)]
    tmp_sum = sum(tmp)
    return [round(i / tmp_sum, 4) for i in tmp]


@pytest.fixture
def rand_gen(values, probabilities):
    return RandomGen(values=values, probabilities=probabilities)


def test_ok(rand_gen, faker):
    amount_of_repetitions = faker.pyint(min_value=10**6, max_value=5 * 10**6)
    c = Counter(rand_gen.next_val() for _ in range(amount_of_repetitions))
    result = {k: v / amount_of_repetitions for k, v in dict(c).items()}

    expected = dict(zip(rand_gen.values, rand_gen.probabilities, strict=True))
    assert set(result.keys()) == set(expected.keys())
    for k, v in expected.items():
        assert is_float_equal(result[k], v)


def test_creation_incorrect_len(values, probabilities):
    values_short = values[1:]
    with pytest.raises(ValueError, match=r'Different lens: \d != \d'):
        RandomGen(values=values_short, probabilities=probabilities)

    probabilities_short = probabilities[1:]
    with pytest.raises(ValueError, match=r'Different lens: \d != \d'):
        RandomGen(values=values, probabilities=probabilities_short)


def test_creation_zero_len():
    with pytest.raises(ValueError, match='Zero length'):
        RandomGen(values=[], probabilities=[])


def test_creation_non_uniq_values(values, probabilities):
    values[1] = values[0]
    with pytest.raises(ValueError, match='Non uniq values'):
        RandomGen(values=values, probabilities=probabilities)


def test_creation_incorrect_probs(values, probabilities):
    probabilities[0] = -probabilities[0]
    with pytest.raises(ValueError, match='Incorrect values of probabilities'):
        RandomGen(values=values, probabilities=probabilities)

    probabilities[0] = abs(probabilities[0]) + 1
    with pytest.raises(ValueError, match='Incorrect values of probabilities'):
        RandomGen(values=values, probabilities=probabilities)


def test_creation_incorrect_sum_of_probabilities(values, probabilities):
    probabilities = [i + 0.1 for i in probabilities]
    with pytest.raises(ValueError, match=r'Sum of probabilities = .*, instead of 1'):
        RandomGen(values=values, probabilities=probabilities)
