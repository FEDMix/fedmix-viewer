import configparser
import os
from functools import partial

from flask import Flask, json, redirect, send_file, url_for
from flask_graphql import GraphQLView
from graphene import Context
from werkzeug.exceptions import HTTPException

from .datastore import Datastore
from .schema import get_schema

app = Flask(__name__)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.route('/')
def index():
    return redirect(url_for('graphql'))


def get_image(datastore, path):
    path = os.path.join(datastore.abspath, path)
    return send_file(path)


def add_routes(datadir, remote_url):
    datastore = Datastore(datadir, remote_url)
    app.add_url_rule('/graphql',
                     view_func=GraphQLView.as_view(
                         'graphql',
                         schema=get_schema(),
                         graphiql=True,
                         get_context=lambda: Context(datastore=datastore)))

    # Optional, for adding batch query support (used in Apollo-Client)
    app.add_url_rule('/graphql',
                     view_func=GraphQLView.as_view(
                         'graphql-batch',
                         schema=get_schema(),
                         graphiql=True,
                         get_context=lambda: Context(datastore=datastore),
                         batch=True))

    view = partial(get_image, datastore)
    app.add_url_rule('/files/<path:path>', 'send_file', view)


def main():
    # Read local file `config.ini`
    config = configparser.ConfigParser()
    configs = config.read('config/config.ini')
    print("Read configuration from: ", configs)

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
    remote_url = f'{schema}://{hostname}:{port}'
    if 'remote_url' in config['datastore']:
        remote_url = config['datastore']['remote_url']

    print("Using remote url: ", remote_url)
    add_routes(datadir, remote_url)
    app.run()


if __name__ == "__main__":
    main()
