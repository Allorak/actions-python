from typing import Any, get_origin, Union, get_args

def is_compatible(handler_type, expected_type) -> bool:
    if expected_type is Any:
        return True

    if get_origin(expected_type) is Union:
        return any(is_compatible(handler_type, t) for t in get_args(expected_type))

    return handler_type == expected_type

def type_name(t) -> str:
    try:
        return t.__name__
    except AttributeError:
        return str(t)