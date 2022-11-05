from datetime import datetime
import unittest
from unittest import mock

from ohdieux.util.dateparse import parse_fr_date, extract_tentative_date


class FrDateParseTests(unittest.TestCase):

    def test_parse_date(self):
        for expected, formatted in [
                (datetime(2022, 4, 2), "2 avril 2022"),
                (datetime(2022, 3, 26), "26 mars 2022")
        ]:
            actual = parse_fr_date(formatted)

            self.assertEqual(expected, actual)

    def test_infer_date(self):
        for expected, formatted in [
                (datetime(2022, 9, 14), "Rattrapage du mercredi 14 sept. 2022 : Alain Rayes, Marie-Louise Arsenault et Gabrielle Côté"),
                (datetime(2022, 3, 26), "26 mars 2022"),
                (datetime(2022, 11, 1), "1er nov. 2022"),
        ]:
            actual = extract_tentative_date(formatted)

            self.assertEqual(expected, actual)
