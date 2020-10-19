import configparser

from flask import Flask, redirect, url_for
from flask_graphql import GraphQLView
from graphene import Context

from .datastore import Datastore
from .schema import get_schema
from .validate_config import validate_config

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('graphql'))


app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=get_schema(),
        graphiql=True,
        get_context=lambda: Context(datastore=Datastore('tests/mock-data/*'))))

# Optional, for adding batch query support (used in Apollo-Client)
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql-batch',
        schema=get_schema(),
        graphiql=True,
        get_context=lambda: Context(datastore=Datastore('tests/mock-data/*')),
        batch=True))

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
    app.run()


if __name__ == "__main__":
    main()
