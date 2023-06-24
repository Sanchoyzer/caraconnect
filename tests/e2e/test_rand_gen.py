import pytest
from fastapi import status


@pytest.fixture(scope='session')
def path_create():
    return '/v1/rand_gen'


@pytest.fixture
def path_get(path_create, uid):
    return f'{path_create}/{uid}'


@pytest.fixture
def path_get_fake(path_create, faker):
    return f'{path_create}/{faker.uuid4()}'


@pytest.fixture
def count_items(faker):
    return faker.pyint(min_value=2, max_value=9)


@pytest.fixture
def values(faker, count_items):
    result = [faker.unique.pyint(min_value=-100, max_value=100) for _ in range(count_items)]
    faker.unique.clear()
    return result


@pytest.fixture
def probabilities(faker, count_items):
    tmp = [faker.pyint(min_value=1, max_value=10**4) for _ in range(count_items)]
    tmp_sum = sum(tmp)
    return [round(i / tmp_sum, 4) for i in tmp]


@pytest.fixture(name='uid')
def create_params(path_create, client, values, probabilities):
    payload = {'values': values, 'probabilities': probabilities}
    r = client.post(path_create, json=payload)
    assert r.status_code == status.HTTP_200_OK, r.text
    return r.json()['uid']


class TestSetParams:
    def test_ok(self, client, path_create, values, probabilities):
        payload = {'values': values, 'probabilities': probabilities}
        r = client.post(path_create, json=payload)
        assert r.status_code == status.HTTP_200_OK, r.text
        assert (r_json := r.json()) and r_json['uid']
        assert r_json['values'] == payload['values']
        assert r_json['probabilities'] == payload['probabilities']

    def test_creation_incorrect_len(self, client, path_create, values, probabilities):
        values_short = values[1:]
        payload = {'values': values_short, 'probabilities': probabilities}
        r = client.post(path_create, json=payload)
        assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, r.text
        assert 'Different lens' in r.json()['detail'][0]['msg']

        probabilities_short = probabilities[1:]
        probabilities_short[0] += probabilities[0]
        payload = {'values': values, 'probabilities': probabilities_short}
        r = client.post(path_create, json=payload)
        assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, r.text
        assert 'Different lens' in r.json()['detail'][0]['msg']

    def test_creation_zero_len(self, client, path_create):
        payload = {'values': [], 'probabilities': []}
        r = client.post(path_create, json=payload)
        assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, r.text
        assert (r_json := r.json())
        for i in range(len(payload)):
            assert 'ensure this value has at least 1 items' in r_json['detail'][i]['msg'], r_json

    def test_creation_non_uniq_values(self, client, path_create, values, probabilities):
        values[1] = values[0]
        payload = {'values': values, 'probabilities': probabilities}
        r = client.post(path_create, json=payload)
        assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, r.text
        assert 'Non uniq values' in r.json()['detail'][0]['msg']

    def test_creation_incorrect_probs(self, client, path_create, values, probabilities):
        probabilities[0] = -probabilities[0]
        payload = {'values': values, 'probabilities': probabilities}
        r = client.post(path_create, json=payload)
        assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, r.text
        assert 'Incorrect values of probabilities' in r.json()['detail'][0]['msg']

        probabilities[0] = abs(probabilities[0]) + 1
        payload = {'values': values, 'probabilities': probabilities}
        r = client.post(path_create, json=payload)
        assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, r.text
        assert 'Incorrect values of probabilities' in r.json()['detail'][0]['msg']

    def test_creation_incorrect_sum_of_probs(self, client, path_create, values, probabilities):
        probabilities = [i + 0.1 for i in probabilities]
        payload = {'values': values, 'probabilities': probabilities}
        r = client.post(path_create, json=payload)
        assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, r.text
        assert 'Sum of probabilities' in r.json()['detail'][0]['msg']


class TestGetValues:
    def test_ok(self, client, path_get, values):
        r = client.get(path_get)
        assert r.status_code == status.HTTP_200_OK, r.text
        assert (r_json := r.json()) and len(r_json['values']) == 1, r.text
        assert r_json['values'][0] in values

    def test_ok_several_values(self, client, path_get, faker, values):
        amount = faker.pyint(min_value=2, max_value=9)
        r = client.get(path_get, params={'amount': amount})
        assert r.status_code == status.HTTP_200_OK, r.text
        assert (r_json := r.json()) and len(r_json['values']) == amount, r.text
        assert all(v in values for v in r_json['values'])

    def test_non_existing_uid(self, client, path_get_fake):
        r = client.get(path_get_fake)
        assert r.status_code == status.HTTP_404_NOT_FOUND, r.text
        assert 'not found' in r.json()['detail']
