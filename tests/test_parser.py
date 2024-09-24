import unittest
from gator.engine import Environment, Template

class TestParser(unittest.TestCase):

    def test_basic_tag(self):
        Template.from_str("<template>content</template>")
        Template.from_str("<exec>content</exec>")
        Template.from_str("{{ 1 }}")
        Template.from_str("{{ $content }}")
        Template.from_str("<content />")

    def test_with_tags_inside_template_tag(self):
        Template.from_str(
            """
            <template>
                content
                {{ $content }}
                <exec>
                    print("content")
                </exec>
                <content />
            </template>
            """
        )

    def test_with_empty_tag(self):
        Template.from_str("<template></template>")
        Template.from_str("<exec></exec>")

if __name__ == '__main__':
    unittest.main()
