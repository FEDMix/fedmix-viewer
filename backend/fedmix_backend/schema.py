# -*- coding: utf-8 -*-
import logging
import os

from flask import request
from graphene import (ID, Float, Int, List, NonNull, ObjectType, Schema,
                      String)

logger = logging.getLogger(__name__)


class Cluster(ObjectType):
    name = NonNull(ID)
    patients = List(Int)

    def __init__(self, cluster, **args):
        super().__init__(**args)
        self._cluster = cluster

    @staticmethod
    def resolve_patients(root, info):
        return root._cluster['patients']


class Metric(ObjectType):
    name = NonNull(ID)
    value_for_case = Float()
    values_per_slice = List(Float)

    def __init__(self, metric, **args):
        super().__init__(**args)
        self._metric = metric

    @staticmethod
    def resolve_value_for_case(root, info):
        return root._metric['value_for_patient']

    @staticmethod
    def resolve_values_per_slice(root, info):
        return root._metric['values_per_slice']


def build_url(datadir, datasetname, path):
    host_url = request.host_url

    return os.path.join(host_url, datadir, datasetname, path)


class Algorithm(ObjectType):
    name = NonNull(ID)
    predicted_masks = List(String)
    metrics = List(Metric)

    def __init__(self, algorithm, parent, **args):
        super().__init__(**args)
        self._parent = parent
        self._algorithm = algorithm

    @staticmethod
    def resolve_predicted_masks(root, info):
        return [
            build_url('files', root._parent.id, predicted_mask)
            for predicted_mask in sorted(root._algorithm['predicted_masks'])
        ]

    @staticmethod
    def resolve_metrics(root, info):
        return [
            Metric(metric, name=name)
            for name, metric in root._algorithm['metrics'].items()
        ]


class Case(ObjectType):
    id = NonNull(ID)
    scans = List(String)
    ground_truth_masks = List(String)
    algorithms = List(Algorithm)

    def __init__(self, case, parent, **args):
        super().__init__(**args)
        self._parent = parent
        self._case = case

    @staticmethod
    def resolve_scans(root, info):
        return [
            build_url('files', root._parent.id, scan)
            for scan in sorted(root._case['scans'])
        ]

    @staticmethod
    def resolve_ground_truth_masks(root, info):
        return [
            build_url('files', root._parent.id, ground_truth_mask)
            for ground_truth_mask in sorted(root._case['ground_truth_masks'])
        ]

    @staticmethod
    def resolve_algorithms(root, info):
        return [
            Algorithm(algorithm, root._parent, name=name)
            for name, algorithm in root._case['algorithms'].items()
        ]


class Dataset(ObjectType):
    id = NonNull(ID)
    title = String(description="The title of the dataset")
    clusters = List(Cluster,
                    description="The clusters the algorithms were trained on")
    cases = List(Case, description="The cases the algorithms predicted for")

    def __init__(self, dataset, **args):
        super().__init__(**args)
        self._dataset = dataset

    @staticmethod
    def resolve_title(root, info):
        return root._dataset['title']

    @staticmethod
    def resolve_clusters(root, info):
        return [
            Cluster(cluster, name=cluster['name'])
            for cluster in root._dataset['clusters']
        ]

    @staticmethod
    def resolve_cases(root, info):
        return [
            Case(case, root, id=id)
            for id, case in root._dataset['cases'].items()
        ]


class Query(ObjectType):
    datasets = List(Dataset, ids=List(ID))

    @staticmethod
    def resolve_datasets(root, info, ids=None):
        sets = info.context.datastore.datasets
        datasets = []
        keys = ids
        if not keys:
            keys = sorted(sets.keys())

        for key in keys:
            datasets.append(Dataset(sets[key], id=key))
        return datasets


def get_schema():
    return Schema(query=Query)
