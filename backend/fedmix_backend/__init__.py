# -*- coding: utf-8 -*-

import logging

from .__version__ import __version__
from .schema import get_schema
from .datastore import Datastore
from .fedmix_backend import app, main, add_routes

logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = "Berend Weel"
__email__ = 'b.weel@esciencecenter.nl'

__all__ = [
    '__version__', 'get_schema', 'Datastore', 'app', 'main', 'add_routes'
]
