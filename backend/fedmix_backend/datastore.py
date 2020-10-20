import os
import json


class Datastore:
    def __init__(self, path):
        self._path = path
        self.datasets = dict()
        self.load_datasets()

    def load_datasets(self):
        with os.scandir(self._path) as directories:
            for directory in directories:
                if directory.is_dir():
                    if 'manifest.json' in os.listdir(directory.path):
                        self.datasets[directory.name] = self.load_dataset(
                            directory)

    def load_dataset(self, directory):
        with open(os.path.join(directory, 'manifest.json')) as file:
            return json.load(file)
