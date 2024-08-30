from jivago.inject.annotation import Component
from jivago.lang.annotations import Override
from jivago.wsgi.filter.system_filters.error_handling.exception_mapper import \
    ExceptionMapper
from jivago.wsgi.request.response import Response
from ohdieux.service.programme_fetching_service import \
    ProgrammeNotFoundException


@Component
class ProgrammeNotFoundExceptionMapper(ExceptionMapper):

    @Override
    def handles(self, exception: Exception) -> bool:
        return isinstance(exception, ProgrammeNotFoundException)

    def create_response(self, exception: Exception) -> Response:
        return Response(400, {}, "Unknown programme ID.\nID Programme inconnu.")
