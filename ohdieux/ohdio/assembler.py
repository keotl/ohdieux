from datetime import datetime
from typing import Iterable, List

from jivago.lang.stream import Stream
from ohdieux.model.episode_descriptor import EpisodeDescriptor, MediaDescriptor
from ohdieux.model.programme import Programme
from ohdieux.model.programme_descriptor import ProgrammeDescriptor
from ohdieux.ohdio.guess_programme_ordering import guess_programme_ordering
from ohdieux.ohdio.parse_utils import clean
from ohdieux.ohdio.types import (PlaybackList, ProgrammeContentItem,
                                 ProgrammeWithoutCuesheet)


def assemble_pending_programme(programme: ProgrammeWithoutCuesheet) -> Programme:
    programme_descriptor = ProgrammeDescriptor(
        title=clean(programme["header"]["title"]),
        description="Ce programme est en cours de chargement par Ohdieux. "
        "This programme is currently being indexed by Ohdieux. "
        "Veuillez patienter quelques minutes avant de rafraîchir. "
        "Wait a few minutes before refreshing.",
        author="Radio-Canada",
        link="https://ici.radio-canada.ca/ohdio" + programme["canonicalUrl"],
        image_url=programme["header"]["picture"]["pattern"].replace("{width}",
                                                                    "1400").replace(
                                                                        "{ratio}", "1x1"))

    return Programme(programme_descriptor, [], datetime.now(), "unknown")


def assemble_programme(programme: ProgrammeWithoutCuesheet,
                       episodes: List[EpisodeDescriptor]) -> Programme:
    programme_descriptor = ProgrammeDescriptor(
        title=clean(programme["header"]["title"]),
        description=clean(programme["header"]["summary"]),
        author="Radio-Canada",
        link="https://ici.radio-canada.ca/ohdio" + programme["canonicalUrl"],
        image_url=programme["header"]["picture"]["pattern"].replace("{width}",
                                                                    "1400").replace(
                                                                        "{ratio}", "1x1"))

    return Programme(programme_descriptor,
                     episodes,
                     datetime.now(),
                     ordering=guess_programme_ordering(episodes))


def assemble_episode(episode: ProgrammeContentItem, playback_list: PlaybackList,
                     streams: Iterable[str]) -> EpisodeDescriptor:
    return EpisodeDescriptor(
        title=clean(episode["title"]),
        description=clean(episode.get("summary") or ""),
        guid=str(episode["playlistItemId"]["globalId2"]["id"]),
        date=datetime.strptime(playback_list["items"][0]["broadcastedFirstTimeAt"],
                               "%Y-%m-%dT%H:%M:%S.%fZ"),
        duration=int(episode["duration"]["durationInSeconds"]),
        media=Stream(streams).map(lambda stream: MediaDescriptor(
            stream, "audio/mpeg", int(episode["duration"]["durationInSeconds"]))
                                  ).toList(),
        is_broadcast_replay=episode['isBroadcastedReplay'])
