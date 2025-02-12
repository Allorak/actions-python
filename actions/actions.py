from typing import Callable, List, TypeVar, get_args, Type, get_type_hints, Optional
import inspect

from loguru import logger

from .utils import is_compatible, type_name
from .type_safety_level import TypeSafetyLevel

Args = TypeVar('Args')

#TODO: тесты; обработка параметров при вызове, если нет тайп хинтов

class Action:
    """
    Represents an action that can connect handlers and invoke them with specified argument types.
    Handlers are validated to ensure their argument types match the expected types when connected or invoked.
    """
    def __init__(self, *arg_types: Type, type_safety: TypeSafetyLevel = TypeSafetyLevel.ERROR) -> None:
        """
        Initializes the action with the expected argument types for handlers.

        Args:
            arg_types: One or more types that the action handlers should expect as arguments.
        """
        self._arg_types = arg_types
        self._type_safety = type_safety

        self._handlers: List[Callable[..., None]] = []

    def connect(self, handler: Callable[..., None]) -> None:
        """
        Connects a handler (callback) to the action and validates its signature against the expected argument types.

        Args:
            handler: A callable to be connected to the action. It should match the expected argument types.

        Raises:
            TypeError: If the handler's signature does not match the expected argument types.
        """

        if self._type_safety != TypeSafetyLevel.NONE:
            types_compatible: bool
            error: TypeError
            types_compatible, error= self._check_connect_types(handler)

            self._process_type_check_result(types_compatible, error)

        self._handlers.append(handler)

    def disconnect(self, handler: Callable[..., None]) -> None:
        """
        Disconnects a handler (callback) from the action.

        Args:
            handler: A callable to be disconnected from the action. It should be connected first.

        Raises:
            ValueError: If the handler is not connected to the action.
        """
        try:
            self._handlers.remove(handler)
        except ValueError:
            raise ValueError("Can't disconnect handler: handler is not connected..")


    def invoke(self, *args: Args) -> None:
        """
        Invokes all connected handlers with the provided arguments, ensuring type validation before calling.

        Args:
            args: Arguments to pass to the connected handlers. These must match the expected types.

        Raises:
            TypeError: If the arguments passed do not match the expected types.
        """
        if self._type_safety != TypeSafetyLevel.NONE:
            types_compatible: bool
            error: TypeError
            types_compatible, error= self._check_invoke_types(*args)

            self._process_type_check_result(types_compatible, error)

        for handler in self._handlers:
            handler(*args)

    def _check_connect_types(self, handler: Callable[..., None]) -> (bool, Optional[TypeError]):
        if not callable(handler):
            return False, TypeError("Connected handler must be a callable.")

        signature = inspect.signature(handler)
        type_hints = get_type_hints(handler)
        handler_params = {param.name: type_hints.get(param.name, inspect._empty)
                          for param in signature.parameters.values()}

        param_names = list(handler_params.keys())
        param_types = list(handler_params.values())

        if len(handler_params) != len(self._arg_types):
            return False, TypeError(f"Handler argument count mismatch. "
                                    f"Expected {len(self._arg_types)}, got {len(handler_params)}.")

        for param_name, handler_type, expected_type in zip(param_names, param_types, self._arg_types):
            if handler_type is inspect._empty:
                return False, TypeError(f"Parameter ('{param_name}') of action handler has no type annotation.")
            if not is_compatible(handler_type, expected_type):
                return False, TypeError(f"Handler argument type mismatch. "
                                        f"Expected '{type_name(expected_type)}', got '{type_name(handler_type)}'.")

        return True, None

    def _check_invoke_types(self, *args: Args) -> (bool, Optional[TypeError]):
        if len(args) != len(self._arg_types):
            return False, TypeError(
                f"Call argument count mismatch. Expected {len(self._arg_types)}, got {len(args)}."
            )

        for arg, expected_type in zip(args, self._arg_types):
            concrete_types = tuple(t for t in get_args(expected_type) if not isinstance(t, TypeVar))

            if not concrete_types:
                concrete_types = (expected_type,)

            if not any(isinstance(arg, t) for t in concrete_types):
                return False, TypeError(f"Call argument type mismatch. Expected '{type_name(expected_type)}',"
                                f" got '{type_name(type(arg))}'.")

        return True, None

    def _process_type_check_result(self, types_compatible: bool ,error: TypeError) -> None:
        if types_compatible:
            return

        if self._type_safety == TypeSafetyLevel.NONE:
            return

        if self._type_safety == TypeSafetyLevel.WARNING:
            logger.warning(str(error))
            return

        if self._type_safety == TypeSafetyLevel.ERROR:
            raise error
