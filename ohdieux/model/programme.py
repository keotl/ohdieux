from datetime import datetime
from typing import List

from jivago.lang.annotations import Serializable
from ohdieux.model.episode_descriptor import EpisodeDescriptor
from ohdieux.model.programme_descriptor import ProgrammeDescriptor


@Serializable
class Programme(object):
    programme: ProgrammeDescriptor
    episodes: List[EpisodeDescriptor]
    build_date: datetime

    def __init__(self, programme: ProgrammeDescriptor,
                 episodes: List[EpisodeDescriptor], build_date: datetime):
        self.programme = programme
        self.episodes = episodes
        self.build_date = build_date
