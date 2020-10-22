#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the fedmix_backend module.
"""
import flask
from graphene import Context
from graphene.test import Client

from fedmix_backend import Datastore, app


def test_empty(schema):
    assert (schema)


def test_dataset_list(schema):
    client = Client(schema)
    data = client.execute(
        '''{
        datasets {
            id
            title
            clusters {
                name
            }
        }
    }''',
        context=Context(datastore=Datastore('tests/mock-data/')))

    print(data)
    # Check if all datasets are there
    assert 'data' in data
    assert 'datasets' in data['data']
    assert len(data['data']['datasets']) == 2

    # Check the individual properties
    assert data['data']['datasets'][0]['id'] == 'dataset-1'
    assert data['data']['datasets'][1]['id'] == 'dataset-2'

    assert data['data']['datasets'][0]['title'] == 'My First Dataset'
    assert data['data']['datasets'][1]['title'] == 'My Second Dataset'

    assert data['data']['datasets'][0]['clusters'][0]['name'] == 'cluster1'
    assert data['data']['datasets'][0]['clusters'][1]['name'] == 'cluster2'


def test_dataset_detail(schema):
    client = Client(schema)
    with app.test_request_context("/graphql"):
        data = client.execute(
            '''
            {
                datasets {
                    id
                    cases {
                        id
                        scans
                        groundTruthMasks
                    }
                }
            }
            ''',
            context=Context(datastore=Datastore('tests/mock-data/')))

        print(data)
        assert data['data']['datasets'][0]['id'] == 'dataset-1'

        assert data['data']['datasets'][0]['cases'][0]['scans'][
            0] == 'http://localhost/files/dataset-1/files/scans/0/0.png'
        assert data['data']['datasets'][1]['cases'][0]['scans'][
            0] == 'http://localhost/files/dataset-2/files/scans/0/0.png'
