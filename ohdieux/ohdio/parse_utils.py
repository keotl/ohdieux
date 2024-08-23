import html
from xml.sax import saxutils as xml

from jivago.lang.stream import Stream
from ohdieux.ohdio.types import PlaybackList
from ohdieux.util.xml import unsafe_strip_tags


def clean(human_readable_text: str) -> str:
    return xml.escape(html.unescape(unsafe_strip_tags(human_readable_text or "")))


def filter_playbacklist_items_by_episode_id(
        episode_id: str, playback_list: PlaybackList) -> PlaybackList:

    return {
        "items": Stream(playback_list["items"]) \
        .filter(lambda item: item["mediaPlaybackItem"]["globalId"]["id"] == episode_id) \
        .toList()
    }
