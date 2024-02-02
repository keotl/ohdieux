import itertools
import logging
import multiprocessing.pool
import os
from datetime import datetime
from typing import List, NamedTuple, Optional

import requests
from jivago.inject.annotation import Component, Singleton
from jivago.lang.annotations import Inject, Override
from jivago.lang.stream import Stream
from ohdieux.config import Config
from ohdieux.model.episode_descriptor import EpisodeDescriptor, MediaDescriptor
from ohdieux.model.programme import Programme
from ohdieux.model.programme_descriptor import ProgrammeDescriptor
from ohdieux.ohdio.parse_utils import clean
from ohdieux.service.programme_fetching_service import (
    ProgrammeFetchingService, ProgrammeNotFoundException)
from ohdieux.util.dateparse import infer_fr_date

if os.environ.get("USER_AGENT"):
    USER_AGENT = {"User-Agent": os.environ.get("USER_AGENT") or ""}
else:
    USER_AGENT = None


@Component
@Singleton
class OhdioProgrammeFetcher(ProgrammeFetchingService):

    @Inject
    def __init__(self, config: Config):
        self._pool = multiprocessing.Pool(config.fetch_threads)

    @Override
    def fetch_slim_programme(self, programme_id: int) -> Programme:
        summary_block = _fetch_summary_block(programme_id)
        programme_descriptor = ProgrammeDescriptor(
            title=summary_block.title,
            description="Ce programme est en cours de chargement par Ohdieux. "
            "This programme is currently being indexed by Ohdieux. "
            "Veuillez patienter quelques minutes avant de rafraîchir. "
            "Wait a few minutes before refreshing.",
            author=summary_block.author,
            link=summary_block.link,
            image_url=summary_block.image_url)

        return Programme(programme_descriptor, [], datetime.now())

    @Override
    def fetch_newest_episode(self,
                             programme_id: int) -> Optional[EpisodeDescriptor]:
        page = _fetch_page(programme_id, 1)
        if page:
            episode_urls = _fetch_episode_streams(page[0])
            return _assemble_episode_descriptor(page[0], episode_urls)
        # Programmes with no episodes, e.g. 7220
        return None

    @Override
    def fetch_programme(self, programme_id: int) -> Programme:
        summary_block = _fetch_summary_block(programme_id)
        estimated_number_of_pages = summary_block.total_episodes // summary_block.episodes_per_page + 1
        episode_payloads: List[dict] = list(
            itertools.chain(*self._pool.starmap(
                _fetch_page,
                zip(itertools.repeat(programme_id),
                    range(1, estimated_number_of_pages + 1)))))  # type: ignore

        episode_urls = self._pool.map(_fetch_episode_streams, episode_payloads)

        episode_descriptors = Stream.zip(
            episode_payloads,
            episode_urls).map(_assemble_episode_descriptor).filter(
                lambda x: x is not None).toList()  # type: ignore

        programme_descriptor = ProgrammeDescriptor(
            title=summary_block.title,
            description=summary_block.description,
            author=summary_block.author,
            link=summary_block.link,
            image_url=summary_block.image_url)

        return Programme(programme_descriptor, episode_descriptors,
                         datetime.now())


def _fetch_page(programme_id: int, page_number: int) -> List[dict]:
    response = requests.get(
        f"https://services.radio-canada.ca/neuro/sphere/v1/audio/apps/products/programmes-without-cuesheet-v2/{programme_id}/{page_number}",
        headers=USER_AGENT)
    if not response.ok:
        return []
    json = response.json()
    return json["content"]["contentDetail"]["items"]


def _fetch_episode_streams(episode_payload: dict) -> List[str]:
    playlist_item_id = episode_payload["playlistItemId"]["globalId"]
    episode_media_id = episode_payload["playlistItemId"]["mediaId"]
    if episode_media_id:
        return _fetch_stream_url([episode_media_id])
    else:
        response = requests.get(
            f"https://services.radio-canada.ca/neuro/sphere/v1/medias/apps/playback-lists/{playlist_item_id}?context=web&globalId={playlist_item_id}",
            timeout=10,
            headers=USER_AGENT)
        if response.ok:
            segment_media_ids = Stream(response.json()["items"]).map(
                lambda x: x["playlistItemId"]["mediaId"]).toList()
            episode_media_ids = []
            for segment in segment_media_ids:
                if segment in episode_media_ids:
                    continue
                episode_media_ids.append(segment)

            return _fetch_stream_url(episode_media_ids)
        _logger.warning(
            f"Failed to find any streams for episode {episode_payload.get('share', {}).get('url', '')}.")
        return []


_logger = logging.getLogger("OhdioProgrammeFetcher")


def _assemble_episode_descriptor(
        episode_payload: dict,
        stream_urls: List[str]) -> Optional[EpisodeDescriptor]:
    try:
        return EpisodeDescriptor(
            title=clean(episode_payload["title"]),
            description=clean(episode_payload["summary"]),
            guid=episode_payload["globalId"]["id"],
            date=infer_fr_date(episode_payload),
            duration=episode_payload["media2"]["duration"]
            ["durationInSeconds"],
            media=Stream(stream_urls).map(lambda x: MediaDescriptor(
                x, "audio/mpeg", episode_payload["media2"]["duration"][
                    "durationInSeconds"])).toList())
    except AttributeError:
        return None
    except TypeError:
        # broken data model, e.g. programme 3858 with empty episode
        return None


class ProgrammeSummary(NamedTuple):
    title: str
    description: str
    author: str
    link: str
    image_url: str
    episodes_per_page: int
    total_episodes: int


def _fetch_summary_block(programme_id: int):
    response = requests.get(
        f"https://services.radio-canada.ca/neuro/sphere/v1/audio/apps/products/programmes-without-cuesheet-v2/{programme_id}/1",
        headers=USER_AGENT)
    if not response.ok:
        raise ProgrammeNotFoundException(programme_id)

    json = response.json()
    return ProgrammeSummary(title=clean(json["header"]["title"]),
                            description=clean(json["header"]["summary"]),
                            author="Radio-Canada",
                            link="http://ici.radio-canada.ca" +
                            json["header"]["share"]["url"],
                            image_url=json["header"]["picture"]["url"].replace(
                                "{0}", "1400").replace("{1}", "1x1"),
                            episodes_per_page=json["content"]["contentDetail"]
                            ["pagedConfiguration"]["pageMaxLength"],
                            total_episodes=json["content"]["contentDetail"]
                            ["pagedConfiguration"]["totalNumberOfItems"])


def _fetch_stream_url(episode_media_ids: List[str]) -> List[str]:
    urls: List[str] = []
    for media_id in episode_media_ids:
        for platform in ["progressive", "hls"]:
            # Some programmes only work with HLS, e.g. 8362
            res = requests.get(
                f"https://services.radio-canada.ca/media/validation/v2/?appCode=medianet&connectionType=hd&deviceType=ipad&idMedia={media_id}&multibitrate=true&output=json&tech={platform}",
                headers=USER_AGENT)
            if not res.ok or res.json()["url"] is None:
                continue

            urls.append(res.json()["url"])
            break

    return urls
