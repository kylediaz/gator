from types import FunctionType
import unittest
import gator.code_executor as ce

class TestCodeExecutor(unittest.TestCase):
    def test_code_preprocessor(self):
        preprocess_code = ce.__dict__.get('__preprocess_code')
        assert type(preprocess_code) == FunctionType

        self.assertEqual(preprocess_code('$var_name'), 'env.var["var_name"]')
        self.assertEqual(preprocess_code('"test" + $var_name'), '"test" + env.var["var_name"]')

    def test_indent_remover(self):
        remove_indent = ce.__dict__.get('__remove_indent')
        assert type(remove_indent) == FunctionType

        self.assertEqual(remove_indent("print('hi')"), "print('hi')")

        self.assertEqual(remove_indent("line 1\n    line2"), "line 1\n    line2")
        self.assertEqual(remove_indent("    line 1\n        line2"), "line 1\n    line2")
        self.assertEqual(remove_indent("\n    line 1\n        line2"), "\nline 1\n    line2")

        code = """
        line 1
            line 2
                line 3
            line 4
        line 5
        """
        res = remove_indent(code)
        self.assertEqual(res, "\nline 1\n    line 2\n        line 3\n    line 4\nline 5\n")
