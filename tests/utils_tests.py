import unittest

from actions.utils import is_compatible_type, type_name, get_real_types

class TestGetRealTypes(unittest.TestCase):
    def test_simple_type(self):
        result = get_real_types(int)
        self.assertEqual(result, [(int,)])

    def test_generic_type(self):
        from typing import List

        result = get_real_types(List[int])
        self.assertEqual(result, [(int,)])

    def test_union_type(self):
        from typing import Union

        result = get_real_types(Union[int, str])
        self.assertEqual(result, [(int, str)])

    def test_multiple_args(self):
        from typing import List, Union

        result = get_real_types(int, List[str], Union[int, float])
        self.assertEqual(result, [(int,), (str,), (int, float)])

class TestIsCompatibleType(unittest.TestCase):
    def test_any(self):
        from typing import Any

        self.assertTrue(is_compatible_type(int, (Any,)))
        self.assertTrue(is_compatible_type(str, (Any,)))

    def test_simple_types(self):
        self.assertTrue(is_compatible_type(int, (int,)))
        self.assertFalse(is_compatible_type(int, (str,)))
        self.assertTrue(is_compatible_type(str, (str,)))

    def test_union(self):
        from typing import Union

        self.assertTrue(is_compatible_type(int, (Union[int, str],)))
        self.assertTrue(is_compatible_type(str, (Union[int, str],)))
        self.assertFalse(is_compatible_type(float, (Union[int, str],)))

    def test_annotated(self):
        from typing import Annotated

        self.assertTrue(is_compatible_type(int, (Annotated[int, "meta"],)))
        self.assertFalse(is_compatible_type(str, (Annotated[int, "meta"],)))

    def test_callable(self):
        from typing import Callable

        callable_type1 = Callable[[int], str]
        callable_type2 = Callable[[int], str]
        callable_type3 = Callable[[str], str]
        callable_type4 = Callable[..., str]

        self.assertTrue(is_compatible_type(callable_type1, (callable_type1,)))
        self.assertTrue(is_compatible_type(callable_type1, (callable_type2,)))
        self.assertFalse(is_compatible_type(callable_type1, (callable_type3,)))
        self.assertTrue(is_compatible_type(callable_type1, (callable_type4,)))
        self.assertTrue(is_compatible_type(callable_type4, (callable_type1,)))

    def test_typevar(self):
        from typing import TypeVar
        T = TypeVar('T', bound=int)

        self.assertTrue(is_compatible_type(int, (T,)))
        self.assertFalse(is_compatible_type(str, (T,)))

    def test_newtype(self):
        from typing import NewType

        UserId = NewType("UserId", int)
        self.assertTrue(is_compatible_type(UserId, (UserId,)))
        self.assertFalse(is_compatible_type(int, (UserId,)))

class TestTypeName(unittest.TestCase):
    def test_single_type(self):
        self.assertEqual(type_name(int), 'int')

    def test_tuple_of_types(self):
        result = type_name((int, str))

        self.assertIn("int", result)
        self.assertIn("str", result)

    def test_type_without_name(self):
        class NoNameMeta(type):
            @property
            def __name__(cls):
                raise AttributeError("No __name__ available")

        class Dummy(metaclass=NoNameMeta):
            pass

        result = type_name(Dummy)
        self.assertEqual(result, str(Dummy))

    def test_types_from_get_real_types(self):
        from typing import Union

        types = get_real_types(Union[int, str])
        result = type_name(types[0])

        self.assertIn("int", result)
        self.assertIn("str", result)

if __name__ == '__main__':
    unittest.main()
