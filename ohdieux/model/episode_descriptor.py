from datetime import datetime
from typing import List, NamedTuple


class MediaDescriptor(NamedTuple):
    media_url: str
    media_type: str
    length: int


class EpisodeDescriptor(NamedTuple):
    title: str
    description: str
    guid: str
    date: datetime
    duration: int
    media: List[MediaDescriptor]
