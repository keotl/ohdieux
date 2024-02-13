from typing import Literal

from jivago.config.properties.application_properties import \
    ApplicationProperties
from jivago.config.properties.system_environment_properties import \
    SystemEnvironmentProperties
from jivago.inject.annotation import Component, Singleton
from jivago.lang.annotations import Inject


@Component
@Singleton
class Config(object):
    cache_refresh_delay_s: int
    cache_strategy: Literal["memory", "redis"]
    user_agent: str
    run_fetcher_worker: bool

    @Inject
    def __init__(self, application_properties: ApplicationProperties,
                 env: SystemEnvironmentProperties):
        self.cache_refresh_delay_s = int(application_properties.get("CACHE_REFRESH_DELAY") or \
            env.get("CACHE_REFRESH_DELAY") or \
            application_properties.get("DELAI_RAFRAICHISSEMENT_CACHE") or \
            env.get("DELAI_RAFRAICHISSEMENT_CACHE") or \
            3600 * 24 * 7)

        self.cache_strategy = application_properties.get("CACHE_STRATEGY") or \
            env.get("CACHE_STRATEGY") or \
            application_properties.get("STRATEGIE_CACHE") or \
            env.get("STRATEGIE_CACHE") or \
            "memory"

        self.user_agent = application_properties.get("USER_AGENT") or \
            env.get("USER_AGENT") or ""

        self.run_fetcher_worker = (application_properties.get("RUN_FETCHER_WORKER")
                                   or env.get("RUN_FETCHER_WORKER")
                                   or "") in ("", "True", "true", "t", "1", "y", "yes")
