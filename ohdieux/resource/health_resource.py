from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import GET

@Resource("/health")
class HealthResource(object):

    @GET
    def health(self):
        return "OK"
