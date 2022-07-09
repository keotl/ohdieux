from datetime import datetime
from typing import NamedTuple

class MediaDescriptor(object):
    media_url: str
    media_type: str
    length: int

    def __init__(self, media_url: str, media_type: str, length: int):
        self.media_url = media_url
        self.media_type = media_type
        self.length = length
        


class EpisodeDescriptor(NamedTuple):
    title: str
    description: str
    guid: str
    date: datetime
    duration: int
    media: MediaDescriptor
