from typing import Any, get_origin, Union, get_args, Type

def is_compatible(type_a: Type[Any], type_b: Type[Any]) -> bool:
    """
    Check whether a concrete type is compatible with another type

    This function verifies if the concrete type `type_a` is acceptable when the expected type
    annotation is `type_b`.
    it can be thought of like 'Is type_a the same as type_b?'

    Args:
        type_a (Type[Any]): A concrete type (typically from a handler’s signature).
        type_b (Any): A type annotation representing the expected type. This may be a concrete type,
                      a union, or another form of type hint.

    Returns:
        bool: True if `type_a` is compatible with `type_b`, otherwise False.
    """
    if type_b is Any:
        return True

    if get_origin(type_b) is Union:
        return any(is_compatible(type_a, t) for t in get_args(type_b))

    return type_a == type_b

def type_name(t: Type[Any]) -> str:
    """
    Retrieve the name of a given type as a string.

    This function attempts to return the __name__ attribute of the provided type. If the type
    does not have a __name__ attribute, it falls back to converting the type to its string representation.

    Args:
        t (Type[Any]): The type (class) for which to obtain the name.

    Returns:
        str: The name of the type if available, otherwise its string representation.
    """
    try:
        return t.__name__
    except AttributeError:
        return str(t)