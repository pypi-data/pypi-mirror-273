"""
Create a method to instance and serve the GraphQL API
into a FastAPI server
"""
from typing import Type, Any, Optional
# Strawberry imports
import strawberry
from strawberry.fastapi import GraphQLRouter
# FastAPI imports
from fastapi.responses import FileResponse
# Local imports
from personal_interfaces.graphql.models_builder import models
from personal_interfaces.graphql.connectors.template import DatabaseConnector
from personal_interfaces.graphql.query_builder import QueryBuilder
from personal_interfaces.graphql.mutation_builder import MutationBuilder

def initialize_graphql_server(
    app_server,
    connector: Type[DatabaseConnector],
    connector_args: Optional[Any] = None
) -> None:
    """Initialize a GraphQL Server"""
    # Init the QueryBuilder and MutationBuilder based on the connector that
    # the user share
    if not issubclass(connector, DatabaseConnector):
        raise ValueError("The connector must inheritance from `DatabaseConnector`.")
    # Init the connector
    if connector_args:
        if isinstance(connector, list):
            db_connect = connector(models, *connector_args)
        else:
            db_connect = connector(models, connector_args)
    else:
        db_connect = connector(models)
    # Now, init the QueryBuilder and MutationBuilder
    query_b = QueryBuilder(db_connect)
    mutation_b = MutationBuilder(db_connect)
    # First, create the GraphQL API with Strawberry and use it on the GraphQL app
    # from strawberry.asgi client. Just return that value.
    gql_schema = strawberry.Schema(
        query=query_b.query,
        mutation=mutation_b.mutation
    )
    # Also, connect the API to the GraphQL endpoint
    graphql_router = GraphQLRouter(gql_schema)
    app_server.include_router(graphql_router, prefix="/graphql")


async def custom_favicon():
    """Add custom favicon for a Router page"""
    return FileResponse("public/favicon.ico")
