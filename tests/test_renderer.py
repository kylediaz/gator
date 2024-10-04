import unittest
from gator.engine import Environment, Template, CONTENT

class Testrender_to_strer(unittest.TestCase):

    def test_template_render_to_str(self):
        env = Environment()

        env.template["t"] = Template.from_str("[t content]")
        self.assertEqual(Template.from_str("<template t='t'></template>").render_to_str(env), "[t content]")

        self.assertEqual(Template.from_str("[t]<content />[t]").render_to_str(env, content='[content]'), '[t][content][t]')

        env.template["tc"] = Template.from_str("[t]<content/>[t]")
        self.assertEqual(
            Template.from_str("[T]<template t='tc'>[content]</template>[T]").render_to_str(env, content='[content]'),
            "[T][t][content][t][T]"
        )

    def test_template_vars(self):
        env = Environment()

        env.template["t"] = Template.from_str("[key={{ $value }}]")
        self.assertEqual(Template.from_str("[t]<template t='t', value='value'></template>[t]").render_to_str(env), "[t][key=value][t]")

if __name__ == '__main__':
    unittest.main()
