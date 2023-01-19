import logging
from math import ceil
import threading
from datetime import datetime, timedelta
from typing import Dict, Generic, Tuple, TypeVar, Union
from jivago.inject.annotation import Component, Singleton
from jivago.lang.annotations import Inject, Override
from ohdieux.config import Config
from ohdieux.model.programme import Programme
from ohdieux.ohdio.ohdio_manifest_service import OhdioManifestService

from ohdieux.service.manifest_service import ManifestService

@Component
@Singleton
class CachedManifestService(ManifestService):

    @Inject
    def __init__(self, manifest_service: OhdioManifestService, config: Config):
        self._manifest_service = manifest_service
        self._global_lock = threading.Lock()
        self._programmes : Dict[Tuple[Union[str, bool]], Tuple[threading.Lock, CacheEntry]] = {}
        self._cache_refresh_delay = config.cache_refresh_delay_s
        self._logger = logging.getLogger(self.__class__.__name__)

    @Override
    def generate_podcast_manifest(self, programme_id: str, reverse_segments: bool) -> Programme:
        lock, cache_entry = self.programme_lock(programme_id, reverse_segments)
        with lock:
            if datetime.utcnow() > cache_entry.expiry:
                start_time = datetime.now()
                self._logger.info(f"Refreshing programme {programme_id}, reverse={reverse_segments}.")
                updated = self._manifest_service.generate_podcast_manifest(programme_id, reverse_segments)
                cache_entry.update(updated, self.expiry_date(updated))
                self._logger.info(f"Completed refresh of programme {programme_id} in {datetime.now() - start_time}, expiring at {cache_entry.expiry}.")
            return cache_entry.data

    def programme_lock(self, *key: Union[str, bool]):
        with self._global_lock:
            if key not in self._programmes:
                self._programmes[key] = (threading.Lock(), CacheEntry())

            return self._programmes[key]

    def expiry_date(self, programme: Programme):
        now = datetime.utcnow()
        if len(programme.episodes) > 0:
            most_recent = programme.episodes[0].date
            days_ago = (now - most_recent).total_seconds() / (3600 * 24)
            possible_next_episode_time = most_recent + timedelta(days=ceil(days_ago)) + SCHEDULE_TOLERANCE

            if possible_next_episode_time > now:
                return possible_next_episode_time

        return now + timedelta(seconds=self._cache_refresh_delay)


T = TypeVar("T")

class CacheEntry(Generic[T]):
    data: T
    expiry: datetime

    def __init__(self):
        self.data = None
        self.expiry = datetime.min

    def update(self, data: T, expiry: datetime):
        self.data = data
        self.expiry = expiry

SCHEDULE_TOLERANCE = timedelta(minutes=5)
