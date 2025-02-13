from actions import Action
from actions.utils import is_compatible_type
from loguru import logger

if __name__ == '__main__':
    from typing import Callable

    logger.info("START")

    callable_type1 = Callable[[int], str]
    callable_type2 = Callable[[int], str]
    callable_type3 = Callable[[str], str]
    callable_type4 = Callable[..., str]

    is_compatible_type(callable_type1, (callable_type1,))
    is_compatible_type(callable_type1, (callable_type2,))
    is_compatible_type(callable_type1, (callable_type3,))
    is_compatible_type(callable_type1, (callable_type4,))
    is_compatible_type(callable_type4, (callable_type1,))