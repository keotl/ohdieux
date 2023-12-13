from email.utils import formatdate
from typing import List, NamedTuple

from ohdieux.model.episode_descriptor import EpisodeDescriptor, MediaDescriptor


class RenderedEpisode(NamedTuple):
    title: str
    description: str
    guid: str
    date: str
    duration: int
    media: MediaDescriptor


def renderer(*,
             tag_segments: bool = False,
             favor_aac: bool = False,
             reverse_segments: bool = False):
    media_transform = _replace_mp4_url_for_aac if favor_aac else _noop
    title_transform = _tag_title_with_index if tag_segments else _noop
    episode_transform = _reverse_episode_segments if reverse_segments else _noop

    def _render_episode(episode: EpisodeDescriptor) -> List[RenderedEpisode]:
        res = []
        for i, stream in enumerate(episode_transform(episode).media):
            res.append(
                RenderedEpisode(title=title_transform(episode.title, i),
                                description=episode.description,
                                guid=f"{episode.guid}_{i}",
                                date=formatdate(
                                    float(episode.date.strftime("%s"))),
                                duration=episode.duration,
                                media=media_transform(stream)))
        return res

    return _render_episode


def _replace_mp4_url_for_aac(media: MediaDescriptor) -> MediaDescriptor:
    if ".mp4" in media.media_url and "/mp4/" in media.media_url:
        return MediaDescriptor(
            media.media_url.replace("/mp4/", "/hls/").replace(".mp4", ".aac"),
            media.media_type, media.length)

    return media


def _noop(x, _=None):
    return x


def _tag_title_with_index(title: str, stream_index: int) -> str:
    return f"{title} ({stream_index + 1})"


def _reverse_episode_segments(e: EpisodeDescriptor) -> EpisodeDescriptor:
    return EpisodeDescriptor(e.title, e.description, e.guid, e.date,
                             e.duration, list(reversed(e.media)))
