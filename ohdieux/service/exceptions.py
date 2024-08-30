from jivago.inject.annotation import Component
from jivago.lang.annotations import Override
from jivago.wsgi.filter.system_filters.error_handling.exception_mapper import ExceptionMapper
from jivago.wsgi.request.response import Response


class ManifestGenerationException(Exception):

    def __init__(self, message: str):
        self.message = message


@Component
class ManifestGenerationExceptionMapper(ExceptionMapper):

    @Override
    def handles(self, exception: Exception) -> bool:
        return isinstance(exception, ManifestGenerationException)

    @Override
    def create_response(self, exception: Exception) -> Response:
        return Response(
            400, {}, """Une erreur est survenue lors de la conversion. 
Si l'erreur persiste, veuillez coller le message ci-dessous dans un rapport d'anomalie au https://github.com/keotl/ohdieux/issues

An error occurred during conversion. 
If the issue persists, please file a bug report with the error message at https://github.com/keotl/ohdieux/issues

Message:
""" + exception.message)
