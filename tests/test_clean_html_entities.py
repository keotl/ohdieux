import unittest

from ohdieux.ohdio.parse_utils import clean


class CleanHtmlEntitiesTests(unittest.TestCase):

    def test_evaluates_html_special_entities(self):
        result = clean("&#x27;")

        self.assertEqual("'", result)
