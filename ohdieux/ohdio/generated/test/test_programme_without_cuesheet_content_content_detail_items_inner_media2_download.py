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

from ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner_media2_download import ProgrammeWithoutCuesheetContentContentDetailItemsInnerMedia2Download

class TestProgrammeWithoutCuesheetContentContentDetailItemsInnerMedia2Download(unittest.TestCase):
    """ProgrammeWithoutCuesheetContentContentDetailItemsInnerMedia2Download unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ProgrammeWithoutCuesheetContentContentDetailItemsInnerMedia2Download:
        """Test ProgrammeWithoutCuesheetContentContentDetailItemsInnerMedia2Download
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ProgrammeWithoutCuesheetContentContentDetailItemsInnerMedia2Download`
        """
        model = ProgrammeWithoutCuesheetContentContentDetailItemsInnerMedia2Download()
        if include_optional:
            return ProgrammeWithoutCuesheetContentContentDetailItemsInnerMedia2Download(
                formatted_file_size = '',
                media_id = '',
                url = '',
                file_size_in_bytes = 1.337
            )
        else:
            return ProgrammeWithoutCuesheetContentContentDetailItemsInnerMedia2Download(
                file_size_in_bytes = 1.337,
        )
        """

    def testProgrammeWithoutCuesheetContentContentDetailItemsInnerMedia2Download(self):
        """Test ProgrammeWithoutCuesheetContentContentDetailItemsInnerMedia2Download"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
