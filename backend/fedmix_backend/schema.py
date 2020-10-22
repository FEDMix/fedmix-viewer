# -*- coding: utf-8 -*-
import logging
import os
import json

from flask import request

from graphene import List, ObjectType, Field, String, ID, Int, Schema, NonNull

logger = logging.getLogger(__name__)


class Cluster(ObjectType):
    name = NonNull(String)


def build_url(datadir, datasetname, path):
    host_url = request.host_url

    return os.path.join(host_url, datadir, datasetname, path)


class Case(ObjectType):
    id = NonNull(String)
    scans = List(String)
    groundTruthMasks = List(String)

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
    def resolve_groundTruthMasks(root, info):
        return [
            build_url('files', root._parent.id, ground_truth_mask)
            for ground_truth_mask in sorted(root._case['ground_truth_masks'])
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
            Cluster(name=cluster['name'])
            for cluster in root._dataset['clusters']
        ]

    @staticmethod
    def resolve_cases(root, info):
        return [
            Case(case, root, id=id)
            for id, case in root._dataset['cases'].items()
        ]


class Query(ObjectType):
    datasets = List(Dataset)

    @staticmethod
    def resolve_datasets(root, info):
        sets = info.context.datastore.datasets
        datasets = []
        for key in sorted(sets.keys()):
            datasets.append(Dataset(sets[key], id=key))
        return datasets


def get_schema():
    return Schema(query=Query)
