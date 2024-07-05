from datetime import datetime
from typing import List, Literal, Optional, TypedDict

from jivago.lang.annotations import Serializable
from ohdieux.model.episode_descriptor import EpisodeDescriptor
from ohdieux.model.programme_descriptor import ProgrammeDescriptor

EpisodeOrdering = Literal["oldest_to_newest", "newest_to_oldest", "unknown"]


@Serializable
class Programme(object):
    programme: ProgrammeDescriptor
    episodes: List[EpisodeDescriptor]
    build_date: datetime
    ordering: EpisodeOrdering

    def __init__(self, programme: ProgrammeDescriptor,
                 episodes: List[EpisodeDescriptor], build_date: datetime,
                 ordering: Optional[str]):
        self.programme = programme
        self.episodes = episodes
        self.build_date = build_date
        if ordering not in ("oldest_to_newest", "newest_to_oldest", "unknown"):
            self.ordering = "unknown"
        else:
            self.ordering = ordering


class ProgrammeSummary(TypedDict):
    episodes: int
    first_episodes: List[EpisodeDescriptor]
    title: str
    description: str
    ordering: EpisodeOrdering
