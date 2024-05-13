"""Generate utilities for the GraphQL development"""
from typing import (
    Any, Union, Annotated,
    Optional, List,
    get_origin, get_args
)
# Strawberry imports
import strawberry


def is_optional(field: Any) -> bool:
    """Evaluate if a field is optional or not."""
    return get_origin(field) is Union and \
        type(None) in get_args(field)


def is_annotated(variable: Any) -> bool:
    """Evaluate if a function is annotated or not"""
    return get_origin(variable) == Annotated


def is_list(variable: Any) -> bool:
    """Evaluate if a field or model is a list"""
    if is_optional(variable):
        variable = get_args(variable)[0]
    return get_origin(variable) == list

def decapitalize(model: str) -> str:
    """Return a string in Camel format"""
    return model[0].lower() + model[1:]


def capitalize(model: str) -> str:
    """Return a string with the first letter capitalized"""
    return model[0].upper() + model[1:]


@strawberry.input
class FindBy:  # pylint: disable=R0903
    """FindBy method for inputs for the functions."""
    id: Optional[strawberry.ID] = strawberry.UNSET


@strawberry.input
class Filter:  # pylint: disable=R0903
    """Filter method for inputs"""
    id: Optional[strawberry.ID] = strawberry.UNSET
    ids: Optional[List[strawberry.ID]] = strawberry.UNSET


@strawberry.type
class Response:  # pylint: disable=R0903
    """Response for all the mutation types"""
    messages: Optional[str]
    successful: Optional[bool]
