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

from ohdieux.ohdio.generated.models.programme_without_cuesheet_header_picture import ProgrammeWithoutCuesheetHeaderPicture

class TestProgrammeWithoutCuesheetHeaderPicture(unittest.TestCase):
    """ProgrammeWithoutCuesheetHeaderPicture unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ProgrammeWithoutCuesheetHeaderPicture:
        """Test ProgrammeWithoutCuesheetHeaderPicture
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ProgrammeWithoutCuesheetHeaderPicture`
        """
        model = ProgrammeWithoutCuesheetHeaderPicture()
        if include_optional:
            return ProgrammeWithoutCuesheetHeaderPicture(
                url = ''
            )
        else:
            return ProgrammeWithoutCuesheetHeaderPicture(
                url = '',
        )
        """

    def testProgrammeWithoutCuesheetHeaderPicture(self):
        """Test ProgrammeWithoutCuesheetHeaderPicture"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()