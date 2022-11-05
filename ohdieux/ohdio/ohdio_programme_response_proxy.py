from datetime import datetime
from typing import Dict, List, Optional
from jivago.lang.stream import Stream
from jivago.lang.nullable import Nullable

from ohdieux.model.episode_descriptor import EpisodeDescriptor, MediaDescriptor
from ohdieux.model.programme import Programme
from ohdieux.model.programme_descriptor import ProgrammeDescriptor

from ohdieux.ohdio.ohdio_api import ApiException, OhdioApi
from ohdieux.util.dateparse import parse_fr_date


class OhdioProgrammeResponseProxy(Programme):

    def __init__(self, api: OhdioApi, show_id: str, reverse_episode_segments: bool = False):
        self.reverse_episode_segments = reverse_episode_segments
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
                for x in response["content"]["contentDetail"]["items"]:
                    episode_id = x["media2"]["context"]["id"]
                    segments = self._api.query_episode_segments(self.programme_id, episode_id)
                    distinct_streams = []

                    for segment in segments["content"]["contentDetail"]["items"]:
                        stream_id = segment["media2"]["id"]
                        if stream_id not in distinct_streams:
                            distinct_streams.append(stream_id)
                    if self.reverse_episode_segments:
                        distinct_streams = distinct_streams[::-1]

                    for i, stream_id in enumerate(distinct_streams):
                        res.append(self._map_episode(x, stream_id, index=(i + 1) if len(distinct_streams) > 1 else None))
                current_page += 1
            except ApiException:
                break

        self._episodes = res

    def _map_episode(self, json: dict, stream_id: str, index=None) -> Optional[EpisodeDescriptor]:
        return EpisodeDescriptor(
            title=clean(json["title"]) + (f" ({index})" if index is not None else ""),
            description=clean(json["summary"]),
            guid=stream_id,
            date=parse_fr_date(json["media2"]["details"]),
            duration=json["media2"]["duration"]["durationInSeconds"],
            media=MediaDescriptorProxy(self._api,
                                       stream_id,
                                       json["media2"]["duration"]["durationInSeconds"])
        )

    def _fetch_programme(self):
        json = self._api.query_programme(self.programme_id)
        self._programme = ProgrammeDescriptor(
            title=clean(json["header"]["title"]),
            description=clean(json["header"]["summary"]),
            author="Radio-Canada",
            link=json["header"]["share"]["url"],
            image_url=json["header"]["picture"]["url"].replace("{0}", "400").replace("{1}", "1x1"),
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
            .orElse("")  # type: ignore

    @property
    def media_type(self) -> str:
        return "audio/mpeg"  # Has to be overwritten since vnd.apple.mpegURL is not recognized by Apple Podcasts
        # if self._content is None:
        #     self._fetch()
        # return Stream(self._content["params"])\
        #     .firstMatch(lambda x: x["name"] == "contentType")\
        #     .map(lambda x: x["value"])\
        #     .orElse("")

    @property
    def length(self) -> int:
        return self._length

    def _fetch(self):
        try:
            self._content = self._api.query_media(self._media_id)
        except ApiException:
            pass  # TODO


def clean(human_readable_text: str) -> str:
    return (human_readable_text or "") \
        .replace("&nbsp;", " ") \
        .replace("&", "&amp; ") \
        .replace("<br>", "<br/>")
