# -*- coding: utf-8 -*-
import logging
import os
import json

from graphene import List, ObjectType, Field, String, ID, Int, Schema, NonNull

logger = logging.getLogger(__name__)


class Cluster(ObjectType):
    name = NonNull(String)


class Dataset(ObjectType):
    id = NonNull(ID)
    title = String(description="The title of the dataset")
    clusters = List(Cluster,
                    description="The clusters the algorithms were trained on")

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


class Query(ObjectType):
    datasets = List(Dataset)

    @staticmethod
    def resolve_datasets(root, info):
        datasets = []
        for key, dataset in info.context.datastore.datasets.items():
            datasets.append(Dataset(dataset, id=key))
        return datasets


def get_schema():
    return Schema(query=Query)
