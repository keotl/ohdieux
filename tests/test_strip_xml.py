import unittest

from ohdieux.util.xml import unsafe_strip_tags


class StripXmlTests(unittest.TestCase):

    def test_strip_tags(self):
        for text, expected in [("<em>Emphasis text</em>", "Emphasis text"),
                               ("<em>text", "text")]:
            actual = unsafe_strip_tags(text)
            self.assertEqual(expected, actual)
