import enum

class TypeSafetyLevel(enum.Enum):
    NONE = "NONE"
    WARNING = "WARNING"
    ERROR = "ERROR"