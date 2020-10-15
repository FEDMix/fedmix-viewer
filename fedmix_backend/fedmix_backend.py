from flask import Flask
from flask_graphql import GraphQLView

from graphene import Context
from .schema import get_schema
from .datastore import Datastore

app = Flask(__name__)

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


def main():
    app.run()


if __name__ == '__main__':
    main()