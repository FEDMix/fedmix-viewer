import os
import json
import logging

logger = logging.getLogger(__name__)


class Datastore:
    def __init__(self, path, remote_url):
        self.path = path
        self.remote_url = remote_url
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
                            self.load_dataset(directory)
        except FileNotFoundError as error:
            print("Could not find data directory!")
            raise error

    def load_dataset(self, directory):
        with open(os.path.join(directory, 'manifest.json')) as file:
            self.datasets[directory.name] = json.load(file)
