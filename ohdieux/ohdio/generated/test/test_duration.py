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

from ohdieux.ohdio.generated.models.duration import Duration

class TestDuration(unittest.TestCase):
    """Duration unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Duration:
        """Test Duration
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Duration`
        """
        model = Duration()
        if include_optional:
            return Duration(
                duration_in_seconds = 1.337
            )
        else:
            return Duration(
                duration_in_seconds = 1.337,
        )
        """

    def testDuration(self):
        """Test Duration"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
