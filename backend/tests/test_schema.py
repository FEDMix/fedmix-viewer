#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the fedmix_backend module.
"""
import graphene
import graphene.test
from fedmix_backend import Datastore, app


def test_empty(schema):
    assert schema


def test_dataset_list(schema):
    client = graphene.test.Client(schema)
    data = client.execute(
        '''{
        datasets {
            id
            title
            clusters {
                name
                patients
            }
        }
    }''',
        context=graphene.Context(
            datastore=Datastore('tests/mock-data/', 'http://localhost/')))

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
    assert data['data']['datasets'][0]['clusters'][0]['patients'] == [
        0, 2, 4, 6, 8, 10, 12, 14, 16, 18
    ]
    assert data['data']['datasets'][0]['clusters'][1]['name'] == 'cluster2'
    assert data['data']['datasets'][0]['clusters'][1]['patients'] == [
        1, 3, 5, 7, 9, 11, 13, 15, 17, 19
    ]


def test_dataset_detail(schema):
    client = graphene.test.Client(schema)
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
            context=graphene.Context(
                datastore=Datastore('tests/mock-data/', 'http://localhost/')))

        print(data)
        assert data['data']['datasets'][0]['id'] == 'dataset-1'

        assert data['data']['datasets'][0]['cases'][0]['scans'][
            0] == 'http://localhost/files/dataset-1/images/logo.png'
        assert data['data']['datasets'][1]['cases'][0]['scans'][
            0] == 'http://localhost/files/dataset-2/files/scans/0/0.png'


def test_dataset_algorithm_detail(schema):
    client = graphene.test.Client(schema)
    with app.test_request_context("/graphql"):
        data = client.execute(
            '''
            {
                datasets {
                    id
                    cases {
                        id
                        algorithms {
                            name
                            predictedMasks
                            metrics {
                                name
                                valueForCase
                                valuesPerSlice
                            }
                        }
                    }
                }
            }
            ''',
            context=graphene.Context(
                datastore=Datastore('tests/mock-data/', 'http://localhost/')))

        print(data)
        assert data['data']['datasets'][0]['id'] == 'dataset-1'

        assert data['data']['datasets'][0]['cases'][0]['algorithms'][0][
            'name'] == 'algorithm_1'
        assert (data['data']['datasets'][0]['cases'][0]['algorithms'][0]
                ['predictedMasks'][0] ==
                'http://localhost/files/dataset-1/images/logo.png')

        assert data['data']['datasets'][0]['cases'][0]['algorithms'][0][
            'metrics'][0]['name'] == 'metric1'
        assert data['data']['datasets'][0]['cases'][0]['algorithms'][0][
            'metrics'][0]['valueForCase'] == 0.7
        assert data['data']['datasets'][0]['cases'][0]['algorithms'][0][
            'metrics'][0]['valuesPerSlice'] == [0.1, 0.2, 0.3, 0.4]


def test_dataset_single_details(schema):
    client = graphene.test.Client(schema)
    with app.test_request_context("/graphql"):
        data = client.execute(
            '''
            {
                datasets(ids: ["dataset-1"]) {
                    id
                }
            }
            ''',
            context=graphene.Context(
                datastore=Datastore('tests/mock-data/', 'http://localhost/')))

        print(data)
        assert len(data['data']['datasets']) == 1
        assert data['data']['datasets'][0]['id'] == 'dataset-1'
