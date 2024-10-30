import json
import logging
from typing import Literal

import aiohttp
from ohdieux.ohdio.parse_utils import filter_playbacklist_items_by_episode_id
from ohdieux.ohdio.programme_type import ProgrammeType
from ohdieux.ohdio.types import (MediaStreamDescriptor, PlaybackList,
                                 ProgrammeWithoutCuesheet)


class ApiClient(object):

    def __init__(self, base_url: str, user_agent: str):
        self._base_url = base_url
        self._user_agent = user_agent
        self._logger = logging.getLogger(self.__class__.__name__)

    async def get_programme_by_id(
            self, programme_id: int, page_number: int,
            programme_type: ProgrammeType) -> ProgrammeWithoutCuesheet:
        candidates = _PROGRAMME_BY_ID_QUERIES.keys() if programme_type is None else [
            programme_type
        ]
        for candidate_programme_type in candidates:
            try:
                response = await self._do_request(
                    "GET",
                    "/bff/audio/graphql", {
                        "opname": "programmeById",
                        "extensions": json.dumps({
                            "persistedQuery": {
                                "version": 1,
                                "sha256Hash": _PROGRAMME_BY_ID_QUERIES[
                                    candidate_programme_type]
                            }
                        }),
                        "variables": json.dumps({
                            "params": {
                                "context": "web",
                                "forceWithoutCueSheet": programme_type == "balado",
                                "id": programme_id,
                                "pageNumber": page_number
                            }
                        })
                    },
                    headers={"Content-Type": "application/json"})
                result = response["data"]["programmeById"]
                if "content" in result:
                    return result
            except Exception:
                continue

        raise Exception(
            f"Could not fetch programme {programme_id}, with assumed type {candidates}")

    async def get_playback_list_by_id(
            self,
            content_type_id: int,
            playback_list_id: str,
            filter_related_episodes: bool = True) -> PlaybackList:
        response = await self._do_request(
            "GET",
            "/bff/audio/graphql", {
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
            },
            headers={"Content-Type": "application/json"})
        if filter_related_episodes:
            return filter_playbacklist_items_by_episode_id(
                playback_list_id, response["data"]["playbackListByGlobalId"])

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

    async def _do_request(self,
                          method: Literal["GET", "POST"],
                          path: str,
                          params: dict,
                          headers: dict = {}):
        self._logger.debug(
            f"Issuing request {self._base_url}{path}?{params.get('opname') or json.dumps(params)}"
        )
        async with aiohttp.ClientSession() as session:
            async with session.request(method,
                                       f"{self._base_url}{path}",
                                       params=params,
                                       headers={
                                           "User-Agent": self._user_agent,
                                           **headers
                                       }) as response:
                if response.status >= 400:
                    self._logger.warning(
                        f"Got error on {path}{params} – {response.status}")
                    raise FetchException()
                body = await response.text()
                return json.loads(body)


class FetchException(Exception):
    pass


_PROGRAMME_BY_ID_QUERIES = {
    "balado": "01278be1ca37eec8570a3c6341c475c8b5799d571f407f3a9c1a3e2703cc5cc1",
    "emissionpremiere": "a6d745162f4b6d9011e53382fcf981c09968d77909391b9c0e5302853f852444"
}
