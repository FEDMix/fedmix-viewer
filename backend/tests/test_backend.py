import pytest
import json

from fedmix_backend import app, add_routes


@pytest.fixture(scope="module", autouse=True)
def add_test_data_folder():
    add_routes('tests/mock-data/')


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_get_empty(client):
    rv = client.get('/')

    assert rv.status_code == 302


def test_get_simple(client):
    rv = client.get('/graphql?query={datasets{id}}')

    assert rv.status_code == 200
    # Check if all datasets are there

    data = json.loads(rv.data.decode())
    print(data)

    assert 'data' in data
    assert 'datasets' in data['data']
    assert len(data['data']['datasets']) == 2

    # Check the individual properties
    assert data['data']['datasets'][0]['id'] == 'dataset-1'
    assert data['data']['datasets'][1]['id'] == 'dataset-2'
