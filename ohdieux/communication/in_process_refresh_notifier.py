import threading

from jivago.event.async_event_bus import AsyncEventBus
from jivago.event.config.annotations import EventHandler
from jivago.inject.annotation import Singleton, Component
from jivago.lang.annotations import Inject, Override

from ohdieux.communication.programme_refresh_notifier import \
    ProgrammeRefreshNotifier

@Component
@Singleton
# @EventHandlerClass # Configured dynamically in context.py
class InProcessRefreshNotifier(ProgrammeRefreshNotifier):

    @Inject
    def __init__(self, event_bus: AsyncEventBus):
        self._event_bus = event_bus
        self._pending = set()
        self._lock = threading.Lock()

    @Override
    def notify_refresh(self, programme_id: int):
        with self._lock:
            if programme_id in self._pending:
                return
            self._event_bus.emit("refresh_programme", programme_id)
            self._pending.add(programme_id)

    @EventHandler("refresh_complete")
    def on_refresh_complete(self, programme_id: int):
        with self._lock:
            self._pending.discard(programme_id)
