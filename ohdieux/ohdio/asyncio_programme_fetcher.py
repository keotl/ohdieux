import asyncio
import logging
import threading
from typing import Awaitable, Iterable, List, Optional, cast

import ohdieux.ohdio.generated
from jivago.inject.annotation import Component, Singleton
from jivago.lang.annotations import Inject, Override
from ohdieux.config import Config
from ohdieux.model.episode_descriptor import EpisodeDescriptor
from ohdieux.model.programme import Programme
from ohdieux.ohdio.assembler import (assemble_episode, assemble_pending_programme,
                                     assemble_programme)
from ohdieux.ohdio.generated.api.default_api import DefaultApi
from ohdieux.ohdio.generated.configuration import Configuration
from ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner import \
    ProgrammeWithoutCuesheetContentContentDetailItemsInner
from ohdieux.ohdio.generated.models.streaming_tech import StreamingTech
from ohdieux.ohdio.generated.rest import ApiException
from ohdieux.service.programme_fetching_service import ProgrammeFetchingService
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
        self._logger = logging.getLogger(self.__class__.__name__)

    @Override
    def fetch_newest_episode(self, programme_id: int) -> Optional[EpisodeDescriptor]:
        res = asyncio.run_coroutine_threadsafe(self._fetch_newest_episode(programme_id),
                                               self.event_loop)
        return res.result()

    async def _fetch_newest_episode(self,
                                    programme_id: int) -> Optional[EpisodeDescriptor]:
        api = self._create_api_client()
        try:
            programme = await api.get_programme_without_cuesheet(str(programme_id), 1)
            if not programme.content.content_detail:
                return None

            return await self._fetch_episode(api,
                                             programme.content.content_detail.items[0])
        finally:
            await api.api_client.close()

    @Override
    def fetch_programme(self, programme_id: int) -> Programme:
        res = asyncio.run_coroutine_threadsafe(
            self._fetch_entire_programme(programme_id), self.event_loop)
        return res.result()

    @Override
    def fetch_slim_programme(self, programme_id: int) -> Programme:
        res = asyncio.run_coroutine_threadsafe(self._fetch_slim_programme(programme_id),
                                               self.event_loop)
        return res.result()

    async def _fetch_slim_programme(self, programme_id: int) -> Programme:
        api = self._create_api_client()
        try:
            response = await api.get_programme_without_cuesheet(str(programme_id), 1)
            return assemble_pending_programme(response)
        finally:
            await api.api_client.close()

    async def _fetch_entire_programme(self, programme_id: int) -> Programme:
        api = self._create_api_client()
        try:
            next_page: Optional[int] = 1
            episodes: List[Awaitable[Optional[EpisodeDescriptor]]] = []
            first_page = None
            while next_page != None:
                page = await api.get_programme_without_cuesheet(
                    str(programme_id), next_page)
                if first_page is None:
                    first_page = page
                episodes.extend(
                    map(lambda item: self._fetch_episode(api, item),
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
        finally:
            await api.api_client.close()

    async def _fetch_episode(
        self, api: DefaultApi,
        episode: ProgrammeWithoutCuesheetContentContentDetailItemsInner
    ) -> Optional[EpisodeDescriptor]:
        try:
            if episode.playlist_item_id.media_id:
                streams = await self._fetch_episode_streams(
                    api, [episode.playlist_item_id.media_id])
            else:
                playlist_item_id = episode.playlist_item_id.global_id
                playlist_items = await api.get_playlist_item(playlist_item_id, "web",
                                                             playlist_item_id)
                media_ids = _distinct(item.playlist_item_id.media_id
                                      for item in playlist_items.items)
                streams = await self._fetch_episode_streams(api, media_ids)

            return assemble_episode(episode, streams)
        except ValidationError as e:
            self._logger.warning(e)
        except ApiException:
            return None

    async def _fetch_episode_streams(self, api: DefaultApi,
                                     media_ids: Iterable[str]) -> Iterable[str]:
        streams = await asyncio.gather(
            *map(lambda media_id: self._fetch_single_episode_stream(api, media_id),
                 media_ids))
        return cast(Iterable[str], filter(lambda x: x is not None, streams))

    async def _fetch_single_episode_stream(self, api: DefaultApi,
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
        api_client = ohdieux.ohdio.generated.ApiClient(
            Configuration(host="https://services.radio-canada.ca"))
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
