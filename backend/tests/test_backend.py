import json
import os

import pytest
from fedmix_backend import add_routes, app


@pytest.fixture(scope="module", autouse=True)
def add_test_data_folder():
    print(os.getcwd())
    add_routes('tests/mock-data/', 'http://localhost/')


@pytest.fixture(name='client')
def fixture_client():
    app.config['TESTING'] = True

    with app.test_client() as test_client:
        yield test_client


def test_get_empty(client):
    response = client.get('/')

    assert response.status_code == 302


def test_get_simple(client):
    response = client.get('/graphql?query={datasets{id}}')

    assert response.status_code == 200
    # Check if all datasets are there

    data = json.loads(response.data.decode())
    print(data)

    assert 'data' in data
    assert 'datasets' in data['data']
    assert len(data['data']['datasets']) == 2

    # Check the individual properties
    assert data['data']['datasets'][0]['id'] == 'dataset-1'
    assert data['data']['datasets'][1]['id'] == 'dataset-2'


def test_get_image(client):
    response = client.get('/files/dataset-1/images/logo.png')

    assert response.status_code == 200
