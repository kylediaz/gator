import unittest
from gator.engine import Environment, Template

class TestTemplate(unittest.TestCase):

    def test_code_execution(self):
        env = Environment()
        env.var["test_var"] = "test_val"

        self.assertEqual(Template.from_str("{{ 1 }}").render_to_str(env), "1")
        self.assertEqual(Template.from_str("test {{ 1 }}").render_to_str(env), "test 1")
        self.assertEqual(Template.from_str("{{ 1 + 1 }}").render_to_str(env), "2")
        self.assertEqual(Template.from_str("{{ $test_var }}").render_to_str(env), "test_val")
        self.assertEqual(Template.from_str("test {{ $test_var }}").render_to_str(env), "test test_val")
        self.assertEqual(Template.from_str("{{ 1 if $test_var else 0 }}").render_to_str(env), "1")

if __name__ == '__main__':
    unittest.main()
