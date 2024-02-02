from datetime import datetime
from typing import Iterable, List

from jivago.lang.stream import Stream
from ohdieux.model.episode_descriptor import EpisodeDescriptor, MediaDescriptor
from ohdieux.model.programme import Programme
from ohdieux.model.programme_descriptor import ProgrammeDescriptor
from ohdieux.ohdio.generated.models.programme_without_cuesheet import \
    ProgrammeWithoutCuesheet
from ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner import \
    ProgrammeWithoutCuesheetContentContentDetailItemsInner
from ohdieux.ohdio.parse_utils import clean
from ohdieux.util.dateparse import infer_fr_date


def assemble_pending_programme(programme: ProgrammeWithoutCuesheet) -> Programme:
    programme_descriptor = ProgrammeDescriptor(
        title=clean(programme.header.title),
        description="Ce programme est en cours de chargement par Ohdieux. "
        "This programme is currently being indexed by Ohdieux. "
        "Veuillez patienter quelques minutes avant de rafraîchir. "
        "Wait a few minutes before refreshing.",
        author="Radio-Canada",
        link="http://ici.radio-canada.ca" + programme.header.share.url,
        image_url=programme.header.picture.url.replace("{0}",
                                                       "1400").replace("{1}", "1x1"))

    return Programme(programme_descriptor, [_pending_placeholder_episode],
                     datetime.now())


_pending_placeholder_episode = EpisodeDescriptor(
    "Veuillez patienter. Please wait.",
    "Ce programme est en cours de chargement par Ohdieux. "
    "This programme is currently being indexed by Ohdieux. "
    "Veuillez patienter quelques minutes avant de rafraîchir. "
    "Wait a few minutes before refreshing.",
    "0000000000",
    datetime.now(),
    duration=1,
    media=[
        MediaDescriptor("https://ohdieux.ligature.ca/placeholder.mp4",
                        media_type="audio/mpeg",
                        length=1)
    ])


def assemble_programme(programme: ProgrammeWithoutCuesheet,
                       episodes: List[EpisodeDescriptor]) -> Programme:
    programme_descriptor = ProgrammeDescriptor(
        title=clean(programme.header.title),
        description=clean(programme.header.summary),
        author="Radio-Canada",
        link="http://ici.radio-canada.ca" + programme.header.share.url,
        image_url=programme.header.picture.url.replace("{0}",
                                                       "1400").replace("{1}", "1x1"))

    return Programme(programme_descriptor, episodes, datetime.now())


def assemble_episode(episode: ProgrammeWithoutCuesheetContentContentDetailItemsInner,
                     streams: Iterable[str]) -> EpisodeDescriptor:
    return EpisodeDescriptor(
        title=clean(episode.title),
        description=clean(episode.summary),
        guid=episode.global_id.id,
        date=episode.broadcasted_first_time_at,
        duration=int(episode.media2.duration.duration_in_seconds),
        media=Stream(streams).map(lambda stream: MediaDescriptor(
            stream, "audio/mpeg", int(episode.media2.duration.duration_in_seconds))
                                  ).toList())
