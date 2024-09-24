import unittest
from gator.engine import Environment, Template

class TestTemplate(unittest.TestCase):

    def test_code_execution(self):
        env = Environment()
        env.var["test_var"] = "test_val"

        assert Template.from_str("{{ 1 }}").render(env) == "1"
        assert Template.from_str("test {{ 1 }}").render(env) == "test 1"
        assert Template.from_str("{{ 1 + 1 }}").render(env) == "2"
        assert Template.from_str("{{ $test_var }}").render(env) == "test_val"
        assert Template.from_str("test {{ $test_var }}").render(env) == "test test_val"
        assert Template.from_str("{{ 1 if $test_var else 0 }}").render(env) == "1"

        assert Template.from_str("<exec></exec>").render(env) == ""
        assert Template.from_str("<exec>print('test')</exec>").render(env) == "test"
        assert Template.from_str("<exec>print($test_var)</exec>").render(env) == "test_val"

if __name__ == '__main__':
    unittest.main()
