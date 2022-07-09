from datetime import datetime
from typing import NamedTuple

class MediaDescriptor(object):
    media_url: str
    media_type: str
    length: int

class EpisodeDescriptor(NamedTuple):
    title: str
    description: str
    guid: str
    date: datetime
    duration: int
    media: MediaDescriptor
