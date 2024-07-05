import asyncio
import logging
import threading
import traceback
from typing import Awaitable, Iterable, List, Literal, Optional, Sequence, cast

from jivago.config.startup_hooks import PreShutdown
from jivago.inject.annotation import Component, Singleton
from jivago.lang.annotations import Inject, Override
from jivago.lang.runnable import Runnable
from ohdieux.config import Config
from ohdieux.model.episode_descriptor import EpisodeDescriptor
from ohdieux.model.programme import Programme, ProgrammeSummary
from ohdieux.ohdio.api_client import ApiClient, FetchException
from ohdieux.ohdio.assembler import (assemble_episode, assemble_pending_programme,
                                     assemble_programme)
from ohdieux.ohdio.guess_programme_ordering import guess_programme_ordering
from ohdieux.ohdio.parse_utils import clean
from ohdieux.ohdio.types import ProgrammeContentItem
from ohdieux.service.programme_fetching_service import (ProgrammeFetchingService,
                                                        ProgrammeNotFoundException)
from pydantic import ValidationError


@Component
@Singleton
class AsyncioProgrammeFetcher(ProgrammeFetchingService):

    @Inject
    def __init__(self, config: Config):
        self.event_loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=_run_loop, args=(self.event_loop, ))
        self.thread.start()
        self._user_agent = config.user_agent
        self._api_base_url = config.api_base_url
        self._logger = logging.getLogger(self.__class__.__name__)

    @Override
    def fetch_programme_summary(self, programme_id: int) -> ProgrammeSummary:
        res = asyncio.run_coroutine_threadsafe(
            self.fetch_programme_summary_async(programme_id), self.event_loop)
        return res.result()

    async def fetch_programme_summary_async(self,
                                            programme_id: int) -> ProgrammeSummary:
        api = self._create_api_client()
        programme = await api.get_programme_by_id(programme_id, 1)

        episodes = []

        if len(programme["content"]["contentDetail"]["items"]) > 0:
            first_episode = await self._fetch_episode_async(
                api, programme["content"]["contentDetail"]["items"][0])
            episodes.append(first_episode)

        return {
            "episodes": programme['content']["contentDetail"]["pagedConfiguration"].get(
                "totalNumberOfItems", 0),
            "first_episodes": episodes,
            "title": clean(programme["header"]["title"]),
            "description": clean(programme["header"]["summary"]),
            "ordering": guess_programme_ordering(episodes)
        }

    @Override
    def fetch_programme(self, programme_id: int) -> Programme:
        res = asyncio.run_coroutine_threadsafe(
            self.fetch_entire_programme_async(programme_id), self.event_loop)
        return res.result()

    @Override
    def fetch_slim_programme(self, programme_id: int) -> Programme:
        res = asyncio.run_coroutine_threadsafe(
            self.fetch_slim_programme_async(programme_id), self.event_loop)
        return res.result()

    async def fetch_slim_programme_async(self, programme_id: int) -> Programme:
        api = self._create_api_client()
        try:
            response = await api.get_programme_by_id(programme_id, 1)
            return assemble_pending_programme(response)
        except FetchException:
            raise ProgrammeNotFoundException(programme_id)

    async def fetch_entire_programme_async(self, programme_id: int) -> Programme:
        api = self._create_api_client()
        try:
            next_page: Optional[int] = 1
            episodes: List[Awaitable[Optional[EpisodeDescriptor]]] = []
            first_page = None
            while next_page != None and len(episodes) < 9500:
                page = await api.get_programme_by_id(programme_id, next_page)
                if first_page is None:
                    first_page = page
                episodes.extend(
                    map(lambda item: self._fetch_episode_async(api, item),
                        page["content"]["contentDetail"]["items"]))

                if page["content"]["contentDetail"]["pagedConfiguration"][
                        "pageSize"] == page["content"]["contentDetail"][
                            "pagedConfiguration"]["pageMaxLength"]:
                    next_page += 1
                else:
                    next_page = None

            if first_page is None:
                raise Exception("Could not fetch programme")
            episode_descriptors = await asyncio.gather(*episodes)
            valid_episodes = cast(Iterable[EpisodeDescriptor],
                                  filter(lambda x: x, episode_descriptors))
            return assemble_programme(first_page, list(valid_episodes))
        except FetchException:
            raise ProgrammeNotFoundException(programme_id)

    async def fetch_programme_incremental_async(self, programme_id: int,
                                                programme: Programme) -> Programme:
        api = self._create_api_client()
        next_page: Optional[int] = 1
        new_episodes: List[EpisodeDescriptor] = []
        first_page = None
        try:
            while next_page is not None:
                page = await api.get_programme_by_id(
                    programme_id,
                    next_page,
                )
                if first_page is None:
                    first_page = page
                if page["content"]["contentDetail"]["pagedConfiguration"][
                        "pageSize"] == page["content"]["contentDetail"][
                            "pagedConfiguration"]["pageMaxLength"]:
                    next_page += 1
                else:
                    next_page = None

                for item in page["content"]["contentDetail"]["items"]:
                    episode = await self._fetch_episode_async(api, item)
                    if not episode:
                        raise Exception("Could not fetch episode")
                    new_episodes.append(episode)
                    if _is_same(episode, programme.episodes[0]):
                        return assemble_programme(
                            first_page, [*new_episodes, *programme.episodes[1:]])
        except:
            self._logger.error(
                f"Could not update pgoramme {programme_id} incrementally.")
            traceback.print_exc()
        return programme

    async def _fetch_episode_async(
            self, api: ApiClient,
            episode: ProgrammeContentItem) -> Optional[EpisodeDescriptor]:
        try:
            playback_list_item_id = episode["playlistItemId"]["globalId2"]
            playback_list = await api.get_playback_list_by_id(
                playback_list_item_id["contentType"]["id"],
                str(playback_list_item_id["id"]))

            media_ids = _distinct(item["mediaPlaybackItem"]["mediaId"]
                                  for item in playback_list["items"]
                                  if item["mediaPlaybackItem"]["globalId"]["id"] ==
                                  playback_list_item_id["id"])

            streams = await self._fetch_episode_streams_async(api, media_ids)

            return assemble_episode(episode, playback_list, streams)
        except ValidationError as e:
            self._logger.warning(e)
        except FetchException:
            return None

    async def _fetch_episode_streams_async(self, api: ApiClient,
                                           media_ids: Iterable[str]) -> Iterable[str]:
        streams = await asyncio.gather(*map(
            lambda media_id: self._fetch_single_episode_stream_async(api, media_id),
            media_ids))
        return cast(Iterable[str], filter(lambda x: x is not None, streams))

    async def _fetch_single_episode_stream_async(self, api: ApiClient,
                                                 media_id: str) -> Optional[str]:
        for tech in TECHS:
            try:
                stream = await api.get_media_stream(int(media_id), tech)
                return stream["url"]
            except ValidationError:
                continue
            except FetchException:
                continue
        return None

    def _create_api_client(self) -> ApiClient:
        api = ApiClient(self._api_base_url, self._user_agent)
        return api


def _run_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def _distinct(items: Iterable[str]) -> List[str]:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def _is_same(a: EpisodeDescriptor, b: EpisodeDescriptor) -> bool:
    return a.guid == b.guid


TECHS: Sequence[Literal["hls", "progressive"]] = ["progressive", "hls"]


@PreShutdown
@Component
class _AsyncioProgrammeFetcherCleanup(Runnable):

    @Inject
    def __init__(self, fetcher: AsyncioProgrammeFetcher):
        self._fetcher = fetcher
        self._logger = logging.getLogger(self.__class__.__name__)

    @Override
    def run(self):
        self._logger.info("Stopping event loop.")
        self._fetcher.event_loop.call_soon_threadsafe(self._fetcher.event_loop.stop)
        self._fetcher.thread.join()
