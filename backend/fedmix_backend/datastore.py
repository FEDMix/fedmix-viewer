import os
import sys
import json
import logging

logger = logging.getLogger(__name__)


class Datastore:
    def __init__(self, path):
        self.path = path
        self.datasets = dict()
        self.load_datasets()

    def load_datasets(self):
        print(f"Loading datasets from {self.path} relative to {os.getcwd()}")
        try:
            with os.scandir(self.path) as directories:
                self.abspath = os.path.abspath(self.path)
                for directory in directories:
                    if directory.is_dir():
                        if 'manifest.json' in os.listdir(directory.path):
                            self.datasets[directory.name] = self.load_dataset(
                                directory)
        except FileNotFoundError as e:
            print(f"Could not find data directory!")
            raise e

    def load_dataset(self, directory):
        with open(os.path.join(directory, 'manifest.json')) as file:
            return json.load(file)
