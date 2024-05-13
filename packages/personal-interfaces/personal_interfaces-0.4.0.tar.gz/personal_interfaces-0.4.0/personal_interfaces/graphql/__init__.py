"""
Provide a GraphQL Interface for Python.

This API interface allow us to use the power and flexibility of GraphQL
in different projects, connecting a database to our systems easily.

Currently, it supports:
- Deta Base
- TinyDB

To access to this connectors, use:
    - personal_interfaces.graphql.connectors
"""
# Import the interface
from .interface import initialize_graphql_server
# Import the SCHEMA_PATH var
from .models_builder import SCHEMA_PATH
