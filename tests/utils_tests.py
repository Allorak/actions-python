import unittest

from actions.utils import is_compatible_type, type_name, get_real_types


class TestGetRealTypes(unittest.TestCase):
    def test_simple_type(self):
        """
        Test that get_real_types returns a singleton tuple containing the type itself
        when no type arguments are present.
        """
        result = get_real_types(int)
        self.assertEqual(result, [(int,)])

    def test_generic_type(self):
        """
        Test that get_real_types extracts the concrete type argument from a generic type.

        For example, for List[int] it should return [(int,)].
        """
        from typing import List
        result = get_real_types(List[int])
        self.assertEqual(result, [(int,)])

    def test_union_type(self):
        """
        Test that get_real_types returns a tuple of all member types when provided a Union.

        For example, for Union[int, str] it should return [(int, str)].
        """
        from typing import Union
        result = get_real_types(Union[int, str])
        self.assertEqual(result, [(int, str)])

    def test_multiple_args(self):
        """
        Test that get_real_types processes multiple type hints at once,
        returning a list of tuples with the concrete types extracted.
        """
        from typing import List, Union
        result = get_real_types(int, List[str], Union[int, float])
        self.assertEqual(result, [(int,), (str,), (int, float)])


class TestIsCompatibleType(unittest.TestCase):
    def test_any(self):
        """
        Test that if the valid type is Any, any type is considered compatible.
        """
        from typing import Any
        self.assertTrue(is_compatible_type(int, (Any,)))
        self.assertTrue(is_compatible_type(str, (Any,)))

    def test_simple_types(self):
        """
        Test that is_compatible_type correctly handles simple type equality.
        """
        self.assertTrue(is_compatible_type(int, (int,)))
        self.assertFalse(is_compatible_type(int, (str,)))
        self.assertTrue(is_compatible_type(str, (str,)))

    def test_union(self):
        """
        Test that is_compatible_type correctly resolves Union types.
        """
        from typing import Union
        self.assertTrue(is_compatible_type(int, (Union[int, str],)))
        self.assertTrue(is_compatible_type(str, (Union[int, str],)))
        self.assertFalse(is_compatible_type(float, (Union[int, str],)))

    def test_annotated(self):
        """
        Test that is_compatible_type properly handles Annotated types by checking compatibility
        based on their underlying base type.
        """
        from typing import Annotated
        self.assertTrue(is_compatible_type(int, (Annotated[int, "meta"],)))
        self.assertFalse(is_compatible_type(str, (Annotated[int, "meta"],)))

    def test_callable(self):
        """
        Test that is_compatible_type correctly compares callable type hints.

        This includes:
          - Comparing identical callable types.
          - Recognizing callables with the same signature.
          - Detecting mismatches in argument types.
          - Handling callables with Ellipsis (any argument list).
        """
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
        """
        Test that is_compatible_type handles TypeVar instances by checking compatibility with their bounds.
        """
        from typing import TypeVar
        T = TypeVar('T', bound=int)
        self.assertTrue(is_compatible_type(int, (T,)))
        self.assertFalse(is_compatible_type(str, (T,)))

    def test_newtype(self):
        """
        Test that is_compatible_type correctly distinguishes between a NewType and its underlying type.

        The NewType itself should be compatible with itself, but the underlying type should not be
        considered compatible with the NewType.
        """
        from typing import NewType
        UserId = NewType("UserId", int)
        self.assertTrue(is_compatible_type(UserId, (UserId,)))
        self.assertFalse(is_compatible_type(int, (UserId,)))


class TestTypeName(unittest.TestCase):
    def test_single_type(self):
        """
        Test that type_name returns the __name__ attribute for a single type.
        """
        self.assertEqual(type_name(int), 'int')

    def test_tuple_of_types(self):
        """
        Test that type_name returns a comma-separated string of type names when provided a tuple of types.
        """
        result = type_name((int, str))
        self.assertIn("int", result)
        self.assertIn("str", result)

    def test_type_without_name(self):
        """
        Test that type_name falls back to the string representation of the type if __name__ is not available.

        This is simulated by using a metaclass that raises an AttributeError when __name__ is accessed.
        """

        class NoNameMeta(type):
            @property
            def __name__(cls):
                raise AttributeError("No __name__ available")

        class Dummy(metaclass=NoNameMeta):
            pass

        result = type_name(Dummy)
        self.assertEqual(result, str(Dummy))

    def test_types_from_get_real_types(self):
        """
        Test that type_name works correctly on types returned by get_real_types.

        For example, given a Union type, get_real_types returns a tuple of member types and
        type_name should generate a string that includes the names of those types.
        """
        from typing import Union
        types = get_real_types(Union[int, str])
        result = type_name(types[0])
        self.assertIn("int", result)
        self.assertIn("str", result)

if __name__ == '__main__':
    unittest.main()
