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

from ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail import ProgrammeWithoutCuesheetContentContentDetail

class TestProgrammeWithoutCuesheetContentContentDetail(unittest.TestCase):
    """ProgrammeWithoutCuesheetContentContentDetail unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ProgrammeWithoutCuesheetContentContentDetail:
        """Test ProgrammeWithoutCuesheetContentContentDetail
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ProgrammeWithoutCuesheetContentContentDetail`
        """
        model = ProgrammeWithoutCuesheetContentContentDetail()
        if include_optional:
            return ProgrammeWithoutCuesheetContentContentDetail(
                items = [
                    ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner.ProgrammeWithoutCuesheet_content_contentDetail_items_inner(
                        url = '', 
                        title = '', 
                        summary = '', 
                        playlist_item_id = ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner_playlist_item_id.ProgrammeWithoutCuesheet_content_contentDetail_items_inner_playlistItemId(
                            title = '', 
                            media_id = '', 
                            has_transcription = True, 
                            global_id2 = ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner_playlist_item_id_global_id2.ProgrammeWithoutCuesheet_content_contentDetail_items_inner_playlistItemId_globalId2(
                                id = '', 
                                content_type = null, ), 
                            global_id = '', ), 
                        media2 = ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner_media2.ProgrammeWithoutCuesheet_content_contentDetail_items_inner_media2(
                            title = '', 
                            global_id = ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner_playlist_item_id_global_id2.ProgrammeWithoutCuesheet_content_contentDetail_items_inner_playlistItemId_globalId2(
                                id = '', 
                                content_type = null, ), 
                            duration = ohdieux.ohdio.generated.models.duration.Duration(
                                duration_in_seconds = 1.337, ), 
                            download = ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner_media2_download.ProgrammeWithoutCuesheet_content_contentDetail_items_inner_media2_download(
                                formatted_file_size = '', 
                                media_id = '', 
                                url = '', 
                                file_size_in_bytes = 1.337, ), 
                            details = '', 
                            context = ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner_media2_context.ProgrammeWithoutCuesheet_content_contentDetail_items_inner_media2_context(
                                id = '', 
                                content_type = , ), ), 
                        global_id = , 
                        duration = ohdieux.ohdio.generated.models.duration.Duration(
                            duration_in_seconds = 1.337, ), 
                        broadcasted_first_time_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                    ],
                paged_configuration = ohdieux.ohdio.generated.models.pagination.Pagination(
                    total_number_of_items = 1.337, 
                    previous_page_url = '', 
                    page_size = 1.337, 
                    page_number = 1.337, 
                    page_max_length = 1.337, 
                    next_page_url = '', )
            )
        else:
            return ProgrammeWithoutCuesheetContentContentDetail(
                items = [
                    ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner.ProgrammeWithoutCuesheet_content_contentDetail_items_inner(
                        url = '', 
                        title = '', 
                        summary = '', 
                        playlist_item_id = ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner_playlist_item_id.ProgrammeWithoutCuesheet_content_contentDetail_items_inner_playlistItemId(
                            title = '', 
                            media_id = '', 
                            has_transcription = True, 
                            global_id2 = ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner_playlist_item_id_global_id2.ProgrammeWithoutCuesheet_content_contentDetail_items_inner_playlistItemId_globalId2(
                                id = '', 
                                content_type = null, ), 
                            global_id = '', ), 
                        media2 = ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner_media2.ProgrammeWithoutCuesheet_content_contentDetail_items_inner_media2(
                            title = '', 
                            global_id = ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner_playlist_item_id_global_id2.ProgrammeWithoutCuesheet_content_contentDetail_items_inner_playlistItemId_globalId2(
                                id = '', 
                                content_type = null, ), 
                            duration = ohdieux.ohdio.generated.models.duration.Duration(
                                duration_in_seconds = 1.337, ), 
                            download = ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner_media2_download.ProgrammeWithoutCuesheet_content_contentDetail_items_inner_media2_download(
                                formatted_file_size = '', 
                                media_id = '', 
                                url = '', 
                                file_size_in_bytes = 1.337, ), 
                            details = '', 
                            context = ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner_media2_context.ProgrammeWithoutCuesheet_content_contentDetail_items_inner_media2_context(
                                id = '', 
                                content_type = , ), ), 
                        global_id = , 
                        duration = ohdieux.ohdio.generated.models.duration.Duration(
                            duration_in_seconds = 1.337, ), 
                        broadcasted_first_time_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                    ],
                paged_configuration = ohdieux.ohdio.generated.models.pagination.Pagination(
                    total_number_of_items = 1.337, 
                    previous_page_url = '', 
                    page_size = 1.337, 
                    page_number = 1.337, 
                    page_max_length = 1.337, 
                    next_page_url = '', ),
        )
        """

    def testProgrammeWithoutCuesheetContentContentDetail(self):
        """Test ProgrammeWithoutCuesheetContentContentDetail"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
