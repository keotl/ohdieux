import asyncio
import logging
import threading
from datetime import datetime
from typing import Awaitable, Iterable, List, Optional, cast

import ohdieux.ohdio.generated
from jivago.config.startup_hooks import PreShutdown
from jivago.inject.annotation import Component, Singleton
from jivago.lang.annotations import Inject, Override
from jivago.lang.runnable import Runnable
from ohdieux.config import Config
from ohdieux.model.episode_descriptor import EpisodeDescriptor
from ohdieux.model.programme import Programme
from ohdieux.ohdio.assembler import (assemble_episode, assemble_pending_programme,
                                     assemble_programme)
from ohdieux.ohdio.generated.api.default_api import DefaultApi
from ohdieux.ohdio.generated.configuration import Configuration
from ohdieux.ohdio.generated.exceptions import NotFoundException
from ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner import \
    ProgrammeWithoutCuesheetContentContentDetailItemsInner
from ohdieux.ohdio.generated.models.streaming_tech import StreamingTech
from ohdieux.ohdio.generated.rest import ApiException
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
        self.user_agent = config.user_agent
        self.proxy_url = config.proxy_url
        self._api_base_url = config.api_base_url
        self._logger = logging.getLogger(self.__class__.__name__)

    @Override
    def fetch_newest_episode(self, programme_id: int) -> Optional[EpisodeDescriptor]:
        res = asyncio.run_coroutine_threadsafe(
            self.fetch_newest_episode_async(programme_id), self.event_loop)
        return res.result()

    async def fetch_newest_episode_async(
            self, programme_id: int) -> Optional[EpisodeDescriptor]:
        api = self._create_api_client()
        try:
            programme = await api.get_programme_without_cuesheet(str(programme_id),
                                                                 1,
                                                                 context="web")
            if not programme.content.content_detail or not programme.content.content_detail.items:
                return None

            return await self._fetch_episode_async(
                api, programme.content.content_detail.items[0])
        except NotFoundException:
            raise ProgrammeNotFoundException(programme_id)
        finally:
            await api.api_client.close()

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
            response = await api.get_programme_without_cuesheet(str(programme_id),
                                                                1,
                                                                context="web")
            return assemble_pending_programme(response)
        except NotFoundException:
            raise ProgrammeNotFoundException(programme_id)
        finally:
            await api.api_client.close()

    async def fetch_entire_programme_async(self, programme_id: int) -> Programme:
        api = self._create_api_client()
        try:
            next_page: Optional[int] = 1
            episodes: List[Awaitable[Optional[EpisodeDescriptor]]] = []
            first_page = None
            while next_page != None:
                page = await api.get_programme_without_cuesheet(str(programme_id),
                                                                next_page,
                                                                context="web")
                if first_page is None:
                    first_page = page
                episodes.extend(
                    map(lambda item: self._fetch_episode_async(api, item),
                        page.content.content_detail.items))

                if page.content.content_detail.paged_configuration.next_page_url:
                    next_page += 1
                else:
                    next_page = None

            if first_page is None:
                raise Exception("Could not fetch programme")
            episode_descriptors = await asyncio.gather(*episodes)
            valid_episodes = cast(Iterable[EpisodeDescriptor],
                                  filter(lambda x: x, episode_descriptors))
            return assemble_programme(first_page, list(valid_episodes))
        except NotFoundException:
            raise ProgrammeNotFoundException(programme_id)
        finally:
            await api.api_client.close()

    async def fetch_programme_incremental_async(self, programme_id: int,
                                                programme: Programme) -> Programme:
        api = self._create_api_client()
        next_page: Optional[int] = 1
        new_episodes: List[EpisodeDescriptor] = []
        first_page = None
        try:
            while next_page != None:
                page = await api.get_programme_without_cuesheet(str(programme_id),
                                                                next_page,
                                                                context="web")
                if first_page is None:
                    first_page = page
                if page.content.content_detail.paged_configuration.next_page_url:
                    next_page += 1
                else:
                    next_page = None

                for item in page.content.content_detail.items:
                    episode = await self._fetch_episode_async(api, item)
                    if not episode:
                        raise Exception("Could not fetch episode")
                    new_episodes.append(episode)

                    if _is_same(episode, programme.episodes[0]):
                        return assemble_programme(
                            first_page, [*new_episodes, *programme.episodes[1:]])

        finally:
            await api.api_client.close()

        self._logger.error(f"Could not update pgoramme {programme_id} incrementally.")
        return programme

    async def _fetch_episode_async(
        self, api: DefaultApi,
        episode: ProgrammeWithoutCuesheetContentContentDetailItemsInner
    ) -> Optional[EpisodeDescriptor]:
        try:
            if episode.playlist_item_id.media_id:
                streams = await self._fetch_episode_streams_async(
                    api, [episode.playlist_item_id.media_id])
            else:
                playlist_item_id = episode.playlist_item_id.global_id
                playlist_items = await api.get_playlist_item(playlist_item_id, "web",
                                                             playlist_item_id)
                media_ids = _distinct(item.playlist_item_id.media_id
                                      for item in playlist_items.items)
                streams = await self._fetch_episode_streams_async(api, media_ids)

            return assemble_episode(episode, streams)
        except ValidationError as e:
            self._logger.warning(e)
        except ApiException:
            return None

    async def _fetch_episode_streams_async(self, api: DefaultApi,
                                           media_ids: Iterable[str]) -> Iterable[str]:
        streams = await asyncio.gather(*map(
            lambda media_id: self._fetch_single_episode_stream_async(api, media_id),
            media_ids))
        return cast(Iterable[str], filter(lambda x: x is not None, streams))

    async def _fetch_single_episode_stream_async(self, api: DefaultApi,
                                                 media_id: str) -> Optional[str]:
        for tech in ["progressive", "hls"]:
            try:
                stream = await api.get_media_stream(app_code="medianet",
                                                    connection_type="hd",
                                                    device_type="ipad",
                                                    id_media=media_id,
                                                    multibitrate="true",
                                                    output="json",
                                                    tech=cast(StreamingTech, tech))
                return stream.url
            except ValidationError:
                continue
            except ApiException:
                continue
        return None

    def _create_api_client(self) -> DefaultApi:
        config = Configuration(host=self._api_base_url)
        if self.proxy_url:
            config.proxy = self.proxy_url  # type: ignore
        api_client = ohdieux.ohdio.generated.ApiClient(config)
        api_client.user_agent = self.user_agent
        api = ohdieux.ohdio.generated.DefaultApi(api_client)
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
