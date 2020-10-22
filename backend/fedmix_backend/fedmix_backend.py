import configparser
import os
from functools import partial

from flask import Flask, redirect, send_from_directory, url_for
from flask_graphql import GraphQLView
from graphene import Context

from .datastore import Datastore
from .schema import get_schema
from .validate_config import validate_config

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('graphql'))


def send_file(datadir, path):
    if not os.path.isabs(datadir):
        # We prepend .. to the datadir because send_from_directory
        # is relative to the module root, which is fedmix_backend
        # but the configuration assumes from the project root
        datadir = os.path.join('..', datadir)
    return send_from_directory(datadir, path)


def add_routes(datadir):
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=get_schema(),
            graphiql=True,
            get_context=lambda: Context(datastore=Datastore(datadir))))

    # Optional, for adding batch query support (used in Apollo-Client)
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql-batch',
            schema=get_schema(),
            graphiql=True,
            get_context=lambda: Context(datastore=Datastore(datadir)),
            batch=True))

    view = partial(send_file, datadir)
    app.add_url_rule('/files/<path:path>', 'send_file', view)


CONFIGTEMPLATE = {
    'app': {
        'host': 'str',
        'port': 5000,
        'schema': 'str'
    },
    'datastore': {
        'directory': 'str'
    }
}


def main():
    # Read local file `config.ini`
    config = configparser.ConfigParser()
    configs = config.read('config/config.ini')
    print("Read configuration from: ", configs)

    validation_errors = validate_config(config, CONFIGTEMPLATE)
    if validation_errors:
        print("Found some issues with the config file")
        for error in validation_errors:
            print(error)

    if 'app' in config:
        hostname = config['app'].get('host', '127.0.0.1')
        port = config['app'].getint('port', 5000)
        schema = config['app'].get('schema', 'http')

        servername = f'{hostname}:{port}'
        app.config.update(SERVER_NAME=servername)
        app.config.update(PREFERRED_URL_SCHEME=schema)

    if 'datastore' not in config or 'directory' not in config['datastore']:
        print('''Datastore not set correctly in configuration
        Please add the following datastore section to config/config.ini and try again.

        [datastore]
        directory = data
        ''')

    datadir = config['datastore']['directory']
    add_routes(datadir)
    app.run()


if __name__ == "__main__":
    main()
