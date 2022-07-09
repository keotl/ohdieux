from jivago.lang.stream import Stream
from jivago.wsgi.annotations import Resource
from jivago.lang.annotations import Inject
from jivago.wsgi.methods import GET
from jivago.wsgi.invocation.parameters import QueryParam

from ohdieux.model.episode_descriptor import EpisodeDescriptor, MediaDescriptor
from ohdieux.ohdio.ohdio_reader import OhdioReader

@Resource("/debug")
class DebugResource(object):

    @Inject
    def __init__(self, ohdio_reader: OhdioReader):
        self._ohdio_reader = ohdio_reader
        
    @GET
    def query_programme(self, programme_id: QueryParam[str]):
        programme = self._ohdio_reader.query(str(programme_id))

        return {"programme": programme.programme,
                "episodes": Stream(programme.episodes).map(
                    lambda x: EpisodeDescriptor(x.title, x.description, x.guid, x.date, x.duration,
                                                MediaDescriptor(x.media.media_url, x.media.media_type, x.media.length))
                    ).toList()
                }
