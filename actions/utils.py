from typing import Any, Union, Type, Tuple, TypeVar, Callable, Annotated, get_args, get_origin

def is_compatible_type(type_a: Type[Any], valid_types: Tuple[Type[Any], ...]) -> bool:
    """
    Check whether a concrete type is compatible with at least one of the expected valid types.

    This function verifies if the concrete type `type_a` is acceptable when any of the expected types
    in `valid_types` is provided.

    Args:
        type_a (Type[Any]): A concrete type (typically from a handler’s signature).
        valid_types (Tuple[Type[Any], ...]): A tuple of type annotations representing the acceptable types.
            These may be concrete types, unions, or other forms of type hints.

    Returns:
        bool: True if `type_a` is compatible with at least one of the types in `valid_types`, otherwise False.
    """
    for expected_type in valid_types:
        if expected_type is Any:
            return True

        type_a_origin = get_origin(type_a)
        expected_origin = get_origin(expected_type)
        expected_args = get_args(expected_type)

        if expected_origin is Union:
            if any(is_compatible_type(type_a, (arg,)) for arg in expected_args):
                return True

        elif expected_origin is not None and type_a_origin is expected_origin:
            if all(is_compatible_type(type_a, (arg,)) for arg in expected_args):
                return True

        elif expected_origin is Annotated:
            base_type = get_args(expected_type)[0]
            if is_compatible_type(type_a, (base_type,)):
                return True

        elif expected_origin is Callable and type_a_origin is Callable:
            callable_args = expected_args[0]
            expected_return_type = expected_args[1]

            type_a_args = get_args(type_a)

            actual_args = type_a_args[0] if hasattr(type_a, '__args__') else ()
            actual_return_type = type_a_args[1] if hasattr(type_a, '__args__') else Any

            if len(callable_args) == len(actual_args):
                if all(is_compatible_type(arg_a, (arg_b,))
                       for arg_a, arg_b
                       in zip(actual_args, callable_args)):
                    return is_compatible_type(actual_return_type, (expected_return_type,))
            return False

        elif isinstance(expected_type, TypeVar):
            if type_a == expected_type.__bound__:
                return True

        # Checks for NewType variables
        elif (callable(expected_type) and
              not isinstance(expected_type, type) and
              hasattr(expected_type, '__supertype__')):
            base_type = expected_type.__supertype__
            if isinstance(type_a, base_type):
                return True

        elif type_a == expected_type:
            return True

    return False

def type_name(t: Union[Type[Any], Tuple[Type[Any], ...]]) -> str:
    """
    Retrieve the name of a given type or a tuple of types as a string.

    This function attempts to return the __name__ attribute of the provided type. If a tuple
    of types is provided, it returns a comma-separated list of the names (or string representations)
    of each type. If the type does not have a __name__ attribute, the function falls back to its
    string representation.

    Args:
        t (Union[Type[Any], Tuple[Type[Any], ...]]):
            The type or tuple of types for which to obtain the name.

    Returns:
        str: The name of the type if available, otherwise its string representation. For a tuple
             of types, a comma-separated list of names is returned.
    """
    if isinstance(t, tuple):
        return ', '.join(map(str, t))

    try:
        return t.__name__
    except AttributeError:
        return str(t)

def get_real_types(*arg_types: Type) -> list[Tuple[Type, ...]]:
    """
        Extract concrete type arguments from one or more type hints.

        For each type hint provided in `arg_types`, this function retrieves its type arguments using `get_args()`
        and filters out any type variables (`TypeVar`). If no type arguments are found, the original type hint
        is returned as a singleton tuple.

        Examples:
            >>> from typing import List, Tuple
            >>> get_real_types(List[int], Tuple[str, float], int)
            [(<class 'int'>,), (<class 'str'>, <class 'float'>), (<class 'int'>,)]

        Args:
            *arg_types (Type): One or more type hints, which may be generic (e.g., List[int]) or concrete types.

        Returns:
            list[Tuple[Type, ...]]:
                A list of tuples where each tuple contains the concrete type arguments extracted from the corresponding
                type hint. If a type hint has no type arguments, the tuple will contain the type hint itself.
        """
    result = []

    for expected_type in arg_types:
        types = tuple(t for t in get_args(expected_type) if not isinstance(t, TypeVar))

        if not types:
            types = (expected_type,)

        result.append(types)

    return result