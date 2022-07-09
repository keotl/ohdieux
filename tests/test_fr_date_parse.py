from datetime import datetime
import unittest
from unittest import mock

from ohdieux.util.dateparse import parse_fr_date

class FrDateParseTests(unittest.TestCase):

    def test_parse_date(self):
        for expected, formatted in [
                (datetime(2022, 4, 2), "2 avril 2022"),
                (datetime(2022, 3, 26), "26 mars 2022")
        ]:
            actual = parse_fr_date(formatted)

            self.assertEqual(expected, actual)
