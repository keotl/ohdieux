import logging

import requests
from jivago.inject.annotation import Component, Provider


class ApiException(Exception):
    pass


@Component
class OhdioApi(object):

    def __init__(self,
                 base_url: str = "https://services.radio-canada.ca/neuro/sphere/v1/audio/apps/products/programmes-v2/") -> None:
        self.base_url = base_url
        self._logger = logging.getLogger(self.__class__.__name__)

    def query_episodes(self, programme_id: str, page_number) -> dict:
        self._logger.debug(f"Querying episodes for programme: {programme_id}/{page_number}.")
        response = requests.get(self.base_url + programme_id + "/" + str(page_number))
        if response.ok:
            return response.json()
        else:
            self._logger.debug(f"Failed to retrieve page number {page_number}.")
            raise ApiException(response.text)

    def query_programme(self, programme_id: str) -> dict:
        response = requests.get(self.base_url + programme_id)
        if response.ok:
            return response.json()
        else:
            self._logger.debug(f"Failed to retrieve programme {programme_id}.")
            raise ApiException(response.text)

    def query_media(self, media_id: str) -> dict:
        response = requests.get(
            f"https://services.radio-canada.ca/media/validation/v2/?appCode=medianet&connectionType=hd&deviceType=ipad&idMedia={media_id}&multibitrate=true&output=json&tech=hls")
        if response.ok:
            return response.json()
        else:
            self._logger.debug(f"Failed to retrieve media for {media_id}.")
            raise ApiException(response.text)


@Provider
def ohdio_api_provider() -> OhdioApi:
    return OhdioApi()
