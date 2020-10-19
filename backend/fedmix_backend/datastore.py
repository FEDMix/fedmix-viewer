import os
import json
from glob import glob


class Datastore:
    def __init__(self, glob):
        self._glob = glob
        self.datasets = dict()
        self.load_datasets()

    def load_datasets(self):
        directories = sorted(glob(self._glob))
        for directory in directories:
            dataset_id = os.path.basename(directory)
            self.datasets[dataset_id] = self.load_dataset(directory)

    def load_dataset(self, directory):
        with open(os.path.join(directory, 'manifest.json')) as file:
            return json.load(file)
