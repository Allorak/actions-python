import unittest
from actions import Action, TypeSafetyLevel

class TestAction(unittest.TestCase):
    def test_valid_handler_and_invoke_error_mode(self):
        """Test connecting a valid handler and invoking it (TypeSafetyLevel.ERROR)."""
        action = Action(int, type_safety=TypeSafetyLevel.ERROR)
        results = []

        def handler(a: int) -> None:
            results.append(a)

        action.connect(handler)
        action.invoke(42)

        self.assertEqual(results, [42])

    def test_invalid_handler_missing_annotation_error_mode(self):
        """Test that connecting a handler missing type annotations raises TypeError in ERROR mode."""
        action = Action(int, type_safety=TypeSafetyLevel.ERROR)

        def handler(a) -> None:
            pass

        with self.assertRaises(TypeError) as context:
            action.connect(handler)
        self.assertIn("has no type annotation", str(context.exception))

    def test_invalid_handler_argument_count_error_mode(self):
        """Test that connecting a handler with mismatched argument count raises TypeError."""
        action = Action(int, str, type_safety=TypeSafetyLevel.ERROR)

        def handler(a: int) -> None:
            pass

        with self.assertRaises(TypeError) as context:
            action.connect(handler)
        self.assertIn("argument count mismatch", str(context.exception))

    def test_invoke_wrong_argument_error_mode(self):
        """Test that invoking with wrong argument type raises TypeError in ERROR mode."""
        action = Action(int, type_safety=TypeSafetyLevel.ERROR)
        called = False

        def handler(a: int) -> None:
            nonlocal called
            called = True

        action.connect(handler)

        with self.assertRaises(TypeError) as context:
            action.invoke("not an int")

        self.assertIn("Call argument type mismatch", str(context.exception))
        self.assertFalse(called, "Handler should not be called when type check fails.")

    def test_disconnect_handler(self):
        """Test disconnecting a handler and that disconnecting a non-connected handler raises ValueError."""
        action = Action(int, type_safety=TypeSafetyLevel.ERROR)

        def handler(a: int) -> None:
            pass

        action.connect(handler)
        self.assertIn(handler, action._handlers)

        action.disconnect(handler)
        self.assertNotIn(handler, action._handlers)

        with self.assertRaises(ValueError) as context:
            action.disconnect(handler)

        self.assertIn("not connected", str(context.exception))

    def test_warning_mode_connect(self):
        """Test that in WARNING mode, a handler with missing annotation is connected (after logging a warning)."""
        action = Action(int, type_safety=TypeSafetyLevel.WARNING)

        def handler(a) -> None:
            pass

        try:
            action.connect(handler)
        except Exception as e:
            self.fail(f"Connect raised an exception in WARNING mode: {e}")

        self.assertIn(handler, action._handlers)

    def test_warning_mode_invoke(self):
        """
        Test that in WARNING mode, invoking with a wrong argument type logs a warning
        but still calls the handler.
        """
        action = Action(int, type_safety=TypeSafetyLevel.WARNING)
        results = []

        def handler(a: int) -> None:
            results.append(a)

        action.connect(handler)
        try:
            action.invoke("wrong type")
        except Exception as e:
            self.fail(f"Invoke raised an exception in WARNING mode: {e}")

        self.assertEqual(results, ["wrong type"])

    def test_none_mode_allows_mismatch(self):
        """Test that in NONE mode, type checks are skipped and any handler/arguments are accepted."""
        action = Action(int, type_safety=TypeSafetyLevel.NONE)
        results = []

        def handler(a) -> None:
            results.append(a)

        action.connect(handler)

        action.invoke("anything")
        self.assertEqual(results, ["anything"])

if __name__ == '__main__':
    unittest.main()
