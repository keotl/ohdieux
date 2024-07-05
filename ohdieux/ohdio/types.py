from typing import List, TypedDict

from typing_extensions import NotRequired


class ProgrammePicture(TypedDict):
    pattern: str


class ProgrammeHeader(TypedDict):
    title: str
    summary: str
    picture: ProgrammePicture


class Pagination(TypedDict):
    nextPageUrl: NotRequired[str]
    pageMaxLength: int
    pageNumber: int
    pageSize: int
    previousPageUrl: NotRequired[str]
    totalNumberOfItems: int


class Duration(TypedDict):
    durationInSeconds: int


class ContentType(TypedDict):
    id: int
    name: str


class ContentGlobalId(TypedDict):
    contentType: ContentType
    id: int


class PlaylistItemId(TypedDict):
    globalId2: ContentGlobalId
    hasTranscription: bool
    mediaId: NotRequired[str]


class ProgrammeContentItem(TypedDict):
    duration: Duration
    globalId: ContentGlobalId
    playlistItemId: PlaylistItemId
    summary: NotRequired[str]
    title: str
    url: str
    isBroadcastedReplay: bool


class ProgrammeContentDetail(TypedDict):
    pagedConfiguration: Pagination
    items: List[ProgrammeContentItem]


class ProgrammeContent(TypedDict):
    contentDetail: ProgrammeContentDetail


class ProgrammeWithoutCuesheet(TypedDict):
    canonicalUrl: str
    header: ProgrammeHeader
    primaryClassificationTagId: int
    content: ProgrammeContent


class MediaPlaybackItem(TypedDict):
    mediaId: str
    globalId: ContentGlobalId
    mediaSeekTime: int


class PlaybackListItem(TypedDict):
    broadcastedFirstTimeAt: str
    mediaPlaybackItem: MediaPlaybackItem
    duration: Duration
    title: str
    subtitle: str


class PlaybackList(TypedDict):
    items: List[PlaybackListItem]
    appCode: str


class MediaStreamDescriptor(TypedDict):
    url: str
