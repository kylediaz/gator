import unittest
from gator.engine import Environment, Template, CONTENT

class TestRenderer(unittest.TestCase):

    def test_template_render(self):
        env = Environment()

        env.template["t"] = Template.from_str("[t content]")
        assert Template.from_str("<template t='t'></template>").render(env) == "[t content]"

        env.var[CONTENT] = "[content]"
        assert Template.from_str("[t]<content />[t]").render(env) == '[t][content][t]'
        env.var[CONTENT] = None

        env.template["tc"] = Template.from_str("[t]<content/>[t]")
        assert Template.from_str("[T]<template t='tc'>[content]</template>[T]").render(env) == "[T][t][content][t][T]"

    def test_template_vars(self):
        env = Environment()

        env.template["t"] = Template.from_str("[key={{ $value }}]")
        assert Template.from_str("[t]<template t='t', value='value'></template>[t]").render(env) == "[t][key=value][t]"

if __name__ == '__main__':
    unittest.main()
