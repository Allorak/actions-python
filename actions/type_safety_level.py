import enum

class TypeSafetyLevel(enum.Enum):
    """
    Enum representing different levels of type safety enforcement.

    Attributes:
        NONE (str): No type safety checks are enforced.
        WARNING (str): Type safety issues result in warnings.
        ERROR (str): Type safety issues are treated as errors.
    """
    NONE = "NONE"
    WARNING = "WARNING"
    ERROR = "ERROR"