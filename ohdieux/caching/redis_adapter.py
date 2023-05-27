import logging
from typing import List, Optional

import redis
from jivago.config.properties.system_environment_properties import \
    SystemEnvironmentProperties
from jivago.config.startup_hooks import PostInit
from jivago.event.config.annotations import EventHandler, EventHandlerClass
from jivago.event.synchronous_event_bus import SynchronousEventBus
from jivago.inject.annotation import Component, Singleton
from jivago.lang.annotations import BackgroundWorker, Inject, Override
from jivago.lang.runnable import Runnable
from jivago.scheduling.annotations import Duration, Scheduled
from jivago.serialization.object_mapper import ObjectMapper
from jivago.wsgi.invocation.incorrect_attribute_type_exception import \
    IncorrectAttributeTypeException
from ohdieux.caching.programme_cache import ProgrammeCache
from ohdieux.communication.programme_refresh_notifier import \
    ProgrammeRefreshNotifier
from ohdieux.model.programme import Programme


@Component
@Singleton
@EventHandlerClass
class RedisAdapter(ProgrammeCache, ProgrammeRefreshNotifier):

    @Inject
    def __init__(self, env: SystemEnvironmentProperties):
        self._url = env.get("REDIS_URL")
        self._logger = logging.getLogger(self.__class__.__name__)
        self._mapper = ObjectMapper()

        if not self._url:
            self._logger.fatal(f"Missing REDIS_URL environment variable.")
            raise Exception(f"Missing REDIS_URL environment variable.")

        self._connection = redis.StrictRedis(decode_responses=True,
                                             health_check_interval=30,
                                             charset="utf-8").from_url(
                                                 self._url)
        self._connection.ping()
        self._logger.info("Established Redis connection.")
        self._pubsub = self._connection.pubsub()

    @Override
    def set(self, programme_id: int, programme: Programme):
        self._connection.set(str(programme_id),
                             self._mapper.serialize(programme))

    @Override
    def get(self, programme_id: int) -> Optional[Programme]:
        try:
            value = self._connection.get(str(programme_id))
            if value is None:
                return None
            return self._mapper.deserialize(value.decode("utf-8"), Programme)
        except IncorrectAttributeTypeException:
            return None

    @Override
    def notify_refresh(self, programme_id: int):
        self._connection.publish("refresh_programme", str(programme_id))

    @EventHandler("refresh_complete")
    def on_refresh_complete(self, programme_id: int):
        with self._connection.lock("pending_lock"):
            saved = self._connection.get("pending")
            if saved is None:
                pending = []
            else:
                pending = self._mapper.deserialize(saved.decode("utf-8"),
                                                   List[int])
            pending.remove(programme_id)
            self._connection.set("pending", self._mapper.serialize(pending))

    def _mark_pending_and_should_send_refresh_message(
            self, programme_id: int) -> bool:
        with self._connection.lock("pending_lock"):
            saved = self._connection.get("pending")
            if saved is None:
                pending = []
            else:
                pending = self._mapper.deserialize(saved.decode("utf-8"),
                                                   List[int])
            if programme_id in pending:
                return False

            pending.append(programme_id)
            self._connection.set("pending", self._mapper.serialize(pending))
            return True


@Component
@BackgroundWorker
class RedisRefreshListener(Runnable):

    @Inject
    def __init__(self, redis: RedisAdapter, event_bus: SynchronousEventBus):
        self._redis = redis
        self._pubsub = self._redis._connection.pubsub()
        self._event_bus = event_bus

    @Override
    def run(self):
        self._pubsub.subscribe("refresh_programme")
        for message in self._pubsub.listen():
            if message is None:
                continue
            programme_id = int(message.get("data"))
            if self._redis._mark_pending_and_should_send_refresh_message(
                    programme_id):
                self._event_bus.emit("refresh_programme", programme_id)


@Component
@PostInit
@Scheduled(every=Duration.DAY)
class RedisPendingQueueJanitor(Runnable):

    @Inject
    def __init__(self, redis: RedisAdapter):
        self._redis = redis

    @Override
    def run(self):
        with self._redis._connection.lock("pending_lock"):
            self._redis._connection.delete("pending")
