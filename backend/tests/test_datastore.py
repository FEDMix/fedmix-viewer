from fedmix_backend import Datastore


def test_datastore():
    datastore = Datastore('tests/mock-data/')

    assert sorted(list(datastore.datasets)) == ['dataset-1', 'dataset-2']
    assert 'title' in datastore.datasets['dataset-1']
