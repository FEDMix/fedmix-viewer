# -*- coding: utf-8 -*-
import logging
import os
import json

from graphene import List, ObjectType, Field, String, ID, Int, Schema

logger = logging.getLogger(__name__)


def get_dataset(context, id):
    return context.datastore.datasets[id]


class Cluster(ObjectType):
    name = String()


class Dataset(ObjectType):
    id = ID()
    title = String()
    clusters = List(Cluster)

    @staticmethod
    def resolve_title(root, info):
        dataset = get_dataset(info.context, root.id)
        return dataset['title']

    @staticmethod
    def resolve_clusters(root, info):
        dataset = get_dataset(info.context, root.id)
        return [
            Cluster(name=cluster['name']) for cluster in dataset['clusters']
        ]


def get_datasets(context):
    datasets = []
    for key, _ in context.datastore.datasets.items():
        datasets.append(Dataset(id=key))
    return datasets


class Query(ObjectType):
    datasets = List(Dataset)

    @staticmethod
    def resolve_datasets(root, info):
        return get_datasets(info.context)


def get_schema():
    return Schema(query=Query)
