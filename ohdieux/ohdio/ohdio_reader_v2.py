import itertools
import logging
import multiprocessing
from typing import List, Optional

import requests
from jivago.inject.annotation import Component
from jivago.lang.stream import Stream

from ohdieux.model.episode_descriptor import EpisodeDescriptor, MediaDescriptor
from ohdieux.model.programme import Programme
from ohdieux.model.programme_descriptor import ProgrammeDescriptor
from ohdieux.ohdio.ohdio_api import OhdioApi
from ohdieux.ohdio.ohdio_programme_response_proxy import clean
from ohdieux.util.dateparse import parse_fr_date, infer_fr_date


@Component
class OhdioReaderV2(object):

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._pool = multiprocessing.Pool(4)

    def query(self, programme_id: str, reverse_segments: bool) -> Programme:
        page_number = 1
        reached_end = False
        episode_media_ids = []
        incomplete_episode_descriptors = []
        programme_descriptor: Optional[ProgrammeDescriptor] = None

        while not reached_end:
            response = requests.get(
                f"https://services.radio-canada.ca/neuro/sphere/v1/audio/apps/products/programmes-without-cuesheet-v2/{programme_id}/{page_number}")
            if not response.ok:
                self._logger.debug(
                    f"got {response.status_code} while querying programme page {page_number}. Assuming end of content.")
                break
            json = response.json()
            paged_configuration = json["content"]["contentDetail"]["pagedConfiguration"]
            if paged_configuration["nextPageUrl"] is None:
                reached_end = True

            for item in json["content"]["contentDetail"]["items"]:
                episode_media_ids.append(item["globalId"]["id"])
                incomplete_episode_descriptors.append(EpisodeDescriptor(
                    title=clean(item["title"]),
                    description=clean(item["summary"]),
                    guid="",
                    date=infer_fr_date(item),
                    duration=item["media2"]["duration"]["durationInSeconds"],
                    media=MediaDescriptor("", "audio/mpeg",
                                          item["media2"]["duration"]["durationInSeconds"])
                ))

            if programme_descriptor is None:
                programme_descriptor = ProgrammeDescriptor(
                    title=clean(json["header"]["title"]),
                    description=clean(json["header"]["summary"]),
                    author="Radio-Canada",
                    link="http://ici.radio-canada.ca" + json["header"]["share"]["url"],
                    image_url=json["header"]["picture"]["url"].replace("{0}", "400").replace("{1}", "1x1"),
                )
            # TODO remove
            break
        # segment_urls = Stream.zip(episode_media_ids, itertools.repeat(reverse_segments)).map(lambda a,b: _fetch_stream_url(a,b)).toList()
        segment_urls = self._pool.starmap(_fetch_stream_url, zip(episode_media_ids, itertools.repeat(reverse_segments)))
        print("hello")
        episodes = []
        for incomplete_episode_descriptor, stream_urls in zip(incomplete_episode_descriptors, segment_urls):
            episodes.append(Stream(stream_urls).map(lambda url:
                                    EpisodeDescriptor(title=incomplete_episode_descriptor.title,
                                                      description=incomplete_episode_descriptor.description,
                                                      guid=url,
                                                      date=incomplete_episode_descriptor.date,
                                                      duration=incomplete_episode_descriptor.duration,
                                                      media=MediaDescriptor(url, "audio/mpeg",
                                                                            incomplete_episode_descriptor.media.length)
                                                      )
                                    ).toList())
        return Programme(programme_descriptor, Stream(episodes).flat().toList())


def _fetch_stream_url(episode_media_id: str, reverse_segments: bool) -> List[str]:
    try:
        episode_segments = OhdioApi().query_episode_segments("ignored", episode_media_id)
        distinct_streams = []
        if "contentDetail" in episode_segments["content"]:
            # Multi-segment episodes (e.g. programme 672)
            for segment in episode_segments["content"]["contentDetail"]["items"]:
                stream_id = segment["media2"]["id"]
                if stream_id not in distinct_streams:
                    distinct_streams.append(stream_id)
            if reverse_segments:
                distinct_streams = distinct_streams[::-1]
        else:
            # Single-segment episodes (e.g. programme 9887)
            distinct_streams.append(episode_segments["header"]["media2"]["id"])
        segments = distinct_streams
    except:
        segments = [episode_media_id]
    urls: List[str] = []
    for media_id in segments:
        res = requests.get(
            f"https://services.radio-canada.ca/media/validation/v2/?appCode=medianet&connectionType=hd&deviceType=ipad&idMedia={media_id}&multibitrate=true&output=json&tech=hls")
        if not res.ok:
            urls.append("")

        urls.append(res.json()["url"])

    return urls
