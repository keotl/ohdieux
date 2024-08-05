import sys
from typing import List, Literal, Optional

if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

from typing_extensions import NotRequired


class ProgrammePicture(TypedDict):
    pattern: str


class ProgrammeHeader(TypedDict):
    title: str
    summary: str
    picture: ProgrammePicture


class Pagination(TypedDict):
    pageMaxLength: int
    pageNumber: int
    pageSize: int
    totalNumberOfItems: int


class Duration(TypedDict):
    durationInSeconds: int


class ContentType(TypedDict):
    id: int
    name: str


class ContentGlobalId(TypedDict):
    contentType: ContentType
    id: str


class PlaylistItemId(TypedDict):
    globalId2: ContentGlobalId
    hasTranscription: bool


class ProgrammeContentItem(TypedDict):
    duration: Duration
    playlistItemId: PlaylistItemId
    summary: NotRequired[Optional[str]]
    title: str
    url: str
    isBroadcastedReplay: bool


class ProgrammeContentDetail(TypedDict):
    pagedConfiguration: Pagination
    items: List[ProgrammeContentItem]


class ProgrammeContent(TypedDict):
    contentDetail: ProgrammeContentDetail


class ProgrammeWithoutCuesheet(TypedDict):
    typename: str
    canonicalUrl: str
    header: ProgrammeHeader
    primaryClassificationTagId: int
    content: ProgrammeContent


class MediaPlaybackItem(TypedDict):
    mediaId: str
    globalId: ContentGlobalId
    mediaSeekTime: Optional[int]


class PlaybackListItem(TypedDict):
    broadcastedFirstTimeAt: str
    mediaPlaybackItem: MediaPlaybackItem
    duration: Duration
    title: str
    subtitle: str
    appCode: Literal["medianet"]


class PlaybackList(TypedDict):
    items: List[PlaybackListItem]


class MediaStreamDescriptor(TypedDict):
    url: str
