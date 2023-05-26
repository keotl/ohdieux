from jivago.lang.stream import Stream
from ohdieux.model.episode_descriptor import EpisodeDescriptor
from ohdieux.model.programme import Programme


def reverse_episode_segments(programme: Programme) -> Programme:

    return Programme(programme.programme,
                     Stream(programme.episodes).map(_reverse_episode).toList(),
                     programme.build_date)


def _reverse_episode(e: EpisodeDescriptor) -> EpisodeDescriptor:
    return EpisodeDescriptor(e.title, e.description, e.guid, e.date,
                             e.duration, list(reversed(e.media)))
