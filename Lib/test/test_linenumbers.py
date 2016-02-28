"""
Tests for attributing code to line numbers
"""

import sys
import traceback
import unittest


def boom(*args, **kwargs):
    raise RuntimeError()

def dummy(*args, **kwargs):
    pass


class TestPEP380Operation(unittest.TestCase):
    def expect_line(self, f, expected_relative_line, depth=1):
        """Expect an exception in f at the given line offset."""
        try:
            f()
        except Exception:
            frames = traceback.extract_tb(sys.exc_info()[2])
            line = frames[depth][1]
            relative_line = line - f.__code__.co_firstlineno
            self.assertEqual(relative_line, expected_relative_line)
        else:
            self.fail("expected an exception")

    def test_call(self):
        def f():
            boom(
                1,
                x=2,
                )
        self.expect_line(f, 3) # want 1

        def f():
            boom \
                (
                1,
                x=2,
                )
        self.expect_line(f, 4) # want 2

        def f():
            dummy(
                1,
                boom(),
                x=3,
                )
        self.expect_line(f, 3)

    def test_comprehensions(self):
        def f():
            [
                boom()
                for x in range(2)
                if x
            ]
        self.expect_line(f, 2, depth=2)

        def f():
            {
                x: boom()
                for x in range(2)
                if x
            }
        self.expect_line(f, 2, depth=2)

        def f():
            {
                boom()
                for x in range(2)
                if x
            }
        self.expect_line(f, 2, depth=2)

    def test_operators(self):
        class C:
            def __neg__(self):
                boom()

            def __add__(self, other):
                boom()

            def __rsub__(self, other):
                boom()

            def __imul__(self, other):
                boom()

            def __lt__(self, other):
                boom()

        def f():
            x = (
                -
                C())
        self.expect_line(f, 3) # want 2

        def f():
            x = (C()
                 +
                 None
                 )
        self.expect_line(f, 3) # want 2

        def f():
            x = (None
                 -
                 C()
                 )
        self.expect_line(f, 3) # want 2

        def f():
            x = C()
            x \
                *= (
                C())
        self.expect_line(f, 4) # want 3

        def f():
            c = C()
            (c
             is
             c
             <
             C()
             )
        self.expect_line(f, 6) # want 5

    # TODO getitem, getattr
    # TODO with, for/else, try/except/else/finally


if __name__ == '__main__':
    unittest.main()
