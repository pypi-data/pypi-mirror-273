from typing import NoReturn, Optional

from .exceptions import InvalidParamsException


def validate_id(value: int) -> NoReturn:
    if not type(value) is int:
        raise InvalidParamsException("id must be of type int", "id", id)


def validate_limit(value: int) -> NoReturn:
    if not type(value) is int or value > 500 or value < 1:
        raise InvalidParamsException("Limit must be between 1 and 500 and must be int instance", "limit", value)


def validate_jurisdiction(allow_empty: bool, value: Optional[str]) -> NoReturn:
    if not isinstance(value, (str, type(None))):
        raise InvalidParamsException(
            "jurisdiction must be of type str or can be None if allowed", "jurisdiction", value
        )
    if not allow_empty and not value:
        raise InvalidParamsException("jurisdiction is empty, but its not allowed", "jurisdiction", value)
