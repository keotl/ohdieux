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

from ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner_playlist_item_id import ProgrammeWithoutCuesheetContentContentDetailItemsInnerPlaylistItemId

class TestProgrammeWithoutCuesheetContentContentDetailItemsInnerPlaylistItemId(unittest.TestCase):
    """ProgrammeWithoutCuesheetContentContentDetailItemsInnerPlaylistItemId unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ProgrammeWithoutCuesheetContentContentDetailItemsInnerPlaylistItemId:
        """Test ProgrammeWithoutCuesheetContentContentDetailItemsInnerPlaylistItemId
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ProgrammeWithoutCuesheetContentContentDetailItemsInnerPlaylistItemId`
        """
        model = ProgrammeWithoutCuesheetContentContentDetailItemsInnerPlaylistItemId()
        if include_optional:
            return ProgrammeWithoutCuesheetContentContentDetailItemsInnerPlaylistItemId(
                title = '',
                media_id = '',
                has_transcription = True,
                global_id2 = ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner_playlist_item_id_global_id2.ProgrammeWithoutCuesheet_content_contentDetail_items_inner_playlistItemId_globalId2(
                    id = '', 
                    content_type = null, ),
                global_id = ''
            )
        else:
            return ProgrammeWithoutCuesheetContentContentDetailItemsInnerPlaylistItemId(
                title = '',
                has_transcription = True,
                global_id2 = ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner_playlist_item_id_global_id2.ProgrammeWithoutCuesheet_content_contentDetail_items_inner_playlistItemId_globalId2(
                    id = '', 
                    content_type = null, ),
                global_id = '',
        )
        """

    def testProgrammeWithoutCuesheetContentContentDetailItemsInnerPlaylistItemId(self):
        """Test ProgrammeWithoutCuesheetContentContentDetailItemsInnerPlaylistItemId"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
