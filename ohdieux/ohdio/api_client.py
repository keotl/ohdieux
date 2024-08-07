import json
import logging
from typing import Literal

import aiohttp
from ohdieux.ohdio.types import (MediaStreamDescriptor, PlaybackList,
                                 ProgrammeWithoutCuesheet)


class ApiClient(object):

    def __init__(self, base_url: str, user_agent: str):
        self._base_url = base_url
        self._user_agent = user_agent
        self._logger = logging.getLogger(self.__class__.__name__)

    async def get_programme_by_id(self, programme_id: int,
                                  page_number: int) -> ProgrammeWithoutCuesheet:
        response = await self._do_request(
            "GET", "/bff/audio/graphql", {
                "opname": "programmeById",
                "extensions": json.dumps({
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "7c1f3e0c576c2f82a45ef4a74026a41bd32e2cf4ebea974fadd22409a95e8ee3"
                    }
                }),
                "variables": json.dumps({
                    "params": {
                        "context": "web",
                        "forceWithoutCueSheet": False,
                        "id": programme_id,
                        "pageNumber": page_number
                    }
                })
            })
        return response["data"]["programmeById"]

    async def get_playback_list_by_id(self, content_type_id: int,
                                      playback_list_id: str) -> PlaybackList:
        response = await self._do_request(
            "GET", "/bff/audio/graphql", {
                "opname": "playbackListByGlobalId",
                "extensions": json.dumps({
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "ae95ebffe69f06d85a0f287931b61e3b7bfb7485f28d4d906c376be5f830b8c0"
                    }
                }),
                "variables": json.dumps({
                    "params": {
                        "contentTypeId": content_type_id,
                        "id": playback_list_id
                    }
                })
            })
        return response["data"]["playbackListByGlobalId"]

    async def get_media_stream(
            self, media_id: int, tech: Literal["hls",
                                               "progressive"]) -> MediaStreamDescriptor:
        return await self._do_request(
            "GET", "/media/validation/v2", {
                "appCode": "medianet",
                "connectionType": "hd",
                "deviceType": "ipad",
                "idMedia": media_id,
                "multibitrate": "true",
                "output": "json",
                "tech": tech
            })

    async def _do_request(self, method: Literal["GET", "POST"], path: str,
                          params: dict):
        self._logger.debug(
            f"Issuing request {self._base_url}{path}?{params.get('opname') or json.dumps(params)}"
        )
        async with aiohttp.ClientSession() as session:
            async with session.request(method, f"{self._base_url}{path}",
                                       params=params) as response:
                if response.status >= 400:
                    self._logger.warning(
                        f"Got error on {path}{params} – {response.status}")
                    raise FetchException()
                body = await response.text()
                return json.loads(body)


class FetchException(Exception):
    pass

