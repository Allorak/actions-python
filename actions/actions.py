from typing import Callable, List, TypeVar, get_args, Type, get_type_hints
import inspect

from .utils import is_compatible, type_name

Args = TypeVar('Args')

class Action:
    """
    Represents an action that can connect handlers and invoke them with specified argument types.
    Handlers are validated to ensure their argument types match the expected types when connected or invoked.
    """
    def __init__(self, *arg_types: Type) -> None:
        """
        Initializes the action with the expected argument types for handlers.

        Args:
            arg_types: One or more types that the action handlers should expect as arguments.
        """
        self._arg_types = arg_types

        self._handlers: List[Callable[..., None]] = []

    def connect(self, handler: Callable[..., None]) -> None:
        """
        Connects a handler (callback) to the action and validates its signature against the expected argument types.

        Args:
            handler: A callable to be connected to the action. It should match the expected argument types.

        Raises:
            TypeError: If the handler's signature does not match the expected argument types.
        """
        if not callable(handler):
            raise TypeError("Connected handler must be a callable.")

        signature = inspect.signature(handler)
        type_hints = get_type_hints(handler)
        handler_params = [type_hints.get(param.name, inspect._empty) for param in signature.parameters.values()]

        if len(handler_params) != len(self._arg_types):
            raise TypeError(
                f"Handler argument count mismatch. Expected {len(self._arg_types)}, got {len(handler_params)}."
            )

        for handler_type, expected_type in zip(handler_params, self._arg_types):
            if handler_type.annotation is inspect._empty:
                raise TypeError(f"Parameter ('{handler_type.name}') of action handler has no type annotation.")
            if is_compatible(handler_type, expected_type):
                raise TypeError(
                    f"Handler argument type mismatch. Expected '{type_name(expected_type)}', "
                    f"got '{type_name(handler_type)}'."
                )

        self._handlers.append(handler)

    def invoke(self, *args: Args) -> None:
        """
        Invokes all connected handlers with the provided arguments, ensuring type validation before calling.

        Args:
            args: Arguments to pass to the connected handlers. These must match the expected types.

        Raises:
            TypeError: If the arguments passed do not match the expected types.
        """
        if len(args) != len(self._arg_types):
            raise TypeError(
                f"Call argument count mismatch. Expected {len(self._arg_types)}, got {len(args)}."
            )

        for arg, expected_type in zip(args, self._arg_types):
            concrete_types = tuple(t for t in get_args(expected_type) if not isinstance(t, TypeVar))

            if not concrete_types:
                concrete_types = (expected_type,)

            if not any(isinstance(arg, t) for t in concrete_types):
                raise TypeError(f"Call argument type mismatch. Expected '{type_name(expected_type)}',"
                                f" got '{type_name(type(arg))}'.")

        for handler in self._handlers:
            handler(*args)
