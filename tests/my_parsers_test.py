import unittest
import ast
from io import StringIO
from contextlib import redirect_stdout
from typing import Callable, List
from src.my_parsers import GenericFinder, RecursionDetector, get_all_methods, submission_parser


class TestGenericFinder(unittest.TestCase):
    def test_generic_finder(self):
        code = '''
def foo():
  x = 5
  y = x + 2
  return y
                '''
        tree = ast.parse(code)
        visitor = GenericFinder('Assign')
        visitor.visit(tree)

        self.assertEqual(len(visitor.found), 2)
        self.assertIsInstance(visitor.found[0], ast.Assign)
        self.assertIsInstance(visitor.found[1], ast.Assign)


class TestRecursionDetector(unittest.TestCase):
    def test_recursive_detection(self):
        code = '''
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
                '''
        tree = ast.parse(code)
        visitor = RecursionDetector()
        visitor.visit(tree)

        self.assertTrue(visitor.recursive)

    def test_non_recursive_detection(self):
        code = '''
def add(x, y):
    return x + y
                '''
        tree = ast.parse(code)
        visitor = RecursionDetector()
        visitor.visit(tree)

        self.assertFalse(visitor.recursive)


class TestGetAllMethods(unittest.TestCase):
    def test_get_all_methods(self):
        def foo():
            pass

        def bar():
            pass

        locals_dict = {"__builtins__": None, "foo": foo, "bar": bar}
        functions = get_all_methods(locals_dict)

        self.assertEqual(len(functions), 2)
        self.assertIn('foo', functions)
        self.assertIn('bar', functions)


class TestSubmissionParser(unittest.TestCase):
    def test_submission_parser(self):
        code = '''
def foo():
    x = 5
    y = x + 2
    return y

def bar():
    a = 10
    b = a * 3
    return b
                '''
                
        elements = [
            {"name": "Assign", "occurences": []},
            {"name": "Return", "occurences": []}
        ]

        submission_parser(code, elements)

        self.assertEqual(len(elements[0]['occurences']), 4)
        self.assertEqual(len(elements[1]['occurences']), 2)
        self.assertEqual(elements[0]['occurences'], [3, 4, 8, 9])
        self.assertEqual(elements[1]['occurences'], [5, 10])


if __name__ == '__main__':
    unittest.main()
