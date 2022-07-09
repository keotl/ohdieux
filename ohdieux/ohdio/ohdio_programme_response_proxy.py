from datetime import datetime
from typing import Dict, List, Optional
from jivago.lang.stream import Stream
from jivago.lang.nullable import Nullable

from ohdieux.model.episode_descriptor import EpisodeDescriptor, MediaDescriptor
from ohdieux.model.programme_descriptor import ProgrammeDescriptor

from ohdieux.ohdio.ohdio_api import ApiException, OhdioApi


class OhdioProgrammeResponseProxy(object):

    def __init__(self, api: OhdioApi, show_id: str):
        self.programme_id = show_id
        self._api = api
        self._episodes: Optional[List[EpisodeDescriptor]] = None
        self._programme: Optional[ProgrammeDescriptor] = None

    @property
    def programme(self) -> ProgrammeDescriptor:
        if self._programme is None:
            self._fetch_programme()

        return self._programme  # type: ignore

    @property
    def episodes(self) -> List[EpisodeDescriptor]:
        if self._episodes is None:
            self._fetch_episodes()

        return self._episodes  # type: ignore

    def _fetch_episodes(self):
        res = []
        current_page = 1
        while True:
            try:
                response = self._api.query_episodes(self.programme_id, current_page)
                if not response["content"]["contentDetail"]["items"]:
                    break
                res.extend(
                    Stream(response["content"]["contentDetail"]["items"])
                    .map(self._map_episode)
                    .filter(lambda x: x is not None))
                current_page += 1
                break # TODO remove
            except ApiException:
                break

        self._episodes = res

    def _map_episode(self, json: dict) -> Optional[EpisodeDescriptor]:
        return EpisodeDescriptor(
            title=json["title"],
            description=json["summary"],
            guid=json["url"],
            date=datetime.now(), # TODO parse FR human date
            duration=json["media2"]["duration"]["durationInSeconds"],
            media=MediaDescriptorProxy(self._api,
                                       json["media2"]["id"],
                                       json["media2"]["duration"]["durationInSeconds"])
        )

    def _fetch_programme(self):
        json = self._api.query_programme(self.programme_id)
        self._programme = ProgrammeDescriptor(
            title=json["header"]["title"],
            description=json["header"]["summary"],
            author="Radio-Canada",
            link=json["header"]["share"]["url"],
            image_url=json["header"]["picture"]["url"],
        )

class MediaDescriptorProxy(MediaDescriptor):

    def __init__(self, api: OhdioApi, media_id: str, length: int):
        self._api = api
        self._media_id = media_id
        self._content: Optional[dict] = None
        self._length = length

    @property
    def media_url(self) -> str:
        if self._content is None:
            self._fetch()
        
        return Nullable(self._content) \
            .map(lambda x: x.get("url")) \
            .orElse("") # type: ignore

    @property
    def media_type(self) -> str:
        if self._content is None:
            self._fetch()
        return Stream(self._content["params"])\
            .firstMatch(lambda x: x["name"] == "contentType")\
            .map(lambda x: x["value"])\
            .orElse("")

    @property
    def length(self) -> int:
        return self._length

    def _fetch(self):
        try:
            self._content = self._api.query_media(self._media_id)
        except ApiException:
            pass # TODO
