import pytest
from fastapi import status


@pytest.fixture(scope='session')
def path_():
    return '/health'


def test_health(client, path_):
    r = client.get(path_)
    assert r.status_code == status.HTTP_200_OK, r.text
    assert (r_json := r.json()) and r_json.keys() == {'up_since', 'version'}
