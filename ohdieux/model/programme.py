from typing import List

from ohdieux.model.episode_descriptor import EpisodeDescriptor
from ohdieux.model.programme_descriptor import ProgrammeDescriptor


class Programme(object):
    programme: ProgrammeDescriptor
    episodes: List[EpisodeDescriptor]

    def __init__(self, programme: ProgrammeDescriptor, episodes: List[EpisodeDescriptor]):
        self.programme = programme
        self.episodes = episodes
