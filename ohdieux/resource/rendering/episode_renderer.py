from collections.abc import Callable
from email.utils import formatdate
from typing import Iterable, List, NamedTuple, TypeVar

from jivago.lang.stream import Stream
from ohdieux.model.episode_descriptor import EpisodeDescriptor, MediaDescriptor
from ohdieux.model.programme import Programme
from ohdieux.model.programme_descriptor import ProgrammeDescriptor


class RenderedEpisode(NamedTuple):
    title: str
    description: str
    guid: str
    date: str
    duration: int
    media: MediaDescriptor
    source_episode_guid_: str


class RenderedProgramme(NamedTuple):
    programme: ProgrammeDescriptor
    episodes: Iterable[RenderedEpisode]


def renderer(*,
             tag_segments: bool = False,
             favor_aac: bool = False,
             reverse_segments: bool = False,
             limit_episodes: bool = False):
    episode_transforms: List[Callable[[EpisodeDescriptor], EpisodeDescriptor]] = [
        _replace_mp4_url_for_aac if favor_aac else _noop,
        _reverse_episode_segments if reverse_segments else _noop
    ]
    programme_transforms: List[Callable[[RenderedProgramme], RenderedProgramme]] = [
        _tag_episode_title_with_segment_index if tag_segments else _noop,
        _limit_episodes if limit_episodes else _noop
    ]

    def _render_episode(episode: EpisodeDescriptor) -> List[RenderedEpisode]:
        res = []
        for i, stream in enumerate(_apply(episode_transforms)(episode).media):
            res.append(
                RenderedEpisode(title=episode.title,
                                description=episode.description,
                                guid=f"{episode.guid}_{i}",
                                date=formatdate(float(episode.date.strftime("%s"))),
                                duration=episode.duration,
                                media=stream,
                                source_episode_guid_=episode.guid))
        return res

    def _render_programme(programme: Programme) -> RenderedProgramme:
        rendered_programme = RenderedProgramme(
            programme.programme,
            Stream(programme.episodes).map(_render_episode).flat())
        return _apply(programme_transforms)(rendered_programme)

    return _render_programme


def _replace_mp4_url_for_aac(episode: EpisodeDescriptor) -> EpisodeDescriptor:

    def _transform_media(media: MediaDescriptor) -> MediaDescriptor:
        if ".mp4" in media.media_url and "/mp4/" in media.media_url:
            return MediaDescriptor(
                media.media_url.replace("/mp4/", "/hls/").replace(".mp4", ".aac"),
                media.media_type, media.length)

        return media

    new_media = Stream(episode.media).map(_transform_media).toList()
    return EpisodeDescriptor(title=episode.title,
                             description=episode.description,
                             guid=episode.guid,
                             date=episode.date,
                             duration=episode.duration,
                             media=new_media)


def _noop(x, _=None):
    return x


def _tag_episode_title_with_segment_index(
        programme: RenderedProgramme) -> RenderedProgramme:

    def _tag_episodes(episodes: Iterable[RenderedEpisode]) -> Iterable[RenderedEpisode]:
        current_episode = ""
        index = 1
        for episode in episodes:
            if current_episode != episode.source_episode_guid_:
                current_episode = episode.source_episode_guid_
                index = 1

            yield RenderedEpisode(title=f"{episode.title} ({index})",
                                  description=episode.description,
                                  guid=episode.guid,
                                  date=episode.date,
                                  duration=episode.duration,
                                  media=episode.media,
                                  source_episode_guid_=episode.source_episode_guid_)
            index += 1

    return RenderedProgramme(programme.programme, _tag_episodes(programme.episodes))


def _reverse_episode_segments(e: EpisodeDescriptor) -> EpisodeDescriptor:
    return EpisodeDescriptor(e.title, e.description, e.guid, e.date, e.duration,
                             list(reversed(e.media)))


def _limit_episodes(programme: RenderedProgramme) -> RenderedProgramme:
    return RenderedProgramme(programme.programme,
                             Stream(programme.episodes).take(_EPISODE_LIMIT))


_EPISODE_LIMIT = 50

T = TypeVar("T")


def _apply(operations: List[Callable[[T], T]]) -> Callable[[T], T]:

    def _res(x: T) -> T:
        value = x
        for op in operations:
            value = op(value)
        return value

    return _res
