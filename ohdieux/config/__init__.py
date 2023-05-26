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
    fetch_threads: int
    cache_strategy: Literal["memory", "mongodb"]

    @Inject
    def __init__(self, application_properties: ApplicationProperties,
                 env: SystemEnvironmentProperties):
        self.cache_refresh_delay_s = \
            application_properties.get("CACHE_REFRESH_DELAY") or \
            env.get("CACHE_REFRESH_DELAY") or \
            application_properties.get("DELAI_RAFRAICHISSEMENT_CACHE") or \
            env.get("DELAI_RAFRAICHISSEMENT_CACHE") or \
            86400

        self.fetch_threads = int(application_properties.get("FETCH_THREADS") or \
            env.get("FETCH_THREADS") or \
            application_properties.get("FILS_REQUETES") or \
            env.get("FILS_REQUETES") or \
            4)

        self.cache_strategy = application_properties.get("CACHE_STRATEGY") or \
            env.get("CACHE_STRATEGY") or \
            application_properties.get("STRATEGIE_CACHE") or \
            env.get("STRATEGIE_CACHE") or \
            "memory"
