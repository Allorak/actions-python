from typing import Callable, Generic, List, Tuple, TypeVar, get_args, get_type_hints
import inspect

Args = TypeVar("Args")


class Action(Generic[Args]):
    """
    A generic action class
    """
    def __init__(self) -> None:
        """Initialize the action and infer argument types."""
        self._handlers: List[Callable[..., None]] = []
        self._arg_types = get_type_hints(self).get("Args", Tuple)

    def connect(self, handler: Callable[..., None]) -> None:
        """
        Connect a handler (callback) to the action. Validates that the handler's signature matches the expected types.

        Args:
            handler: A callable to connect to this action.

        Raises:
            TypeError: If the handler's signature does not match the expected argument types.
        """
        if not callable(handler):
            raise TypeError("Connected handler must be a callable.")

        signature = inspect.signature(handler)
        handler_params = [param.annotation for param in signature.parameters.values()]

        if len(handler_params) != len(self._arg_types):
            raise TypeError(
                f"Handler argument count mismatch. Expected {len(self._arg_types)}, got {len(handler_params)}."
            )

        for handler_type, expected_type in zip(handler_params, self._arg_types):
            if handler_type != expected_type:
                raise TypeError(
                    f"Handler argument type mismatch. Expected '{expected_type.__name__}', "
                    f"got '{handler_type.__name__}'."
                )

        self._handlers.append(handler)

    def invoke(self, *args: Args) -> None:
        """
        Call the action, invoking all connected handlers. Validates argument types before calling.

        Args:
            args: Arguments to pass to the connected handlers.

        Raises:
            TypeError: If called arguments do not match the expected types.
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
                raise TypeError(f"Call argument type mismatch. Expected '{expected_type}', got '{type(arg).__name__}'.")

        for handler in self._handlers:
            handler(*args)
