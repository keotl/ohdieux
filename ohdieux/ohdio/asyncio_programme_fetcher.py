import asyncio
from typing import Awaitable, Iterable, List, Optional, cast

import ohdieux.ohdio.generated
from jivago.inject.annotation import Component, Singleton
from jivago.lang.annotations import Inject, Override
from ohdieux.config import Config
from ohdieux.model.episode_descriptor import EpisodeDescriptor
from ohdieux.model.programme import Programme
from ohdieux.ohdio.assembler import (assemble_episode, assemble_pending_programme,
                                     assemble_programme)
from ohdieux.ohdio.generated.configuration import Configuration
from ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner import \
    ProgrammeWithoutCuesheetContentContentDetailItemsInner
from ohdieux.ohdio.generated.models.streaming_tech import StreamingTech
from ohdieux.ohdio.generated.rest import ApiException
from ohdieux.service.programme_fetching_service import ProgrammeFetchingService


@Component
@Singleton
class AsyncioProgrammeFetcher(ProgrammeFetchingService):

    @Inject
    def __init__(self, config: Config):
        self.runner = asyncio.Runner()

        self.api_client = ohdieux.ohdio.generated.ApiClient(
            Configuration(host="https://services.radio-canada.ca"))
        self.api_client.user_agent = config.user_agent
        self.api = ohdieux.ohdio.generated.DefaultApi(self.api_client)

    @Override
    def fetch_newest_episode(self, programme_id: int) -> Optional[EpisodeDescriptor]:
        return self.runner.run(self._fetch_newest_episode(programme_id))

    async def _fetch_newest_episode(self,
                                    programme_id: int) -> Optional[EpisodeDescriptor]:
        programme = await self.api.get_programme_without_cuesheet(str(programme_id), 1)
        if not programme.content.content_detail:
            return None

        return await self._fetch_episode(programme.content.content_detail.items[0])

    @Override
    def fetch_programme(self, programme_id: int) -> Programme:
        return self.runner.run(self._fetch_entire_programme(programme_id))

    @Override
    def fetch_slim_programme(self, programme_id: int) -> Programme:
        programme = self.runner.run(
                self.api.get_programme_without_cuesheet(str(programme_id), 1))
        return assemble_pending_programme(programme)

    async def _fetch_entire_programme(self, programme_id: int) -> Programme:
        next_page: Optional[int] = 1
        episodes: List[Awaitable[EpisodeDescriptor]] = []
        first_page = None
        while next_page != None:
            page = await self.api.get_programme_without_cuesheet(
                str(programme_id), next_page)
            if first_page is None:
                first_page = page
            episodes.extend(map(self._fetch_episode, page.content.content_detail.items))

            if page.content.content_detail.paged_configuration.next_page_url:
                next_page += 1
            else:
                next_page = None

        if first_page is None:
            raise Exception("Could not fetch programme")
        episode_descriptors = await asyncio.gather(*episodes)
        return assemble_programme(first_page, episode_descriptors)

    async def _fetch_episode(
        self, episode: ProgrammeWithoutCuesheetContentContentDetailItemsInner
    ) -> EpisodeDescriptor:
        if episode.playlist_item_id.media_id:
            streams = await self._fetch_episode_streams(
                [episode.playlist_item_id.media_id])
        else:
            playlist_item_id = episode.playlist_item_id.global_id
            playlist_items = await self.api.get_playlist_item(
                playlist_item_id, "web", playlist_item_id)
            media_ids = set(item.playlist_item_id.media_id
                            for item in playlist_items.items)
            streams = await self._fetch_episode_streams(media_ids)

        return assemble_episode(episode, streams)

    async def _fetch_episode_streams(self, media_ids: Iterable[str]) -> Iterable[str]:
        streams = await asyncio.gather(
            *map(self._fetch_single_episode_stream, media_ids))
        return cast(Iterable[str], filter(lambda x: x is not None, streams))

    async def _fetch_single_episode_stream(self, media_id: str) -> Optional[str]:
        for tech in ["progressive", "hls"]:
            try:
                stream = await self.api.get_media_stream(app_code="medianet",
                                                         connection_type="hd",
                                                         device_type="ipad",
                                                         id_media=media_id,
                                                         multibitrate="true",
                                                         output="json",
                                                         tech=cast(StreamingTech, tech))
                return stream.url
            except ApiException:
                continue
        return None
