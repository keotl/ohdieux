# coding: utf-8

"""
    ohdieux-api-spec

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest
import datetime

from ohdieux.ohdio.generated.models.pagination import Pagination

class TestPagination(unittest.TestCase):
    """Pagination unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Pagination:
        """Test Pagination
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Pagination`
        """
        model = Pagination()
        if include_optional:
            return Pagination(
                total_number_of_items = 1.337,
                previous_page_url = '',
                page_size = 1.337,
                page_number = 1.337,
                page_max_length = 1.337,
                next_page_url = ''
            )
        else:
            return Pagination(
                total_number_of_items = 1.337,
                previous_page_url = '',
                page_size = 1.337,
                page_number = 1.337,
                page_max_length = 1.337,
                next_page_url = '',
        )
        """

    def testPagination(self):
        """Test Pagination"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
